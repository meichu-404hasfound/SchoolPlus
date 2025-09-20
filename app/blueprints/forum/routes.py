from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from ...extensions import db
from ...models.issue import Issue
from ...models.comment import Comment
from ...models.user import User
from ..utils import get_current_user
from sqlalchemy import or_, func

forum_bp = Blueprint("forum", __name__)


@forum_bp.get("/forum")
def forum_home():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    # Your Jinja shell; frontend will fetch data via /api endpoints
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Issue.query.order_by(Issue.id.desc())

    # keep the same pagination style you already use in /api/search
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    # pass both the items and the pagination object into the template
    return render_template(
        "forum.html",
        user=user,
        items=pagination.items,
        pagination=pagination,
    )

@forum_bp.get("/forum/issues/<int:issue_id>")
def forum_issue(issue_id: int):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Issue.query.order_by(Issue.id.desc())
    # keep the same pagination style you already use in /api/search
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    issue = Issue.query.get_or_404(issue_id)
    
    print(issue)
    
    return render_template(
        "forum.html",
        user=user, 
        issue=issue,
        pagination=pagination
    )

def split_csv(csv: str):
    if not csv:
        return []
    return [p.strip() for p in csv.split(",") if p.strip()]

def normalize_label(s: str):
    return (s or "").strip().lower()

# ---------- Create Issue ----------
@forum_bp.post("/forum/issues")
def forum_create_issue():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    title       = (request.form.get("title")       or "").strip()
    body        = (request.form.get("body")        or "").strip()
    label   = (request.form.get("label")      or "").strip()  # optional comma labels
    
    if not title:
        flash("請輸入標題.", "error")
        return redirect(url_for("forum.forum_home"))
    
    if not body:
        flash("請輸入身體.", "error")
        return redirect(url_for("forum.forum_home"))
    
    if not label:
        flash("請輸入類別.", "error")
        return redirect(url_for("forum.forum_home"))

    issue = Issue(author_id=user.account, title=title, body=body, label=label)

    db.session.add(issue)
    db.session.commit()
    
    flash("成功發布Issue", "success")
    
    return redirect(url_for("forum.forum_issue", issue_id=issue.id))

# ---------- Comments ----------
@forum_bp.post("/forum/issues/<int:issue_id>/comments")
def forum_add_comment(issue_id: int):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    Issue.query.get_or_404(issue_id)
    body = request.form.get("body", "").strip()

    if not body:
        flash("請輸入文本。", "error")
        return redirect(url_for("forum.forum_issue", issue_id=issue_id))

    c = Comment(author_id=user.account, issue_id=issue_id, body=body)
    db.session.add(c)
    db.session.commit()
    
    flash("成功發布回復。", "success")
    return redirect(url_for("forum.forum_issue", issue_id=issue_id))

# ---------- Card list API (for the grid of cards) ----------
@forum_bp.get("/forum/api/issues")
def api_list_issues():
    """
    Returns only what the cards need.
    Query params: page (default 1), per_page (default 20), label=category(optional)
    """
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    label    = normalize_label(request.args.get("label"))

    q = Issue.query
    if label:
        q = q.filter(Issue.labels.any(Issue.label == label))

    q = q.order_by(Issue.id.desc())
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)

    items = [{
        "id": i.id,
        "title": i.title,
        "author_name": i.author_name,
        "labels": [l.name for l in i.labels],
        "upvote": i.upvote,
    } for i in pagination.items]

    return jsonify({
        "items": items,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    })

# ---------- Issue detail API (for the 70% modal) ----------
@forum_bp.get("/forum/api/issues/<int:issue_id>")
def api_get_issue(issue_id: int):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    i = Issue.query.get_or_404(issue_id)
    data = {
        "id": i.id,
        "title": i.title,
        "body": i.body,
        "author_id": i.author_id,
        "author_name": i.author_name,
        "labels": [l.name for l in i.labels],
        "upvote": i.upvote,
        "comments": [{
            "id": c.id,
            "author_id": c.author_id,
            "body": c.body,
            "upvote": c.upvote
        } for c in i.comments]
    }
    return jsonify(data)

# ---------- Search (title tokens + labels) ----------
@forum_bp.get("/forum/api/search")
def api_search_issues():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    qstr       = (request.args.get("q") or "").strip()
    label_csv  = (request.args.get("labels") or "").strip()
    label_mode = (request.args.get("label_mode") or "any").lower()
    page       = request.args.get("page", 1, type=int)
    per_page   = request.args.get("per_page", 20, type=int)

    q = Issue.query

    if qstr:
        tokens = [t for t in qstr.lower().split() if t]
        if tokens:
            like_clauses = [func.lower(Issue.title).like(f"%{t}%") for t in tokens]
            q = q.filter(or_(*like_clauses))

    names = [normalize_label(n) for n in split_csv(label_csv)]
    if names:
        if label_mode == "all":
            for name in names:
                q = q.filter(Issue.label == name)
        else:
            q = q.filter(Issue.label.in_(names))

    q = q.order_by(Issue.id.desc())
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [{
            "id": i.id, "title": i.title, "author_name": i.author_name,
            "labels": [l.name for l in i.labels], "upvote": i.upvote
        } for i in pagination.items],
        "page": pagination.page, "per_page": pagination.per_page,
        "total": pagination.total, "pages": pagination.pages
    })

# ---------- Upvote: issue + author tally ----------
@forum_bp.post("/forum/api/issues/<int:issue_id>/upvote")
def api_issue_upvote(issue_id: int):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    issue = Issue.query.get_or_404(issue_id)
    issue.upvote = (issue.upvote or 0) + 1

    # also increment the author's total upvotes_received
    if issue.author:  # relationship to User
        issue.author.upvotes_received = (issue.author.upvotes_received or 0) + 1

    db.session.commit()
    return jsonify({"id": issue.id, "upvote": issue.upvote, "author_upvotes_received": issue.author.upvotes_received if issue.author else None})


# from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
# from ...extensions import db
# from ...models.issue import Issue
# from ...models.user import User
# # ... (rest of your imports and code)

# forum_bp = Blueprint("forum", __name__, url_prefix="/forum")

# @forum_bp.get("/")
# def forum_home():
#     # pick up page & per_page from querystring, with sensible defaults
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 10, type=int)

#     query = Issue.query.order_by(Issue.id.desc())

#     # keep the same pagination style you already use in /api/search
#     pagination = query.paginate(page=page, per_page=per_page, error_out=False)

#     # pass both the items and the pagination object into the template
#     return render_template(
#         "forum.html",
#         items=pagination.items,
#         pagination=pagination,
#     )


# @forum_bp.get("/issues/<int:issue_id>")
# def forum_issue(issue_id: int):
#     issue = Issue.query.get_or_404(issue_id)
#     return render_template("forum/detail.html", issue=issue)


# @forum_bp.post("/issues")
# def forum_create_issue():
#     author_id = (request.form.get("author_id") or "").strip()
#     title = (request.form.get("title") or "").strip()
#     body = (request.form.get("body") or "").strip()
#     # labels can come as comma-separated "math, exam, urgent"
#     raw_labels = (request.form.get("labels") or "").strip()

#     if not (author_id and title and body):
#         flash("author_id, title, and body are required.", "error")
#         return redirect(url_for("forum.forum_home"))

#     if not User.query.get(author_id):
#         flash("Author account not found. Create the user first.", "error")
#         return redirect(url_for("forum.forum_home"))

#     issue = Issue(author_id=author_id, title=title, body=body)
#     # attach labels
#     labels = [normalize_label(n) for n in split_labels(raw_labels)]
#     if labels:
#         existing = {l.name: l for l in Label.query.filter(Label.name.in_(labels)).all()}
#         for name in labels:
#             issue.labels.append(existing.get(name) or Label(name=name))

#     db.session.add(issue)
#     db.session.commit()
#     flash("Issue created.", "success")
#     return redirect(url_for("forum.forum_issue", issue_id=issue.id))

# # ---------- Comments (unchanged) ----------
# @forum_bp.post("/issues/<int:issue_id>/comments")
# def forum_add_comment(issue_id: int):
#     Issue.query.get_or_404(issue_id)
#     author_id = (request.form.get("author_id") or "").strip()
#     body = (request.form.get("body") or "").strip()

#     if not (author_id and body):
#         flash("author_id and body are required for comments.", "error")
#         return redirect(url_for("forum.forum_issue", issue_id=issue_id))

#     if not User.query.get(author_id):
#         flash("Author account not found. Create the user first.", "error")
#         return redirect(url_for("forum.forum_issue", issue_id=issue_id))

#     c = Comment(author_id=author_id, issue_id=issue_id, body=body)
#     db.session.add(c)
#     db.session.commit()
#     flash("Comment added.", "success")
#     return redirect(url_for("forum.forum_issue", issue_id=issue_id))

# # ---------- Serializers ----------
# def issue_to_dict(issue: Issue, with_comments=True):
#     data = {
#         "id": issue.id,
#         "author_id": issue.author_id,
#         "title": issue.title,
#         "body": issue.body,
#         "upvote": issue.upvote,
#         "image_id": issue.image_id,
#         "labels": [l.name for l in (issue.labels or [])],  # NEW
#     }
#     if with_comments:
#         data["comments"] = [
#             {"id": c.id, "author_id": c.author_id, "issue_id": c.issue_id, "body": c.body, "upvote": c.upvote}
#             for c in issue.comments
#         ]
#     return data

# # ---------- Core list ----------
# @forum_bp.get("/api/issues")
# def api_list_issues():
#     qs = Issue.query.order_by(Issue.id.desc())
#     items = qs.all()
#     return jsonify([issue_to_dict(i, with_comments=False) for i in items])

# @forum_bp.get("/api/issues/<int:issue_id>")
# def api_get_issue(issue_id: int):
#     issue = Issue.query.get_or_404(issue_id)
#     return jsonify(issue_to_dict(issue))

# # ---------- NEW: Search & filter ----------
# @forum_bp.get("/api/search")
# def api_search_issues():
#     """
#     Query params:
#       q=string           -> fuzzy-ish match on title (case-insensitive contains & token OR)
#       labels=a,b,c       -> filter by labels (comma-separated)
#       label_mode=any|all -> 'any' (default) or 'all'
#       page, per_page     -> pagination (defaults 1/20)
#     """
#     q = (request.args.get("q") or "").strip()
#     label_csv = (request.args.get("labels") or "").strip()
#     label_mode = (request.args.get("label_mode") or "any").lower()
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 20, type=int)

#     query = Issue.query

#     # Title fuzzy-ish: split into tokens and OR them with LIKE
#     # ex: "mid term" -> title LIKE %mid% OR title LIKE %term%
#     if q:
#         tokens = [t for t in q.lower().split() if t]
#         if tokens:
#             like_clauses = [db.func.lower(Issue.title).like(f"%{t}%") for t in tokens]
#             query = query.filter(db.or_(*like_clauses))

#     # Labels filter
#     names = [normalize_label(n) for n in split_labels(label_csv)]
#     if names:
#         if label_mode == "all":
#             # every label must be present
#             for name in names:
#                 query = query.filter(Issue.labels.any(Label.name == name))
#         else:
#             # any of the labels
#             query = query.filter(Issue.labels.any(Label.name.in_(names)))

#     query = query.order_by(Issue.id.desc())
#     pagination = query.paginate(page=page, per_page=per_page, error_out=False)

#     return jsonify({
#         "items": [issue_to_dict(i, with_comments=False) for i in pagination.items],
#         "page": pagination.page,
#         "per_page": pagination.per_page,
#         "total": pagination.total,
#         "pages": pagination.pages
#     })

# # ---------- NEW: Labels API ----------
# @forum_bp.get("/api/labels")
# def api_list_labels():
#     labels = Label.query.order_by(Label.name.asc()).all()
#     return jsonify([{"id": l.id, "name": l.name} for l in labels])

# @forum_bp.post("/api/labels")
# def api_create_label():
#     data = request.get_json(silent=True) or {}
#     name = normalize_label(data.get("name") or "")
#     if not name:
#         return jsonify({"error": "name is required"}), 400
#     ex = Label.query.filter_by(name=name).first()
#     if ex:
#         return jsonify({"id": ex.id, "name": ex.name}), 200
#     l = Label(name=name)
#     db.session.add(l)
#     db.session.commit()
#     return jsonify({"id": l.id, "name": l.name}), 201


# @forum_bp.post("/api/issues/<int:issue_id>/upvote")
# def api_issue_upvote(issue_id: int):
#     issue = Issue.query.get_or_404(issue_id)
#     issue.upvote = (issue.upvote or 0) + 1
#     db.session.commit()
#     return jsonify({"id": issue.id, "upvote": issue.upvote})


# def split_labels(csv: str):
#     if not csv:
#         return []
#     return [p.strip() for p in csv.split(",") if p.strip()]

# def normalize_label(s: str):
#     return s.lower()
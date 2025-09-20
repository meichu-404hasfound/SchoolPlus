// forum.js
document.querySelectorAll('.issue-card').forEach(card => {
  card.addEventListener('click', async (e) => {
    e.preventDefault();                    // <-- prevent navigation
    const id = card.dataset.issueId;

    // load partial HTML for the issue (you can return a small snippet from your route)
    const res = await fetch(`/forum/issue/${id}?body=`);
    const html = await res.text();
    document.querySelector('#issueDetail').innerHTML = html;

    const modalEl = document.getElementById('issueModal');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
  });
});

// If you keep buttons inside the anchor, prevent the bubble-up:
document.querySelectorAll('[data-action="open-comments"],[data-action="upvote"]')
  .forEach(btn => btn.addEventListener('click', e => e.stopPropagation()));
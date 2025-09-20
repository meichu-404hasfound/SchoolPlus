(function () {
    const byId = (id) => document.getElementById(id);

    const chatForm = byId("chatForm");
    const chatInput = byId("chatInput");
    const chatScroll = byId("chatScroll");
    const typingRow = byId("typingRow");
    const btnSend = byId("btnSend");
    const btnClear = byId("btnClear");
    const btnExport = byId("btnExport");
    const btnMic = byId("btnMic");
    const fileInput = byId("fileInput");
    const fileChips = byId("fileChips");
    const chatIdEl = byId("chatId");
    const modelSelect = byId("modelSelect");
    const tempRange = byId("tempRange");
    const tempValue = byId("tempValue");

    // Presets
    document.querySelectorAll(".preset-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const p = btn.getAttribute("data-prompt") || "";
            chatInput.value = p;
            chatInput.focus();
            chatInput.setSelectionRange(chatInput.value.length, chatInput.value.length);
        });
    });

    // Temperature display
    if (tempRange && tempValue) {
        const setTemp = () => (tempValue.textContent = Number(tempRange.value).toFixed(1));
        tempRange.addEventListener("input", setTemp);
        setTemp();
    }

    // Voice button (placeholder)
    if (btnMic) {
        let active = false;
        btnMic.addEventListener("click", () => {
            active = !active;
            btnMic.setAttribute("aria-pressed", String(active));
            btnMic.classList.toggle("btn-accent", active);
        });
    }

    // File chips
    if (fileInput && fileChips) {
        fileInput.addEventListener("change", () => {
            fileChips.innerHTML = "";
            Array.from(fileInput.files || []).forEach((file, idx) => {
                const chip = document.createElement("span");
                chip.className = "badge rounded-pill text-bg-secondary";
                chip.textContent = file.name;
                chip.setAttribute("title", `${file.name} (${Math.round(file.size / 1024)} KB)`);
                fileChips.appendChild(chip);
            });
        });
    }

    // Copy buttons (delegated)
    if (chatScroll) {
        chatScroll.addEventListener("click", (e) => {
            const copyBtn = e.target.closest(".btn-copy");
            if (copyBtn) {
                const text = copyBtn.getAttribute("data-text") || "";
                navigator.clipboard.writeText(text).then(() => {
                    copyBtn.classList.add("active");
                    setTimeout(() => copyBtn.classList.remove("active"), 800);
                });
            }
        });

        // Regenerate (stub)
        chatScroll.addEventListener("click", (e) => {
            const regenBtn = e.target.closest(".btn-regenerate");
            if (regenBtn) {
                // You can hook this to a /ai/regenerate endpoint if desired.
                // For now, just flash the typing indicator briefly.
                showTyping(true);
                setTimeout(() => showTyping(false), 800);
            }
        });
    }

    // Send message
    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (!chatInput.value.trim()) return;

            const chatId = chatIdEl ? chatIdEl.value : "";
            const model = modelSelect ? modelSelect.value : "gpt-4o-mini";
            const temperature = tempRange ? Number(tempRange.value) : 0.7;

            // Optimistic render user bubble
            appendMessage("user", chatInput.value.trim());
            scrollToBottom();

            showTyping(true);
            disableSend(true);

            try {
                const res = await fetch("/ai/send", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        chat_id: chatId,
                        message: chatInput.value.trim(),
                        model,
                        temperature
                    })
                });
                const data = await res.json();

                if (data.chat_id && chatIdEl) chatIdEl.value = data.chat_id;
                if (Array.isArray(data.messages)) {
                    // First message is the user (already appended), next is AI
                    const ai = data.messages.find((m) => m.role === "assistant");
                    if (ai) appendMessage("assistant", ai.content, ai.timestamp);
                }
            } catch (err) {
                console.error(err);
                appendSystem("Oops, something went wrong. Please try again.");
            } finally {
                chatInput.value = "";
                showTyping(false);
                disableSend(false);
                scrollToBottom();
            }
        });

        // Shift+Enter for newline, Enter to send
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                btnSend.click();
            }
        });
    }

    function appendMessage(role, content, timestamp) {
        const isUser = role === "user";
        const row = document.createElement("div");
        row.className = `d-flex mb-3 ${isUser ? "justify-content-end" : "justify-content-start"}`;

        const wrap = document.createElement("div");
        wrap.className = `d-flex ${isUser ? "flex-row-reverse" : ""} align-items-start gap-2`;

        const avatar = document.createElement("div");
        avatar.className = `rounded-circle bg-${isUser ? "secondary" : "primary"} d-inline-flex align-items-center justify-content-center`;
        avatar.style.width = "36px";
        avatar.style.height = "36px";
        avatar.innerHTML = `<i class="bi ${isUser ? "bi-person" : "bi-robot"} text-white"></i>`;

        const bubble = document.createElement("div");
        bubble.className = `card rounded-3 shadow-sm ${isUser ? "bg-light" : ""}`;
        bubble.innerHTML = `
      <div class="card-body p-3">
        <p class="mb-1">${escapeHtml(content)}</p>
        <div class="d-flex justify-content-between align-items-center">
          <small class="text-muted">${timestamp || new Date().toISOString().slice(0, 16).replace("T", " ")}</small>
          ${!isUser ? `
            <div class="d-inline-flex gap-1">
              <button class="btn btn-outline-secondary btn-sm rounded-pill btn-copy" data-text="${escapeAttr(content)}">
                <i class="bi bi-clipboard"></i>
              </button>
              <button class="btn btn-outline-secondary btn-sm rounded-pill btn-regenerate">
                <i class="bi bi-arrow-clockwise"></i>
              </button>
            </div>` : ""}
        </div>
      </div>
    `;

        wrap.appendChild(avatar);
        wrap.appendChild(bubble);
        row.appendChild(wrap);
        chatScroll.appendChild(row);
    }

    function appendSystem(text) {
        const alert = document.createElement("div");
        alert.className = "alert alert-danger mt-2";
        alert.textContent = text;
        chatScroll.appendChild(alert);
    }

    function showTyping(show) {
        if (!typingRow) return;
        typingRow.classList.toggle("d-none", !show);
    }

    function disableSend(disabled) {
        btnSend?.toggleAttribute("disabled", disabled);
        chatInput?.toggleAttribute("disabled", disabled);
    }

    function scrollToBottom() {
        if (!chatScroll) return;
        chatScroll.scrollTop = chatScroll.scrollHeight;
    }

    function escapeHtml(s) {
        return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    }
    function escapeAttr(s) {
        return s.replace(/"/g, "&quot;");
    }

    // Clear chat
    btnClear?.addEventListener("click", async () => {
        const chatId = chatIdEl ? chatIdEl.value : "";
        if (!chatId) {
            chatScroll.innerHTML = "";
            return;
        }
        await fetch("/ai/clear", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ chat_id: chatId })
        });
        chatScroll.innerHTML = "";
    });

    // Export conversation
    btnExport?.addEventListener("click", () => {
        const texts = Array.from(chatScroll.querySelectorAll(".card-body p")).map(p => p.textContent);
        const blob = new Blob([texts.join("\n\n")], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "schoolplus_chat.txt";
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        a.remove();
    });
})();

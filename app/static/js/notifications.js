document.addEventListener("DOMContentLoaded", () => {
    // Mark as read buttons
    document.querySelectorAll(".mark-read").forEach(btn => {
        btn.addEventListener("click", () => {
            btn.closest(".card").classList.remove("border-primary");
            btn.remove();
            console.log("Notification marked as read:", btn.dataset.id);
        });
    });

    // Bulk actions
    document.getElementById("markAllRead")?.addEventListener("click", () => {
        document.querySelectorAll(".mark-read").forEach(btn => btn.click());
    });
    document.getElementById("clearAll")?.addEventListener("click", () => {
        document.querySelectorAll(".card").forEach(c => c.remove());
    });
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("Settings page loaded.");

    // Example: Toggle animations instantly
    const animSwitch = document.getElementById("animations");
    if (animSwitch) {
        animSwitch.addEventListener("change", () => {
            document.body.classList.toggle("no-animations", !animSwitch.checked);
        });
    }

    // Example: Clear cache button
    document.querySelectorAll("button.btn-outline-danger").forEach(btn => {
        btn.addEventListener("click", () => {
            alert("Cache cleared!");
        });
    });
});

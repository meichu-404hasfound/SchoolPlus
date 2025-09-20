// index.js — Home page interactivity (no inline scripts)
// Assumes Bootstrap already loaded; uses your theme’s animations and focus styles.

// IntersectionObserver to add .animate-fade when sections enter view
(function () {
  const els = document.querySelectorAll("section");
  if (!("IntersectionObserver" in window) || els.length === 0) return;

  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add("animate-fade");
        io.unobserve(e.target);
      }
    }
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });

  els.forEach((el) => io.observe(el));
})();

// Example: focus-visible helper for keyboard nav (accessibility)
document.addEventListener("keydown", (e) => {
  if (e.key === "Tab") document.documentElement.classList.add("user-tabbing");
});
document.addEventListener("mousedown", () => {
  document.documentElement.classList.remove("user-tabbing");
});

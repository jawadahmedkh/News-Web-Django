// ============================
// NewsHub Frontend JS
// ============================

// Smooth scroll for internal links
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener("click", function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
});

// Sticky navbar shadow on scroll
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.classList.add("shadow-sm", "bg-dark");
  } else {
    navbar.classList.remove("shadow-sm");
  }
});

// Track ad clicks
document.addEventListener("click", (e) => {
  if (e.target.closest(".ad-click")) {
    const adTitle = e.target.closest(".ad-click").dataset.title;
    console.log(`Ad Clicked: ${adTitle}`);
    // TODO: Send this info to backend via fetch/AJAX if needed
  }
});

// Pageview log (placeholder for analytics)
console.log(`Page Loaded: ${document.title} at ${new Date().toLocaleString()}`);

// Dark / Light mode toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.querySelector("#themeToggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
      const mode = document.body.classList.contains("dark-mode") ? "Dark" : "Light";
      console.log(`Theme switched to ${mode} Mode`);
    });
  }
});

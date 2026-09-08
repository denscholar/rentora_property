document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("dashboard-menu-button");

  const closeButton = document.getElementById("dashboard-sidebar-close");

  const sidebar = document.getElementById("dashboard-sidebar");

  const overlay = document.getElementById("dashboard-sidebar-overlay");

  if (!menuButton || !closeButton || !sidebar || !overlay) {
    return;
  }

  const openSidebar = () => {
    sidebar.classList.add("is-open");
    overlay.classList.add("is-visible");
    document.body.classList.add("dashboard-menu-open");
  };

  const closeSidebar = () => {
    sidebar.classList.remove("is-open");
    overlay.classList.remove("is-visible");
    document.body.classList.remove("dashboard-menu-open");
  };

  menuButton.addEventListener("click", openSidebar);

  closeButton.addEventListener("click", closeSidebar);

  overlay.addEventListener("click", closeSidebar);

  sidebar.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeSidebar);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeSidebar();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      closeSidebar();
    }
  });
});

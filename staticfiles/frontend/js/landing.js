document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("mobile-menu-button");

  const navigationLinks = document.getElementById("navigation-links");

  if (!menuButton || !navigationLinks) {
    return;
  }

  menuButton.addEventListener("click", () => {
    const isOpen = navigationLinks.classList.toggle("is-open");

    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  navigationLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navigationLinks.classList.remove("is-open");

      menuButton.setAttribute("aria-expanded", "false");
    });
  });
});

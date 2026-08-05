document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("mobile-menu-button");

  const closeButton = document.getElementById("mobile-menu-close");

  const mobileNavigation = document.getElementById("mobile-navigation");

  const menuOverlay = document.getElementById("mobile-menu-overlay");

  if (!menuButton || !closeButton || !mobileNavigation || !menuOverlay) {
    console.error("Rentora mobile navigation elements were not found.");

    return;
  }

  let lastFocusedElement = null;

  const openMenu = () => {
    lastFocusedElement = document.activeElement;

    mobileNavigation.classList.add("is-open");
    menuOverlay.classList.add("is-visible");
    document.body.classList.add("mobile-menu-open");

    menuButton.setAttribute("aria-expanded", "true");
    mobileNavigation.setAttribute("aria-hidden", "false");
    menuOverlay.setAttribute("aria-hidden", "false");

    window.requestAnimationFrame(() => {
      closeButton.focus();
    });
  };

  const closeMenu = () => {
    mobileNavigation.classList.remove("is-open");
    menuOverlay.classList.remove("is-visible");
    document.body.classList.remove("mobile-menu-open");

    menuButton.setAttribute("aria-expanded", "false");
    mobileNavigation.setAttribute("aria-hidden", "true");
    menuOverlay.setAttribute("aria-hidden", "true");

    if (lastFocusedElement) {
      lastFocusedElement.focus();
    }
  };

  const isMenuOpen = () => {
    return mobileNavigation.classList.contains("is-open");
  };

  menuButton.addEventListener("click", () => {
    if (isMenuOpen()) {
      closeMenu();
      return;
    }

    openMenu();
  });

  closeButton.addEventListener("click", closeMenu);
  menuOverlay.addEventListener("click", closeMenu);

  mobileNavigation.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isMenuOpen()) {
      closeMenu();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 980 && isMenuOpen()) {
      closeMenu();
    }
  });
});

// FEATURED PROPERTIES SLIDER
const sliderTrack = document.getElementById("featured-slider-track");

const previousButton = document.getElementById("featured-prev");

const nextButton = document.getElementById("featured-next");

const dotsContainer = document.getElementById("featured-slider-dots");

if (sliderTrack && previousButton && nextButton && dotsContainer) {
  const cards = Array.from(
    sliderTrack.querySelectorAll(".featured-property-card"),
  );

  let currentIndex = 0;
  let visibleCards = 3;

  const getVisibleCardCount = () => {
    if (window.innerWidth <= 700) {
      return 1;
    }

    if (window.innerWidth <= 980) {
      return 2;
    }

    return 3;
  };

  const getMaximumIndex = () => {
    return Math.max(cards.length - visibleCards, 0);
  };

  const createDots = () => {
    dotsContainer.innerHTML = "";

    const pageCount = getMaximumIndex() + 1;

    for (let index = 0; index < pageCount; index += 1) {
      const dot = document.createElement("button");

      dot.type = "button";
      dot.className = "featured-slider-dot";
      dot.setAttribute(
        "aria-label",
        `Show featured property group ${index + 1}`,
      );

      dot.addEventListener("click", () => {
        currentIndex = index;
        updateSlider();
      });

      dotsContainer.appendChild(dot);
    }
  };

  const updateSlider = () => {
    const firstCard = cards[0];

    if (!firstCard) {
      return;
    }

    const trackStyles = window.getComputedStyle(sliderTrack);

    const gap = Number.parseFloat(
      trackStyles.columnGap || trackStyles.gap || "0",
    );

    const cardWidth = firstCard.getBoundingClientRect().width;

    const offset = currentIndex * (cardWidth + gap);

    sliderTrack.style.transform = `translate3d(-${offset}px, 0, 0)`;

    previousButton.disabled = currentIndex === 0;

    nextButton.disabled = currentIndex >= getMaximumIndex();

    Array.from(dotsContainer.children).forEach((dot, index) => {
      dot.classList.toggle("is-active", index === currentIndex);

      dot.setAttribute(
        "aria-current",
        index === currentIndex ? "true" : "false",
      );
    });
  };

  const rebuildSlider = () => {
    visibleCards = getVisibleCardCount();

    currentIndex = Math.min(currentIndex, getMaximumIndex());

    createDots();
    updateSlider();
  };

  previousButton.addEventListener("click", () => {
    currentIndex = Math.max(currentIndex - 1, 0);

    updateSlider();
  });

  nextButton.addEventListener("click", () => {
    currentIndex = Math.min(currentIndex + 1, getMaximumIndex());

    updateSlider();
  });

  window.addEventListener("resize", rebuildSlider);

  rebuildSlider();
}

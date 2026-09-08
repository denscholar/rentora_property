(function () {
  "use strict";

  // =====================================================
  // NAVBAR
  // =====================================================

  const navbar = document.querySelector(".site-header");

  if (!navbar) {
    return;
  }

  // =====================================================
  // CONFIGURATION
  // =====================================================

  const COMPACT_THRESHOLD = 50;

  /*
   * Ignore tiny scroll movements.
   *
   * This prevents the navbar from rapidly
   * switching states because of 1-2px changes.
   */

  const DIRECTION_THRESHOLD = 8;

  let lastScrollY = window.scrollY;

  let ticking = false;

  // =====================================================
  // UPDATE NAVBAR
  // =====================================================

  function updateNavbar() {
    const currentScrollY = window.scrollY;

    const scrollDifference = currentScrollY - lastScrollY;

    /*
     * Always use the full navbar near
     * the top of the page.
     */

    if (currentScrollY <= COMPACT_THRESHOLD) {
      navbar.classList.remove("is-compact");

      lastScrollY = currentScrollY;

      ticking = false;

      return;
    }

    /*
     * Ignore tiny movements.
     */

    if (Math.abs(scrollDifference) < DIRECTION_THRESHOLD) {
      ticking = false;

      return;
    }

    /*
     * Scroll DOWN
     *
     * Compact the navbar.
     */

    if (scrollDifference > DIRECTION_THRESHOLD) {
      navbar.classList.add("is-compact");
    } else if (scrollDifference < -DIRECTION_THRESHOLD) {

    /*
     * Scroll UP
     *
     * Restore the navbar.
     */
      navbar.classList.remove("is-compact");
    }

    lastScrollY = currentScrollY;

    ticking = false;
  }

  // =====================================================
  // SCROLL HANDLER
  // =====================================================

  window.addEventListener(
    "scroll",
    function () {
      if (ticking) {
        return;
      }

      ticking = true;

      window.requestAnimationFrame(updateNavbar);
    },
    {
      passive: true,
    },
  );

  // =====================================================
  // INITIAL STATE
  // =====================================================

  updateNavbar();
})();

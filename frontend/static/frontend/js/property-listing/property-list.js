(function () {
  "use strict";

  // =====================================================
  // PAGE
  // =====================================================

  const page = document.getElementById("property-list-page");

  if (!page) {
    return;
  }

  // =====================================================
  // CONFIGURATION
  // =====================================================

  const apiUrl = page.dataset.propertiesApi || "/api/properties/public/";

  const state = {
    page: 1,
    pageSize: 10,

    location: "",
    propertyType: "",

    minPrice: "",
    maxPrice: "",

    propertyTypes: [],
  };

  // =====================================================
  // DOM ELEMENTS
  // =====================================================

  const elements = {
    // Search
    searchForm: document.getElementById("property-search-form"),

    locationSearch: document.getElementById("property-location-search"),

    priceRange: document.getElementById("property-price-range"),

    propertyTypeFilter: document.getElementById("property-type-filter"),

    // Results
    propertyGrid: document.getElementById("property-grid"),

    resultsCount: document.getElementById("property-results-count"),

    resultsSubtitle: document.getElementById("property-results-subtitle"),

    // Status
    status: document.getElementById("property-list-status"),

    emptyState: document.getElementById("property-empty-state"),

    clearSearch: document.getElementById("property-clear-search"),

    // Pagination
    pagination: document.querySelector(".property-pagination"),

    // Sort
    sortButton: document.getElementById("property-sort-toggle"),

    sortLabel: document.getElementById("property-sort-label"),
  };

  // =====================================================
  // VALIDATE REQUIRED ELEMENTS
  // =====================================================

  if (
    !elements.searchForm ||
    !elements.locationSearch ||
    !elements.priceRange ||
    !elements.propertyTypeFilter ||
    !elements.propertyGrid
  ) {
    console.error(
      "Property listing page could not initialize because required elements are missing.",
    );

    return;
  }

  // =====================================================
  // HTML SAFETY
  // =====================================================

  function escapeHtml(value) {
    const element = document.createElement("div");

    element.textContent = value == null ? "" : String(value);

    return element.innerHTML;
  }

  // =====================================================
  // API RESPONSE HELPERS
  // =====================================================

  function extractProperties(responseData) {
    if (Array.isArray(responseData)) {
      return {
        properties: responseData,
        pagination: {},
      };
    }

    if (Array.isArray(responseData?.results)) {
      return {
        properties: responseData.results,

        pagination: responseData.pagination || {},
      };
    }

    if (Array.isArray(responseData?.data?.results)) {
      return {
        properties: responseData.data.results,

        pagination: responseData.data.pagination || {},
      };
    }

    return {
      properties: [],
      pagination: {},
    };
  }

  function extractLookupRecords(responseData) {
    if (Array.isArray(responseData)) {
      return responseData;
    }

    if (Array.isArray(responseData?.data)) {
      return responseData.data;
    }

    if (Array.isArray(responseData?.data?.results)) {
      return responseData.data.results;
    }

    if (Array.isArray(responseData?.results)) {
      return responseData.results;
    }

    return [];
  }

  // =====================================================
  // GENERIC VALUE HELPERS
  // =====================================================

  function getNestedValue(value, fallback = "") {
    if (value === null || value === undefined || value === "") {
      return fallback;
    }

    if (typeof value === "string" || typeof value === "number") {
      return value;
    }

    return value.name || value.title || value.label || value.slug || fallback;
  }

  function getPropertyTitle(property) {
    if (!property) {
      return "Property";
    }

    return property.title || getNestedValue(property.property_type, "Property");
  }

  function getPropertyLocation(property) {
    if (!property) {
      return "Location unavailable";
    }

    if (property.area) {
      return getNestedValue(property.area, "Location unavailable");
    }

    if (property.location) {
      return getNestedValue(property.location, "Location unavailable");
    }

    return "Location unavailable";
  }

  function getCoverImage(property) {
    const image = property?.cover_image;

    if (!image) {
      return "";
    }

    if (typeof image === "string") {
      return image;
    }

    return image.url || image.secure_url || image.image_url || "";
  }

  function getPaymentFrequency(property) {
    if (!property?.payment_frequency) {
      return "";
    }

    return String(property.payment_frequency)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (character) => character.toUpperCase());
  }

  // =====================================================
  // CURRENCY
  // =====================================================

  function formatCurrency(value) {
    if (value === null || value === undefined || value === "") {
      return "Price on request";
    }

    const amount = Number(value);

    if (Number.isNaN(amount)) {
      return String(value);
    }

    return new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency: "NGN",
      maximumFractionDigits: 0,
    }).format(amount);
  }

  // =====================================================
  // PRICE RANGE
  // =====================================================

  function applyPriceRange(value) {
    state.minPrice = "";
    state.maxPrice = "";

    if (!value) {
      return;
    }

    const [minimum, maximum] = value.split("-");

    if (minimum) {
      state.minPrice = minimum.trim();
    }

    if (maximum) {
      state.maxPrice = maximum.trim();
    }
  }

  // =====================================================
  // SELECT HELPERS
  // =====================================================

  function populateSelect({ select, records, placeholder }) {
    if (!select) {
      return;
    }

    select.innerHTML = "";

    const placeholderOption = document.createElement("option");

    placeholderOption.value = "";

    placeholderOption.textContent = placeholder;

    select.appendChild(placeholderOption);

    records.forEach((record) => {
      const value = record.uuid || record.id || record.slug || "";

      const label =
        record.name ||
        record.label ||
        record.title ||
        record.property_type_name ||
        "Unnamed property type";

      if (!value) {
        return;
      }

      const option = document.createElement("option");

      option.value = value;

      option.textContent = label;

      select.appendChild(option);
    });

    select.disabled = records.length === 0;
  }

  // =====================================================
  // LOAD PROPERTY TYPE LOOKUP
  // =====================================================

  async function loadPropertyTypes() {
    try {
      const response = await fetch("/api/properties/lookups/property-types/", {
        method: "GET",

        headers: {
          Accept: "application/json",
        },

        credentials: "same-origin",
      });

      if (!response.ok) {
        throw new Error(
          `Property type request failed with status ${response.status}`,
        );
      }

      const data = await response.json();

      const records = extractLookupRecords(data);

      state.propertyTypes = records;

      populateSelect({
        select: elements.propertyTypeFilter,

        records,

        placeholder: "Any",
      });
    } catch (error) {
      console.error("Failed to load property types:", error);

      /*
       * Keep the property-type field
       * usable even if the lookup
       * request fails.
       */

      elements.propertyTypeFilter.innerHTML = `
        <option value="">
          Any
        </option>
      `;

      elements.propertyTypeFilter.disabled = false;
    }
  }

  // =====================================================
  // QUERY PARAMETERS
  // =====================================================

  function buildQueryParams(pageNumber) {
    const params = new URLSearchParams();

    params.set("page", String(pageNumber));

    params.set("page_size", String(state.pageSize));

    /*
     * The backend's existing search
     * parameter handles location
     * searching.
     */

    if (state.location) {
      params.set("search", state.location);
    }

    if (state.propertyType) {
      params.set("property_type", state.propertyType);
    }

    if (state.minPrice) {
      params.set("min_price", state.minPrice);
    }

    if (state.maxPrice) {
      params.set("max_price", state.maxPrice);
    }

    return params;
  }

  // =====================================================
  // LOADING STATE
  // =====================================================

  function setLoading(isLoading) {
    if (!elements.status) {
      return;
    }

    elements.status.hidden = !isLoading;
  }

  // =====================================================
  // RESULT STATE
  // =====================================================

  function showEmptyState() {
    if (!elements.emptyState) {
      return;
    }

    elements.emptyState.hidden = false;
  }

  function hideEmptyState() {
    if (!elements.emptyState) {
      return;
    }

    elements.emptyState.hidden = true;
  }

  // =====================================================
  // PROPERTY CARD
  // =====================================================

  function renderPropertyCard(property) {
    const uuid = property.uuid || "";

    const title = getPropertyTitle(property);

    const location = getPropertyLocation(property);

    const imageUrl = getCoverImage(property);

    const price = formatCurrency(property.proposed_price);

    const frequency = getPaymentFrequency(property);

    const bedrooms = Number(property.bedrooms || 0);

    const bathrooms = Number(property.bathrooms || 0);

    const parkingSpaces = Number(property.parking_spaces || 0);

    const isVerified =
      property.is_verified === true || Boolean(property.verification);

    // -------------------------------------------------
    // IMAGE
    // -------------------------------------------------

    const imageMarkup = imageUrl
      ? `
            <img
              src="${escapeHtml(imageUrl)}"
              alt="${escapeHtml(title)}"
              loading="lazy"
            />
          `
      : `
            <div
              class="property-card-image-placeholder"
              aria-hidden="true"
            >
              <i class="fa-regular fa-image"></i>
            </div>
          `;

    // -------------------------------------------------
    // VERIFIED BADGE
    // -------------------------------------------------

    const verifiedMarkup = isVerified
      ? `
            <span class="property-card-verified">
              <i class="fa-solid fa-check"></i>
              SheltaMe Verified
            </span>
          `
      : "";

    // -------------------------------------------------
    // PRICE
    // -------------------------------------------------

    const priceFrequency = frequency
      ? `
            <span>
              / ${escapeHtml(frequency)}
            </span>
          `
      : "";

    // -------------------------------------------------
    // CARD
    // -------------------------------------------------

    return `
      <article
        class="property-card"
        data-property-uuid="${escapeHtml(uuid)}"
      >

        <div class="property-card-image">

          ${imageMarkup}

          ${verifiedMarkup}

          <button
            type="button"
            class="property-card-favorite"
            aria-label="Save ${escapeHtml(title)}"
            data-favorite-property="${escapeHtml(uuid)}"
            aria-pressed="false"
          >
            <i class="fa-regular fa-heart"></i>
          </button>

        </div>


        <a
          href="/properties/${encodeURIComponent(uuid)}/"
          class="property-card-link"
        >

          <div class="property-card-content">

            <div class="property-card-location">
              ${escapeHtml(location)}
            </div>


            <h2 class="property-card-title">
              ${escapeHtml(title)}
            </h2>


            <div class="property-card-price">
              ${escapeHtml(price)}
              ${priceFrequency}
            </div>


            <div class="property-card-meta">

              ${
                bedrooms > 0
                  ? `
                      <span>
                        <i class="fa-solid fa-bed"></i>
                        ${bedrooms} beds
                      </span>
                    `
                  : ""
              }


              ${
                bathrooms > 0
                  ? `
                      <span>
                        <i class="fa-solid fa-bath"></i>
                        ${bathrooms} baths
                      </span>
                    `
                  : ""
              }


              ${
                parkingSpaces > 0
                  ? `
                      <span>
                        <i class="fa-solid fa-car"></i>
                        ${parkingSpaces} parking
                      </span>
                    `
                  : ""
              }

            </div>

          </div>

        </a>

      </article>
    `;
  }

  // =====================================================
  // RENDER PROPERTIES
  // =====================================================

  function renderProperties(properties) {
    elements.propertyGrid.innerHTML = "";

    if (!Array.isArray(properties) || properties.length === 0) {
      showEmptyState();
      return;
    }

    hideEmptyState();

    elements.propertyGrid.innerHTML = properties
      .map(renderPropertyCard)
      .join("");
  }

  // =====================================================
  // PAGINATION
  // =====================================================

  function createPaginationButton({
    value,
    ariaLabel,
    text,
    active = false,
    disabled = false,
  }) {
    const button = document.createElement("button");

    button.type = "button";

    button.className = "pagination-button";

    if (active) {
      button.classList.add("is-active");
    }

    button.disabled = disabled;

    button.setAttribute("aria-label", ariaLabel);

    button.textContent = text;

    return button;
  }

  function renderPagination(pagination) {
    if (!elements.pagination) {
      return;
    }

    elements.pagination.innerHTML = "";

    const currentPage = Number(pagination?.page || state.page || 1);

    const totalPages = Number(pagination?.total_pages || 1);

    if (totalPages <= 1) {
      return;
    }

    // -------------------------------------------------
    // PREVIOUS
    // -------------------------------------------------

    const previousButton = createPaginationButton({
      value: currentPage - 1,

      ariaLabel: "Previous page",

      text: "‹",

      disabled: currentPage <= 1,
    });

    if (currentPage > 1) {
      previousButton.addEventListener("click", function () {
        loadProperties(currentPage - 1);
      });
    }

    elements.pagination.appendChild(previousButton);

    // -------------------------------------------------
    // PAGE NUMBERS
    // -------------------------------------------------

    const maxVisiblePages = 5;

    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));

    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    // First page / ellipsis

    if (startPage > 1) {
      const firstButton = createPaginationButton({
        value: 1,
        ariaLabel: "Page 1",
        text: "1",
      });

      firstButton.addEventListener("click", function () {
        loadProperties(1);
      });

      elements.pagination.appendChild(firstButton);

      if (startPage > 2) {
        const ellipsis = document.createElement("span");

        ellipsis.textContent = "...";

        ellipsis.className = "pagination-ellipsis";

        elements.pagination.appendChild(ellipsis);
      }
    }

    // Pages

    for (let pageNumber = startPage; pageNumber <= endPage; pageNumber++) {
      /*
       * Avoid rendering page 1 twice
       * if it was already rendered above.
       */

      if (pageNumber === 1 && startPage > 1) {
        continue;
      }

      const button = createPaginationButton({
        value: pageNumber,

        ariaLabel: `Page ${pageNumber}`,

        text: String(pageNumber),

        active: pageNumber === currentPage,
      });

      button.addEventListener("click", function () {
        loadProperties(pageNumber);
      });

      elements.pagination.appendChild(button);
    }

    // Last page / ellipsis

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        const ellipsis = document.createElement("span");

        ellipsis.textContent = "...";

        ellipsis.className = "pagination-ellipsis";

        elements.pagination.appendChild(ellipsis);
      }

      const lastButton = createPaginationButton({
        value: totalPages,

        ariaLabel: `Page ${totalPages}`,

        text: String(totalPages),
      });

      lastButton.addEventListener("click", function () {
        loadProperties(totalPages);
      });

      elements.pagination.appendChild(lastButton);
    }

    // -------------------------------------------------
    // NEXT
    // -------------------------------------------------

    const nextButton = createPaginationButton({
      value: currentPage + 1,

      ariaLabel: "Next page",

      text: "›",

      disabled: currentPage >= totalPages,
    });

    if (currentPage < totalPages) {
      nextButton.addEventListener("click", function () {
        loadProperties(currentPage + 1);
      });
    }

    elements.pagination.appendChild(nextButton);
  }

  // =====================================================
  // LOAD PROPERTIES
  // =====================================================

  async function loadProperties(pageNumber = 1) {
    state.page = pageNumber;

    setLoading(true);

    hideEmptyState();

    try {
      const params = buildQueryParams(pageNumber);

      const response = await fetch(`${apiUrl}?${params.toString()}`, {
        method: "GET",

        headers: {
          Accept: "application/json",
        },

        credentials: "same-origin",
      });

      if (!response.ok) {
        throw new Error(
          `Property request failed with status ${response.status}`,
        );
      }

      const data = await response.json();

      const { properties, pagination } = extractProperties(data);

      renderProperties(properties);

      renderPagination(pagination);

      const count = Number(pagination?.count ?? properties.length);

      if (elements.resultsCount) {
        elements.resultsCount.textContent = `${count} ${
          count === 1 ? "property" : "properties"
        }`;
      }

      if (elements.resultsSubtitle) {
        elements.resultsSubtitle.textContent =
          count === 0
            ? "Try adjusting your search."
            : "Verified homes available on SheltaMe";
      }
    } catch (error) {
      console.error("Failed to load public properties:", error);

      elements.propertyGrid.innerHTML = "";

      hideEmptyState();

      if (elements.resultsCount) {
        elements.resultsCount.textContent = "Unable to load properties";
      }

      if (elements.resultsSubtitle) {
        elements.resultsSubtitle.textContent = "Please try again in a moment.";
      }
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // SEARCH SUBMIT
  // =====================================================

  elements.searchForm.addEventListener("submit", function (event) {
    event.preventDefault();

    state.location = elements.locationSearch.value.trim();

    state.propertyType = elements.propertyTypeFilter.value;

    applyPriceRange(elements.priceRange.value);

    loadProperties(1);
  });

  // =====================================================
  // PRICE RANGE CHANGE
  // =====================================================

  elements.priceRange.addEventListener("change", function () {
    applyPriceRange(this.value);
  });

  // =====================================================
  // PROPERTY TYPE CHANGE
  // =====================================================

  elements.propertyTypeFilter.addEventListener("change", function () {
    state.propertyType = this.value;
  });

  // =====================================================
  // CLEAR SEARCH
  // =====================================================

  if (elements.clearSearch) {
    elements.clearSearch.addEventListener("click", function () {
      elements.locationSearch.value = "";

      elements.priceRange.value = "";

      elements.propertyTypeFilter.value = "";

      state.location = "";

      state.propertyType = "";

      state.minPrice = "";

      state.maxPrice = "";

      loadProperties(1);
    });
  }

  // =====================================================
  // FAVORITES
  // =====================================================

  elements.propertyGrid.addEventListener("click", function (event) {
    const button = event.target.closest("[data-favorite-property]");

    if (!button) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    const isActive = button.classList.toggle("is-active");

    button.setAttribute("aria-pressed", String(isActive));

    const icon = button.querySelector("i");

    if (!icon) {
      return;
    }

    icon.classList.toggle("fa-regular", !isActive);

    icon.classList.toggle("fa-solid", isActive);
  });

  // =====================================================
  // SORT
  // =====================================================

  /*
   * Sorting is intentionally not sent
   * to the backend yet because the
   * current public property API contract
   * has not established a supported
   * ordering parameter.
   *
   * The button remains part of the UI,
   * ready for the backend sort contract.
   */

  if (elements.sortButton && elements.sortLabel) {
    elements.sortButton.addEventListener("click", function () {
      /*
       * Deliberately no backend request
       * here yet.
       *
       * We will wire this once the
       * public API supports ordering.
       */
      console.info(
        "Property sorting will be connected when the public API ordering contract is added.",
      );
    });
  }

  // =====================================================
  // INITIALIZE
  // =====================================================

  async function initialize() {
    await loadPropertyTypes();

    await loadProperties(1);
  }

  initialize();
})();

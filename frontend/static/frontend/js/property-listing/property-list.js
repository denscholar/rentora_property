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

  const propertyTypesApi = "/api/properties/lookups/property-types/";

  const state = {
    page: 1,
    pageSize: 10,

    location: "",
    priceRange: "",
    propertyType: "",

    ordering: "-created_at",
  };

  // =====================================================
  // DOM ELEMENTS
  // =====================================================

  const elements = {
    searchForm: document.getElementById("property-search-form"),

    locationSearch: document.getElementById("property-location-search"),

    priceRange: document.getElementById("property-price-range"),

    propertyTypeFilter: document.getElementById("property-type-filter"),

    propertyGrid: document.getElementById("property-grid"),

    status: document.getElementById("property-list-status"),

    resultsCount: document.getElementById("property-results-count"),

    resultsSubtitle: document.getElementById("property-results-subtitle"),

    emptyState: document.getElementById("property-empty-state"),

    clearSearch: document.getElementById("property-clear-search"),

    pagination: document.querySelector(".property-pagination"),

    sortSelect: document.getElementById("property-sort-select"),
  };

  // =====================================================
  // VALIDATION
  // =====================================================

  const requiredElements = [
    ["searchForm", elements.searchForm],
    ["locationSearch", elements.locationSearch],
    ["priceRange", elements.priceRange],
    ["propertyTypeFilter", elements.propertyTypeFilter],
    ["propertyGrid", elements.propertyGrid],
    ["status", elements.status],
    ["emptyState", elements.emptyState],
    ["clearSearch", elements.clearSearch],
    ["pagination", elements.pagination],
  ];

  const missingElements = requiredElements.filter(([, element]) => !element);

  if (missingElements.length > 0) {
    console.error(
      "Property listing page is missing elements:",
      missingElements.map(([name]) => name),
    );

    return;
  }

  // =====================================================
  // HTML ESCAPING
  // =====================================================

  function escapeHtml(value) {
    const element = document.createElement("div");

    element.textContent = value == null ? "" : String(value);

    return element.innerHTML;
  }

  // =====================================================
  // VALUE HELPER
  // =====================================================

  function getNestedValue(value, fallback = "") {
    if (value === null || value === undefined) {
      return fallback;
    }

    if (typeof value === "string" || typeof value === "number") {
      return value;
    }

    return value.name || value.title || value.label || value.slug || fallback;
  }

  // =====================================================
  // API RESPONSE HELPERS
  // =====================================================

  function extractApiList(data) {
    if (!data) {
      return [];
    }

    if (Array.isArray(data)) {
      return data;
    }

    if (Array.isArray(data.results)) {
      return data.results;
    }

    if (data.data && Array.isArray(data.data.results)) {
      return data.data.results;
    }

    if (data.data && Array.isArray(data.data)) {
      return data.data;
    }

    return [];
  }

  function extractPropertyResponse(data) {
    if (!data) {
      return {
        results: [],
        pagination: {},
      };
    }

    if (Array.isArray(data)) {
      return {
        results: data,
        pagination: {},
      };
    }

    if (Array.isArray(data.results)) {
      return {
        results: data.results,
        pagination: data.pagination || {},
      };
    }

    if (data.data && Array.isArray(data.data.results)) {
      return {
        results: data.data.results,
        pagination: data.data.pagination || {},
      };
    }

    return {
      results: [],
      pagination: {},
    };
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
  // PROPERTY TITLE
  // =====================================================

  function getPropertyTitle(property) {
    if (!property) {
      return "Property";
    }

    return property.title || getNestedValue(property.property_type, "Property");
  }

  // =====================================================
  // LOCATION
  // =====================================================

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

  // =====================================================
  // PAYMENT FREQUENCY
  // =====================================================

  function getPaymentFrequency(property) {
    if (!property) {
      return "";
    }

    if (!property.payment_frequency) {
      return "";
    }

    return String(property.payment_frequency);
  }

  // =====================================================
  // COVER IMAGE
  // =====================================================

  function getCoverImage(property) {
    if (!property) {
      return "";
    }

    const image = property.cover_image;

    if (!image) {
      return "";
    }

    if (typeof image === "string") {
      return image;
    }

    return image.url || image.secure_url || image.image_url || "";
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

    const parking = Number(property.parking_spaces || 0);

    const isVerified =
      property.verification?.is_verified === true ||
      property.is_verified === true;

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
            Verified
          </span>
        `
      : "";

    // -------------------------------------------------
    // PRICE FREQUENCY
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
                parking > 0
                  ? `
                    <span>
                      <i class="fa-solid fa-car"></i>
                      ${parking} parking
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
      elements.emptyState.hidden = false;

      return;
    }

    elements.emptyState.hidden = true;

    elements.propertyGrid.innerHTML = properties
      .map(renderPropertyCard)
      .join("");
  }

  // =====================================================
  // LOADING
  // =====================================================

  function setLoading(isLoading) {
    elements.status.hidden = !isLoading;
  }

  // =====================================================
  // PAGINATION
  // =====================================================

  function createPaginationButton(value, ariaLabel, text) {
    const button = document.createElement("button");

    button.type = "button";

    button.className = "pagination-button";

    button.setAttribute("aria-label", ariaLabel);

    button.textContent = text;

    return button;
  }

  function renderPagination(pagination) {
    elements.pagination.innerHTML = "";

    if (!pagination) {
      return;
    }

    const currentPage = Number(pagination.page || state.page);

    const totalPages = Number(pagination.total_pages || 1);

    if (totalPages <= 1) {
      return;
    }

    // -------------------------------------------------
    // PREVIOUS
    // -------------------------------------------------

    if (currentPage > 1) {
      const button = createPaginationButton("previous", "Previous page", "‹");

      button.addEventListener("click", function () {
        loadProperties(currentPage - 1);
      });

      elements.pagination.appendChild(button);
    }

    // -------------------------------------------------
    // PAGES
    // -------------------------------------------------

    for (let pageNumber = 1; pageNumber <= totalPages; pageNumber += 1) {
      const button = createPaginationButton(
        pageNumber,
        `Page ${pageNumber}`,
        String(pageNumber),
      );

      if (pageNumber === currentPage) {
        button.classList.add("is-active");

        button.setAttribute("aria-current", "page");
      }

      button.addEventListener("click", function () {
        loadProperties(pageNumber);
      });

      elements.pagination.appendChild(button);
    }

    // -------------------------------------------------
    // NEXT
    // -------------------------------------------------

    if (currentPage < totalPages) {
      const button = createPaginationButton("next", "Next page", "›");

      button.addEventListener("click", function () {
        loadProperties(currentPage + 1);
      });

      elements.pagination.appendChild(button);
    }
  }

  // =====================================================
  // QUERY PARAMETERS
  // =====================================================

  function buildQueryParams(pageNumber) {
    const params = new URLSearchParams();

    params.set("page", String(pageNumber));

    params.set("page_size", String(state.pageSize));

    if (state.location) {
      params.set("search", state.location);
    }

    if (state.propertyType) {
      params.set("property_type", state.propertyType);
    }

    if (state.priceRange) {
      params.set("price_range", state.priceRange);
    }

    params.set("ordering", state.ordering);

    return params;
  }

  // =====================================================
  // LOAD PROPERTY TYPES
  // =====================================================

  async function loadPropertyTypes() {
    try {
      const response = await fetch(propertyTypesApi, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        credentials: "same-origin",
      });

      if (!response.ok) {
        throw new Error(`Unable to load property types (${response.status}).`);
      }

      const data = await response.json();

      const records = extractApiList(data);

      elements.propertyTypeFilter.innerHTML = `
          <option value="">
            Any
          </option>
        `;

      records.forEach(function (record) {
        const uuid = record.uuid || record.id || record.slug || "";

        const name = record.name || record.title || record.label || "Property";

        if (!uuid) {
          return;
        }

        const option = document.createElement("option");

        option.value = uuid;
        option.textContent = name;

        elements.propertyTypeFilter.appendChild(option);
      });
    } catch (error) {
      console.error("Failed to load property types:", error);

      elements.propertyTypeFilter.innerHTML = `
          <option value="">
            Property types unavailable
          </option>
        `;
    }
  }

  // =====================================================
  // LOAD PROPERTIES
  // =====================================================

  async function loadProperties(pageNumber = 1) {
    state.page = pageNumber;

    setLoading(true);

    elements.emptyState.hidden = true;

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
          `Property request failed with status ${response.status}.`,
        );
      }

      const data = await response.json();

      const { results, pagination } = extractPropertyResponse(data);

      renderProperties(results);

      renderPagination(pagination);

      const count = Number(pagination.count ?? results.length);

      elements.resultsCount.textContent = `${count} ${
        count === 1 ? "property" : "properties"
      }`;

      elements.resultsSubtitle.textContent =
        state.location || state.priceRange || state.propertyType
          ? "Showing verified homes matching your search."
          : "Verified homes available on SheltaMe.";
    } catch (error) {
      console.error("Failed to load public properties:", error);

      elements.propertyGrid.innerHTML = "";

      elements.emptyState.hidden = true;

      elements.resultsCount.textContent = "Unable to load properties";

      elements.resultsSubtitle.textContent = "Please try again in a moment.";
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // SEARCH
  // =====================================================

  elements.searchForm.addEventListener("submit", function (event) {
    event.preventDefault();

    state.location = elements.locationSearch.value.trim();

    state.priceRange = elements.priceRange.value || "";

    state.propertyType = elements.propertyTypeFilter.value || "";

    loadProperties(1);
  });

  // =====================================================
  // SORTING
  // =====================================================

  if (elements.sortSelect) {
    elements.sortSelect.addEventListener("change", function () {
      state.ordering = this.value || "-created_at";

      loadProperties(1);
    });
  }

  // =====================================================
  // CLEAR SEARCH
  // =====================================================

  elements.clearSearch.addEventListener("click", function () {
    elements.locationSearch.value = "";

    elements.priceRange.value = "";

    elements.propertyTypeFilter.value = "";

    state.location = "";

    state.priceRange = "";

    state.propertyType = "";

    loadProperties(1);
  });

  // =====================================================
  // FAVORITE PLACEHOLDER
  // =====================================================

  elements.propertyGrid.addEventListener("click", function (event) {
    const button = event.target.closest("[data-favorite-property]");

    if (!button) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    button.classList.toggle("is-active");

    const icon = button.querySelector("i");

    if (!icon) {
      return;
    }

    icon.classList.toggle("fa-regular");

    icon.classList.toggle("fa-solid");
  });

  // =====================================================
  // INITIALIZE
  // =====================================================

  async function initialize() {
    await loadPropertyTypes();

    elements.sortSelect.value = state.ordering;

    await loadProperties(1);
  }

  initialize();
})();

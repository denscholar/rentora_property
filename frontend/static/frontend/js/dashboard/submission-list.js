document.addEventListener("DOMContentLoaded", () => {
  const submissionList = document.getElementById("submission-list");

  const loadingState = document.getElementById("submission-loading-state");

  const emptyState = document.getElementById("submission-empty-state");

  const errorState = document.getElementById("submission-error-state");

  const submissionTotal = document.getElementById("submission-total");

  const emptyTitle = document.getElementById("submission-empty-title");

  const emptyDescription = document.getElementById(
    "submission-empty-description",
  );

  const errorMessage = document.getElementById("submission-error-message");

  const retryButton = document.getElementById("retry-submissions-button");

  const paginationContainer = document.getElementById("submission-pagination");

  const previousButton = document.getElementById("submission-previous-button");

  const nextButton = document.getElementById("submission-next-button");

  const pageInfo = document.getElementById("submission-page-info");

  const searchInput = document.getElementById("submission-search-input");

  const searchButton = document.getElementById("submission-search-button");

  const filterButtons = Array.from(
    document.querySelectorAll("[data-submission-status]"),
  );

  /*
   * =========================================================
   * VALID FRONTEND STATUSES
   * =========================================================
   *
   * IMPORTANT:
   *
   * There is NO "submitted" status anymore.
   *
   * A completed property moves directly into:
   *
   *     under_review
   *
   * after the user submits it.
   */
  const FILTERABLE_STATUSES = ["draft", "under_review", "approved", "rejected"];

  /*
   * =========================================================
   * REQUIRED DOM CHECK
   * =========================================================
   */

  if (
    !submissionList ||
    !loadingState ||
    !emptyState ||
    !errorState ||
    !submissionTotal
  ) {
    return;
  }

  /*
   * =========================================================
   * FRONTEND STATE
   * =========================================================
   */

  let allSubmissions = [];

  /*
   * Empty string means:
   *
   * "Show all statuses"
   */
  let activeStatus = "";

  /*
   * Current search text.
   */
  let searchTerm = "";

  /*
   * Backend pagination state.
   */
  let currentPage = 1;
  let totalPages = 1;

  /*
   * =========================================================
   * LOAD SUBMISSIONS
   * =========================================================
   */

  const loadSubmissions = async ({
    page = 1,
    statusFilter = activeStatus,
    search = searchTerm,
  } = {}) => {
    showLoadingState();

    try {
      /*
       * Keep frontend state synchronized with the request.
       */
      currentPage = page;
      activeStatus = statusFilter;
      searchTerm = search;

      /*
       * Build query parameters.
       *
       * Example:
       *
       * /api/properties/submissions/?page=2
       *
       * or:
       *
       * /api/properties/submissions/
       *     ?page=1
       *     &status=under_review
       *     &search=lagos
       */
      const params = new URLSearchParams();

      params.set("page", currentPage);

      if (statusFilter && FILTERABLE_STATUSES.includes(statusFilter)) {
        params.set("status", statusFilter);
      }

      if (searchTerm) {
        params.set("search", searchTerm);
      }

      const result = await apiRequest(
        `/api/properties/submissions/?${params.toString()}`,
        {
          method: "GET",
        },
      );

      /*
       * =====================================================
       * AUTHENTICATION
       * =====================================================
       */

      if (!result.ok) {
        if (result.status === 401 || result.status === 403) {
          window.location.href = "/login/";
          return;
        }

        throw new Error(
          result.data?.message || "Unable to retrieve property submissions.",
        );
      }

      /*
       * =====================================================
       * EXPECTED API RESPONSE
       * =====================================================
       *
       * {
       *   success: true,
       *   message: "...",
       *   data: {
       *     results: [...],
       *     pagination: {
       *       count: 20,
       *       page: 1,
       *       page_size: 10,
       *       total_pages: 2,
       *       has_next: true,
       *       has_previous: false
       *     }
       *   }
       * }
       */

      const responseData = result.data?.data || {};

      allSubmissions = Array.isArray(responseData.results)
        ? responseData.results
        : [];

      const pagination = responseData.pagination || {};

      currentPage = Number(pagination.page) || page;

      totalPages = Number(pagination.total_pages) || 1;

      /*
       * Display total number of records returned
       * by the backend query.
       */
      updateTotalLabel(Number(pagination.count) || 0);

      /*
       * Render the current page.
       */
      renderCurrentSubmissions();

      /*
       * Render pagination controls.
       */
      renderPagination();
    } catch (error) {
      console.error("Property submissions request failed:", error);

      showErrorState(
        error.message || "Unable to load your property submissions.",
      );
    }
  };

  /*
   * =========================================================
   * FILTER AND RENDER CURRENT PAGE
   * =========================================================
   *
   * Filtering is already done by the backend.
   *
   * Therefore, we DO NOT filter allSubmissions again here.
   */

  const renderCurrentSubmissions = () => {
    submissionList.innerHTML = "";

    if (!allSubmissions.length) {
      showEmptyState();
      return;
    }

    allSubmissions.forEach((submission) => {
      submissionList.appendChild(createSubmissionCard(submission));
    });

    hideAllStates();

    submissionList.hidden = false;
  };

  /*
   * =========================================================
   * CREATE SUBMISSION CARD
   * =========================================================
   */

  const createSubmissionCard = (submission) => {
    const article = document.createElement("article");

    article.className = "submission-card";

    const title = submission.title?.trim() || "Untitled property";

    const propertyType = submission.property_type || "Property type not added";

    const area = submission.area || "Location not added";

    const bedrooms = Number(submission.bedrooms || 0);

    const price = formatCurrency(submission.proposed_price);

    const frequency = formatReadableValue(submission.payment_frequency);

    const statusDisplay =
      submission.status_display || formatReadableValue(submission.status);

    const updatedAt = formatDateTime(submission.updated_at);

    /*
     * =====================================================
     * EDIT RULE
     * =====================================================
     *
     * Draft:
     *     editable
     *
     * More information required:
     *     editable
     *
     * Under review:
     *     view only
     *
     * Approved:
     *     view only
     *
     * Rejected:
     *     view only
     */

    const canEdit = ["draft", "more_information_required"].includes(
      submission.status,
    );

    /*
     * =====================================================
     * ARCHIVE RULE
     * =====================================================
     *
     * Only approved properties can be archived.
     */

    const canArchive = submission.status === "approved";

    /*
     * =====================================================
     * SUBMISSION URL
     * =====================================================
     */

    const submissionUrl = canEdit
      ? `/dashboard/submissions/${encodeURIComponent(submission.uuid)}/edit/`
      : `/dashboard/submissions/${encodeURIComponent(submission.uuid)}/detail/`;

    /*
     * Normalize status for CSS.
     *
     * Example:
     *
     * under_review
     * approved
     * rejected
     */

    const normalizedStatus = String(
      submission.status || "unknown",
    ).toLowerCase();

    /*
     * =====================================================
     * CARD HTML
     * =====================================================
     */

    article.innerHTML = `
      <div class="submission-card-main">

        <div class="submission-property-icon">
          ⌂
        </div>

        <div class="submission-property-details">

          <div class="submission-card-title-row">

            <h3>
              ${escapeHtml(title)}
            </h3>

            <span
              class="
                submission-status
                submission-status-${escapeHtml(normalizedStatus)}
              "
            >
              ${escapeHtml(statusDisplay)}
            </span>

          </div>

          <div class="submission-meta">

            <span>
              ${escapeHtml(propertyType)}
            </span>

            <span>
              ${escapeHtml(area)}
            </span>

            <span>
              ${bedrooms}
              ${bedrooms === 1 ? "bedroom" : "bedrooms"}
            </span>

          </div>

          <div class="submission-price-row">

            ${
              price
                ? `
                  <strong>
                    ${escapeHtml(price)}
                  </strong>

                  <span>
                    /
                    ${escapeHtml(frequency || "period")}
                  </span>
                `
                : `
                  <strong>
                    Price not added
                  </strong>
                `
            }

          </div>

          <p class="submission-date">
            Last updated:
            ${escapeHtml(updatedAt)}
          </p>

        </div>

      </div>

      <div class="submission-card-actions">

        <a
          href="${submissionUrl}"
          class="
            button
            ${
              canEdit
                ? "button-primary submission-edit-button"
                : "button-secondary"
            }
          "
        >
          ${canEdit ? "Continue editing" : "View details"}
        </a>

        ${
          canArchive
            ? `
              <button
                type="button"
                class="submission-more-button"
                data-archive-submission="${escapeHtml(submission.uuid)}"
                aria-label="Archive approved property"
                title="Archive approved property"
              >
                •••
              </button>
            `
            : ""
        }

      </div>
    `;

    /*
     * Attach archive event.
     */

    const archiveButton = article.querySelector("[data-archive-submission]");

    if (archiveButton) {
      archiveButton.addEventListener("click", () => {
        archiveSubmission(submission, archiveButton);
      });
    }

    return article;
  };

  /*
   * =========================================================
   * ARCHIVE APPROVED PROPERTY
   * =========================================================
   */

  const archiveSubmission = async (submission, button) => {
    /*
     * Frontend safety check.
     */

    if (submission.status !== "approved") {
      alert("Only approved properties can be archived.");

      return;
    }

    const confirmed = window.confirm(
      `Archive "${submission.title || "this property"}"?`,
    );

    if (!confirmed) {
      return;
    }

    button.disabled = true;
    button.textContent = "...";

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          submission.uuid,
        )}/archive/`,
        {
          method: "DELETE",
        },
      );

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to archive this property.",
        );
      }

      /*
       * Remove from current page.
       */

      allSubmissions = allSubmissions.filter(
        (item) => item.uuid !== submission.uuid,
      );

      /*
       * If the current page becomes empty,
       * reload it from the backend.
       *
       * This also handles the situation where
       * the last item on a page was archived.
       */

      if (!allSubmissions.length && currentPage > 1) {
        await loadSubmissions({
          page: currentPage - 1,
          statusFilter: activeStatus,
          search: searchTerm,
        });
      } else {
        renderCurrentSubmissions();
      }

      showPageMessage("Property archived successfully.", "success");
    } catch (error) {
      console.error("Unable to archive property:", error);

      alert(error.message || "Unable to archive this property.");

      button.disabled = false;
      button.textContent = "•••";
    }
  };

  /*
   * =========================================================
   * FILTER BUTTONS
   * =========================================================
   */

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const requestedStatus = button.dataset.submissionStatus || "";

      /*
       * Safety:
       *
       * Ignore statuses that are not supported.
       *
       * This prevents "submitted" from ever being
       * sent to the API even if an old button somehow
       * remains in the HTML.
       */

      if (requestedStatus && !FILTERABLE_STATUSES.includes(requestedStatus)) {
        return;
      }

      /*
       * Clicking the active filter again
       * clears the filter.
       */

      if (activeStatus === requestedStatus) {
        activeStatus = "";
      } else {
        activeStatus = requestedStatus;
      }

      currentPage = 1;

      /*
       * Update active UI state.
       */

      filterButtons.forEach((item) => {
        const itemStatus = item.dataset.submissionStatus || "";

        item.classList.toggle("active", activeStatus === itemStatus);
      });

      /*
       * Load filtered results from backend.
       */

      loadSubmissions({
        page: 1,
        statusFilter: activeStatus,
        search: searchTerm,
      });
    });
  });

  /*
   * =========================================================
   * SEARCH
   * =========================================================
   */

  const performSearch = () => {
    if (!searchInput) {
      return;
    }

    searchTerm = searchInput.value.trim();

    currentPage = 1;

    loadSubmissions({
      page: 1,
      statusFilter: activeStatus,
      search: searchTerm,
    });
  };

  /*
   * Search button.
   */

  searchButton?.addEventListener("click", performSearch);

  /*
   * Allow Enter key to search.
   */

  searchInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();

      performSearch();
    }
  });

  /*
   * =========================================================
   * PAGINATION - PREVIOUS
   * =========================================================
   */

  previousButton?.addEventListener("click", () => {
    if (currentPage <= 1) {
      return;
    }

    loadSubmissions({
      page: currentPage - 1,
      statusFilter: activeStatus,
      search: searchTerm,
    });
  });

  /*
   * =========================================================
   * PAGINATION - NEXT
   * =========================================================
   */

  nextButton?.addEventListener("click", () => {
    if (currentPage >= totalPages) {
      return;
    }

    loadSubmissions({
      page: currentPage + 1,
      statusFilter: activeStatus,
      search: searchTerm,
    });
  });

  /*
   * =========================================================
   * RENDER PAGINATION
   * =========================================================
   */

  const renderPagination = () => {
    if (!paginationContainer || !previousButton || !nextButton || !pageInfo) {
      return;
    }

    /*
     * Hide pagination when there is only one page.
     */

    if (totalPages <= 1) {
      paginationContainer.hidden = true;

      return;
    }

    paginationContainer.hidden = false;

    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

    previousButton.disabled = currentPage <= 1;

    nextButton.disabled = currentPage >= totalPages;
  };

  /*
   * =========================================================
   * DISPLAY STATES
   * =========================================================
   */

  const hideAllStates = () => {
    loadingState.hidden = true;
    emptyState.hidden = true;
    errorState.hidden = true;
    submissionList.hidden = true;
  };

  /*
   * =========================================================
   * LOADING STATE
   * =========================================================
   */

  const showLoadingState = () => {
    hideAllStates();

    submissionTotal.textContent = "Loading submissions...";

    loadingState.hidden = false;
  };

  /*
   * =========================================================
   * EMPTY STATE
   * =========================================================
   */

  const showEmptyState = () => {
    hideAllStates();

    if (activeStatus || searchTerm) {
      emptyTitle.textContent = "No matching submissions";

      if (searchTerm && activeStatus) {
        emptyDescription.textContent =
          `No properties matching "${searchTerm}" ` +
          `were found in the selected status.`;
      } else if (searchTerm) {
        emptyDescription.textContent =
          `No properties matching "${searchTerm}" ` + "were found.";
      } else {
        emptyDescription.textContent =
          "You do not currently have property submissions with this status.";
      }
    } else {
      emptyTitle.textContent = "You haven’t submitted any properties yet";

      emptyDescription.textContent =
        "Create your first property draft and complete it at your own pace.";
    }

    emptyState.hidden = false;

    /*
     * Pagination should not remain visible
     * when there are no results.
     */

    if (paginationContainer) {
      paginationContainer.hidden = true;
    }
  };

  /*
   * =========================================================
   * ERROR STATE
   * =========================================================
   */

  const showErrorState = (message) => {
    hideAllStates();

    submissionTotal.textContent = "Unable to load submissions";

    errorMessage.textContent = message;

    errorState.hidden = false;

    if (paginationContainer) {
      paginationContainer.hidden = true;
    }
  };

  /*
   * =========================================================
   * TOTAL LABEL
   * =========================================================
   */

  const updateTotalLabel = (count) => {
    submissionTotal.textContent = `${count} submission${
      count === 1 ? "" : "s"
    }`;
  };

  /*
   * =========================================================
   * PAGE MESSAGE
   * =========================================================
   */

  const showPageMessage = (message, type = "success") => {
    const messageElement = document.getElementById("submission-page-message");

    if (!messageElement) {
      return;
    }

    messageElement.textContent = message;

    messageElement.className = `submission-page-message ${type}`;

    messageElement.hidden = false;

    window.setTimeout(() => {
      messageElement.hidden = true;
    }, 4000);
  };

  /*
   * =========================================================
   * FORMAT CURRENCY
   * =========================================================
   */

  const formatCurrency = (value) => {
    if (value === null || value === undefined || value === "") {
      return "";
    }

    const numericValue = Number(value);

    if (Number.isNaN(numericValue)) {
      return "";
    }

    return new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency: "NGN",
      maximumFractionDigits: 2,
    }).format(numericValue);
  };

  /*
   * =========================================================
   * FORMAT DATE
   * =========================================================
   */

  const formatDateTime = (value) => {
    if (!value) {
      return "Not available";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return "Not available";
    }

    return new Intl.DateTimeFormat("en-NG", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    }).format(date);
  };

  /*
   * =========================================================
   * FORMAT READABLE VALUE
   * =========================================================
   */

  const formatReadableValue = (value) => {
    if (!value) {
      return "";
    }

    return String(value)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (character) => character.toUpperCase());
  };

  /*
   * =========================================================
   * ESCAPE HTML
   * =========================================================
   */

  const escapeHtml = (value) => {
    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
  };

  /*
   * =========================================================
   * RETRY
   * =========================================================
   */

  retryButton?.addEventListener("click", () => {
    loadSubmissions({
      page: currentPage,
      statusFilter: activeStatus,
      search: searchTerm,
    });
  });

  /*
   * =========================================================
   * INITIAL LOAD
   * =========================================================
   */

  loadSubmissions({
    page: 1,
    statusFilter: "",
    search: "",
  });
});

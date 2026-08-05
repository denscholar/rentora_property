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

  const filterButtons = Array.from(
    document.querySelectorAll("[data-submission-status]"),
  );

  if (
    !submissionList ||
    !loadingState ||
    !emptyState ||
    !errorState ||
    !submissionTotal
  ) {
    return;
  }

  let allSubmissions = [];
  let activeStatus = "";

  // =================================================
  // LOAD SUBMISSIONS
  // =================================================
  const loadSubmissions = async () => {
    showLoadingState();

    try {
      const result = await apiRequest("/api/properties/submissions/", {
        method: "GET",
      });

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
       * Expected API response:
       *
       * {
       *   success: true,
       *   message: "...",
       *   data: [...]
       * }
       */
      allSubmissions = Array.isArray(result.data?.data) ? result.data.data : [];

      renderCurrentSubmissions();
    } catch (error) {
      console.error("Property submissions request failed:", error);

      showErrorState(
        error.message || "Unable to load your property submissions.",
      );
    }
  };

  // =================================================
  // FILTER AND RENDER
  // =================================================
  const renderCurrentSubmissions = () => {
    const filteredSubmissions = activeStatus
      ? allSubmissions.filter(
          (submission) => submission.status === activeStatus,
        )
      : allSubmissions;

    updateTotalLabel(filteredSubmissions.length);

    submissionList.innerHTML = "";

    if (!filteredSubmissions.length) {
      showEmptyState();
      return;
    }

    filteredSubmissions.forEach((submission) => {
      submissionList.appendChild(createSubmissionCard(submission));
    });

    hideAllStates();
    submissionList.hidden = false;
  };

  // =================================================
  // CREATE SUBMISSION CARD
  // =================================================
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

    const canEdit = ["draft", "more_information_required"].includes(
      submission.status,
    );

    const canArchive = submission.status === "draft";

    article.innerHTML = `
      <div class="submission-card-main">
        <div class="submission-property-icon">
          ⌂
        </div>

        <div class="submission-property-details">
          <div class="submission-card-title-row">
            <h3>${escapeHtml(title)}</h3>

            <span
              class="
                submission-status
                submission-status-${escapeHtml(submission.status || "unknown")}
              "
            >
              ${escapeHtml(statusDisplay)}
            </span>
          </div>

          <div class="submission-meta">
            <span>${escapeHtml(propertyType)}</span>

            <span>${escapeHtml(area)}</span>

            <span>
              ${bedrooms}
              ${bedrooms === 1 ? "bedroom" : "bedrooms"}
            </span>
          </div>

          <div class="submission-price-row">
            ${
              price
                ? `
                  <strong>${price}</strong>
                  <span>
                    / ${escapeHtml(frequency || "period")}
                  </span>
                `
                : `
                  <strong>Price not added</strong>
                `
            }
          </div>

          <p class="submission-date">
            Last updated: ${escapeHtml(updatedAt)}
          </p>
        </div>
      </div>

      <div class="submission-card-actions">
        <a
          href="/dashboard/submissions/${encodeURIComponent(
            submission.uuid,
          )}/${canEdit ? "edit" : ""}"
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
                aria-label="Archive property submission"
                title="Archive draft"
              >
                •••
              </button>
            `
            : ""
        }
      </div>
    `;

    const archiveButton = article.querySelector("[data-archive-submission]");

    if (archiveButton) {
      archiveButton.addEventListener("click", () => {
        archiveSubmission(submission, archiveButton);
      });
    }

    return article;
  };

  // =================================================
  // ARCHIVE DRAFT
  // =================================================
  const archiveSubmission = async (submission, button) => {
    const confirmed = window.confirm(
      `Archive "${submission.title || "this draft"}"?`,
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
          result.data?.message || "Unable to archive this submission.",
        );
      }

      allSubmissions = allSubmissions.filter(
        (item) => item.uuid !== submission.uuid,
      );

      renderCurrentSubmissions();

      showPageMessage("Property submission archived successfully.", "success");
    } catch (error) {
      alert(error.message || "Unable to archive this submission.");

      button.disabled = false;
      button.textContent = "•••";
    }
  };

  // =================================================
  // FILTER BUTTONS
  // =================================================
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeStatus = button.dataset.submissionStatus || "";

      filterButtons.forEach((item) => {
        item.classList.toggle("active", item === button);
      });

      renderCurrentSubmissions();
    });
  });

  // =================================================
  // DISPLAY STATES
  // =================================================
  const hideAllStates = () => {
    loadingState.hidden = true;
    emptyState.hidden = true;
    errorState.hidden = true;
    submissionList.hidden = true;
  };

  const showLoadingState = () => {
    hideAllStates();

    submissionTotal.textContent = "Loading submissions...";

    loadingState.hidden = false;
  };

  const showEmptyState = () => {
    hideAllStates();

    if (activeStatus) {
      emptyTitle.textContent = "No matching submissions";

      emptyDescription.textContent =
        "You do not currently have property submissions with this status.";
    } else {
      emptyTitle.textContent = "You haven’t submitted any properties yet";

      emptyDescription.textContent =
        "Create your first property draft and complete it at your own pace.";
    }

    emptyState.hidden = false;
  };

  const showErrorState = (message) => {
    hideAllStates();

    submissionTotal.textContent = "Unable to load submissions";

    errorMessage.textContent = message;

    errorState.hidden = false;
  };

  const updateTotalLabel = (count) => {
    submissionTotal.textContent = `${count} submission${count === 1 ? "" : "s"}`;
  };

  // =================================================
  // PAGE MESSAGE
  // =================================================
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

  // =================================================
  // UTILITIES
  // =================================================
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

  const formatReadableValue = (value) => {
    if (!value) {
      return "";
    }

    return String(value)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (character) => character.toUpperCase());
  };

  const escapeHtml = (value) => {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  };

  // =================================================
  // RETRY
  // =================================================
  retryButton?.addEventListener("click", loadSubmissions);

  loadSubmissions();
});

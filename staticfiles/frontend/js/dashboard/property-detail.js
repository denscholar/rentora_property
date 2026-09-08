document.addEventListener("DOMContentLoaded", () => {
  // =====================================================
  // PAGE PATH / SUBMISSION UUID
  // =====================================================

  const pathParts = window.location.pathname.split("/").filter(Boolean);

  /*
   * Expected detail URL:
   *
   * /dashboard/submissions/<uuid>/detail/
   * /dashboard/submissions/<uuid>/detail/
   *
   * Therefore:
   * pathParts[pathParts.length - 2] === uuid
   */

  const submissionUuid =
    pathParts.length >= 2 ? pathParts[pathParts.length - 2] : null;

  console.log("Submission UUID:", submissionUuid);

  // =====================================================
  // PROPERTY ARCHIVE MODAL DOM ELEMENTS
  // =====================================================

  const propertyArchiveModal = document.getElementById(
    "property-archive-modal",
  );

  const propertyArchiveModalMessage = document.getElementById(
    "property-archive-modal-message",
  );

  const cancelPropertyArchiveButton = document.getElementById(
    "cancel-property-archive-button",
  );

  const confirmPropertyArchiveButton = document.getElementById(
    "confirm-property-archive-button",
  );

  // =====================================================
  // UTILITY
  // =====================================================

  const escapeHtml = (value) => {
    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
  };

  // =====================================================
  // GENERAL PAGE MESSAGE
  // =====================================================

  const showGeneralMessage = (message, type = "error") => {
    const messageElement = document.getElementById("property-detail-message");

    if (!messageElement) {
      console.error(message);
      return;
    }

    messageElement.textContent = message;

    messageElement.className = `property-detail-message ${type}`;

    messageElement.hidden = false;
  };

  // =====================================================
  // GUARD AGAINST MISSING UUID
  // =====================================================

  if (!submissionUuid) {
    showGeneralMessage("Invalid property submission.", "error");

    console.error(
      "Submission UUID could not be determined from URL:",
      window.location.pathname,
    );

    return;
  }

  // =====================================================
  // PAGE STATE
  // =====================================================

  const state = {
    submissionUuid: submissionUuid,
    submission: null,
  };

  // =====================================================
  // LOAD SUBMISSION
  // =====================================================

  const loadSubmission = async () => {
    try {
      const endpoint = `/api/properties/submissions/${encodeURIComponent(
        state.submissionUuid,
      )}/`;

      console.log("Loading submission from:", endpoint);

      const result = await apiRequest(endpoint, {
        method: "GET",
      });

      console.log("Submission API response:", result);

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to load property submission.",
        );
      }

      state.submission = result.data?.data || result.data;

      console.log("Property submission:", state.submission);

      renderPropertyHeader();
      renderPropertyAmenities();
      renderPropertyDescription();
      renderPropertyOverview();
      renderPropertyLocation();
      renderPropertyPricing();
      renderPropertyMedia();
    } catch (error) {
      console.error("Unable to load property submission:", error);

      showGeneralMessage(
        error.message || "Unable to load property submission.",
        "error",
      );
    }
  };

  // =====================================================
  // CONTINUE EDITING
  // =====================================================

  const handleContinueEditing = () => {
    if (!state.submissionUuid) {
      showGeneralMessage("Invalid property submission.", "error");

      return;
    }

    const editUrl = `/dashboard/submissions/${encodeURIComponent(
      state.submissionUuid,
    )}/edit/`;

    console.log("Continue editing URL:", editUrl);

    window.location.href = editUrl;
  };

  // =====================================================
  // OPEN PROPERTY ARCHIVE MODAL
  // =====================================================

  const openPropertyArchiveModal = () => {
    const submission = state.submission;

    if (!submission || !state.submissionUuid) {
      showGeneralMessage(
        "Unable to archive this property submission.",
        "error",
      );

      return;
    }

    if (
      !propertyArchiveModal ||
      !propertyArchiveModalMessage ||
      !confirmPropertyArchiveButton
    ) {
      console.error(
        "Property archive modal elements are missing from the page.",
      );

      showGeneralMessage("Archive modal is not available.", "error");

      return;
    }

    const propertyTitle = submission.title || "this property submission";

    propertyArchiveModalMessage.textContent =
      `Are you sure you want to archive "${propertyTitle}"? ` +
      `The submission will be removed from your active submissions.`;

    propertyArchiveModal.hidden = false;

    document.body.style.overflow = "hidden";

    confirmPropertyArchiveButton.focus();
  };

  // =====================================================
  // CLOSE PROPERTY ARCHIVE MODAL
  // =====================================================

  const closePropertyArchiveModal = () => {
    if (!propertyArchiveModal) {
      return;
    }

    /*
     * Do not allow the modal to close while
     * the archive request is being processed.
     */
    if (confirmPropertyArchiveButton && confirmPropertyArchiveButton.disabled) {
      return;
    }

    propertyArchiveModal.hidden = true;

    document.body.style.overflow = "";
  };

  // =====================================================
  // RENDER PROPERTY HEADER
  // =====================================================

  const renderPropertyHeader = () => {
    const headerContainer = document.getElementById("property-detail-header");

    const submission = state.submission;

    if (!headerContainer || !submission) {
      return;
    }

    const status = String(submission.status || "").toLowerCase();

    // Only these statuses can still be edited.
    const canEdit = ["draft", "more_information_required"].includes(status);

    // Only approved properties can be archived.
    const canArchive = status === "approved";

    headerContainer.innerHTML = `
    <div class="property-detail-header-content">
    <div>
    <span class="property-status-badge">
    ${escapeHtml(submission.status_display || submission.status || "Unknown")}
    </span>

    <h1>
      ${escapeHtml(submission.title || "Untitled Property")}
    </h1>

    <p>
      ${escapeHtml(submission.area?.name || "Location not specified")}
    </p>
  </div>

  <div class="property-detail-actions">

    ${
      canEdit
        ? `
          <button
            type="button"
            id="continue-property-edit"
            class="btn btn-primary"
          >
            Continue Editing
          </button>
        `
        : ""
    }

    ${
      canArchive
        ? `
          <button
            type="button"
            id="archive-property"
            class="btn btn-danger"
          >
            Archive
          </button>
        `
        : ""
    }

  </div>
</div>
  `;

    // const continueEditButton = document.getElementById(
    //   "continue-property-edit",
    // );

    // const archiveButton = document.getElementById("archive-property");

    // continueEditButton?.addEventListener("click", handleContinueEditing);

    // archiveButton?.addEventListener("click", openPropertyArchiveModal);
    // Continue Editing
    document
      .getElementById("continue-property-edit")
      ?.addEventListener("click", handleContinueEditing);

    // Archive — only exists for approved submissions
    document
      .getElementById("archive-property")
      ?.addEventListener("click", openPropertyArchiveModal);
  };

  // =====================================================
  // PROPERTY OVERVIEW
  // =====================================================

  const renderPropertyOverview = () => {
    const container = document.getElementById("property-overview-content");

    const submission = state.submission;

    if (!container || !submission) {
      return;
    }

    container.innerHTML = `
      <div class="property-detail-grid">

        <div>
          <span>Property type</span>
          <strong>
            ${escapeHtml(submission.property_type?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Purpose</span>
          <strong>
            ${escapeHtml(submission.purpose?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Condition</span>
          <strong>
            ${escapeHtml(
              submission.property_condition?.name || "Not specified",
            )}
          </strong>
        </div>

        <div>
          <span>Furnishing</span>
          <strong>
            ${escapeHtml(submission.furnishing_status?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Bedrooms</span>
          <strong>
            ${submission.bedrooms ?? 0}
          </strong>
        </div>

        <div>
          <span>Bathrooms</span>
          <strong>
            ${submission.bathrooms ?? 0}
          </strong>
        </div>

        <div>
          <span>Toilets</span>
          <strong>
            ${submission.toilets ?? 0}
          </strong>
        </div>

        <div>
          <span>Parking spaces</span>
          <strong>
            ${submission.parking_spaces ?? 0}
          </strong>
        </div>

        <div>
          <span>Floors</span>
          <strong>
            ${submission.floors ?? 0}
          </strong>
        </div>

        <div>
          <span>Units available</span>
          <strong>
            ${submission.units_available ?? 0}
          </strong>
        </div>

        <div>
          <span>Year built</span>
          <strong>
            ${submission.year_built || "Not specified"}
          </strong>
        </div>

        <div>
          <span>Building size</span>
          <strong>
            ${submission.building_size || "Not specified"}
            ${escapeHtml(submission.size_unit || "")}
          </strong>
        </div>

        <div>
          <span>Land size</span>
          <strong>
            ${submission.land_size || "Not specified"}
            ${escapeHtml(submission.size_unit || "")}
          </strong>
        </div>

        <div>
          <span>New build</span>
          <strong>
            ${submission.is_new_build ? "Yes" : "No"}
          </strong>
        </div>

        <div>
          <span>Serviced</span>
          <strong>
            ${submission.is_serviced ? "Yes" : "No"}
          </strong>
        </div>

      </div>
    `;
  };

  // =====================================================
  // PROPERTY LOCATION
  // =====================================================

  const renderPropertyLocation = () => {
    const container = document.getElementById("property-location-content");

    const submission = state.submission;

    if (!container || !submission) {
      return;
    }

    container.innerHTML = `
      <div class="property-detail-grid">

        <div>
          <span>Country</span>
          <strong>
            ${escapeHtml(submission.country?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>State</span>
          <strong>
            ${escapeHtml(submission.state?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>LGA</span>
          <strong>
            ${escapeHtml(submission.lga?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Area</span>
          <strong>
            ${escapeHtml(submission.area?.name || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Landmark</span>
          <strong>
            ${escapeHtml(submission.landmark || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Street address</span>
          <strong>
            ${escapeHtml(submission.street_address || "Not specified")}
          </strong>
        </div>

      </div>
    `;
  };

  // =====================================================
  // PROPERTY MEDIA
  // =====================================================

  const renderPropertyMedia = () => {
    const imagesContainer = document.getElementById("property-images");

    const videoContainer = document.getElementById("property-video");

    const submission = state.submission;

    if (!submission) {
      return;
    }

    const media = submission.media || [];

    console.log("Media received:", media);

    const images = media.filter(
      (item) =>
        item.media_type === "image" && item.upload_status === "completed",
    );

    const video = media.find(
      (item) =>
        item.media_type === "video" && item.upload_status === "completed",
    );

    // ===================================================
    // IMAGES
    // ===================================================

    if (imagesContainer) {
      if (!images.length) {
        imagesContainer.innerHTML = `
          <p>
            No property images uploaded.
          </p>
        `;
      } else {
        imagesContainer.innerHTML = `
          <div class="property-detail-gallery">
            ${images
              .map(
                (image) => `
                  <div class="property-detail-gallery-item">

                    <img
                      src="${escapeHtml(image.secure_url)}"
                      alt="${escapeHtml(
                        image.alt_text ||
                          image.original_filename ||
                          "Property image",
                      )}"
                    />

                    ${
                      image.is_cover
                        ? `
                          <span class="property-media-cover-badge">
                            Cover
                          </span>
                        `
                        : ""
                    }

                  </div>
                `,
              )
              .join("")}
          </div>
        `;
      }
    }

    // ===================================================
    // VIDEO
    // ===================================================

    if (videoContainer) {
      if (!video) {
        videoContainer.innerHTML = `
          <p>
            No property video uploaded.
          </p>
        `;
      } else {
        videoContainer.innerHTML = `
          <div class="property-detail-video">

            <video
              controls
              preload="metadata"
              playsinline
            >
              <source
                src="${escapeHtml(video.secure_url)}"
                type="${escapeHtml(video.content_type || "video/mp4")}"
              />

              Your browser does not support
              video playback.
            </video>

          </div>
        `;
      }
    }
  };

  // =====================================================
  // PROPERTY PRICING
  // =====================================================

  const renderPropertyPricing = () => {
    const container = document.getElementById("property-pricing-content");

    const submission = state.submission;

    if (!container || !submission) {
      return;
    }

    const formatMoney = (value) => {
      if (value === null || value === undefined || value === "") {
        return "Not specified";
      }

      const numericValue = Number(value);

      if (Number.isNaN(numericValue)) {
        return "Not specified";
      }

      return new Intl.NumberFormat("en-NG", {
        style: "currency",
        currency: "NGN",
        maximumFractionDigits: 0,
      }).format(numericValue);
    };

    const formatPaymentFrequency = (value) => {
      if (!value) {
        return "Not specified";
      }

      return String(value)
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
    };

    container.innerHTML = `
      <div class="property-detail-grid">

        <div>
          <span>Proposed price</span>
          <strong>
            ${formatMoney(submission.proposed_price)}
          </strong>
        </div>

        <div>
          <span>Payment frequency</span>
          <strong>
            ${escapeHtml(formatPaymentFrequency(submission.payment_frequency))}
          </strong>
        </div>

        <div>
          <span>Service charge</span>
          <strong>
            ${formatMoney(submission.service_charge)}
          </strong>
        </div>

        <div>
          <span>Caution fee</span>
          <strong>
            ${formatMoney(submission.caution_fee)}
          </strong>
        </div>

        <div>
          <span>Legal fee</span>
          <strong>
            ${formatMoney(submission.legal_fee)}
          </strong>
        </div>

        <div>
          <span>Agency fee</span>
          <strong>
            ${formatMoney(submission.agency_fee)}
          </strong>
        </div>

        <div>
          <span>Negotiable</span>
          <strong>
            ${submission.is_negotiable ? "Yes" : "No"}
          </strong>
        </div>

        <div>
          <span>Available from</span>
          <strong>
            ${escapeHtml(submission.available_from || "Not specified")}
          </strong>
        </div>

        <div>
          <span>Minimum stay</span>
          <strong>
            ${
              submission.minimum_stay
                ? `${submission.minimum_stay} ${
                    submission.minimum_stay === 1 ? "month" : "months"
                  }`
                : "Not specified"
            }
          </strong>
        </div>

      </div>
    `;
  };

  // =====================================================
  // PROPERTY AMENITIES
  // =====================================================

  const renderPropertyAmenities = () => {
    const container = document.getElementById("property-amenities-content");

    const submission = state.submission;

    if (!container || !submission) {
      return;
    }

    const amenities = submission.amenities || [];

    if (!amenities.length) {
      container.innerHTML = `
        <h2>Amenities</h2>

        <p>
          No amenities added.
        </p>
      `;

      return;
    }

    container.innerHTML = `
      <div class="property-amenities-grid">

        ${amenities
          .map(
            (amenity) => `
              <div class="property-amenity-item">

                <div class="property-amenity-icon">
                  ${
                    amenity.icon
                      ? `
                        <img
                          src="${escapeHtml(amenity.icon)}"
                          alt="${escapeHtml(amenity.name || "Amenity")}"
                        />
                      `
                      : "•"
                  }
                </div>

                <div class="property-amenity-info">

                  <strong>
                    ${escapeHtml(amenity.name || "Amenity")}
                  </strong>

                  ${
                    amenity.category
                      ? `
                        <span>
                          ${escapeHtml(amenity.category)}
                        </span>
                      `
                      : ""
                  }

                </div>

              </div>
            `,
          )
          .join("")}

      </div>
    `;
  };

  // =====================================================
  // PROPERTY DESCRIPTION
  // =====================================================

  const renderPropertyDescription = () => {
    const container = document.getElementById("property-description-content");

    const submission = state.submission;

    if (!container || !submission) {
      return;
    }

    container.innerHTML = `
    <h2>Description</h2>

    <div class="property-description-content">
      ${
        submission.description
          ? `
            <p>
              ${escapeHtml(submission.description)}
            </p>
          `
          : `
            <p>
              No description provided.
            </p>
          `
      }
    </div>
  `;
  };

  // =====================================================
  // ARCHIVE PROPERTY SUBMISSION
  // =====================================================

  const archivePropertySubmission = async () => {
    if (!state.submissionUuid || !confirmPropertyArchiveButton) {
      return;
    }

    confirmPropertyArchiveButton.disabled = true;

    confirmPropertyArchiveButton.textContent = "Archiving...";

    try {
      const endpoint = `/api/properties/submissions/${encodeURIComponent(
        state.submissionUuid,
      )}/archive/`;

      const result = await apiRequest(endpoint, {
        method: "DELETE",
      });

      if (!result.ok) {
        console.error("Archive API response:", result);
        console.error(
          "Archive API errors:",
          JSON.stringify(result.data?.errors, null, 2),
        );

        throw new Error(
          result.data?.message || "Unable to archive property submission.",
        );
      }

      // -----------------------------------------------
      // CLOSE MODAL
      // -----------------------------------------------

      if (propertyArchiveModal) {
        propertyArchiveModal.hidden = true;
      }

      document.body.style.overflow = "";

      // -----------------------------------------------
      // REDIRECT TO SUBMISSIONS LIST
      // -----------------------------------------------

      window.location.href = "/dashboard/submissions/";
    } catch (error) {
      console.error("Unable to archive property submission:", error);

      showGeneralMessage(
        error.message || "Unable to archive property submission.",
        "error",
      );
    } finally {
      confirmPropertyArchiveButton.disabled = false;

      confirmPropertyArchiveButton.textContent = "Archive";
    }
  };

  // =====================================================
  // ARCHIVE MODAL EVENTS
  // =====================================================

  cancelPropertyArchiveButton?.addEventListener(
    "click",
    closePropertyArchiveModal,
  );

  confirmPropertyArchiveButton?.addEventListener(
    "click",
    archivePropertySubmission,
  );

  // =====================================================
  // OPTIONAL: CLOSE MODAL WHEN CLICKING BACKDROP
  // =====================================================

  propertyArchiveModal?.addEventListener("click", (event) => {
    if (event.target === propertyArchiveModal) {
      closePropertyArchiveModal();
    }
  });

  // =====================================================
  // OPTIONAL: ESCAPE KEY CLOSES MODAL
  // =====================================================

  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      propertyArchiveModal &&
      !propertyArchiveModal.hidden
    ) {
      closePropertyArchiveModal();
    }
  });

  // =====================================================
  // INITIALIZE PAGE
  // =====================================================

  loadSubmission();
});

document.addEventListener("DOMContentLoaded", () => {
  // =================================================
  // DOM ELEMENTS
  // =================================================

  const wizardForm = document.getElementById("property-wizard-form");

  const loadingState = document.getElementById("wizard-loading-state");

  const loadErrorState = document.getElementById("wizard-load-error");

  const loadErrorMessage = document.getElementById("wizard-load-error-message");

  const retryButton = document.getElementById("wizard-retry-button");

  const propertyTypeContainer = document.getElementById(
    "property-type-options",
  );

  const purposeContainer = document.getElementById("property-purpose-options");

  const titleInput = document.getElementById("property-title");

  const descriptionInput = document.getElementById("property-description");

  const descriptionCount = document.getElementById(
    "description-character-count",
  );

  const nextButton = document.getElementById("wizard-next-button");

  const nextButtonText = document.getElementById("wizard-next-button-text");

  const saveDraftButton = document.getElementById("wizard-save-draft-button");

  const previousButton = document.getElementById("wizard-previous-button");

  const saveStatus = document.querySelector(".wizard-save-status");

  const saveStatusText = document.getElementById("wizard-save-text");

  const generalMessage = document.getElementById("wizard-general-message");

  // Step 2 location elements
  const countrySelect = document.getElementById("property-country");

  const stateSelect = document.getElementById("property-state");

  const lgaSelect = document.getElementById("property-lga");

  const areaSelect = document.getElementById("property-area");

  const streetAddressInput = document.getElementById("property-street-address");

  const landmarkInput = document.getElementById("property-landmark");

  const latitudeInput = document.getElementById("property-latitude");

  const longitudeInput = document.getElementById("property-longitude");

  const currentLocationButton = document.getElementById(
    "use-current-location-button",
  );

  const currentLocationMessage = document.getElementById(
    "current-location-message",
  );

  // step 3 elements
  // =================================================
  // STEP 3 PROPERTY DETAIL ELEMENTS
  // =================================================

  const propertyConditionContainer = document.getElementById(
    "property-condition-options",
  );

  const furnishingStatusContainer = document.getElementById(
    "furnishing-status-options",
  );

  const bedroomsInput = document.getElementById("property-bedrooms");
  const bathroomsInput = document.getElementById("property-bathrooms");
  const toiletsInput = document.getElementById("property-toilets");
  const parkingSpacesInput = document.getElementById("property-parking-spaces");
  const yearBuiltInput = document.getElementById("property-year-built");
  const landSizeInput = document.getElementById("property-land-size");
  const buildingSizeInput = document.getElementById("property-building-size");

  // =================================================
  // STEP 4 PRICING ELEMENTS
  // =================================================

  const proposedPriceInput = document.getElementById("property-proposed-price");
  const paymentFrequencySelect = document.getElementById(
    "property-payment-frequency",
  );
  const isNegotiableInput = document.getElementById("property-is-negotiable");
  const serviceChargeInput = document.getElementById("property-service-charge");
  const cautionFeeInput = document.getElementById("property-caution-fee");
  const legalFeeInput = document.getElementById("property-legal-fee");
  const agencyFeeInput = document.getElementById("property-agency-fee");
  const availableFromInput = document.getElementById("property-available-from");
  const minimumStayInput = document.getElementById("property-minimum-stay");
  const totalCostElement = document.getElementById("property-total-cost");

  // ===================================================
  // STEP 5
  // ==================================================
  // =================================================
  // STEP 5 AMENITY ELEMENTS
  // =================================================

  const amenityCategoryList = document.getElementById("amenity-category-list");
  const amenityEmptyState = document.getElementById("amenity-empty-state");
  const selectedAmenityCount = document.getElementById(
    "selected-amenity-count",
  );

  // ===================================================
  // MODAL DOM ELEMENT
  // ===================================================
  const mediaDeleteModal = document.getElementById("media-delete-modal");

  const mediaDeleteModalMessage = document.getElementById(
    "media-delete-modal-message",
  );

  const cancelMediaDeleteButton = document.getElementById(
    "cancel-media-delete-button",
  );

  const confirmMediaDeleteButton = document.getElementById(
    "confirm-media-delete-button",
  );

  // =================================================
  // STEP 6 DOM MEDIA ELEMENTS
  // =================================================

  const imageDropzone = document.getElementById("property-image-dropzone");
  const imageInput = document.getElementById("property-image-input");
  const imageGrid = document.getElementById("property-image-grid");
  const imageEmptyState = document.getElementById("property-image-empty");
  const imageUploadProgress = document.getElementById("image-upload-progress");
  const imageUploadProgressText = document.getElementById(
    "image-upload-progress-text",
  );

  const imageUploadProgressCount = document.getElementById(
    "image-upload-progress-count",
  );

  const imageUploadProgressBar = document.getElementById(
    "image-upload-progress-bar",
  );

  const videoDropzone = document.getElementById("property-video-dropzone");
  const videoInput = document.getElementById("property-video-input");
  const videoUploadProgress = document.getElementById("video-upload-progress");
  const videoPreview = document.getElementById("property-video-preview");
  const mediaUploadMessage = document.getElementById("media-upload-message");

  // =================================================
  // STEP 7 REVIEW ELEMENTS
  // =================================================

  const reviewLoadingState = document.getElementById("review-loading-state");

  const reviewErrorMessage = document.getElementById("review-error-message");

  const reviewContent = document.getElementById("property-review-content");

  const reviewCoverImage = document.getElementById("review-cover-image");

  const reviewStatusBadge = document.getElementById("review-status-badge");

  const reviewPropertyTitle = document.getElementById("review-property-title");

  const reviewPropertyLocation = document.getElementById(
    "review-property-location",
  );

  const reviewPropertyPrice = document.getElementById("review-property-price");

  const reviewBasicInformation = document.getElementById(
    "review-basic-information",
  );

  const reviewLocationInformation = document.getElementById(
    "review-location-information",
  );

  const reviewPropertyDetails = document.getElementById(
    "review-property-details",
  );

  const reviewPricingInformation = document.getElementById(
    "review-pricing-information",
  );

  const reviewTotalCost = document.getElementById("review-total-cost");

  const reviewAmenityList = document.getElementById("review-amenity-list");

  const reviewMediaGrid = document.getElementById("review-media-grid");

  // =========================================
  // EDITING DOM ELEMENT
  // =========================================
  const propertyTitleInput = document.getElementById("property-title");

  const propertyDescriptionInput = document.getElementById(
    "property-description",
  );

  const propertyStreetAddressInput = document.getElementById(
    "property-street-address",
  );

  if (
    !wizardForm ||
    !loadingState ||
    !loadErrorState ||
    !propertyTypeContainer ||
    !purposeContainer ||
    !titleInput ||
    !descriptionInput ||
    !nextButton ||
    !nextButtonText ||
    !saveDraftButton ||
    !previousButton ||
    !saveStatus ||
    !saveStatusText ||
    !generalMessage ||
    !countrySelect ||
    !stateSelect ||
    !lgaSelect ||
    !areaSelect ||
    !streetAddressInput ||
    !landmarkInput ||
    !latitudeInput ||
    !longitudeInput ||
    !propertyConditionContainer ||
    !furnishingStatusContainer ||
    !bedroomsInput ||
    !bathroomsInput ||
    !toiletsInput ||
    !parkingSpacesInput ||
    !yearBuiltInput ||
    !landSizeInput ||
    !buildingSizeInput ||
    !proposedPriceInput ||
    !paymentFrequencySelect ||
    !isNegotiableInput ||
    !serviceChargeInput ||
    !cautionFeeInput ||
    !legalFeeInput ||
    !agencyFeeInput ||
    !availableFromInput ||
    !minimumStayInput ||
    !totalCostElement ||
    !imageDropzone ||
    !imageInput ||
    !imageGrid ||
    !imageEmptyState ||
    !imageUploadProgress ||
    !imageUploadProgressText ||
    !imageUploadProgressCount ||
    !imageUploadProgressBar ||
    !videoDropzone ||
    !videoInput ||
    !videoUploadProgress ||
    !videoPreview ||
    !mediaUploadMessage ||
    !mediaDeleteModal ||
    !amenityCategoryList ||
    !amenityEmptyState ||
    !selectedAmenityCount ||
    !mediaDeleteModalMessage ||
    !cancelMediaDeleteButton ||
    !confirmMediaDeleteButton ||
    !reviewLoadingState ||
    !reviewErrorMessage ||
    !reviewContent ||
    !reviewCoverImage ||
    !reviewStatusBadge ||
    !reviewPropertyTitle ||
    !reviewPropertyLocation ||
    !reviewPropertyPrice ||
    !reviewBasicInformation ||
    !reviewLocationInformation ||
    !reviewPropertyDetails ||
    !reviewPricingInformation ||
    !reviewTotalCost ||
    !reviewAmenityList ||
    !reviewMediaGrid
  ) {
    return;
  }
  // =================================================
  // APPLICATION STATE
  // =================================================

  const state = {
    currentStep: 1,

    submissionUuid:
      window.submissionWizard?.submissionUuid ||
      sessionStorage.getItem("submission_uuid") ||
      null,

    propertyTypes: [],
    purposes: [],

    countries: [],
    states: [],
    lgas: [],
    areas: [],
    propertyConditions: [],
    furnishingStatuses: [],
    paymentFrequencies: [],
    media: [],
    mediaPendingDeletion: null,
    amenities: [],
    selectedAmenities: new Set(),

    selectedPropertyCondition: "",
    selectedFurnishingStatus: "",

    selectedPropertyType: "",
    selectedPurpose: "",

    selectedCountry: "",
    selectedState: "",
    selectedLga: "",
    selectedArea: "",
  };

  // =================================================
  // API ENDPOINTS
  // =================================================
  const locationEndpoints = {
    countries: "/api/locations/countries/",

    states: (countryUuid) =>
      `/api/locations/states/?uuid=${encodeURIComponent(countryUuid)}`,

    lgas: (stateUuid) =>
      `/api/locations/lgas/?uuid=${encodeURIComponent(stateUuid)}`,

    areas: (lgaUuid) =>
      `/api/locations/areas/?uuid=${encodeURIComponent(lgaUuid)}`,
  };

  // =================================================
  // GENERAL UTILITIES
  // =================================================

  const escapeHtml = (value) => {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  };

  const extractApiList = (responseData) => {
    const data = responseData?.data;

    if (Array.isArray(data)) {
      return data;
    }

    if (Array.isArray(data?.results)) {
      return data.results;
    }

    return [];
  };

  const getPurposeCode = (code) => {
    const purposeCodes = {
      rent: "RNT",
      sale: "SAL",
      lease: "LSE",
      shortlet: "SHT",
    };

    const normalizedCode = String(code || "").toLowerCase();

    return purposeCodes[normalizedCode] || String(code || "PRP").toUpperCase();
  };

  // =================================================
  // DISPLAY HELPERS
  // =================================================

  const showLoading = () => {
    wizardForm.hidden = true;
    loadErrorState.hidden = true;
    loadingState.hidden = false;
  };

  const showLoadError = (message) => {
    loadingState.hidden = true;
    wizardForm.hidden = true;
    loadErrorState.hidden = false;

    if (loadErrorMessage) {
      loadErrorMessage.textContent = message;
    }
  };

  const setSavingState = () => {
    saveStatus.className = "wizard-save-status saving";

    saveStatusText.textContent = "Saving...";
  };

  const setSavedState = () => {
    saveStatus.className = "wizard-save-status saved";

    saveStatusText.textContent = "Draft saved";
  };

  const setSaveErrorState = () => {
    saveStatus.className = "wizard-save-status error";

    saveStatusText.textContent = "Save failed";
  };

  const markUnsaved = () => {
    saveStatus.className = "wizard-save-status";

    saveStatusText.textContent = "Unsaved changes";
  };

  const showGeneralMessage = (message, type) => {
    generalMessage.textContent = message;

    generalMessage.className = `wizard-general-message ${type}`;

    generalMessage.hidden = false;

    window.setTimeout(() => {
      generalMessage.hidden = true;
    }, 4000);
  };

  const showCurrentLocationMessage = (message, type) => {
    if (!currentLocationMessage) {
      return;
    }

    currentLocationMessage.textContent = message;

    currentLocationMessage.className = `wizard-location-message ${type}`;

    currentLocationMessage.hidden = false;
  };

  const setFieldError = (fieldName, message) => {
    const errorElement = wizardForm.querySelector(
      `[data-error-for="${fieldName}"]`,
    );

    if (errorElement) {
      errorElement.textContent = message;
    }
  };

  const showFieldErrors = (errors) => {
    Object.entries(errors).forEach(([fieldName, messages]) => {
      const message = Array.isArray(messages)
        ? messages.join(" ")
        : String(messages);

      setFieldError(fieldName, message);
    });
  };

  const clearFieldError = (fieldName) => {
    setFieldError(fieldName, "");
  };

  const clearAllErrors = () => {
    wizardForm.querySelectorAll(".wizard-field-error").forEach((element) => {
      element.textContent = "";
    });

    generalMessage.hidden = true;
  };

  // =================================================
  // MEDIA RENDERING
  // =================================================

  const renderSubmissionMedia = () => {
    const images = state.media.filter((media) => media.media_type === "image");

    const video = state.media.find((media) => media.media_type === "video");

    renderImages(images);
    renderVideo(video);
  };

  const renderImages = (images) => {
    imageGrid.innerHTML = "";

    imageEmptyState.hidden = images.length > 0;

    images.forEach((media) => {
      const card = document.createElement("article");

      card.className = "property-media-card";

      card.innerHTML = `
      <div class="property-media-card-image">
        <img
          src="${escapeHtml(media.secure_url)}"
          alt="${escapeHtml(
            media.alt_text || media.original_filename || "Property image",
          )}"
        >

        ${
          media.is_cover
            ? `
              <span class="property-media-cover-badge">
                Cover
              </span>
            `
            : ""
        }
      </div>

      <div class="property-media-card-content">
        <strong>
          ${escapeHtml(media.original_filename || "Property image")}
        </strong>

        <div class="property-media-card-actions">
          ${
            media.is_cover
              ? ""
              : `
                <button
                  type="button"
                  class="property-media-action"
                  data-set-cover
                >
                  Set cover
                </button>
              `
          }

          <button
            type="button"
            class="property-media-action danger"
            data-delete-media
          >
            Delete
          </button>
        </div>
      </div>
    `;

      card
        .querySelector("[data-set-cover]")
        ?.addEventListener("click", () => setCoverMedia(media));

      card
        .querySelector("[data-delete-media]")
        ?.addEventListener("click", () => openMediaDeleteModal(media));

      imageGrid.appendChild(card);
    });
  };

  const renderVideo = (media) => {
    videoPreview.innerHTML = "";

    if (!media) {
      videoPreview.hidden = true;
      videoDropzone.hidden = false;
      return;
    }

    videoPreview.hidden = false;
    videoDropzone.hidden = true;

    videoPreview.innerHTML = `
    <video
      controls
      preload="metadata"
    >
      <source
        src="${escapeHtml(media.secure_url)}"
        type="${escapeHtml(media.content_type || "video/mp4")}"
      >
      Your browser does not support video playback.
    </video>

    <div class="property-video-actions">
      <button
        type="button"
        class="property-media-action danger"
        id="delete-property-video"
      >
        Delete video
      </button>
    </div>
  `;

    videoPreview
      .querySelector("#delete-property-video")
      ?.addEventListener("click", () => openMediaDeleteModal(media));
  };

  const showMediaMessage = (message, type) => {
    mediaUploadMessage.textContent = message;

    mediaUploadMessage.className = `media-upload-message ${type}`;

    mediaUploadMessage.hidden = false;

    window.setTimeout(() => {
      mediaUploadMessage.hidden = true;
    }, 5000);
  };

  // ===========================================
  // IMAGE UPLOAD HANDLER
  // ===========================================
  const handleImageFiles = async (selectedFiles) => {
    const files = Array.from(selectedFiles);

    if (!files.length) {
      return;
    }

    const existingImageCount = state.media.filter(
      (media) => media.media_type === "image",
    ).length;

    if (existingImageCount + files.length > 10) {
      showMediaMessage(
        "You can upload a maximum of 10 property images.",
        "error",
      );

      return;
    }

    imageUploadProgress.hidden = false;

    let completedUploads = 0;

    imageUploadProgressBar.style.width = "0%";

    imageUploadProgressCount.textContent = `0 / ${files.length}`;

    try {
      for (const file of files) {
        imageUploadProgressText.textContent = `Uploading ${file.name}...`;

        await uploadSubmissionMedia({
          file,
          mediaType: "image",
          isCover: existingImageCount === 0 && completedUploads === 0,
        });

        completedUploads += 1;

        const percentage = Math.round((completedUploads / files.length) * 100);

        imageUploadProgressBar.style.width = `${percentage}%`;

        imageUploadProgressCount.textContent = `${completedUploads} / ${files.length}`;
      }

      await loadSubmissionMedia();

      showMediaMessage(
        `${completedUploads} image${
          completedUploads === 1 ? "" : "s"
        } uploaded successfully.`,
        "success",
      );
    } catch (error) {
      await loadSubmissionMedia();

      showMediaMessage(
        error.message || "One or more images could not be uploaded.",
        "error",
      );
    } finally {
      window.setTimeout(() => {
        imageUploadProgress.hidden = true;
      }, 900);

      imageInput.value = "";
    }
  };

  // ===========================================
  // VIDEO UPLOAD HANDLER
  // ===========================================

  const handleVideoFile = async (file) => {
    if (!file) {
      return;
    }

    const allowedExtensions = [".mp4", ".mov", ".webm"];

    const allowedContentTypes = ["video/mp4", "video/quicktime", "video/webm"];

    const filename = String(file.name || "").toLowerCase();

    const hasValidExtension = allowedExtensions.some((extension) =>
      filename.endsWith(extension),
    );

    const hasValidContentType = allowedContentTypes.includes(file.type);

    if (!hasValidExtension && !hasValidContentType) {
      showMediaMessage("Please select an MP4, MOV, or WEBM video.", "error");

      videoInput.value = "";

      return;
    }

    const maximumVideoSize = 100 * 1024 * 1024;

    if (file.size > maximumVideoSize) {
      showMediaMessage("The property video cannot exceed 100 MB.", "error");

      videoInput.value = "";

      return;
    }

    const existingVideo = state.media.some(
      (media) => media.media_type === "video",
    );

    if (existingVideo) {
      showMediaMessage(
        "Only one property video is allowed. Delete the existing video before uploading another.",
        "error",
      );

      videoInput.value = "";

      return;
    }

    if (!state.submissionUuid) {
      showMediaMessage(
        "Save the property draft before uploading a video.",
        "error",
      );

      videoInput.value = "";

      return;
    }

    videoUploadProgress.hidden = false;
    videoDropzone.hidden = true;

    try {
      await uploadSubmissionMedia({
        file,
        mediaType: "video",
        isCover: false,
      });

      await loadSubmissionMedia();

      showMediaMessage("Property video uploaded successfully.", "success");
    } catch (error) {
      videoDropzone.hidden = false;

      showMediaMessage(
        error.message || "Unable to upload the property video.",
        "error",
      );
    } finally {
      videoUploadProgress.hidden = true;
      videoInput.value = "";
    }
  };

  // =================================================
  // LOCATION SELECT HELPERS
  // =================================================

  const renderSelectOptions = ({ select, records, placeholder }) => {
    select.innerHTML = "";

    const placeholderOption = document.createElement("option");

    placeholderOption.value = "";
    placeholderOption.textContent = placeholder;

    select.appendChild(placeholderOption);

    records.forEach((record) => {
      const option = document.createElement("option");

      option.value = record.uuid || record.id || record.slug || "";

      option.textContent =
        record.name ||
        record.country_name ||
        record.state_name ||
        record.lga_name ||
        record.area_name ||
        "Unnamed option";

      select.appendChild(option);
    });

    select.disabled = records.length === 0;
  };

  const resetLocationSelect = ({ select, placeholder }) => {
    select.innerHTML = `
      <option value="">
        ${escapeHtml(placeholder)}
      </option>
    `;

    select.disabled = true;
    select.classList.remove("is-loading");
  };

  const setSelectLoading = (select, placeholder) => {
    select.innerHTML = `
      <option value="">
        ${escapeHtml(placeholder)}
      </option>
    `;

    select.disabled = true;
    select.classList.add("is-loading");
  };

  const removeSelectLoading = (select) => {
    select.classList.remove("is-loading");
  };

  // =================================================
  // LOAD INITIAL LOOKUPS
  // =================================================

  const loadLookups = async () => {
    showLoading();

    try {
      const [
        propertyTypeResult,
        purposeResult,
        propertyConditionResult,
        furnishingStatusResult,
        paymentFrequencyResult,
        amenityResult,
        countryResult,
      ] = await Promise.all([
        apiRequest("/api/properties/lookups/property-types/", {
          method: "GET",
        }),

        apiRequest("/api/properties/lookups/property-purposes/", {
          method: "GET",
        }),

        apiRequest("/api/properties/lookups/property-conditions/", {
          method: "GET",
        }),

        apiRequest("/api/properties/lookups/furnishing-statuses/", {
          method: "GET",
        }),

        apiRequest("/api/properties/lookups/payment-frequencies/", {
          method: "GET",
        }),

        apiRequest("/api/properties/lookups/amenities/", {
          method: "GET",
        }),

        apiRequest(locationEndpoints.countries, {
          method: "GET",
        }),
      ]);

      if (!amenityResult.ok) {
        throw new Error(
          amenityResult.data?.message || "Unable to load amenities.",
        );
      }

      if (!paymentFrequencyResult.ok) {
        throw new Error(
          paymentFrequencyResult.data?.message ||
            "Unable to load payment frequencies.",
        );
      }

      if (!propertyConditionResult.ok) {
        throw new Error(
          propertyConditionResult.data?.message ||
            "Unable to load property conditions.",
        );
      }

      if (!furnishingStatusResult.ok) {
        throw new Error(
          furnishingStatusResult.data?.message ||
            "Unable to load furnishing statuses.",
        );
      }

      if (!propertyTypeResult.ok) {
        throw new Error(
          propertyTypeResult.data?.message || "Unable to load property types.",
        );
      }

      if (!purposeResult.ok) {
        throw new Error(
          purposeResult.data?.message || "Unable to load property purposes.",
        );
      }

      if (!countryResult.ok) {
        throw new Error(
          countryResult.data?.message || "Unable to load countries.",
        );
      }

      state.propertyTypes = extractApiList(propertyTypeResult.data);
      state.purposes = extractApiList(purposeResult.data);
      state.countries = extractApiList(countryResult.data);
      state.propertyConditions = extractApiList(propertyConditionResult.data);
      state.paymentFrequencies = extractApiList(paymentFrequencyResult.data);
      state.amenities = extractApiList(amenityResult.data);

      state.furnishingStatuses = extractApiList(furnishingStatusResult.data);

      renderPropertyTypes();
      renderAmenities();
      renderPaymentFrequencies();
      renderPurposes();
      renderPropertyConditions();
      renderFurnishingStatuses();

      renderSelectOptions({
        select: countrySelect,
        records: state.countries,
        placeholder: "Select country",
      });

      loadingState.hidden = true;
      loadErrorState.hidden = true;
      wizardForm.hidden = false;
      await loadExistingSubmission();
    } catch (error) {
      showLoadError(error.message || "Unable to load the property options.");
    }
  };

  // ==============================================
  // CREATE A LOADER FUNCTION
  // ==============================================
  const loadExistingSubmission = async () => {
    if (!state.submissionUuid) {
      return;
    }

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${state.submissionUuid}/`,
        {
          method: "GET",
        },
      );

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to load property submission.",
        );
      }

      const submission = result.data?.data || result.data;

      hydrateSubmissionState(submission);

      // Refresh the UI
      renderPropertyTypes();
      renderPurposes();
      renderPropertyConditions();
      renderFurnishingStatuses();
      renderAmenities();

      // Restore cascading selects
      countrySelect.value = state.selectedCountry;
      await loadStates(state.selectedCountry);
      stateSelect.value = state.selectedState;
      await loadLgas(stateSelect.value);
      lgaSelect.value = state.selectedLga;
      await loadAreas(lgaSelect.value);
      areaSelect.value = state.selectedArea;

      // Restore uploaded images & video
      await loadSubmissionMedia();
    } catch (error) {
      showGeneralMessage(error.message || "Unable to load property.", "error");
    }
  };

  const hydrateSubmissionState = (submission) => {
    state.selectedPropertyType =
      submission.property_type?.uuid || submission.property_type || "";

    state.selectedPurpose =
      submission.purpose?.uuid || submission.purpose || "";

    propertyDescriptionInput.value = submission.description || "";
    propertyStreetAddressInput.value = submission.street_address || "";

    // step 2

    state.selectedCountry =
      submission.country?.uuid || submission.country || "";

    state.selectedState = submission.state?.uuid || submission.state || "";
    state.selectedLga = submission.lga?.uuid || submission.lga || "";

    state.selectedArea = submission.area?.uuid || submission.area || "";

    propertyTitleInput.value = submission.title || "";
    landmarkInput.value = submission.landmark || "";
    latitudeInput.value = submission.latitude || "";
    longitudeInput.value = submission.longitude || "";

    // step 3

    state.selectedPropertyCondition =
      submission.property_condition?.uuid ||
      submission.property_condition ||
      "";
    state.selectedFurnishingStatus =
      submission.furnishing_status?.uuid || submission.furnishing_status || "";

    bedroomsInput.value = submission.bedrooms ?? 0;
    bathroomsInput.value = submission.bathrooms ?? 0;
    toiletsInput.value = submission.toilets ?? 0;
    parkingSpacesInput.value = submission.parking_spaces ?? 0;
    yearBuiltInput.value = submission.year_built || "";
    landSizeInput.value = submission.land_size || "";
    buildingSizeInput.value = submission.building_size || "";

    // hydrate 4
    proposedPriceInput.value = submission.proposed_price || "";
    paymentFrequencySelect.value = submission.payment_frequency || "annually";
    isNegotiableInput.checked = Boolean(submission.is_negotiable);
    serviceChargeInput.value = submission.service_charge || 0;
    cautionFeeInput.value = submission.caution_fee || 0;
    legalFeeInput.value = submission.legal_fee || 0;
    agencyFeeInput.value = submission.agency_fee || 0;
    availableFromInput.value = submission.available_from || "";
    minimumStayInput.value = submission.minimum_stay || "";

    // reset the price
    updateTotalCost();

    // hydrate 5
    state.selectedAmenities.clear();
    (submission.amenities || []).forEach((amenity) => {
      if (typeof amenity === "string") {
        state.selectedAmenities.add(amenity);
      } else {
        state.selectedAmenities.add(amenity.uuid);
      }
    });
  };

  // =================================================
  // PROPERTY TYPE AND PURPOSE OPTIONS
  // =================================================

  const renderPropertyTypes = () => {
    propertyTypeContainer.innerHTML = "";

    state.propertyTypes.forEach((propertyType) => {
      const card = createOptionCard({
        groupName: "property_type",
        value: propertyType.uuid,
        name: propertyType.name,

        description: propertyType.description || "Select this property type.",

        image: propertyType.icon || "",

        code: propertyType.code || "PRP",

        selected: state.selectedPropertyType === propertyType.uuid,
      });

      propertyTypeContainer.appendChild(card);
    });
  };

  const renderPurposes = () => {
    purposeContainer.innerHTML = "";

    state.purposes.forEach((purpose) => {
      const card = createOptionCard({
        groupName: "purpose",
        value: purpose.uuid,
        name: purpose.name,

        description: purpose.description || "Select this listing purpose.",

        image: "",

        code: getPurposeCode(purpose.code),

        selected: state.selectedPurpose === purpose.uuid,
      });

      purposeContainer.appendChild(card);
    });
  };

  // ====================================
  // step 3 rendering function
  // ==================================

  const renderPropertyConditions = () => {
    propertyConditionContainer.innerHTML = "";

    state.propertyConditions.forEach((condition) => {
      const card = createOptionCard({
        groupName: "property_condition",
        value: condition.uuid,
        name: condition.name,

        description: condition.description || "Select this property condition.",

        image: "",

        code: condition.code || condition.name.slice(0, 3).toUpperCase(),

        selected: state.selectedPropertyCondition === condition.uuid,
      });

      propertyConditionContainer.appendChild(card);
    });
  };

  // ================================
  // Step 4 rendering
  // ==============================

  const renderPaymentFrequencies = () => {
    paymentFrequencySelect.innerHTML = `
    <option value="">
      Select payment frequency
    </option>
  `;

    state.paymentFrequencies.forEach((frequency) => {
      const option = document.createElement("option");

      option.value = frequency.value;
      option.textContent = frequency.label;

      paymentFrequencySelect.appendChild(option);
    });

    if (!paymentFrequencySelect.value) {
      paymentFrequencySelect.value = "annually";
    }
  };

  const renderFurnishingStatuses = () => {
    furnishingStatusContainer.innerHTML = "";

    state.furnishingStatuses.forEach((furnishingStatus) => {
      const card = createOptionCard({
        groupName: "furnishing_status",
        value: furnishingStatus.uuid,
        name: furnishingStatus.name,

        description:
          furnishingStatus.description || "Select this furnishing status.",

        image: "",

        code:
          furnishingStatus.code ||
          furnishingStatus.name.slice(0, 3).toUpperCase(),

        selected: state.selectedFurnishingStatus === furnishingStatus.uuid,
      });

      furnishingStatusContainer.appendChild(card);
    });
  };

  const createOptionCard = ({
    groupName,
    value,
    name,
    description,
    image,
    code,
    selected,
  }) => {
    const label = document.createElement("label");

    label.className = "wizard-option-card";

    if (selected) {
      label.classList.add("selected");
    }

    const visualMarkup = image
      ? `
        <div class="wizard-option-image">
          <img
            src="${escapeHtml(image)}"
            alt="${escapeHtml(name)}"
            loading="lazy"
            onerror="
              this.parentElement.innerHTML =
              '<span class=&quot;wizard-option-code&quot;>${escapeHtml(
                code,
              )}</span>'
            "
          >
        </div>
      `
      : `
        <span class="wizard-option-code">
          ${escapeHtml(code)}
        </span>
      `;

    label.innerHTML = `
      <input
        type="radio"
        name="${escapeHtml(groupName)}"
        value="${escapeHtml(value)}"
        ${selected ? "checked" : ""}
      >

      ${visualMarkup}

      <span class="wizard-option-copy">
        <strong>
          ${escapeHtml(name)}
        </strong>

        <span>
          ${escapeHtml(description)}
        </span>
      </span>
    `;

    const input = label.querySelector("input");

    input.addEventListener("change", () => {
      if (groupName === "property_type") {
        state.selectedPropertyType = value;

        clearFieldError("property_type");

        updateSelectedCards(propertyTypeContainer, input);
      }

      if (groupName === "purpose") {
        state.selectedPurpose = value;

        clearFieldError("purpose");

        updateSelectedCards(purposeContainer, input);
      }

      if (groupName === "property_condition") {
        state.selectedPropertyCondition = value;

        clearFieldError("property_condition");

        updateSelectedCards(propertyConditionContainer, input);
      }

      if (groupName === "furnishing_status") {
        state.selectedFurnishingStatus = value;

        clearFieldError("furnishing_status");

        updateSelectedCards(furnishingStatusContainer, input);
      }

      markUnsaved();
    });

    return label;
  };

  const updateSelectedCards = (container, selectedInput) => {
    container.querySelectorAll(".wizard-option-card").forEach((card) => {
      const cardInput = card.querySelector('input[type="radio"]');

      card.classList.toggle("selected", cardInput === selectedInput);
    });
  };

  // =================================================
  // AMENITY RENDERING
  // =================================================

  const getAmenityCategoryName = (amenity) => {
    if (amenity.category && typeof amenity.category === "object") {
      return amenity.category.name || "Other amenities";
    }

    return amenity.category_name || amenity.category || "Other amenities";
  };

  const groupAmenitiesByCategory = (amenities) => {
    return amenities.reduce((groups, amenity) => {
      const categoryName = getAmenityCategoryName(amenity);

      if (!groups[categoryName]) {
        groups[categoryName] = [];
      }

      groups[categoryName].push(amenity);

      return groups;
    }, {});
  };

  const renderAmenities = () => {
    amenityCategoryList.innerHTML = "";

    amenityEmptyState.hidden = state.amenities.length > 0;

    if (!state.amenities.length) {
      updateAmenitySelectionCount();
      return;
    }

    const groupedAmenities = groupAmenitiesByCategory(state.amenities);

    Object.entries(groupedAmenities).forEach(([categoryName, amenities]) => {
      const categorySection = document.createElement("section");

      categorySection.className = "amenity-category-section";

      const optionsMarkup = amenities
        .map((amenity) => {
          const selected = state.selectedAmenities.has(amenity.uuid);

          return `
            <label
              class="amenity-option-card ${selected ? "selected" : ""}"
            >
              <input
                type="checkbox"
                name="amenities"
                value="${escapeHtml(amenity.uuid)}"
                ${selected ? "checked" : ""}
              >

              <span class="amenity-checkmark">
                ✓
              </span>

              <span class="amenity-option-copy">
                <strong>
                  ${escapeHtml(amenity.name)}
                </strong>

                ${
                  amenity.description
                    ? `
                      <small>
                        ${escapeHtml(amenity.description)}
                      </small>
                    `
                    : ""
                }
              </span>
            </label>
          `;
        })
        .join("");

      categorySection.innerHTML = `
        <div class="amenity-category-heading">
          <h4>
            ${escapeHtml(categoryName)}
          </h4>

          <span>
            ${amenities.length}
          </span>
        </div>

        <div class="amenity-option-grid">
          ${optionsMarkup}
        </div>
      `;

      categorySection
        .querySelectorAll('input[name="amenities"]')
        .forEach((input) => {
          input.addEventListener("change", () => {
            const card = input.closest(".amenity-option-card");

            if (input.checked) {
              state.selectedAmenities.add(input.value);
            } else {
              state.selectedAmenities.delete(input.value);
            }

            card?.classList.toggle("selected", input.checked);

            clearFieldError("amenities");

            updateAmenitySelectionCount();
            markUnsaved();
          });
        });

      amenityCategoryList.appendChild(categorySection);
    });

    updateAmenitySelectionCount();
  };

  const updateAmenitySelectionCount = () => {
    selectedAmenityCount.textContent = String(state.selectedAmenities.size);
  };

  // =================================================
  // CASCADING LOCATION REQUESTS
  // =================================================

  const loadStates = async (countryUuid) => {
    state.states = [];
    state.lgas = [];
    state.areas = [];

    // state.lgas = [];
    // state.areas = [];

    resetLocationSelect({
      select: lgaSelect,
      placeholder: "Select state first",
    });

    resetLocationSelect({
      select: areaSelect,
      placeholder: "Select LGA first",
    });

    if (!countryUuid) {
      resetLocationSelect({
        select: stateSelect,
        placeholder: "Select country first",
      });

      return;
    }

    setSelectLoading(stateSelect, "Loading states...");

    try {
      const result = await apiRequest(locationEndpoints.states(countryUuid), {
        method: "GET",
      });

      if (!result.ok) {
        throw new Error(result.data?.message || "Unable to load states.");
      }

      state.states = extractApiList(result.data);

      renderSelectOptions({
        select: stateSelect,
        records: state.states,
        placeholder: "Select state",
      });
    } catch (error) {
      resetLocationSelect({
        select: stateSelect,
        placeholder: "Unable to load states",
      });

      showGeneralMessage(error.message || "Unable to load states.", "error");
    } finally {
      removeSelectLoading(stateSelect);
    }
  };

  const loadLgas = async (stateUuid) => {
    state.lgas = [];
    state.areas = [];

    // state.selectedLga = "";
    // state.selectedArea = "";

    resetLocationSelect({
      select: areaSelect,
      placeholder: "Select LGA first",
    });

    if (!stateUuid) {
      resetLocationSelect({
        select: lgaSelect,
        placeholder: "Select state first",
      });

      return;
    }

    setSelectLoading(lgaSelect, "Loading LGAs...");

    try {
      const result = await apiRequest(locationEndpoints.lgas(stateUuid), {
        method: "GET",
      });

      if (!result.ok) {
        throw new Error(result.data?.message || "Unable to load LGAs.");
      }

      state.lgas = extractApiList(result.data);

      renderSelectOptions({
        select: lgaSelect,
        records: state.lgas,
        placeholder: "Select LGA",
      });
    } catch (error) {
      resetLocationSelect({
        select: lgaSelect,
        placeholder: "Unable to load LGAs",
      });

      showGeneralMessage(error.message || "Unable to load LGAs.", "error");
    } finally {
      removeSelectLoading(lgaSelect);
    }
  };

  const loadAreas = async (lgaUuid) => {
    state.areas = [];
    // state.selectedArea = "";

    if (!lgaUuid) {
      resetLocationSelect({
        select: areaSelect,
        placeholder: "Select LGA first",
      });

      return;
    }

    setSelectLoading(areaSelect, "Loading areas...");

    try {
      const result = await apiRequest(locationEndpoints.areas(lgaUuid), {
        method: "GET",
      });

      if (!result.ok) {
        throw new Error(result.data?.message || "Unable to load areas.");
      }

      state.areas = extractApiList(result.data);

      renderSelectOptions({
        select: areaSelect,
        records: state.areas,
        placeholder: "Select area",
      });
    } catch (error) {
      resetLocationSelect({
        select: areaSelect,
        placeholder: "Unable to load areas",
      });

      showGeneralMessage(error.message || "Unable to load areas.", "error");
    } finally {
      removeSelectLoading(areaSelect);
    }
  };

  // =================================================
  // STEP 1 VALIDATION
  // =================================================

  const validateStepOne = (payload) => {
    let valid = true;

    if (!payload.property_type) {
      setFieldError("property_type", "Select a property type.");

      valid = false;
    }

    if (!payload.purpose) {
      setFieldError("purpose", "Select a property purpose.");

      valid = false;
    }

    if (!payload.title) {
      setFieldError("title", "Enter a title for the property.");

      titleInput.focus();
      valid = false;
    }

    return valid;
  };

  // =================================================
  // STEP 2 VALIDATION
  // =================================================

  const validateStepTwo = (payload) => {
    let valid = true;

    if (!state.selectedCountry) {
      setFieldError("country", "Select the country.");

      valid = false;
    }

    if (!state.selectedState) {
      setFieldError("state", "Select the state.");

      valid = false;
    }

    if (!state.selectedLga) {
      setFieldError("lga", "Select the Local Government Area.");

      valid = false;
    }

    if (!payload.area) {
      setFieldError("area", "Select the area or neighbourhood.");

      valid = false;
    }

    if (!payload.street_address) {
      setFieldError("street_address", "Enter the street address.");

      valid = false;
    }

    return valid;
  };

  // ===============================================
  // step three validation
  // ==============================================
  const validateStepThree = (payload) => {
    let valid = true;

    if (!payload.property_condition) {
      setFieldError("property_condition", "Select the property condition.");

      valid = false;
    }

    if (!payload.furnishing_status) {
      setFieldError("furnishing_status", "Select the furnishing status.");

      valid = false;
    }

    const nonNegativeFields = [
      ["bedrooms", payload.bedrooms],
      ["bathrooms", payload.bathrooms],
      ["toilets", payload.toilets],
      ["parking_spaces", payload.parking_spaces],
    ];

    nonNegativeFields.forEach(([fieldName, value]) => {
      if (Number.isNaN(value) || value < 0) {
        setFieldError(fieldName, "Enter a valid non-negative number.");

        valid = false;
      }
    });

    if (
      payload.year_built !== null &&
      (payload.year_built < 1800 ||
        payload.year_built > new Date().getFullYear())
    ) {
      setFieldError("year_built", "Enter a valid year.");

      valid = false;
    }

    if (payload.land_size !== null && payload.land_size < 0) {
      setFieldError("land_size", "Land size cannot be negative.");

      valid = false;
    }

    if (payload.building_size !== null && payload.building_size < 0) {
      setFieldError("building_size", "Building size cannot be negative.");

      valid = false;
    }

    return valid;
  };

  // ============================================
  // STEP FOUR VALIDATION
  // ============================================
  const validateStepFour = (payload) => {
    let valid = true;

    if (payload.proposed_price === null || payload.proposed_price === "") {
      setFieldError("proposed_price", "Enter the proposed property price.");

      valid = false;
    } else if (Number(payload.proposed_price) < 0) {
      setFieldError("proposed_price", "The proposed price cannot be negative.");

      valid = false;
    }

    if (!payload.payment_frequency) {
      setFieldError("payment_frequency", "Select the payment frequency.");

      valid = false;
    }

    const feeFields = [
      ["service_charge", payload.service_charge],
      ["caution_fee", payload.caution_fee],
      ["legal_fee", payload.legal_fee],
      ["agency_fee", payload.agency_fee],
    ];

    feeFields.forEach(([fieldName, value]) => {
      if (Number.isNaN(Number(value)) || Number(value) < 0) {
        setFieldError(fieldName, "Enter a valid non-negative amount.");

        valid = false;
      }
    });

    if (
      payload.minimum_stay !== null &&
      (Number.isNaN(payload.minimum_stay) || payload.minimum_stay < 1)
    ) {
      setFieldError("minimum_stay", "Minimum stay must be at least 1.");

      valid = false;
    }

    return valid;
  };

  // =================================================
  // SAVE STEP 1
  // =================================================

  const saveStepOne = async ({ continueToNextStep = false } = {}) => {
    clearAllErrors();

    const payload = {
      property_type: state.selectedPropertyType || null,

      purpose: state.selectedPurpose || null,

      title: titleInput.value.trim(),

      description: descriptionInput.value.trim(),
    };

    if (continueToNextStep && !validateStepOne(payload)) {
      return;
    }

    setSavingState();

    nextButton.disabled = true;
    saveDraftButton.disabled = true;

    const isExistingDraft = Boolean(state.submissionUuid);

    const endpoint = isExistingDraft
      ? `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`
      : "/api/properties/submissions/";

    const method = isExistingDraft ? "PATCH" : "POST";

    try {
      const result = await apiRequest(endpoint, {
        method,
        body: JSON.stringify(payload),
      });

      if (!result.ok) {
        showFieldErrors(result.data?.errors || {});

        throw new Error(
          result.data?.message || "Unable to save the property draft.",
        );
      }

      const submission = result.data?.data || {};

      if (!state.submissionUuid && submission.uuid) {
        state.submissionUuid = submission.uuid;

        sessionStorage.setItem("artishelta_submission_uuid", submission.uuid);
      }

      setSavedState();

      if (continueToNextStep) {
        moveToStep(2);
      } else {
        showGeneralMessage("Draft saved successfully.", "success");
      }
    } catch (error) {
      setSaveErrorState();

      showGeneralMessage(
        error.message || "Unable to save the property draft.",
        "error",
      );
    } finally {
      nextButton.disabled = false;
      saveDraftButton.disabled = false;
    }
  };

  // =================================================
  // SAVE STEP 2
  // =================================================

  const saveStepTwo = async ({ continueToNextStep = false } = {}) => {
    clearAllErrors();

    if (!state.submissionUuid) {
      showGeneralMessage(
        "Complete and save Step 1 before adding the property location.",
        "error",
      );

      moveToStep(1);
      return;
    }

    const payload = {
      area: state.selectedArea || null,

      street_address: streetAddressInput.value.trim(),

      landmark: landmarkInput.value.trim() || null,

      latitude: latitudeInput.value || null,

      longitude: longitudeInput.value || null,
    };

    if (continueToNextStep && !validateStepTwo(payload)) {
      return;
    }

    setSavingState();

    nextButton.disabled = true;
    saveDraftButton.disabled = true;
    previousButton.disabled = true;

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`,
        {
          method: "PATCH",
          body: JSON.stringify(payload),
        },
      );

      if (!result.ok) {
        showFieldErrors(result.data?.errors || {});

        throw new Error(
          result.data?.message || "Unable to save the property location.",
        );
      }

      setSavedState();

      if (continueToNextStep) {
        moveToStep(3);
      } else {
        showGeneralMessage("Location saved successfully.", "success");
      }
    } catch (error) {
      setSaveErrorState();

      showGeneralMessage(
        error.message || "Unable to save the property location.",
        "error",
      );
    } finally {
      nextButton.disabled = false;
      saveDraftButton.disabled = false;
      previousButton.disabled = false;
    }
  };

  // =================================================
  // SAVE STEP 3
  // =================================================

  const saveStepThree = async ({ continueToNextStep = false } = {}) => {
    clearAllErrors();

    if (!state.submissionUuid) {
      showGeneralMessage(
        "Complete the previous steps before adding property details.",
        "error",
      );

      moveToStep(1);
      return;
    }

    const payload = {
      property_condition: state.selectedPropertyCondition || null,

      furnishing_status: state.selectedFurnishingStatus || null,

      bedrooms: Number(bedroomsInput.value || 0),

      bathrooms: Number(bathroomsInput.value || 0),

      toilets: Number(toiletsInput.value || 0),

      parking_spaces: Number(parkingSpacesInput.value || 0),

      year_built:
        yearBuiltInput.value === "" ? null : Number(yearBuiltInput.value),

      land_size: landSizeInput.value === "" ? null : landSizeInput.value,

      building_size:
        buildingSizeInput.value === "" ? null : buildingSizeInput.value,
    };

    if (continueToNextStep && !validateStepThree(payload)) {
      return;
    }

    setSavingState();

    nextButton.disabled = true;
    saveDraftButton.disabled = true;
    previousButton.disabled = true;

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`,
        {
          method: "PATCH",
          body: JSON.stringify(payload),
        },
      );

      if (!result.ok) {
        showFieldErrors(result.data?.errors || {});

        throw new Error(
          result.data?.message || "Unable to save the property details.",
        );
      }

      setSavedState();

      if (continueToNextStep) {
        moveToStep(4);
      } else {
        showGeneralMessage("Property details saved successfully.", "success");
      }
    } catch (error) {
      setSaveErrorState();

      showGeneralMessage(
        error.message || "Unable to save the property details.",
        "error",
      );
    } finally {
      nextButton.disabled = false;
      saveDraftButton.disabled = false;
      previousButton.disabled = false;
    }
  };

  // =============================================
  // STEP 4 VALIDATION
  // =============================================

  const saveStepFour = async ({ continueToNextStep = false } = {}) => {
    clearAllErrors();

    if (!state.submissionUuid) {
      showGeneralMessage(
        "Complete the previous steps before adding pricing.",
        "error",
      );

      moveToStep(1);
      return;
    }

    const payload = {
      proposed_price:
        proposedPriceInput.value === "" ? null : proposedPriceInput.value,

      payment_frequency: paymentFrequencySelect.value || null,

      service_charge: serviceChargeInput.value || "0",

      caution_fee: cautionFeeInput.value || "0",

      legal_fee: legalFeeInput.value || "0",

      agency_fee: agencyFeeInput.value || "0",

      is_negotiable: isNegotiableInput.checked,

      available_from: availableFromInput.value || null,

      minimum_stay:
        minimumStayInput.value === "" ? null : Number(minimumStayInput.value),
    };

    if (continueToNextStep && !validateStepFour(payload)) {
      return;
    }

    setSavingState();

    nextButton.disabled = true;
    saveDraftButton.disabled = true;
    previousButton.disabled = true;

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`,
        {
          method: "PATCH",
          body: JSON.stringify(payload),
        },
      );

      if (!result.ok) {
        showFieldErrors(result.data?.errors || {});

        throw new Error(
          result.data?.message || "Unable to save the property pricing.",
        );
      }

      setSavedState();

      if (continueToNextStep) {
        moveToStep(5);
      } else {
        showGeneralMessage("Property pricing saved successfully.", "success");
      }
    } catch (error) {
      setSaveErrorState();

      showGeneralMessage(
        error.message || "Unable to save the property pricing.",
        "error",
      );
    } finally {
      nextButton.disabled = false;
      saveDraftButton.disabled = false;
      previousButton.disabled = false;
    }
  };

  // =================================================
  // SAVE STEP 5
  // =================================================

  const saveStepFive = async ({ continueToNextStep = false } = {}) => {
    clearAllErrors();

    if (!state.submissionUuid) {
      showGeneralMessage(
        "Complete the previous steps before selecting amenities.",
        "error",
      );

      moveToStep(1);
      return;
    }

    const payload = {
      amenities: Array.from(state.selectedAmenities),
    };

    setSavingState();

    nextButton.disabled = true;
    saveDraftButton.disabled = true;
    previousButton.disabled = true;

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`,
        {
          method: "PATCH",
          body: JSON.stringify(payload),
        },
      );

      if (!result.ok) {
        showFieldErrors(result.data?.errors || {});

        throw new Error(
          result.data?.message || "Unable to save the selected amenities.",
        );
      }

      setSavedState();

      if (continueToNextStep) {
        moveToStep(6);
      } else {
        showGeneralMessage("Amenities saved successfully.", "success");
      }
    } catch (error) {
      setSaveErrorState();

      showGeneralMessage(
        error.message || "Unable to save the selected amenities.",
        "error",
      );
    } finally {
      nextButton.disabled = false;
      saveDraftButton.disabled = false;
      previousButton.disabled = false;
    }
  };

  // =================================================
  // STEP NAVIGATION
  // =================================================

  const moveToStep = (stepNumber) => {
    state.currentStep = stepNumber;

    document.querySelectorAll("[data-wizard-step]").forEach((step) => {
      step.classList.toggle(
        "active",
        Number(step.dataset.wizardStep) === stepNumber,
      );
    });

    document
      .querySelectorAll("[data-progress-step]")
      .forEach((progressStep) => {
        const progressNumber = Number(progressStep.dataset.progressStep);

        progressStep.classList.toggle("active", progressNumber === stepNumber);

        progressStep.classList.toggle("completed", progressNumber < stepNumber);

        if (progressNumber <= stepNumber) {
          progressStep.disabled = false;
        }
      });

    if (stepNumber === 1) {
      document.getElementById("wizard-step-label").textContent = "Step 1 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Tell us about the property";

      document.getElementById("wizard-step-description").textContent =
        "Start by selecting the property type and its purpose.";

      document.getElementById("wizard-progress-label").textContent =
        "Basic information";

      document.getElementById("wizard-progress-percentage").textContent = "14%";

      document.getElementById("wizard-progress-bar").style.width = "14%";

      previousButton.hidden = true;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    if (stepNumber === 2) {
      document.getElementById("wizard-step-label").textContent = "Step 2 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Where is the property located?";

      document.getElementById("wizard-step-description").textContent =
        "Provide the location details for this property.";

      document.getElementById("wizard-progress-label").textContent = "Location";

      document.getElementById("wizard-progress-percentage").textContent = "29%";

      document.getElementById("wizard-progress-bar").style.width = "29%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    if (stepNumber === 3) {
      document.getElementById("wizard-step-label").textContent = "Step 3 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Describe the property";

      document.getElementById("wizard-step-description").textContent =
        "Add the condition, furnishing, room and size details.";

      document.getElementById("wizard-progress-label").textContent =
        "Property details";

      document.getElementById("wizard-progress-percentage").textContent = "43%";

      document.getElementById("wizard-progress-bar").style.width = "43%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }
    // =======================================
    // step 4
    // ========================================

    if (stepNumber === 4) {
      document.getElementById("wizard-step-label").textContent = "Step 4 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Set the property price";

      document.getElementById("wizard-step-description").textContent =
        "Add the proposed price, additional charges and availability.";

      document.getElementById("wizard-progress-label").textContent = "Pricing";

      document.getElementById("wizard-progress-percentage").textContent = "57%";

      document.getElementById("wizard-progress-bar").style.width = "57%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;
      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    // ====================================
    // STEP 5
    // =====================================
    if (stepNumber === 5) {
      document.getElementById("wizard-step-label").textContent = "Step 5 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Select the property amenities";

      document.getElementById("wizard-step-description").textContent =
        "Choose the facilities and features available at the property.";

      document.getElementById("wizard-progress-label").textContent =
        "Amenities";

      document.getElementById("wizard-progress-percentage").textContent = "71%";

      document.getElementById("wizard-progress-bar").style.width = "71%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;
      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    // ===================================
    // STEP 6
    // =================================

    if (stepNumber === 6) {
      document.getElementById("wizard-step-label").textContent = "Step 6 of 7";
      document.getElementById("wizard-step-title").textContent =
        "Show the property";
      document.getElementById("wizard-step-description").textContent =
        "Upload clear photos and an optional walkthrough video.";
      document.getElementById("wizard-progress-label").textContent =
        "Photos and video";
      document.getElementById("wizard-progress-percentage").textContent = "86%";
      document.getElementById("wizard-progress-bar").style.width = "86%";
      previousButton.hidden = false;
      saveDraftButton.hidden = true;
      nextButton.disabled = false;
      nextButtonText.textContent = "Continue to review";

      loadSubmissionMedia();
    }

    // =========================================
    // STEP 7
    // =========================================
    if (stepNumber === 7) {
      document.getElementById("wizard-step-label").textContent = "Step 7 of 7";

      document.getElementById("wizard-step-title").textContent =
        "Review your property";

      document.getElementById("wizard-step-description").textContent =
        "Confirm that all information is correct before submission.";

      document.getElementById("wizard-progress-label").textContent =
        "Review and submit";

      document.getElementById("wizard-progress-percentage").textContent =
        "100%";

      document.getElementById("wizard-progress-bar").style.width = "100%";

      previousButton.hidden = false;
      saveDraftButton.hidden = true;

      nextButton.disabled = false;
      nextButtonText.textContent = "Submit property";

      loadSubmissionReview();
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // =================================================
  // MEDIA API HELPERS
  // =================================================

  const getMediaEndpoint = () => {
    return `/api/properties/submissions/${encodeURIComponent(
      state.submissionUuid,
    )}/media/`;
  };

  const loadSubmissionMedia = async () => {
    if (!state.submissionUuid) {
      state.media = [];
      renderSubmissionMedia();
      return;
    }

    try {
      const result = await apiRequest(getMediaEndpoint(), {
        method: "GET",
      });

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to load property media.",
        );
      }

      state.media = extractApiList(result.data);

      renderSubmissionMedia();
    } catch (error) {
      showMediaMessage(
        error.message || "Unable to load property media.",
        "error",
      );
    }
  };

  const uploadSubmissionMedia = async ({
    file,
    mediaType,
    isCover = false,
  }) => {
    if (!state.submissionUuid) {
      throw new Error("Save the property draft before uploading media.");
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("media_type", mediaType);

    formData.append("is_cover", String(isCover));

    const result = await apiRequest(getMediaEndpoint(), {
      method: "POST",
      body: formData,
    });

    if (!result.ok) {
      const errors = result.data?.errors || {};

      const fileErrors = errors.file || errors.non_field_errors;

      const message = Array.isArray(fileErrors)
        ? fileErrors.join(" ")
        : result.data?.message || "Media upload failed.";

      throw new Error(message);
    }

    return result.data?.data;
  };

  // const deleteMedia = async (media) => {
  //   const confirmed = window.confirm("Delete this media file?");

  //   if (!confirmed) {
  //     return;
  //   }

  //   try {
  //     const endpoint = `/api/properties/submissions/${encodeURIComponent(
  //       state.submissionUuid,
  //     )}/media/${encodeURIComponent(media.uuid)}/`;

  //     const result = await apiRequest(endpoint, {
  //       method: "DELETE",
  //     });

  //     if (!result.ok) {
  //       throw new Error(result.data?.message || "Unable to delete media.");
  //     }

  //     await loadSubmissionMedia();

  //     showMediaMessage("Media deleted successfully.", "success");
  //   } catch (error) {
  //     showMediaMessage(error.message || "Unable to delete media.", "error");
  //   }
  // };

  // =======================================
  // DELETE MODAL
  // ===================================

  const openMediaDeleteModal = (media) => {
    state.mediaPendingDeletion = media;

    const mediaLabel = media.media_type === "video" ? "video" : "image";

    mediaDeleteModalMessage.textContent = `This ${mediaLabel} will be permanently removed from the property submission.`;

    mediaDeleteModal.hidden = false;

    document.body.style.overflow = "hidden";

    confirmMediaDeleteButton.focus();
  };

  const closeMediaDeleteModal = () => {
    if (confirmMediaDeleteButton.disabled) {
      return;
    }

    mediaDeleteModal.hidden = true;

    state.mediaPendingDeletion = null;

    document.body.style.overflow = "";
  };

  const deleteMedia = async (media) => {
    if (!media) {
      return;
    }

    confirmMediaDeleteButton.disabled = true;
    confirmMediaDeleteButton.textContent = "Deleting...";

    try {
      const endpoint = `/api/properties/submissions/${encodeURIComponent(
        state.submissionUuid,
      )}/media/${encodeURIComponent(media.uuid)}/`;

      const result = await apiRequest(endpoint, {
        method: "DELETE",
      });

      if (!result.ok) {
        throw new Error(result.data?.message || "Unable to delete media.");
      }

      mediaDeleteModal.hidden = true;
      document.body.style.overflow = "";

      state.mediaPendingDeletion = null;

      await loadSubmissionMedia();

      showMediaMessage("Media deleted successfully.", "success");
    } catch (error) {
      showMediaMessage(error.message || "Unable to delete media.", "error");
    } finally {
      confirmMediaDeleteButton.disabled = false;
      confirmMediaDeleteButton.textContent = "Delete";
    }
  };

  const setCoverMedia = async (media) => {
    try {
      const endpoint = `/api/properties/submissions/${encodeURIComponent(
        state.submissionUuid,
      )}/media/${encodeURIComponent(media.uuid)}/set-cover/`;

      const result = await apiRequest(endpoint, {
        method: "POST",
      });

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to update the cover image.",
        );
      }

      await loadSubmissionMedia();

      showMediaMessage("Cover image updated successfully.", "success");
    } catch (error) {
      showMediaMessage(
        error.message || "Unable to update the cover image.",
        "error",
      );
    }
  };

  // =================================================
  // REVIEW HELPERS
  // =================================================

  const formatCurrency = (value) => {
    if (value === null || value === undefined || value === "") {
      return "Not provided";
    }

    const amount = Number(value);

    if (!Number.isFinite(amount)) {
      return "Not provided";
    }

    return new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency: "NGN",
      minimumFractionDigits: 2,
    }).format(amount);
  };

  const formatReviewValue = (value, fallback = "Not provided") => {
    if (value === null || value === undefined || value === "") {
      return fallback;
    }

    return String(value);
  };

  const createReviewDetailMarkup = (items) => {
    return items
      .map(
        ([label, value]) => `
        <div class="review-detail-item">
          <span>
            ${escapeHtml(label)}
          </span>

          <strong>
            ${escapeHtml(formatReviewValue(value))}
          </strong>
        </div>
      `,
      )
      .join("");
  };

  const renderReview = (submission) => {
    const media = Array.isArray(submission.media)
      ? submission.media
      : state.media;

    const amenities = Array.isArray(submission.amenities)
      ? submission.amenities
      : [];

    const coverImage =
      media.find((item) => item.media_type === "image" && item.is_cover) ||
      media.find((item) => item.media_type === "image");

    if (coverImage?.secure_url) {
      reviewCoverImage.style.backgroundImage = `url("${coverImage.secure_url}")`;
    } else {
      reviewCoverImage.style.backgroundImage = "";
    }

    reviewStatusBadge.textContent =
      submission.status_display || submission.status || "Draft";

    reviewPropertyTitle.textContent = submission.title || "Untitled property";

    const locationParts = [
      submission.area_name,
      submission.lga_name,
      submission.state_name,
      submission.country_name,
    ].filter(Boolean);

    reviewPropertyLocation.textContent =
      locationParts.join(", ") || "Location not provided";

    reviewPropertyPrice.textContent = formatCurrency(submission.proposed_price);

    reviewBasicInformation.innerHTML = createReviewDetailMarkup([
      ["Property type", submission.property_type_name],
      ["Purpose", submission.purpose_name],
      ["Title", submission.title],
      ["Description", submission.description],
    ]);

    reviewLocationInformation.innerHTML = createReviewDetailMarkup([
      ["Country", submission.country_name],
      ["State", submission.state_name],
      ["LGA", submission.lga_name],
      ["Area", submission.area_name],
      ["Street address", submission.street_address],
      ["Landmark", submission.landmark],
    ]);

    reviewPropertyDetails.innerHTML = createReviewDetailMarkup([
      ["Condition", submission.property_condition_name],
      ["Furnishing", submission.furnishing_status_name],
      ["Bedrooms", submission.bedrooms],
      ["Bathrooms", submission.bathrooms],
      ["Toilets", submission.toilets],
      ["Parking spaces", submission.parking_spaces],
      ["Year built", submission.year_built],
      [
        "Land size",
        submission.land_size ? `${submission.land_size} sqm` : null,
      ],
      [
        "Building size",
        submission.building_size ? `${submission.building_size} sqm` : null,
      ],
    ]);

    reviewPricingInformation.innerHTML = createReviewDetailMarkup([
      ["Proposed price", formatCurrency(submission.proposed_price)],
      [
        "Payment frequency",
        submission.payment_frequency_display || submission.payment_frequency,
      ],
      ["Service charge", formatCurrency(submission.service_charge)],
      ["Caution fee", formatCurrency(submission.caution_fee)],
      ["Legal fee", formatCurrency(submission.legal_fee)],
      ["Agency fee", formatCurrency(submission.agency_fee)],
      ["Negotiable", submission.is_negotiable ? "Yes" : "No"],
      ["Available from", submission.available_from],
      ["Minimum stay", submission.minimum_stay],
    ]);

    const total =
      Number(submission.proposed_price || 0) +
      Number(submission.service_charge || 0) +
      Number(submission.caution_fee || 0) +
      Number(submission.legal_fee || 0) +
      Number(submission.agency_fee || 0);

    reviewTotalCost.textContent = formatCurrency(total);

    if (amenities.length) {
      reviewAmenityList.innerHTML = amenities
        .map(
          (amenity) => `
            <span class="review-amenity-chip">
              ${escapeHtml(amenity.name || amenity)}
            </span>
          `,
        )
        .join("");
    } else {
      reviewAmenityList.innerHTML = `
      <p class="review-empty-value">
        No amenities selected.
      </p>
    `;
    }

    if (media.length) {
      reviewMediaGrid.innerHTML = media
        .map((item) => {
          if (item.media_type === "video") {
            return `
              <div class="review-media-item">
                <video
                  controls
                  preload="metadata"
                >
                  <source
                    src="${escapeHtml(item.secure_url)}"
                    type="${escapeHtml(item.content_type || "video/mp4")}"
                  >
                </video>
              </div>
            `;
          }

          return `
            <div class="review-media-item">
              <img
                src="${escapeHtml(item.secure_url)}"
                alt="${escapeHtml(item.alt_text || "Property image")}"
              >

              ${
                item.is_cover
                  ? `
                    <span class="review-media-cover">
                      Cover
                    </span>
                  `
                  : ""
              }
            </div>
          `;
        })
        .join("");
    } else {
      reviewMediaGrid.innerHTML = `
      <p class="review-empty-value">
        No media uploaded.
      </p>
    `;
    }
  };

  // ============================================
  // LOAD THE REVIEW SUBMISSION
  // ===========================================
  const loadSubmissionReview = async () => {
    if (!state.submissionUuid) {
      moveToStep(1);
      return;
    }

    reviewLoadingState.hidden = false;
    reviewErrorMessage.hidden = true;
    reviewContent.hidden = true;

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/`,
        {
          method: "GET",
        },
      );

      if (!result.ok) {
        throw new Error(
          result.data?.message || "Unable to load the property review.",
        );
      }

      const submission = result.data?.data || {};

      renderReview(submission);

      reviewLoadingState.hidden = true;
      reviewContent.hidden = false;
    } catch (error) {
      reviewLoadingState.hidden = true;
      reviewErrorMessage.hidden = false;

      reviewErrorMessage.textContent =
        error.message || "Unable to load the property review.";
    }
  };

  // ============================================
  // SUBMIT FROM JAVASCRIPT
  // =============================================
  const submitProperty = async () => {
    clearAllErrors();

    reviewErrorMessage.hidden = true;
    reviewErrorMessage.textContent = "";

    if (!state.submissionUuid) {
      moveToStep(1);
      return;
    }

    nextButton.disabled = true;
    previousButton.disabled = true;
    nextButtonText.textContent = "Submitting...";

    try {
      const result = await apiRequest(
        `/api/properties/submissions/${encodeURIComponent(
          state.submissionUuid,
        )}/submit/`,
        {
          method: "POST",
        },
      );

      if (!result.ok) {
        const errors = result.data?.errors || {};

        showFieldErrors(errors);

        const errorMessages = Object.values(errors).flatMap((messages) => {
          if (Array.isArray(messages)) {
            return messages;
          }

          return [String(messages)];
        });

        if (errorMessages.length) {
          reviewErrorMessage.innerHTML = `
      <strong>
        Please complete the following:
      </strong>

      <ul>
        ${errorMessages
          .map(
            (message) => `
              <li>
                ${escapeHtml(message)}
              </li>
            `,
          )
          .join("")}
      </ul>
    `;

          reviewErrorMessage.hidden = false;
        }

        throw new Error(
          result.data?.message || "Unable to submit the property.",
        );
      }

      sessionStorage.removeItem("artishelta_submission_uuid");

      showGeneralMessage("Property submitted successfully.", "success");

      window.setTimeout(() => {
        window.location.href = "/dashboard/submissions/";
      }, 1200);
    } catch (error) {
      showGeneralMessage(
        error.message || "Unable to submit the property.",
        "error",
      );

      nextButton.disabled = false;
      previousButton.disabled = false;
      nextButtonText.textContent = "Submit property";
    }
  };

  // =================================================
  // EVENTS
  // =================================================

  wizardForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (state.currentStep === 1) {
      await saveStepOne({
        continueToNextStep: true,
      });

      return;
    }

    if (state.currentStep === 2) {
      await saveStepTwo({
        continueToNextStep: true,
      });

      return;
    }

    if (state.currentStep === 3) {
      await saveStepThree({
        continueToNextStep: true,
      });
      return;
    }

    if (state.currentStep === 4) {
      await saveStepFour({
        continueToNextStep: true,
      });

      return;
    }
    if (state.currentStep === 5) {
      await saveStepFive({
        continueToNextStep: true,
      });

      return;
    }
    if (state.currentStep === 6) {
      const imageCount = state.media.filter(
        (media) => media.media_type === "image",
      ).length;

      if (imageCount === 0) {
        setFieldError("images", "Upload at least one property image.");

        return;
      }

      clearFieldError("images");

      moveToStep(7);
      return;
    }

    if (state.currentStep === 7) {
      await submitProperty();
      return;
    }
  });

  // Review Edit buttons belong here.
  document.querySelectorAll("[data-edit-step]").forEach((button) => {
    button.addEventListener("click", () => {
      const stepNumber = Number(button.dataset.editStep);

      if (Number.isInteger(stepNumber) && stepNumber >= 1 && stepNumber <= 6) {
        moveToStep(stepNumber);
      }
    });
  });

  // ==========================================
  // TOTAL COST HELPER
  // ==========================================
  const updateTotalCost = () => {
    const amounts = [
      proposedPriceInput.value,
      serviceChargeInput.value,
      cautionFeeInput.value,
      legalFeeInput.value,
      agencyFeeInput.value,
    ];

    const total = amounts.reduce((sum, value) => {
      const amount = Number(value || 0);

      return sum + (Number.isFinite(amount) ? amount : 0);
    }, 0);

    totalCostElement.textContent = new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency: "NGN",
      minimumFractionDigits: 2,
    }).format(total);
  };

  // ============================================
  // save draft button click event
  // ============================================

  saveDraftButton.addEventListener("click", async () => {
    if (state.currentStep === 1) {
      await saveStepOne({
        continueToNextStep: false,
      });
      return;
    }

    if (state.currentStep === 2) {
      await saveStepTwo({
        continueToNextStep: false,
      });

      return;
    }

    if (state.currentStep === 3) {
      await saveStepThree({
        continueToNextStep: false,
      });
      return;
    }

    if (state.currentStep === 4) {
      await saveStepFour({
        continueToNextStep: false,
      });

      return;
    }
    if (state.currentStep === 5) {
      await saveStepFive({
        continueToNextStep: false,
      });

      return;
    }
  });

  previousButton.addEventListener("click", () => {
    if (state.currentStep > 1) {
      moveToStep(state.currentStep - 1);
    }
  });

  titleInput.addEventListener("input", () => {
    clearFieldError("title");
    markUnsaved();
  });

  descriptionInput.addEventListener("input", () => {
    if (descriptionCount) {
      descriptionCount.textContent = `${descriptionInput.value.length} / 3000`;
    }

    markUnsaved();
  });

  countrySelect.addEventListener("change", async (e) => {
    state.selectedCountry = e.target.value;

    // User changed country
    state.selectedState = "";
    state.selectedLga = "";
    state.selectedArea = "";

    markUnsaved();

    await loadStates(state.selectedCountry);
  });

  stateSelect.addEventListener("change", async (e) => {
    state.selectedState = e.target.value;

    state.selectedLga = "";
    state.selectedArea = "";

    markUnsaved();

    await loadLgas(state.selectedState);
  });

  lgaSelect.addEventListener("change", async (e) => {
    state.selectedLga = e.target.value;

    state.selectedArea = "";

    markUnsaved();

    await loadAreas(state.selectedLga);
  });

  areaSelect.addEventListener("change", () => {
    state.selectedArea = areaSelect.value;

    clearFieldError("area");
    markUnsaved();
  });

  [streetAddressInput, landmarkInput, latitudeInput, longitudeInput].forEach(
    (input) => {
      input.addEventListener("input", () => {
        clearFieldError(input.name);
        markUnsaved();
      });
    },
  );

  currentLocationButton?.addEventListener("click", () => {
    if (!navigator.geolocation) {
      showCurrentLocationMessage(
        "Location access is not supported by this browser.",
        "error",
      );

      return;
    }

    currentLocationButton.disabled = true;

    currentLocationButton.textContent = "Getting location...";

    navigator.geolocation.getCurrentPosition(
      (position) => {
        latitudeInput.value = position.coords.latitude.toFixed(7);

        longitudeInput.value = position.coords.longitude.toFixed(7);

        clearFieldError("latitude");
        clearFieldError("longitude");

        markUnsaved();

        showCurrentLocationMessage(
          "Your current coordinates have been added.",
          "success",
        );

        currentLocationButton.disabled = false;

        currentLocationButton.textContent = "Use my current location";
      },

      (error) => {
        let errorMessage = "We could not access your current location.";

        if (error.code === error.PERMISSION_DENIED) {
          errorMessage = "Location permission was denied.";
        }

        if (error.code === error.POSITION_UNAVAILABLE) {
          errorMessage = "Your current location is unavailable.";
        }

        if (error.code === error.TIMEOUT) {
          errorMessage = "The location request timed out.";
        }

        showCurrentLocationMessage(errorMessage, "error");

        currentLocationButton.disabled = false;

        currentLocationButton.textContent = "Use my current location";
      },

      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000,
      },
    );
  });

  [
    bedroomsInput,
    bathroomsInput,
    toiletsInput,
    parkingSpacesInput,
    yearBuiltInput,
    landSizeInput,
    buildingSizeInput,
  ].forEach((input) => {
    input.addEventListener("input", () => {
      clearFieldError(input.name);
      markUnsaved();
    });
  });

  const pricingInputs = [
    proposedPriceInput,
    serviceChargeInput,
    cautionFeeInput,
    legalFeeInput,
    agencyFeeInput,
    minimumStayInput,
  ];

  pricingInputs.forEach((input) => {
    input.addEventListener("input", () => {
      clearFieldError(input.name);
      updateTotalCost();
      markUnsaved();
    });
  });

  paymentFrequencySelect.addEventListener("change", () => {
    clearFieldError("payment_frequency");

    markUnsaved();
  });

  availableFromInput.addEventListener("change", () => {
    clearFieldError("available_from");
    markUnsaved();
  });

  // ========================================
  // ADD IMAGE EVENTS
  // =========================================
  imageDropzone.addEventListener("click", () => imageInput.click());

  imageDropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      imageInput.click();
    }
  });

  imageInput.addEventListener("change", () => {
    handleImageFiles(imageInput.files);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    imageDropzone.addEventListener(eventName, (event) => {
      event.preventDefault();

      imageDropzone.classList.add("dragging");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    imageDropzone.addEventListener(eventName, (event) => {
      event.preventDefault();

      imageDropzone.classList.remove("dragging");
    });
  });

  imageDropzone.addEventListener("drop", (event) => {
    handleImageFiles(event.dataTransfer.files);
  });

  videoDropzone.addEventListener("click", () => videoInput.click());

  videoDropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      videoInput.click();
    }
  });

  videoInput.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];

    await handleVideoFile(file);
  });

  isNegotiableInput.addEventListener("change", markUnsaved);

  retryButton?.addEventListener("click", loadLookups);

  // =========================================
  // DELETE IMAGE AND VIDEO EVENTS
  // ========================================
  cancelMediaDeleteButton.addEventListener("click", closeMediaDeleteModal);

  confirmMediaDeleteButton.addEventListener("click", async () => {
    await deleteMedia(state.mediaPendingDeletion);
  });

  mediaDeleteModal
    .querySelectorAll("[data-close-media-modal]")
    .forEach((element) => {
      element.addEventListener("click", closeMediaDeleteModal);
    });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !mediaDeleteModal.hidden) {
      closeMediaDeleteModal();
    }
  });

  // =================================================
  // START WIZARD
  // =================================================

  moveToStep(1);
  loadLookups();
});

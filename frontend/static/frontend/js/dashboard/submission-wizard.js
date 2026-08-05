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
    !totalCostElement
  ) {
    console.error(
      "Property wizard could not start because required elements are missing.",
    );

    return;
  }
  // =================================================
  // APPLICATION STATE
  // =================================================

  const state = {
    currentStep: 1,

    submissionUuid: sessionStorage.getItem("artishelta_submission_uuid"),

    propertyTypes: [],
    purposes: [],

    countries: [],
    states: [],
    lgas: [],
    areas: [],
    propertyConditions: [],
    furnishingStatuses: [],
    paymentFrequencies: [],

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
      `/api/locations/states/?country=${encodeURIComponent(countryUuid)}`,

    lgas: (stateUuid) =>
      `/api/locations/lgas/?state=${encodeURIComponent(stateUuid)}`,

    areas: (lgaUuid) =>
      `/api/locations/areas/?lga=${encodeURIComponent(lgaUuid)}`,
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

        apiRequest(locationEndpoints.countries, {
          method: "GET",
        }),
      ]);

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

      state.furnishingStatuses = extractApiList(furnishingStatusResult.data);

      renderPropertyTypes();
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
    } catch (error) {
      console.error("Wizard lookup request failed:", error);

      showLoadError(error.message || "Unable to load the property options.");
    }
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
  // CASCADING LOCATION REQUESTS
  // =================================================

  const loadStates = async (countryUuid) => {
    state.states = [];
    state.lgas = [];
    state.areas = [];

    state.selectedState = "";
    state.selectedLga = "";
    state.selectedArea = "";

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

    state.selectedLga = "";
    state.selectedArea = "";

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
    state.selectedArea = "";

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
      console.error("Property draft save failed:", error);

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
      console.error("Property location save failed:", error);

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
      console.error("Property details save failed:", error);

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
      console.error("Property pricing save failed:", error);

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
      document.getElementById("wizard-step-label").textContent = "Step 1 of 6";

      document.getElementById("wizard-step-title").textContent =
        "Tell us about the property";

      document.getElementById("wizard-step-description").textContent =
        "Start by selecting the property type and its purpose.";

      document.getElementById("wizard-progress-label").textContent =
        "Basic information";

      document.getElementById("wizard-progress-percentage").textContent = "17%";

      document.getElementById("wizard-progress-bar").style.width = "17%";

      previousButton.hidden = true;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    if (stepNumber === 2) {
      document.getElementById("wizard-step-label").textContent = "Step 2 of 6";

      document.getElementById("wizard-step-title").textContent =
        "Where is the property located?";

      document.getElementById("wizard-step-description").textContent =
        "Provide the location details for this property.";

      document.getElementById("wizard-progress-label").textContent = "Location";

      document.getElementById("wizard-progress-percentage").textContent = "33%";

      document.getElementById("wizard-progress-bar").style.width = "33%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    if (stepNumber === 3) {
      document.getElementById("wizard-step-label").textContent = "Step 3 of 6";

      document.getElementById("wizard-step-title").textContent =
        "Describe the property";

      document.getElementById("wizard-step-description").textContent =
        "Add the condition, furnishing, room and size details.";

      document.getElementById("wizard-progress-label").textContent =
        "Property details";

      document.getElementById("wizard-progress-percentage").textContent = "50%";

      document.getElementById("wizard-progress-bar").style.width = "50%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;

      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }
    // =======================================
    // step 4
    // ========================================

    if (stepNumber === 4) {
      document.getElementById("wizard-step-label").textContent = "Step 4 of 6";

      document.getElementById("wizard-step-title").textContent =
        "Set the property price";

      document.getElementById("wizard-step-description").textContent =
        "Add the proposed price, additional charges and availability.";

      document.getElementById("wizard-progress-label").textContent = "Pricing";

      document.getElementById("wizard-progress-percentage").textContent = "67%";

      document.getElementById("wizard-progress-bar").style.width = "67%";

      previousButton.hidden = false;
      saveDraftButton.hidden = false;
      nextButton.disabled = false;

      nextButtonText.textContent = "Save and continue";
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
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
    }

    if (state.currentStep === 4) {
      await saveStepFour({
        continueToNextStep: true,
      });

      return;
    }
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

  countrySelect.addEventListener("change", async () => {
    state.selectedCountry = countrySelect.value;

    clearFieldError("country");
    markUnsaved();

    await loadStates(state.selectedCountry);
  });

  stateSelect.addEventListener("change", async () => {
    state.selectedState = stateSelect.value;

    clearFieldError("state");
    markUnsaved();

    await loadLgas(state.selectedState);
  });

  lgaSelect.addEventListener("change", async () => {
    state.selectedLga = lgaSelect.value;

    clearFieldError("lga");
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

  isNegotiableInput.addEventListener("change", markUnsaved);

  retryButton?.addEventListener("click", loadLookups);

  // =================================================
  // START WIZARD
  // =================================================

  moveToStep(1);
  loadLookups();
});

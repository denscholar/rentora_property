(function () {
  "use strict";

  // =====================================================
  // CONFIGURATION
  // =====================================================

  const verificationConfig = window.propertyVerification || {};

  let verificationUuid = verificationConfig.verificationUuid || "";

  const token = verificationConfig.token || "";

  // =====================================================
  // DOM ELEMENTS
  // =====================================================

  const elements = {
    page: document.getElementById("property-verification-page"),

    loading: document.getElementById("verification-loading"),

    error: document.getElementById("verification-error"),

    errorTitle: document.getElementById("verification-error-title"),

    errorMessage: document.getElementById("verification-error-message"),

    content: document.getElementById("verification-content"),

    // IMPORTANT:
    // HTML uses verification-success
    authorizedSuccess: document.getElementById("verification-success"),

    rejectedSuccess: document.getElementById("verification-rejected"),

    // ===================================================
    // PROPERTY
    // ===================================================

    propertyTitle: document.getElementById("property-title"),

    propertyLocation: document.getElementById("property-location"),

    propertyType: document.getElementById("property-type"),

    // ===================================================
    // AGENT
    // ===================================================

    agentName: document.getElementById("agent-name"),

    agentAgency: document.getElementById("agent-agency"),

    // ===================================================
    // REPRESENTATIVE
    // ===================================================

    representativeName: document.getElementById("representative-name"),

    representativeRole: document.getElementById("representative-role"),

    representativeEmail: document.getElementById("representative-email"),

    // ===================================================
    // DECISION
    // ===================================================

    decisionAuthorized: document.getElementById("decision-authorize"),

    decisionRejected: document.getElementById("decision-reject"),

    decisionSection: document.getElementById("verification-decision-section"),

    authorizationFields: document.getElementById("authorization-fields"),

    rejectionFields: document.getElementById("rejection-fields"),

    availabilityConfirmed: document.getElementById("availability-confirmed"),

    agentAuthorized: document.getElementById("agent-authorized"),

    authorizationNote: document.getElementById("authorization-note"),

    rejectionReason: document.getElementById("rejection-reason"),

    authorizationError: document.getElementById("authorization-error"),

    // IMPORTANT:
    // There is only ONE submit button in your HTML.
    submitDecisionButton: document.getElementById("submit-decision-button"),

    // ===================================================
    // DOCUMENTS
    // ===================================================

    documentsLoading: document.getElementById("documents-loading"),

    documentsEmpty: document.getElementById("documents-empty"),

    documentsContainer: document.getElementById("documents-container"),

    documentsError: document.getElementById("documents-error"),

    documentsSuccess: document.getElementById("documents-success"),

    documentForm: document.getElementById("verification-document-form"),

    documentType: document.getElementById("verification-document-type"),

    documentFile: document.getElementById("verification-document-file"),

    uploadedByName: document.getElementById("document-uploaded-by-name"),

    uploadDocumentButton: document.getElementById(
      "upload-verification-document-button",
    ),
  };

  // =====================================================
  // DEBUG
  // =====================================================

  // console.log("========================================");
  // console.log("PROPERTY VERIFICATION JS");
  // console.log("========================================");

  // console.log("Token:", token);

  // console.log("Decision authorize:", elements.decisionAuthorized);

  // console.log("Decision reject:", elements.decisionRejected);

  // console.log("Decision section:", elements.decisionSection);

  // console.log("Authorization fields:", elements.authorizationFields);

  // console.log("Rejection fields:", elements.rejectionFields);

  // console.log("Submit button:", elements.submitDecisionButton);

  // =====================================================
  // SPINNER CSS
  // =====================================================

  function installSpinnerStyles() {
    if (document.getElementById("property-verification-spinner-styles")) {
      return;
    }

    const style = document.createElement("style");

    style.id = "property-verification-spinner-styles";

    style.textContent = `
      .property-verification-button-spinner {
        display: inline-block;
        width: 15px;
        height: 15px;
        margin-right: 8px;
        vertical-align: -2px;
        border: 2px solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        animation: propertyVerificationSpin 0.7s linear infinite;
      }

      @keyframes propertyVerificationSpin {
        to {
          transform: rotate(360deg);
        }
      }

      button.property-verification-loading {
        cursor: wait;
        opacity: 0.75;
      }
    `;

    document.head.appendChild(style);
  }

  // =====================================================
  // BUTTON LOADING
  // =====================================================

  function setButtonLoading(button, text) {
    if (!button) {
      return "";
    }

    const originalHtml = button.innerHTML;

    button.disabled = true;

    button.classList.add("property-verification-loading");

    button.innerHTML = `
      <span
        class="property-verification-button-spinner"
        aria-hidden="true"
      ></span>
      ${escapeHtml(text)}
    `;

    return originalHtml;
  }

  function restoreButton(button, originalHtml) {
    if (!button) {
      return;
    }

    button.classList.remove("property-verification-loading");

    button.innerHTML = originalHtml;
  }

  // =====================================================
  // UI STATES
  // =====================================================

  function showLoading() {
    if (elements.loading) {
      elements.loading.hidden = false;
    }

    if (elements.error) {
      elements.error.hidden = true;
    }

    if (elements.content) {
      elements.content.hidden = true;
    }

    if (elements.authorizedSuccess) {
      elements.authorizedSuccess.hidden = true;
    }

    if (elements.rejectedSuccess) {
      elements.rejectedSuccess.hidden = true;
    }
  }

  function showContent() {
    if (elements.loading) {
      elements.loading.hidden = true;
    }

    if (elements.error) {
      elements.error.hidden = true;
    }

    if (elements.content) {
      elements.content.hidden = false;
    }

    if (elements.authorizedSuccess) {
      elements.authorizedSuccess.hidden = true;
    }

    if (elements.rejectedSuccess) {
      elements.rejectedSuccess.hidden = true;
    }
  }

  function showError(title, message) {
    // console.error(title, message);

    if (elements.loading) {
      elements.loading.hidden = true;
    }

    if (elements.content) {
      elements.content.hidden = true;
    }

    if (elements.authorizedSuccess) {
      elements.authorizedSuccess.hidden = true;
    }

    if (elements.rejectedSuccess) {
      elements.rejectedSuccess.hidden = true;
    }

    if (elements.errorTitle) {
      elements.errorTitle.textContent = title;
    }

    if (elements.errorMessage) {
      elements.errorMessage.textContent = message;
    }

    if (elements.error) {
      elements.error.hidden = false;
    }
  }

  function showAuthorizationSuccess() {
    if (elements.loading) {
      elements.loading.hidden = true;
    }

    if (elements.error) {
      elements.error.hidden = true;
    }

    if (elements.content) {
      elements.content.hidden = true;
    }

    if (elements.rejectedSuccess) {
      elements.rejectedSuccess.hidden = true;
    }

    if (elements.authorizedSuccess) {
      elements.authorizedSuccess.hidden = false;
    }
  }

  function showRejectionSuccess() {
    if (elements.loading) {
      elements.loading.hidden = true;
    }

    if (elements.error) {
      elements.error.hidden = true;
    }

    if (elements.content) {
      elements.content.hidden = true;
    }

    if (elements.authorizedSuccess) {
      elements.authorizedSuccess.hidden = true;
    }

    if (elements.rejectedSuccess) {
      elements.rejectedSuccess.hidden = false;
    }
  }

  // =====================================================
  // API URLS
  // =====================================================

  function getVerificationUrl() {
    return (
      "/api/property-verification/public/" + encodeURIComponent(token) + "/"
    );
  }

  function getAuthorizationUrl() {
    return (
      "/api/property-verification/authorize/" + encodeURIComponent(token) + "/"
    );
  }

  function getDocumentsListUrl() {
    if (!verificationUuid) {
      throw new Error("Verification UUID is not available.");
    }

    return (
      "/api/property-verification/public/" +
      encodeURIComponent(verificationUuid) +
      "/" +
      encodeURIComponent(token) +
      "/documents/list/"
    );
  }

  function getDocumentsUploadUrl() {
    if (!verificationUuid) {
      throw new Error("Verification UUID is not available.");
    }

    return (
      "/api/property-verification/public/" +
      encodeURIComponent(verificationUuid) +
      "/" +
      encodeURIComponent(token) +
      "/documents/"
    );
  }

  function getDocumentDeleteUrl(documentUuid) {
    if (!verificationUuid) {
      throw new Error("Verification UUID is not available.");
    }

    if (!documentUuid) {
      throw new Error("Document UUID is not available.");
    }

    return (
      "/api/property-verification/public/" +
      encodeURIComponent(verificationUuid) +
      "/" +
      encodeURIComponent(token) +
      "/documents/" +
      encodeURIComponent(documentUuid) +
      "/"
    );
  }

  // =====================================================
  // CSRF
  // =====================================================

  function getCsrfToken() {
    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");

    return csrfInput ? csrfInput.value : "";
  }

  // =====================================================
  // RESPONSE PARSER
  // =====================================================

  async function parseResponse(response) {
    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
      return await response.json();
    }

    const text = await response.text();

    return {
      detail: text || "The server returned an unexpected response.",
    };
  }

  // =====================================================
  // LOAD VERIFICATION
  // =====================================================

  async function loadVerification() {
    showLoading();

    try {
      // console.log("Loading verification:", getVerificationUrl());

      const response = await fetch(getVerificationUrl(), {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      const data = await parseResponse(response);

      console.log("Verification response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            extractValidationError(data) ||
            "Unable to load this verification.",
        );
      }

      if (!data.uuid) {
        throw new Error("Verification data is missing the verification UUID.");
      }

      verificationUuid = data.uuid;

      console.log("Verification UUID:", verificationUuid);

      populateVerification(data);

      showContent();

      resetDecisionUI();
    } catch (error) {
      console.error("Failed to load verification:", error);

      showError(
        "Verification unavailable",
        error.message || "This verification request could not be loaded.",
      );
    }
  }

  // =====================================================
  // POPULATE VERIFICATION
  // =====================================================

  function populateVerification(data) {
    const property = data.property || {};

    const agent = data.agent || {};

    const representative = data.representative || {};

    if (elements.propertyTitle) {
      elements.propertyTitle.textContent = property.title || "—";
    }

    if (elements.propertyLocation) {
      elements.propertyLocation.textContent = property.street_address || "—";
    }

    if (elements.propertyType) {
      elements.propertyType.textContent = property.property_type || "—";
    }

    if (elements.agentName) {
      elements.agentName.textContent = agent.name || "—";
    }

    if (elements.agentAgency) {
      elements.agentAgency.textContent = agent.agency || "—";
    }

    if (elements.representativeName) {
      elements.representativeName.textContent = representative.name || "—";
    }

    if (elements.representativeRole) {
      elements.representativeRole.textContent = representative.role || "—";
    }

    if (elements.representativeEmail) {
      elements.representativeEmail.textContent = representative.email || "—";
    }
  }

  // =====================================================
  // DECISION
  // =====================================================

  function getSelectedDecision() {
    const selected = document.querySelector(
      'input[name="verification-decision"]:checked',
    );

    return selected ? selected.value : "";
  }

  // =====================================================
  // RESET DECISION UI
  // =====================================================

  function resetDecisionUI() {
    // console.log("Resetting decision UI.");

    if (elements.authorizationFields) {
      elements.authorizationFields.hidden = true;
    }

    if (elements.rejectionFields) {
      elements.rejectionFields.hidden = true;
    }

    if (elements.submitDecisionButton) {
      elements.submitDecisionButton.disabled = true;

      elements.submitDecisionButton.textContent = "Select a Decision";
    }

    hideAuthorizationError();
  }

  // =====================================================
  // HANDLE DECISION CHANGE
  // =====================================================

  function handleDecisionChange() {
    const decision = getSelectedDecision();

    // console.log("========================================");

    // console.log("DECISION CHANGED:", decision);

    // console.log("Authorize radio:", elements.decisionAuthorized?.checked);

    // console.log("Reject radio:", elements.decisionRejected?.checked);

    // console.log("========================================");

    hideAuthorizationError();

    // ===================================================
    // NOTHING SELECTED
    // ===================================================

    if (!decision) {
      resetDecisionUI();

      return;
    }

    // ===================================================
    // AUTHORIZED
    // ===================================================

    if (decision === "authorized") {
      console.log("Showing authorization fields.");

      if (elements.authorizationFields) {
        elements.authorizationFields.hidden = false;
      }

      if (elements.rejectionFields) {
        elements.rejectionFields.hidden = true;
      }

      updateDecisionButton();

      // Load documents because authorization
      // has been selected.
      loadDocuments();

      return;
    }

    // ===================================================
    // REJECTED
    // ===================================================

    if (decision === "rejected") {
      console.log("Showing rejection fields.");

      if (elements.authorizationFields) {
        elements.authorizationFields.hidden = true;
      }

      if (elements.rejectionFields) {
        elements.rejectionFields.hidden = false;
      }

      updateDecisionButton();

      return;
    }

    resetDecisionUI();
  }

  // =====================================================
  // DECISION BUTTON
  // =====================================================

  function updateDecisionButton() {
    if (!elements.submitDecisionButton) {
      return;
    }

    const decision = getSelectedDecision();

    // ===================================================
    // NO DECISION
    // ===================================================

    if (!decision) {
      elements.submitDecisionButton.disabled = true;

      elements.submitDecisionButton.textContent = "Select a Decision";

      return;
    }

    // ===================================================
    // AUTHORIZATION
    // ===================================================

    if (decision === "authorized") {
      const availability = Boolean(elements.availabilityConfirmed?.checked);

      const authorized = Boolean(elements.agentAuthorized?.checked);

      const ready = availability && authorized;

      elements.submitDecisionButton.disabled = !ready;

      elements.submitDecisionButton.textContent = ready
        ? "Authorize Property"
        : "Confirm Both Statements";

      return;
    }

    // ===================================================
    // REJECTION
    // ===================================================

    if (decision === "rejected") {
      const reason = elements.rejectionReason?.value?.trim() || "";

      elements.submitDecisionButton.disabled = !reason;

      elements.submitDecisionButton.textContent = reason
        ? "Reject Property"
        : "Provide Rejection Reason";

      return;
    }

    elements.submitDecisionButton.disabled = true;

    elements.submitDecisionButton.textContent = "Select a Decision";
  }

  // =====================================================
  // SUBMIT DECISION
  // =====================================================

  async function submitDecision() {
    const decision = getSelectedDecision();

    // console.log("Submitting decision:", decision);

    if (!decision) {
      showAuthorizationError("Please select a decision.");

      return;
    }

    if (decision === "authorized") {
      await submitAuthorization();

      return;
    }

    if (decision === "rejected") {
      await submitRejection();

      return;
    }
  }

  // =====================================================
  // SUBMIT AUTHORIZATION
  // =====================================================

  async function submitAuthorization() {
    const availabilityConfirmed = Boolean(
      elements.availabilityConfirmed?.checked,
    );

    const agentAuthorized = Boolean(elements.agentAuthorized?.checked);

    if (!availabilityConfirmed) {
      showAuthorizationError(
        "Please confirm that the property is currently available.",
      );

      return;
    }

    if (!agentAuthorized) {
      showAuthorizationError(
        "Please confirm that the agent is authorized to market this property.",
      );

      return;
    }

    hideAuthorizationError();

    const payload = {
      decision: "authorized",

      availability_confirmed: true,

      agent_authorized: true,

      authorization_note: elements.authorizationNote?.value?.trim() || "",
    };

    // console.log("Authorization payload:", payload);

    const button = elements.submitDecisionButton;

    const originalHtml = button ? button.innerHTML : "";

    setButtonLoading(button, "Authorizing...");

    try {
      const csrfToken = getCsrfToken();

      const headers = {
        Accept: "application/json",

        "Content-Type": "application/json",
      };

      if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
      }

      const response = await fetch(getAuthorizationUrl(), {
        method: "POST",

        headers,

        body: JSON.stringify(payload),
      });

      const data = await parseResponse(response);

      // console.log("Authorization response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            extractValidationError(data) ||
            "Unable to authorize this property.",
        );
      }

      showAuthorizationSuccess();
    } catch (error) {
      console.error("Authorization failed:", error);

      showAuthorizationError(
        error.message || "Unable to authorize this property.",
      );

      restoreButton(button, originalHtml);

      updateDecisionButton();
    }
  }

  // =====================================================
  // SUBMIT REJECTION
  // =====================================================

  async function submitRejection() {
    const rejectionReason = elements.rejectionReason?.value?.trim() || "";

    if (!rejectionReason) {
      showAuthorizationError(
        "Please provide a reason for rejecting this property verification.",
      );

      return;
    }

    hideAuthorizationError();

    const payload = {
      decision: "rejected",

      rejection_reason: rejectionReason,
    };

    // console.log("Rejection payload:", payload);

    const button = elements.submitDecisionButton;

    const originalHtml = button ? button.innerHTML : "";

    setButtonLoading(button, "Rejecting Property...");

    try {
      const csrfToken = getCsrfToken();

      const headers = {
        Accept: "application/json",

        "Content-Type": "application/json",
      };

      if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
      }

      const response = await fetch(getAuthorizationUrl(), {
        method: "POST",

        headers,

        body: JSON.stringify(payload),
      });

      const data = await parseResponse(response);

      // console.log("Rejection response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            extractValidationError(data) ||
            "Unable to reject this property.",
        );
      }

      showRejectionSuccess();
    } catch (error) {
      // console.error("Rejection failed:", error);

      showAuthorizationError(
        error.message || "Unable to reject this property.",
      );

      restoreButton(button, originalHtml);

      updateDecisionButton();
    }
  }

  // =====================================================
  // AUTHORIZATION ERROR
  // =====================================================

  function showAuthorizationError(message) {
    if (!elements.authorizationError) {
      return;
    }

    elements.authorizationError.textContent = message;

    elements.authorizationError.hidden = false;
  }

  function hideAuthorizationError() {
    if (!elements.authorizationError) {
      return;
    }

    elements.authorizationError.textContent = "";

    elements.authorizationError.hidden = true;
  }

  // =====================================================
  // DOCUMENTS
  // =====================================================

  async function loadDocuments() {
    if (!elements.documentsContainer) {
      console.warn("Documents container not found.");

      return;
    }

    if (getSelectedDecision() !== "authorized") {
      return;
    }

    if (elements.documentsLoading) {
      elements.documentsLoading.hidden = false;
    }

    if (elements.documentsEmpty) {
      elements.documentsEmpty.hidden = true;
    }

    if (elements.documentsError) {
      elements.documentsError.hidden = true;
    }

    try {
      const url = getDocumentsListUrl();

      // console.log("Loading documents:", url);

      const response = await fetch(url, {
        method: "GET",

        headers: {
          Accept: "application/json",
        },
      });

      const data = await parseResponse(response);

      // console.log("Documents response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            extractValidationError(data) ||
            "Unable to load verification documents.",
        );
      }

      const documents = Array.isArray(data)
        ? data
        : data.data || data.documents || [];

      renderDocuments(documents);
    } catch (error) {
      // console.error("Failed to load documents:", error);

      showDocumentsError(
        error.message || "Unable to load verification documents.",
      );
    } finally {
      if (elements.documentsLoading) {
        elements.documentsLoading.hidden = true;
      }
    }
  }

  // =====================================================
  // RENDER DOCUMENTS
  // =====================================================

  function renderDocuments(documents) {
    if (!elements.documentsContainer) {
      return;
    }

    elements.documentsContainer.innerHTML = "";

    if (!Array.isArray(documents) || !documents.length) {
      if (elements.documentsEmpty) {
        elements.documentsEmpty.hidden = false;
      }

      return;
    }

    if (elements.documentsEmpty) {
      elements.documentsEmpty.hidden = true;
    }

    documents.forEach((verificationDocument) => {
      const wrapper = document.createElement("div");

      wrapper.className = "verification-document-item";

      const name =
        verificationDocument.original_filename ||
        verificationDocument.file_name ||
        "Verification document";

      const type =
        verificationDocument.document_type_display ||
        verificationDocument.document_type ||
        "Document";

      const url =
        verificationDocument.secure_url ||
        verificationDocument.file_url ||
        verificationDocument.url ||
        "";

      const documentUuid =
        verificationDocument.uuid || verificationDocument.id || "";

      wrapper.innerHTML = `
          <div class="verification-document-info">
            <strong>
              ${escapeHtml(name)}
            </strong>

            <span>
              ${escapeHtml(formatDocumentType(type))}
            </span>
          </div>

          <div class="verification-document-actions">

            ${
              url
                ? `
                  <a
                    href="${escapeAttribute(url)}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="verification-document-link"
                  >
                    View
                  </a>
                `
                : ""
            }

            ${
              documentUuid
                ? `
                  <button
                    type="button"
                    class="verification-document-delete"
                    data-document-uuid="${escapeAttribute(documentUuid)}"
                  >
                    Delete
                  </button>
                `
                : ""
            }

          </div>
        `;

      elements.documentsContainer.appendChild(wrapper);
    });

    const deleteButtons = elements.documentsContainer.querySelectorAll(
      ".verification-document-delete",
    );

    deleteButtons.forEach((button) => {
      button.addEventListener("click", handleDeleteDocument);
    });
  }

  // =====================================================
  // FORMAT DOCUMENT TYPE
  // =====================================================

  function formatDocumentType(value) {
    if (!value) {
      return "Document";
    }

    return String(value)
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  // =====================================================
  // DOCUMENT MESSAGES
  // =====================================================

  function showDocumentsError(message) {
    if (!elements.documentsError) {
      return;
    }

    elements.documentsError.textContent = message;

    elements.documentsError.hidden = false;
  }

  function showDocumentsSuccess(message) {
    if (!elements.documentsSuccess) {
      return;
    }

    elements.documentsSuccess.textContent = message;

    elements.documentsSuccess.hidden = false;
  }

  // =====================================================
  // DOCUMENT UPLOAD BUTTON
  // =====================================================

  // =====================================================
  // DOCUMENT UPLOAD BUTTON STATE
  // =====================================================

  function updateUploadDocumentButton() {
    const button = elements.uploadDocumentButton;

    if (!button) {
      // console.warn("Upload document button not found.");

      return;
    }

    const fileInput = elements.documentFile;

    const documentTypeInput = elements.documentType;

    const hasFile =
      Boolean(fileInput) &&
      Boolean(fileInput.files) &&
      fileInput.files.length > 0;

    const hasDocumentType =
      Boolean(documentTypeInput) &&
      typeof documentTypeInput.value === "string" &&
      documentTypeInput.value.trim() !== "";

    const ready = hasFile && hasDocumentType;

    // console.log("Upload button validation:", {
    //   hasFile,
    //   hasDocumentType,
    //   ready,
    // });

    // ===================================================
    // DISABLED UNTIL BOTH ARE PROVIDED
    // ===================================================

    button.disabled = !ready;

    // Do not change the button text while an upload
    // operation is already in progress.
    if (button.classList.contains("property-verification-loading")) {
      return;
    }

    if (ready) {
      button.textContent = "Upload Document";
    } else {
      button.textContent = "Select Document & Type";
    }
  }

  // =====================================================
  // DOCUMENT UPLOAD
  // =====================================================

  async function uploadDocument(event) {
    event.preventDefault();

    console.log("Document upload submitted.");

    if (getSelectedDecision() !== "authorized") {
      showDocumentsError(
        "Document uploads are only available when authorizing the property.",
      );

      return;
    }

    if (!elements.documentFile || !elements.documentType) {
      return;
    }

    if (elements.documentsError) {
      elements.documentsError.hidden = true;
    }

    if (elements.documentsSuccess) {
      elements.documentsSuccess.hidden = true;
    }

    const file = elements.documentFile.files[0];

    const documentType = elements.documentType.value;

    if (!documentType) {
      showDocumentsError("Please select a document type.");

      return;
    }

    if (!file) {
      showDocumentsError("Please select a document to upload.");

      return;
    }

    const maxSize = 10 * 1024 * 1024;

    if (file.size > maxSize) {
      showDocumentsError("The document cannot be larger than 10 MB.");

      return;
    }

    const formData = new FormData();

    formData.append("document_type", documentType);

    formData.append("document", file);

    if (elements.uploadedByName && elements.uploadedByName.value.trim()) {
      formData.append("uploaded_by_name", elements.uploadedByName.value.trim());
    }

    const csrfToken = getCsrfToken();

    const button = elements.uploadDocumentButton;

    const originalHtml = button ? button.innerHTML : "";

    setButtonLoading(button, "Uploading...");

    try {
      const headers = {
        Accept: "application/json",
      };

      if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
      }

      const response = await fetch(getDocumentsUploadUrl(), {
        method: "POST",

        headers,

        body: formData,
      });

      const data = await parseResponse(response);

      console.log("Document upload response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            extractValidationError(data) ||
            "Unable to upload the document.",
        );
      }

      showDocumentsSuccess("Document uploaded successfully.");

      if (elements.documentForm) {
        elements.documentForm.reset();
      }

      await loadDocuments();
    } catch (error) {
      console.error("Document upload failed:", error);

      showDocumentsError(error.message || "Unable to upload the document.");
    } finally {
      restoreButton(button, originalHtml);

      // Recalculate the button state after upload/reset.
      updateUploadDocumentButton();
    }
  }

  // =====================================================
  // DELETE DOCUMENT
  // =====================================================

  async function handleDeleteDocument(event) {
    const button = event.currentTarget;

    const documentUuid = button.dataset.documentUuid;

    if (!documentUuid) {
      showDocumentsError("Document identifier is missing.");

      return;
    }

    // const confirmed = window.confirm(
    //   "Are you sure you want to delete this document?",
    // );

    // if (!confirmed) {
    //   return;
    // }

    const originalHtml = button.innerHTML;

    setButtonLoading(button, "Deleting...");

    if (elements.documentsError) {
      elements.documentsError.hidden = true;
    }

    if (elements.documentsSuccess) {
      elements.documentsSuccess.hidden = true;
    }

    try {
      const csrfToken = getCsrfToken();

      const headers = {
        Accept: "application/json",
      };

      if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
      }

      const response = await fetch(getDocumentDeleteUrl(documentUuid), {
        method: "DELETE",

        headers,
      });

      let data = {};

      if (response.status !== 204) {
        data = await parseResponse(response);
      }

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || "Unable to delete the document.",
        );
      }

      showDocumentsSuccess("Document deleted successfully.");

      await loadDocuments();
    } catch (error) {
      console.error("Document deletion failed:", error);

      showDocumentsError(error.message || "Unable to delete the document.");

      restoreButton(button, originalHtml);
    }
  }

  // =====================================================
  // VALIDATION ERROR EXTRACTION
  // =====================================================

  function extractValidationError(data) {
    if (!data || typeof data !== "object") {
      return "";
    }

    for (const value of Object.values(data)) {
      if (Array.isArray(value) && value.length) {
        return String(value[0]);
      }

      if (typeof value === "string") {
        return value;
      }

      if (value && typeof value === "object") {
        const nested = extractValidationError(value);

        if (nested) {
          return nested;
        }
      }
    }

    return "";
  }

  // =====================================================
  // ESCAPE HELPERS
  // =====================================================

  function escapeHtml(value) {
    const div = document.createElement("div");

    div.textContent = String(value ?? "");

    return div.innerHTML;
  }

  function escapeAttribute(value) {
    return escapeHtml(value);
  }

  // =====================================================
  // EVENT LISTENERS
  // =====================================================

  // -----------------------------------------------------
  // AUTHORIZATION RADIO
  // -----------------------------------------------------

  if (elements.decisionAuthorized) {
    elements.decisionAuthorized.addEventListener(
      "change",
      handleDecisionChange,
    );
  }

  if (elements.decisionRejected) {
    elements.decisionRejected.addEventListener("change", handleDecisionChange);
  }

  // -----------------------------------------------------
  // AUTHORIZATION CHECKBOXES
  // -----------------------------------------------------

  if (elements.availabilityConfirmed) {
    elements.availabilityConfirmed.addEventListener(
      "change",
      updateDecisionButton,
    );
  }

  if (elements.agentAuthorized) {
    elements.agentAuthorized.addEventListener("change", updateDecisionButton);
  }

  // -----------------------------------------------------
  // REJECTION REASON
  // -----------------------------------------------------

  if (elements.rejectionReason) {
    elements.rejectionReason.addEventListener("input", updateDecisionButton);
  }

  // -----------------------------------------------------
  // MAIN SUBMIT BUTTON
  // -----------------------------------------------------

  if (elements.submitDecisionButton) {
    elements.submitDecisionButton.addEventListener("click", function () {
      // console.log("MAIN DECISION BUTTON CLICKED");

      submitDecision();
    });
  }

  // -----------------------------------------------------
  // DOCUMENT FORM
  // -----------------------------------------------------

  if (elements.documentForm) {
    elements.documentForm.addEventListener("submit", uploadDocument);
  }

  // -----------------------------------------------------
  // DOCUMENT TYPE
  // -----------------------------------------------------

  if (elements.documentType) {
    elements.documentType.addEventListener("change", function () {
      console.log("DOCUMENT TYPE CHANGED:", elements.documentType.value);

      updateUploadDocumentButton();
    });
  }

  // DOCUMENT FILE
  // -----------------------------------------------------

  if (elements.documentFile) {
    elements.documentFile.addEventListener("change", function () {
      const file = elements.documentFile.files?.[0];

      console.log(
        "DOCUMENT FILE CHANGED:",
        file
          ? {
              name: file.name,
              size: file.size,
              type: file.type,
            }
          : "No file selected",
      );

      updateUploadDocumentButton();
    });
  }

  // =====================================================
  // INITIALIZE
  // =====================================================

  installSpinnerStyles();

  resetDecisionUI();
  updateUploadDocumentButton();

  console.log("Property verification initialized.");

  // =====================================================
  // VALIDATE TOKEN
  // =====================================================

  if (!token) {
    showError(
      "Invalid verification link",
      "This verification link is incomplete or invalid.",
    );

    return;
  }

  // =====================================================
  // LOAD
  // =====================================================

  loadVerification();
})();

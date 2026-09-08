document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");

  const submitButton = document.getElementById("login-submit");

  const successMessage = document.getElementById(
    "verification-success-message",
  );

  if (!form || !submitButton) {
    return;
  }

  // ================================================
  // EMAIL VERIFICATION SUCCESS MESSAGE
  // ================================================
  const searchParams = new URLSearchParams(window.location.search);

  if (searchParams.get("verified") === "true" && successMessage) {
    successMessage.hidden = false;
  }

  // ================================================
  // PASSWORD VISIBILITY
  // ================================================
  form.querySelectorAll("[data-password-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const inputId = button.dataset.passwordToggle;
      const passwordInput = document.getElementById(inputId);

      if (!passwordInput) {
        return;
      }

      const shouldShow = passwordInput.type === "password";

      passwordInput.type = shouldShow ? "text" : "password";

      button.textContent = shouldShow ? "Hide" : "Show";

      button.setAttribute(
        "aria-label",
        shouldShow ? "Hide password" : "Show password",
      );
    });
  });

  // ================================================
  // CLEAR FIELD ERRORS
  // ================================================
  form.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", () => {
      const errorElement = form.querySelector(
        `[data-error-for="${input.name}"]`,
      );

      if (errorElement) {
        errorElement.textContent = "";
      }

      const generalError = form.querySelector(".form-general-error");

      if (generalError) {
        generalError.hidden = true;
        generalError.textContent = "";
      }
    });
  });

  // ================================================
  // LOGIN SUBMISSION
  // ================================================
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    clearFormErrors(form);

    const formData = new FormData(form);

    const payload = {
      email: String(formData.get("email") || "")
        .trim()
        .toLowerCase(),

      password: String(formData.get("password") || ""),
    };

    const clientErrors = {};

    if (!payload.email) {
      clientErrors.email = ["Email address is required."];
    }

    if (!payload.password) {
      clientErrors.password = ["Password is required."];
    }

    if (Object.keys(clientErrors).length > 0) {
      showFieldErrors(form, clientErrors);
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Logging in...";

    try {
      const result = await apiRequest("/api/accounts/auth/login/", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!result.ok) {
        showFieldErrors(form, result.data.errors || {});

        showGeneralError(
          form,
          result.data.message || "Unable to log in with these credentials.",
        );

        return;
      }

      /*
       * Your backend response currently contains:
       *
       * data: {
       *   message: "...",
       *   data: {
       *     id,
       *     email,
       *     role,
       *     ...
       *   }
       * }
       */
      const authenticatedUser =
        result.data?.data || {};

      redirectAuthenticatedUser(authenticatedUser.role);
    } catch (error) {
      console.error("Login request failed:", error);

      showGeneralError(
        form,
        "Unable to connect to the server. Please try again.",
      );
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Log in";
    }
  });
});

function redirectAuthenticatedUser(role) {
  const roleRedirects = {
    tenant: "/dashboard/",
    agent: "/dashboard/",
    landlord: "/dashboard/",
    admin: "/admin/",
  };

  window.location.href = roleRedirects[role] || "/dashboard/";
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registration-form");

  const submitButton = document.getElementById("registration-submit");

  if (!form || !submitButton) {
    return;
  }

  form.querySelectorAll("[data-password-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const inputId = button.dataset.passwordToggle;
      const input = document.getElementById(inputId);

      if (!input) {
        return;
      }

      const shouldShow = input.type === "password";

      input.type = shouldShow ? "text" : "password";

      button.textContent = shouldShow ? "Hide" : "Show";
    });
  });

  form.querySelectorAll("input, select").forEach((input) => {
    input.addEventListener("input", () => {
      const errorElement = form.querySelector(
        `[data-error-for="${input.name}"]`,
      );

      if (errorElement) {
        errorElement.textContent = "";
      }
    });
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    clearFormErrors(form);

    const formData = new FormData(form);

    const payload = {
      first_name: formData.get("first_name").trim(),

      last_name: formData.get("last_name").trim(),

      email: formData.get("email").trim().toLowerCase(),

      phone_number: formData.get("phone_number").trim(),

      role: formData.get("role"),

      password: formData.get("password"),

      confirm_password: formData.get("confirm_password"),
    };

    if (payload.password !== payload.confirm_password) {
      showFieldErrors(form, {
        confirm_password: ["Passwords do not match."],
      });

      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Creating account...";

    try {
      const result = await apiRequest("/api/accounts/auth/register/", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!result.ok) {
        showFieldErrors(form, result.data.errors || {});

        showGeneralError(form, result.data.message || "Registration failed.");

        return;
      }

      sessionStorage.setItem(
        "rentora_verification_email",
        result.data.data.email,
      );

      window.location.href = `/verify-email/?email=${encodeURIComponent(
        result.data.data.email,
      )}`;
    } catch (error) {
      showGeneralError(form, "Unable to connect to the server.");
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Create account";
    }
  });
});

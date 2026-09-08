document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("verify-email-form");

  const emailInput = document.getElementById("verification-email");

  const emailDisplay = document.getElementById("verification-email-display");

  const submitButton = document.getElementById("verify-email-submit");

  const resendButton = document.getElementById("resend-otp-button");

  const countdownElement = document.getElementById("resend-countdown");

  const otpInputs = Array.from(document.querySelectorAll(".otp-input"));

  if (
    !form ||
    !emailInput ||
    !emailDisplay ||
    !submitButton ||
    !resendButton ||
    !countdownElement ||
    otpInputs.length !== 6
  ) {
    return;
  }

  const searchParams = new URLSearchParams(window.location.search);

  const emailFromUrl = searchParams.get("email");

  const emailFromSession = sessionStorage.getItem("rentora_verification_email");

  const verificationEmail = emailFromUrl || emailFromSession || "";

//   if (!verificationEmail) {
//     window.location.href = "/register/";
//     return;
//   }

  emailInput.value = verificationEmail;
  emailDisplay.textContent = verificationEmail;

  sessionStorage.setItem("rentora_verification_email", verificationEmail);

  const getOtpValue = () => {
    return otpInputs.map((input) => input.value).join("");
  };

  const clearOtpError = () => {
    const errorElement = form.querySelector('[data-error-for="otp"]');

    if (errorElement) {
      errorElement.textContent = "";
    }

    const generalError = form.querySelector(".form-general-error");

    if (generalError) {
      generalError.hidden = true;
      generalError.textContent = "";
    }
  };

  otpInputs.forEach((input, index) => {
    input.addEventListener("input", () => {
      input.value = input.value.replace(/\D/g, "");

      input.classList.toggle("is-filled", Boolean(input.value));

      clearOtpError();

      if (input.value && index < otpInputs.length - 1) {
        otpInputs[index + 1].focus();
      }
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Backspace" && !input.value && index > 0) {
        otpInputs[index - 1].focus();
      }

      if (event.key === "ArrowLeft" && index > 0) {
        otpInputs[index - 1].focus();
      }

      if (event.key === "ArrowRight" && index < otpInputs.length - 1) {
        otpInputs[index + 1].focus();
      }
    });

    input.addEventListener("paste", (event) => {
      event.preventDefault();

      const pastedValue = event.clipboardData
        .getData("text")
        .replace(/\D/g, "")
        .slice(0, 6);

      if (!pastedValue) {
        return;
      }

      pastedValue.split("").forEach((digit, digitIndex) => {
        if (!otpInputs[digitIndex]) {
          return;
        }

        otpInputs[digitIndex].value = digit;
        otpInputs[digitIndex].classList.add("is-filled");
      });

      const focusIndex = Math.min(pastedValue.length, otpInputs.length) - 1;

      otpInputs[focusIndex].focus();
    });
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    clearFormErrors(form);

    const otp = getOtpValue();

    if (otp.length !== 6) {
      showFieldErrors(form, {
        otp: ["Enter the complete six-digit verification code."],
      });

      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Verifying...";

    try {
      const result = await apiRequest("/api/accounts/auth/verify-email-otp/", {
        method: "POST",
        body: JSON.stringify({
          email: verificationEmail,
          otp,
        }),
      });

      if (!result.ok) {
        showFieldErrors(form, result.data.errors || {});

        showGeneralError(
          form,
          result.data.message || "Unable to verify your email.",
        );

        return;
      }

      sessionStorage.removeItem("rentora_verification_email");

      window.location.href = "/login/?verified=true";
    } catch (error) {
      showGeneralError(form, "Unable to connect to the server.");
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Verify email";
    }
  });

  let remainingSeconds = 60;
  let countdownInterval = null;

  const startCountdown = () => {
    remainingSeconds = 60;
    resendButton.disabled = true;

    resendButton.innerHTML =
      'Resend code in <span id="resend-countdown">60</span>s';

    countdownInterval = window.setInterval(() => {
      remainingSeconds -= 1;

      const activeCountdown = document.getElementById("resend-countdown");

      if (activeCountdown) {
        activeCountdown.textContent = String(remainingSeconds);
      }

      if (remainingSeconds <= 0) {
        window.clearInterval(countdownInterval);

        resendButton.disabled = false;
        resendButton.textContent = "Resend verification code";
      }
    }, 1000);
  };

  resendButton.addEventListener("click", async () => {
    resendButton.disabled = true;
    resendButton.textContent = "Sending...";

    try {
      const result = await apiRequest("/api/accounts/auth/resend-email-otp/", {
        method: "POST",
        body: JSON.stringify({
          email: verificationEmail,
        }),
      });

      if (!result.ok) {
        showGeneralError(
          form,
          result.data.message || "Unable to resend the verification code.",
        );

        resendButton.disabled = false;
        resendButton.textContent = "Resend verification code";

        return;
      }

      otpInputs.forEach((input) => {
        input.value = "";
        input.classList.remove("is-filled");
      });

      otpInputs[0].focus();
      startCountdown();
    } catch (error) {
      showGeneralError(form, "Unable to connect to the server.");

      resendButton.disabled = false;
      resendButton.textContent = "Resend verification code";
    }
  });

  otpInputs[0].focus();
  startCountdown();
});

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];

  for (const cookie of cookies) {
    const trimmedCookie = cookie.trim();

    if (trimmedCookie.startsWith(`${name}=`)) {
      return decodeURIComponent(trimmedCookie.substring(name.length + 1));
    }
  }

  return "";
}

async function apiRequest(url, options = {}) {
  const csrfToken = getCookie("csrftoken");

  const response = await fetch(url, {
    credentials: "same-origin",
    ...options,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
      ...(options.headers || {}),
    },
  });

  let responseData = null;

  try {
    responseData = await response.json();
  } catch (error) {
    responseData = {
      success: false,
      message: "The server returned an invalid response.",
    };
  }

  return {
    ok: response.ok,
    status: response.status,
    data: responseData,
  };
}

function clearFormErrors(form) {
  form.querySelectorAll(".field-error").forEach((element) => {
    element.textContent = "";
  });

  const generalError = form.querySelector(".form-general-error");

  if (generalError) {
    generalError.textContent = "";
    generalError.hidden = true;
  }
}

function showFieldErrors(form, errors = {}) {
  Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
    const errorElement = form.querySelector(`[data-error-for="${fieldName}"]`);

    if (!errorElement) {
      return;
    }

    errorElement.textContent = Array.isArray(fieldErrors)
      ? fieldErrors.join(" ")
      : String(fieldErrors);
  });
}

function showGeneralError(form, message) {
  const errorElement = form.querySelector(".form-general-error");

  if (!errorElement) {
    return;
  }

  errorElement.textContent = message || "Something went wrong.";

  errorElement.hidden = false;
}

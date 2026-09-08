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
  const requestOptions = {
    credentials: "same-origin",
    ...options,
  };

  const headers = new Headers(requestOptions.headers || {});

  const isFormData = requestOptions.body instanceof FormData;

  if (requestOptions.body && !isFormData && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const csrfToken = getCookie("csrftoken");

  if (
    csrfToken &&
    !["GET", "HEAD", "OPTIONS"].includes(
      String(requestOptions.method || "GET").toUpperCase(),
    )
  ) {
    headers.set("X-CSRFToken", csrfToken);
  }

  requestOptions.headers = headers;

  try {
    const response = await fetch(url, requestOptions);

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    return {
      ok: response.ok,
      status: response.status,
      data,
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: {
        message: "Unable to connect to the server.",
      },
      error,
    };
  }
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

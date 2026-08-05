document.addEventListener("DOMContentLoaded", () => {
  const logoutButtons = document.querySelectorAll("[data-logout-button]");

  if (!logoutButtons.length) {
    return;
  }

  logoutButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const originalText = button.textContent;

      button.disabled = true;
      button.textContent = "Logging out...";

      try {
        const result = await apiRequest("/api/accounts/auth/logout/", {
          method: "POST",
          body: JSON.stringify({}),
        });

        if (!result.ok) {
          throw new Error(result.data?.message || "Unable to log out.");
        }

        window.location.href = "/";
      } catch (error) {
        console.error("Logout failed:", error);

        alert(error.message || "Unable to log out. Please try again.");

        button.disabled = false;
        button.textContent = originalText;
      }
    });
  });
});

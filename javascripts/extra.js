/* ==============================================================================
 * Protocol    : Deep State of Mind (DSOM) For My AI
 * Script      : Theme Mode Controller (Light / Dark / Auto)
 * Author      : Harisfazillah Jamel (LinuxMalaysia)
 * License     : GNU General Public License v3.0
 * ==============================================================================
 */

(function () {
  function initThemeToggle() {
    const header = document.querySelector(".md-header__inner");
    if (!header || document.querySelector(".theme-mode-toggle-container")) return;

    const container = document.createElement("div");
    container.className = "theme-mode-toggle-container";
    container.innerHTML = `
      <span class="theme-mode-label">MODE :</span>
      <div class="theme-mode-segmented-control">
        <button type="button" class="theme-mode-btn" data-mode="light">☀️ LIGHT</button>
        <button type="button" class="theme-mode-btn" data-mode="dark">🌙 DARK</button>
        <button type="button" class="theme-mode-btn" data-mode="auto">💻 AUTO</button>
      </div>
    `;

    // Insert into header right before the search/repo section
    const searchOrTitle = header.querySelector(".md-header__title");
    if (searchOrTitle && searchOrTitle.nextSibling) {
      header.insertBefore(container, searchOrTitle.nextSibling);
    } else {
      header.appendChild(container);
    }

    const buttons = container.querySelectorAll(".theme-mode-btn");

    function getSystemScheme() {
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "slate" : "default";
    }

    function applyMode(mode) {
      let scheme = "default";
      if (mode === "dark") {
        scheme = "slate";
      } else if (mode === "light") {
        scheme = "default";
      } else {
        // Auto
        scheme = getSystemScheme();
      }

      document.body.setAttribute("data-md-color-scheme", scheme);
      localStorage.setItem("dsom-theme-mode", mode);

      buttons.forEach((btn) => {
        if (btn.getAttribute("data-mode") === mode) {
          btn.classList.add("active");
        } else {
          btn.classList.remove("active");
        }
      });
    }

    // Read saved mode or default to auto
    const savedMode = localStorage.getItem("dsom-theme-mode") || "auto";
    applyMode(savedMode);

    // Event listeners
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.getAttribute("data-mode");
        applyMode(mode);
      });
    });

    // Watch system color preference changes if in AUTO mode
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      const currentSaved = localStorage.getItem("dsom-theme-mode") || "auto";
      if (currentSaved === "auto") {
        applyMode("auto");
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initThemeToggle);
  } else {
    initThemeToggle();
  }
})();

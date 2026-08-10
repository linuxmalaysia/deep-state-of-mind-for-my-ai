/* ==============================================================================
 * Protocol    : Deep State of Mind (DSOM) For My AI
 * Script      : Theme Mode Controller (Light / Dark / Auto) & Table of Contents Card
 * Author      : Harisfazillah Jamel (LinuxMalaysia)
 * License     : GNU General Public License v3.0
 * ==============================================================================
 */

(function () {
  // Theme Toggle Logic
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

  // Dynamic Table of Contents Card Logic
  function initTOC() {
    // Identify the central content panel
    const contentPanel = document.querySelector('article.md-content__inner.md-typeset');
    if (!contentPanel) return;

    // Identify the secondary sidebar inner container
    const secondarySidebarInner = document.querySelector('.md-sidebar--secondary .md-sidebar__inner');
    if (!secondarySidebarInner) return;

    // Extract h2 and h3 headings
    const headings = Array.from(contentPanel.querySelectorAll('h2, h3'));
    if (headings.length === 0) {
      secondarySidebarInner.innerHTML = '';
      return;
    }

    // Generate clean, unique, deduplicated ID attributes for stable anchors
    const usedIds = new Set();
    const headingData = headings.map((heading) => {
      let id = heading.id || '';

      if (!id) {
        // Generate from slug if empty
        id = heading.textContent
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-+|-+$/g, '');
      }

      let uniqueId = id || 'heading';
      let counter = 1;
      while (usedIds.has(uniqueId)) {
        uniqueId = `${id}-${counter}`;
        counter++;
      }
      usedIds.add(uniqueId);
      heading.id = uniqueId; // Set unique ID on DOM element

      return {
        element: heading,
        id: uniqueId,
        text: heading.textContent.trim(),
        tagName: heading.tagName.toLowerCase()
      };
    });

    // Build hierarchical Table of Contents card
    const tocCard = document.createElement('div');
    tocCard.className = 'custom-toc-card';

    const tocHeader = document.createElement('div');
    tocHeader.className = 'custom-toc-header';
    tocHeader.textContent = 'TABLE OF CONTENTS';
    tocCard.appendChild(tocHeader);

    const tocList = document.createElement('ul');
    tocList.className = 'custom-toc-list';

    let currentH2Li = null;
    let currentH3Ul = null;

    headingData.forEach((item) => {
      const li = document.createElement('li');
      li.className = `custom-toc-item custom-toc-item--${item.tagName}`;

      const link = document.createElement('a');
      link.href = `#${item.id}`;
      link.className = 'custom-toc-link';
      link.textContent = item.text;
      li.appendChild(link);

      if (item.tagName === 'h2') {
        tocList.appendChild(li);
        currentH2Li = li;
        currentH3Ul = null;
      } else {
        if (currentH2Li) {
          if (!currentH3Ul) {
            currentH3Ul = document.createElement('ul');
            currentH3Ul.className = 'custom-toc-sublist';
            currentH2Li.appendChild(currentH3Ul);
          }
          currentH3Ul.appendChild(li);
        } else {
          tocList.appendChild(li);
        }
      }
    });

    tocCard.appendChild(tocList);
    secondarySidebarInner.innerHTML = '';
    secondarySidebarInner.appendChild(tocCard);

    // Intersection scroll highlighting logic
    const tocLinks = tocCard.querySelectorAll('.custom-toc-link');

    function highlightActiveSection() {
      const scrollPosition = window.scrollY + 120; // safe offset for sticky header
      let activeItem = null;

      for (let i = 0; i < headingData.length; i++) {
        const top = headingData[i].element.offsetTop;
        if (scrollPosition >= top) {
          activeItem = headingData[i];
        } else {
          break;
        }
      }

      if (window.scrollY < 50 && headingData.length > 0) {
        activeItem = headingData[0];
      }

      tocLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (activeItem && href === `#${activeItem.id}`) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          highlightActiveSection();
          ticking = false;
        });
        ticking = true;
      }
    });

    highlightActiveSection();
  }

  // Initialize both systems on page ready
  function initAll() {
    initThemeToggle();
    initTOC();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();

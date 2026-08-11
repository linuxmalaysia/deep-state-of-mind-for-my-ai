/**
 * Unit / integration tests for docs/javascripts/extra.js
 *
 * SCOPE: This PR added the "Dynamic Table of Contents Card" feature
 * (initTOC) and refactored the bootstrap logic to call both
 * initThemeToggle() and initTOC() via a new initAll() function. These
 * tests focus on that newly added/changed behavior. The internal
 * implementation details of initThemeToggle() itself are pre-existing
 * and are only exercised here incidentally (to confirm initAll() wires
 * both features together without throwing).
 *
 * The script is a plain IIFE with no module.exports, so it is loaded
 * fresh into the jsdom global scope for every test via `jest.isolateModules`
 * + `require`, relying on Jest's jsdom test environment exposing
 * `window`/`document`/`localStorage` as real globals that the script can
 * reference directly (exactly as it would in a browser).
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_PATH = path.join(__dirname, '..', 'extra.js');

// Sanity check the file exists where we expect before any test runs.
if (!fs.existsSync(SCRIPT_PATH)) {
  throw new Error(`Expected script not found at ${SCRIPT_PATH}`);
}

function buildDom({ header = true, contentHtml = null, sidebar = true, sidebarPrefill = '' } = {}) {
  const headerHtml = header
    ? '<div class="md-header__inner"><div class="md-header__title">Title</div></div>'
    : '';

  const contentPanelHtml =
    contentHtml === null
      ? ''
      : `<article class="md-content__inner md-typeset">${contentHtml}</article>`;

  const sidebarHtml = sidebar
    ? `<div class="md-sidebar--secondary"><div class="md-sidebar__inner">${sidebarPrefill}</div></div>`
    : '';

  document.body.innerHTML = `${headerHtml}${contentPanelHtml}${sidebarHtml}`;
}

function mockBrowserApis() {
  // jsdom does not implement matchMedia; extra.js calls it unconditionally
  // inside initThemeToggle(), which initAll() always invokes.
  window.matchMedia = jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    addListener: jest.fn(),
    removeListener: jest.fn(),
    dispatchEvent: jest.fn(),
  }));

  // Make requestAnimationFrame synchronous & deterministic for tests that
  // exercise the scroll-highlighting throttle logic.
  window.requestAnimationFrame = jest.fn((cb) => {
    cb();
    return 1;
  });
}

function setScrollY(value) {
  Object.defineProperty(window, 'scrollY', {
    configurable: true,
    value,
  });
}

function setOffsetTop(element, value) {
  Object.defineProperty(element, 'offsetTop', {
    configurable: true,
    value,
  });
}

/** Executes extra.js fresh (module cache reset) in the current jsdom document. */
function runScript() {
  jest.isolateModules(() => {
    require(SCRIPT_PATH);
  });
}

beforeEach(() => {
  localStorage.clear();
  mockBrowserApis();
  setScrollY(0);
});

describe('initTOC (Dynamic Table of Contents Card)', () => {
  test('does nothing when the content panel is missing', () => {
    buildDom({ contentHtml: null, sidebar: true, sidebarPrefill: '<p>keep-me</p>' });

    runScript();

    const sidebarInner = document.querySelector('.md-sidebar--secondary .md-sidebar__inner');
    expect(sidebarInner.innerHTML).toBe('<p>keep-me</p>');
    expect(document.querySelector('.custom-toc-card')).toBeNull();
  });

  test('does nothing (and does not throw) when the secondary sidebar is missing', () => {
    buildDom({ contentHtml: '<h2>Intro</h2>', sidebar: false });

    expect(() => runScript()).not.toThrow();
    expect(document.querySelector('.custom-toc-card')).toBeNull();
  });

  test('clears the sidebar and skips rendering when there are no h2/h3 headings', () => {
    buildDom({
      contentHtml: '<p>Just a paragraph, no headings here.</p>',
      sidebarPrefill: '<p>old-toc-marker</p>',
    });

    runScript();

    const sidebarInner = document.querySelector('.md-sidebar--secondary .md-sidebar__inner');
    expect(sidebarInner.innerHTML).toBe('');
  });

  test('replaces any pre-existing sidebar content with a single TOC card', () => {
    buildDom({
      contentHtml: '<h2>Alpha</h2>',
      sidebarPrefill: '<nav class="md-nav--secondary">old default toc</nav>',
    });

    runScript();

    const sidebarInner = document.querySelector('.md-sidebar--secondary .md-sidebar__inner');
    expect(sidebarInner.children).toHaveLength(1);
    expect(sidebarInner.children[0].className).toBe('custom-toc-card');
    expect(sidebarInner.textContent).not.toContain('old default toc');
  });

  test('builds a header labelled "TABLE OF CONTENTS"', () => {
    buildDom({ contentHtml: '<h2>Alpha</h2>' });

    runScript();

    const header = document.querySelector('.custom-toc-header');
    expect(header).not.toBeNull();
    expect(header.textContent).toBe('TABLE OF CONTENTS');
  });

  test('nests h3 headings under the preceding h2 in a sublist', () => {
    buildDom({
      contentHtml: `
        <h2>Introduction</h2>
        <h3>Sub A</h3>
        <h3>Sub B</h3>
        <h2>Next Section</h2>
      `,
    });

    runScript();

    const topLevelItems = document.querySelectorAll('.custom-toc-list > .custom-toc-item');
    expect(topLevelItems).toHaveLength(2);

    const firstH2Item = topLevelItems[0];
    expect(firstH2Item.classList.contains('custom-toc-item--h2')).toBe(true);

    const sublist = firstH2Item.querySelector('.custom-toc-sublist');
    expect(sublist).not.toBeNull();
    const subItems = sublist.querySelectorAll('.custom-toc-item--h3');
    expect(subItems).toHaveLength(2);
    expect(subItems[0].textContent).toBe('Sub A');
    expect(subItems[1].textContent).toBe('Sub B');

    const secondH2Item = topLevelItems[1];
    expect(secondH2Item.querySelector('.custom-toc-sublist')).toBeNull();
  });

  test('places a leading h3 (before any h2) directly at the top level, not nested', () => {
    buildDom({
      contentHtml: `
        <h3>Early Sub-Heading</h3>
        <h2>Main Heading</h2>
      `,
    });

    runScript();

    const topLevelItems = document.querySelectorAll('.custom-toc-list > .custom-toc-item');
    expect(topLevelItems).toHaveLength(2);
    expect(topLevelItems[0].classList.contains('custom-toc-item--h3')).toBe(true);
    expect(topLevelItems[0].querySelector('.custom-toc-sublist')).toBeNull();
    expect(topLevelItems[1].classList.contains('custom-toc-item--h2')).toBe(true);
  });

  test('generates a clean slug id from heading text when no id attribute is present', () => {
    buildDom({ contentHtml: '<h2>Hello World!</h2>' });

    runScript();

    const heading = document.querySelector('h2');
    expect(heading.id).toBe('hello-world');

    const link = document.querySelector('.custom-toc-link');
    expect(link.getAttribute('href')).toBe('#hello-world');
    expect(link.textContent).toBe('Hello World!');
  });

  test('preserves an existing heading id instead of regenerating it', () => {
    buildDom({ contentHtml: '<h2 id="my-custom-id">Title</h2>' });

    runScript();

    const heading = document.querySelector('h2');
    expect(heading.id).toBe('my-custom-id');
    expect(document.querySelector('.custom-toc-link').getAttribute('href')).toBe('#my-custom-id');
  });

  test('deduplicates ids for multiple headings that slugify to the same value', () => {
    buildDom({
      contentHtml: `
        <h2>Overview</h2>
        <h2>Overview</h2>
        <h2>Overview</h2>
      `,
    });

    runScript();

    const headings = document.querySelectorAll('h2');
    expect(headings[0].id).toBe('overview');
    expect(headings[1].id).toBe('overview-1');
    expect(headings[2].id).toBe('overview-2');

    const hrefs = Array.from(document.querySelectorAll('.custom-toc-link')).map((a) =>
      a.getAttribute('href')
    );
    expect(hrefs).toEqual(['#overview', '#overview-1', '#overview-2']);
  });

  test('falls back to the id "heading" when a heading has no usable text for a slug', () => {
    buildDom({ contentHtml: '<h2>!!!</h2>' });

    runScript();

    const heading = document.querySelector('h2');
    expect(heading.id).toBe('heading');
    expect(document.querySelector('.custom-toc-link').getAttribute('href')).toBe('#heading');
  });

  test('avoids id collisions across multiple symbol-only headings', () => {
    buildDom({
      contentHtml: `
        <h2>???</h2>
        <h2>***</h2>
      `,
    });

    runScript();

    const headings = document.querySelectorAll('h2');
    // Both headings slugify to an empty string, so both first fall back to
    // 'heading'. The de-dup loop then rebuilds candidates from the raw
    // (empty) slug plus a counter suffix (`${id}-${counter}`), so the
    // second heading ends up as '-1' rather than 'heading-1'. This test
    // pins down that actual de-dup behavior so a future refactor of the
    // slugging logic doesn't silently reintroduce duplicate ids.
    expect(headings[0].id).toBe('heading');
    expect(headings[1].id).toBe('-1');
    expect(headings[0].id).not.toBe(headings[1].id);
  });
});

describe('initTOC scroll highlighting (highlightActiveSection)', () => {
  function setupThreeHeadings(offsets) {
    buildDom({
      contentHtml: `
        <h2>First</h2>
        <h2>Second</h2>
        <h2>Third</h2>
      `,
    });

    const headings = document.querySelectorAll('h2');
    headings.forEach((h, i) => setOffsetTop(h, offsets[i]));
    return headings;
  }

  function activeLinkText() {
    const active = document.querySelector('.custom-toc-link.active');
    return active ? active.textContent : null;
  }

  test('marks the last heading whose offsetTop is at or above the scroll position as active', () => {
    setupThreeHeadings([0, 200, 400]);
    setScrollY(250); // scrollPosition = 250 + 120 = 370 -> "Second" (200) is active, not "Third" (400)

    runScript();

    expect(activeLinkText()).toBe('Second');
  });

  test('marks only a single link as active at a time', () => {
    setupThreeHeadings([0, 200, 400]);
    setScrollY(500);

    runScript();

    const activeLinks = document.querySelectorAll('.custom-toc-link.active');
    expect(activeLinks).toHaveLength(1);
    expect(activeLinks[0].textContent).toBe('Third');
  });

  test('forces the first heading active when scrollY is near the top, overriding offset math', () => {
    // All offsets are within the computed scroll window, so without the
    // "near top" override the loop would naturally select the *last*
    // heading. The override should force the *first* heading instead.
    setupThreeHeadings([0, 10, 20]);
    setScrollY(0);

    runScript();

    expect(activeLinkText()).toBe('First');
  });

  test('updates the active link in response to a scroll event', () => {
    const headings = setupThreeHeadings([0, 200, 400]);
    setScrollY(0);

    runScript();
    expect(activeLinkText()).toBe('First');

    setScrollY(500);
    window.dispatchEvent(new Event('scroll'));

    expect(window.requestAnimationFrame).toHaveBeenCalled();
    expect(activeLinkText()).toBe('Third');
  });
});

describe('initAll bootstrap wiring', () => {
  test('invokes both the theme toggle and the TOC builder', () => {
    buildDom({ header: true, contentHtml: '<h2>Alpha</h2>', sidebar: true });

    runScript();

    expect(document.querySelector('.theme-mode-toggle-container')).not.toBeNull();
    expect(document.querySelector('.custom-toc-card')).not.toBeNull();
  });

  test('runs immediately when document.readyState is already "complete"', () => {
    buildDom({ header: true, contentHtml: '<h2>Alpha</h2>', sidebar: true });
    expect(document.readyState).toBe('complete');

    runScript();

    expect(document.querySelector('.custom-toc-card')).not.toBeNull();
  });

  test('defers initialization until DOMContentLoaded when the document is still loading', () => {
    buildDom({ header: true, contentHtml: '<h2>Alpha</h2>', sidebar: true });
    Object.defineProperty(document, 'readyState', {
      configurable: true,
      value: 'loading',
    });

    runScript();

    expect(document.querySelector('.custom-toc-card')).toBeNull();

    document.dispatchEvent(new Event('DOMContentLoaded'));

    expect(document.querySelector('.custom-toc-card')).not.toBeNull();

    Object.defineProperty(document, 'readyState', {
      configurable: true,
      value: 'complete',
    });
  });
});
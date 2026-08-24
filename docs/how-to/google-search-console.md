---
okf_version: 0.1
type: documentation
title: "How-To: Verify and Monitor Site with Google Search Console"
timestamp: "2026-08-22T10:00:00Z"
topics: ["dsom", "how-to", "seo", "google-search-console", "okf"]
---
# Verify and monitor site with Google Search Console

This guide details how to verify domain ownership and monitor website performance in Google Search Console for the Deep State of Mind (DSOM) documentation site.

## Overview of Google Search Console

Google Search Console (GSC) is a web service provided by Google that enables website owners, administrators, and SEO specialists to monitor, maintain, and troubleshoot their site's presence in Google Search results.

Adding ownership verification provides access to critical search analytics, crawl reports, indexation status, security alerts, and sitemap management.

## Why site ownership verification is required

Site owners in Google Search Console gain access to sensitive performance data and indexing management controls. To ensure security, Google requires proof of domain control before granting owner permissions.

DSOM implements two redundant verification techniques to maintain persistent verification:

1. **HTML Meta Tag Verification:** Injects a custom `<meta name="google-site-verification" content="..." />` tag into the `<head>` section of every HTML page.
2. **HTML Verification File Upload:** Publishes a dedicated token file (`google953c3228b9041989.html`) at the site root URL.

Using dual verification methods prevents accidental loss of verified owner status if theme overrides or static assets are modified during deployment.

## Verification configuration details

### Method 1: HTML Meta Tag Injection

The HTML meta tag is added to the `<head>` section via MkDocs Material template overrides:

- **Verification Token:** `OKJ30rPxLeaG-OocY3C2xkXbYEVgwfMMoaOycjWQJJw`
- **Override Template:** `docs/overrides/main.html`
- **Injected Code:**

```html
<meta name="google-site-verification" content="OKJ30rPxLeaG-OocY3C2xkXbYEVgwfMMoaOycjWQJJw" />
```

### Method 2: HTML Verification File

The verification file is placed at the documentation build root so it is served directly by GitHub Pages:

- **File Name:** `google953c3228b9041989.html`
- **File Content:** `google-site-verification: google953c3228b9041989.html`
- **Published URL:** `https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/google953c3228b9041989.html`

## Step-by-step verification process

### Step 1: Add property in Google Search Console

1. Navigate to [Google Search Console](https://search.google.com/search-console).
2. Select **URL-prefix property**.
3. Enter the site URL: `https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/`.

### Step 2: Confirm deployment of verification assets

Run the MkDocs build command and verify the generated assets locally:

```bash
uv run --with mkdocs-material mkdocs build
grep -i "google-site-verification" site/index.html
cat site/google953c3228b9041989.html
```

### Step 3: Complete verification in Search Console

1. In Google Search Console, choose **HTML file** or **HTML tag** under ownership verification.
2. Click **Verify**.
3. Upon successful confirmation, Search Console unlocks search traffic and indexation analytics.

## Submitting sitemaps and monitoring search performance

After verifying ownership:

1. Go to **Indexing > Sitemaps** in Search Console.
2. Submit the automated sitemap URL: `https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/sitemap.xml`.
3. Review **Performance > Search results** to monitor search queries, impressions, click-through rates (CTR), and page rankings.
4. Inspect crawl logs under **Indexing > Pages** to detect and fix any unindexed pages or redirection issues.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

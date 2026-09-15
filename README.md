# Simple Site Checker

## (webpages-validator-ssc)

Simple command-line utility for checking links on a web page.

---

## Overview

`simple-site-checker` (`ssc`) is a lightweight, ultra-fast Python CLI tool designed to quickly verify the HTTP status codes of all hyperlinks on a given web page. It uses only standard Python libraries and has no external dependencies.

**Features:**
- **Lightning Fast:** Uses multi-threading for concurrent link validation.
- **Bandwidth Friendly:** Utilizes `HEAD` requests for checking link status.
- **Dependency-Free:** Built entirely with Python's standard library.
- **Session Support:** Pass cookies easily via file or string for checking authenticated pages.
- **Exportable:** Optionally export results to a CSV file.

---

## Installation

### Install via PIP

```bash
pip install webpages-validator-ssc
```

```bash
ssc -links -url https://www.example.com
```

### Optional: Save results to CSV

```bash
ssc -links -url https://www.example.com -res results.csv
```

### Optional: Skip Strict Anti-bot Services

If you're testing pages with many social media links (LinkedIn, Twitter/X, Instagram, etc.), you might get blocked or rate-limited. Use the `-skip-strict` flag to skip validation for these domains. They will be marked as `SKIPPED` in the stats without making HTTP requests.

```bash
ssc -links -url https://www.example.com -skip-strict
```

### Check resources (images, scripts, styles)

You can check if loaded resources (like images, scripts, stylesheets, audio, and video) are available using the `-src` flag:

```bash
ssc -src -url https://www.example.com
```

*Note: You can combine `-links` and `-src` to check everything on the page.*

```bash
ssc -links -src -url https://www.example.com
```

### Optional: set cookies

You can pass a cookie file:
```bash
ssc -links -url https://www.example.com -auth cookies.txt
```

#### cookies.txt

```txt
name=value
```

Or you can pass the cookie string directly:
```bash
ssc -links -url https://www.example.com -auth "name=value"
```

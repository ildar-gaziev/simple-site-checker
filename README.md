# Simple Site Checker

Simple command-line utility for checking links on a web page.

---

## Overview

`simple-site-checker` (`ssc`) is a lightweight Python CLI tool designed to quickly verify the HTTP status codes of all hyperlinks on a given web page. It uses only standard Python libraries and has no external dependencies.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/simple-site-checker.git
cd simple-site-checker
pip install -e .
ssc -links -url https://www.example.com
```

### Optional: Save results to CSV

```bash
ssc -links -url https://www.example.com -res results.csv
```

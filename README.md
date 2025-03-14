# Simple Site Checker

Simple command-line utility for checking links on a web page.

---

## Overview

`simple-site-checker` (`ssc`) is a lightweight Python CLI tool designed to quickly verify the HTTP status codes of all hyperlinks on a given web page. It uses only standard Python libraries and has no external dependencies.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/ildar-gaziev/simple-site-checker.git
```

```bash
cd simple-site-checker
```

```bash
pip install -e .
```

```bash
ssc -links -url https://www.example.com
```

### Optional: Save results to CSV

```bash
ssc -links -url https://www.example.com -res results.csv
```

### Optional: set cookies

```bash
ssc -links -url https://www.example.com -auth cookies.txt
```

#### cookies.txt

```txt
name=value
```

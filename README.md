# 🎭 playwright_ui_testing_framework

A professional, scalable UI end-to-end testing framework built with [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/). Structured around the **Page Object Model** for clean, maintainable test code that scales with your application.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-latest-green?logo=playwright)
![pytest](https://img.shields.io/badge/pytest-latest-orange?logo=pytest)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Page Object Model](#page-object-model)
- [Fixtures](#fixtures)
- [CI/CD Integration](#cicd-integration)

---

## Overview

`playwright_ui_testing_framework` provides a clean, structured foundation for browser-based UI testing. It separates test logic from page interaction logic using the Page Object Model, making tests easy to read, write, and maintain as your application grows.

**Key features:**
- Cross-browser support — Chromium, Firefox, and WebKit
- Headless and headed execution modes
- Automatic screenshot, video, and trace capture on failure
- Shared fixtures for authentication and browser context reuse
- Environment-based configuration via `.env`
- HTML test reports out of the box

---

## Prerequisites

- Python **3.8+**
- pip
- Node.js **16+** *(used internally by Playwright)*

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/playwright_ui_testing_framework.git
cd playwright_ui_testing_framework
```

### 2. Create and activate a virtual environment

Run `python -m venv venv`, then activate it with `source venv/bin/activate` on macOS/Linux or `venv\Scripts\activate` on Windows.

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

> To install a single browser only: `playwright install chromium`

### 5. Set up environment variables

Copy `.env.example` to `.env` and fill in your values — see [Configuration](#configuration) for details.

---

## Project Structure

```
playwright_ui_testing_framework/
│
├── pages/                    # Page Object classes
│   ├── base_page.py          # Shared methods inherited by all page objects
│   ├── login_page.py
│   └── dashboard_page.py
│
├── tests/                    # Test files
│   ├── conftest.py           # Test-level fixtures
│   ├── test_login.py
│   └── test_dashboard.py
│
├── utils/                    # Helpers and utilities
│   ├── config.py             # Loads and exposes environment config
│   └── helpers.py            # Reusable utility functions
│
├── test-results/             # Auto-generated: screenshots, videos, traces
├── reports/                  # Auto-generated: HTML test reports
│
├── conftest.py               # Root fixtures (browser/context/page setup)
├── pytest.ini                # pytest settings
├── requirements.txt          # Python dependencies
├── .env                      # Local environment variables (git-ignored)
└── .env.example              # Committed template for .env
```

---

## Configuration

### `.env` — Environment Variables

```ini
# Application
BASE_URL=https://staging.yourapp.com

# Test credentials
TEST_USERNAME=testuser@yourapp.com
TEST_PASSWORD=your_test_password

# Browser options
BROWSER=chromium          # chromium | firefox | webkit
HEADLESS=true
SLOW_MO=0                 # Delay in ms between actions — useful for debugging
```

> `.env` is git-ignored. Never commit real credentials. Use `.env.example` as the committed template.

### `pytest.ini` — Test Runner Settings

```ini
[pytest]
testpaths = tests
addopts =
    --html=reports/report.html
    --self-contained-html
    --screenshot=only-on-failure
    --video=retain-on-failure
    --tracing=retain-on-failure

markers =
    smoke:      Critical path tests — run on every deploy
    regression: Full regression suite
    auth:       Authentication-related tests
```

### `requirements.txt`

```
pytest
playwright
pytest-playwright
pytest-html
python-dotenv
pytest-xdist
```

---

## Running Tests

### Run the full suite

```bash
pytest
```

### Run a specific file

```bash
pytest tests/test_login.py
```

### Run by marker

```bash
pytest -m smoke
pytest -m regression
pytest -m "regression and not auth"
```

### Run on a specific browser

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run in headed mode (visible browser window)

```bash
pytest --headed
```

### Run tests in parallel

```bash
pytest -n auto       # Uses all available CPU cores
pytest -n 4          # Uses 4 parallel workers
```

### Run with verbose output

```bash
pytest -v
```

### View a failure trace

When a test fails, a trace file is saved to `test-results/`. Open it with:

```bash
playwright show-trace test-results/<trace-file>.zip
```

---

## Page Object Model

All page interaction logic lives in `pages/`. Tests never contain raw selectors or low-level Playwright calls — only Page Object methods.

Each page in the application has a corresponding class in `pages/` that inherits from `BasePage`. `BasePage` provides shared helpers (navigation, visibility checks, screenshots) so individual page objects stay focused on their own interactions and locators.

This separation ensures that when a UI changes, only the relevant Page Object needs updating — not every test that touches that page.

---

## Fixtures

Fixtures are defined in `conftest.py` and automatically injected into tests by pytest. They handle setup and teardown so tests stay clean and focused.

The root `conftest.py` provides session-scoped fixtures for `base_url` and `credentials` (loaded from `.env`), as well as a function-scoped `authenticated_page` fixture that returns a fully logged-in browser page — ready to use in any test that requires an active session.

---

## CI/CD Integration

### GitHub Actions

Add the following workflow file to your repository:

```yaml
# .github/workflows/ui-tests.yml

name: UI Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps

      - name: Run smoke tests
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
        run: pytest -m smoke --browser chromium

      - name: Upload test artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: |
            reports/
            test-results/
```

> Store `BASE_URL`, `TEST_USERNAME`, and `TEST_PASSWORD` as **GitHub Actions Secrets** under *Settings → Secrets and variables → Actions*. Never hardcode credentials in workflow files.

---

## Contributing

1. Branch from `develop`: `git checkout -b feat/your-feature-name`
2. Follow the Page Object Model — all selectors and interactions belong in `pages/`
3. Cover new functionality with tests
4. Verify locally before opening a PR: `pytest -m regression`
5. Keep page objects focused — one class per page or major component

---

## License

MIT © your-org
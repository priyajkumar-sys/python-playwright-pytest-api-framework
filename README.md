# Python Playwright + Pytest UI & API Automation Framework

A Python-based test automation framework using **Playwright** and **pytest** for UI and API testing.

This project demonstrates practical test automation techniques, including reusable fixtures, data-driven testing, browser interactions, locator strategies, and automated assertions. The framework is being developed with a focus on **maintainability, reusability, and scalability**.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Test automation programming language |
| Playwright | Browser automation and API testing |
| pytest | Test execution, fixtures, and parametrization |
| Chromium | Browser test execution |
| PyCharm | Development environment |
| Git & GitHub | Version control |

## Project Structure

```text
python-playwright-pytest-api-framework/
│
├── api_tests/              # API automation tests
├── ui_tests/               # UI automation tests
├── conftest.py             # Shared pytest fixtures
├── .gitignore              # Git exclusion rules
├── LICENSE                 # MIT License
└── README.md               # Project documentation
```

## UI Automation

The UI automation tests use [SauceDemo](https://www.saucedemo.com/) as the application under test.

### Test Scenarios

**Login Validation**
- Successful login with valid credentials
- Invalid login error message validation
- URL verification after authentication attempts

**Inventory and Shopping Cart**
- Product selection and add-to-cart functionality
- Shopping cart navigation
- Validation of selected products

**Footer Social Media Links**
- Validation of X, Facebook, and LinkedIn links
- Handling newly opened browser tabs
- Verification of destination URLs
- Data-driven validation using pytest parametrization

## Framework Design

### Reusable Pytest Fixtures

Shared setup logic is maintained in `conftest.py`.

Fixtures help reduce duplicated code and improve test maintainability.

Examples include:
- Configuring Playwright's `data-test` locator attribute
- Centralizing the application base URL
- Reusing authenticated browser sessions within individual tests

### Locator Strategies

The framework uses Playwright's built

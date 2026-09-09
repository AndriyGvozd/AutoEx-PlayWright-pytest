# AutoEx Playwright + Pytest Test Suite

📊 **[Latest Allure report](https://andriygvozd.github.io/AutoEx-PlayWright-pytest/)** — updated automatically after every push to `main`.

A cross-browser UI test automation project for [automationexercise.com](https://automationexercise.com), covering all 26 official test cases published on the site's [Test Cases](https://automationexercise.com/test_cases) page (registration/login, product browsing & search, cart, checkout & payment, contact form, and home page UI).

## Tech stack

| Tool | Purpose |
|---|---|
| [Playwright](https://playwright.dev/) | Browser automation (sync API) |
| [pytest](https://docs.pytest.org/) | Test runner |
| [pytest-playwright](https://github.com/microsoft/playwright-pytest) | Playwright ↔ pytest integration (browser/page fixtures, `--browser` CLI flag) |
| [Allure](https://allurereport.org/) (`allure-pytest`) | Test reporting — per-step descriptions, screenshots, history/trend |
| [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) | Parallel test execution (`-n`) |
| [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) | Automatic reruns for flaky/transient failures |
| GitHub Actions | CI pipeline |
| GitHub Pages | Hosting the published Allure report |

Only stable (non-pre-release) versions of every dependency are used — see [requirements.txt](requirements.txt).

## Project structure

```
.
├── conftest.py                  # Shared fixtures: home_page, registered_user (+ its teardown)
├── pytest.ini                   # pytest config: addopts, reruns, Allure results dir
├── requirements.txt              # Pinned dependency versions
├── pages/                        # Page Object Model — one class per page
│   ├── base_page.py               # Common base (holds the Playwright Page, .goto())
│   ├── home_page.py                # Header nav, footer subscription, scroll-to-top, recommended items
│   ├── signup_login_page.py        # Signup / Login forms
│   ├── signup_page.py              # "Enter Account Information" registration form
│   ├── account_created_page.py     # "Account Created!" confirmation
│   ├── account_deleted_page.py     # "Account Deleted!" confirmation
│   ├── products_page.py            # All Products grid, search, category/brand navigation
│   ├── product_detail_page.py      # Single product page, quantity, add to cart, reviews
│   ├── cart_page.py                # Cart rows, quantities/prices, remove, checkout entry
│   ├── checkout_page.py            # Address review, order comment, place order
│   ├── payment_page.py             # Card form, order confirmation, invoice download
│   └── contact_us_page.py          # Contact form, file upload, confirm() dialog handling
├── tests/                         # One file per feature area (26 tests total)
│   ├── test_authorization_flow.py  # Test Cases 1-5: register / login / logout
│   ├── test_products.py            # Test Cases 7, 8, 9, 18, 19, 21
│   ├── test_cart.py                # Test Cases 11, 12, 13, 17, 20, 22
│   ├── test_checkout.py            # Test Cases 14, 15, 16, 23, 24
│   ├── test_contact_us.py          # Test Case 6
│   ├── test_home_ui.py             # Test Cases 10, 25, 26
│   └── fixtures/sample_upload.txt  # Sample file used by the Contact Us upload step
├── utils/
│   ├── test_data.py                # unique_user_data() — generates unique, parallel-safe test users
│   └── allure_steps.py             # step() context manager: Allure step + screenshot per action
└── .github/workflows/tests.yml    # CI pipeline (see below)
```

## How it's implemented

### Page Object Model

Every page of the site is its own class extending `BasePage`. Locators are declared in `__init__` (preferring the site's `data-qa`/`id` attributes over brittle CSS where available), and methods that trigger navigation return the next page's object (page-chaining), e.g.:

```python
signup_login_page = home_page.click_signup_login()
signup_page = signup_login_page.signup(name, email)
```

Reusable multi-step actions are collapsed into a single composite method (`SignupPage.complete_registration()`, `PaymentPage.pay()`) rather than repeated inline in every test, and shared setup (`registered_user` fixture in `conftest.py`) creates a real account once and tears it down (deletes it) whether the test itself already did or not.

### Allure reporting with parametrized steps

Every test wraps each official test-case step in a `with step(page, "N. ..."):` block (`utils/allure_steps.py`). Each step:
- is recorded as a named Allure step, with the description **parametrized with the actual data used** at runtime (e.g. `"Enter email 'testuser123@example.com'"` rather than a generic label), matching the numbered steps from the site's own test case descriptions;
- gets a full-page screenshot attached automatically once the step completes.

Tests are also tagged with `@allure.feature("...")` and `@allure.title("Test Case N: ...")` so the report groups them by feature area (Authorization, Products, Cart, Checkout, Contact Us, Home Page UI) and displays each one under its official title.

### Cross-browser & parallel execution

Browser and parallelism are chosen per run via CLI flags, not hardcoded:

```bash
pytest --browser chromium         # default if --browser is omitted
pytest --browser firefox
pytest --browser chromium --browser firefox   # runs the whole suite on both
pytest -n auto                    # parallel across CPU cores (pytest-xdist)
pytest -n 4 --browser firefox     # parallel + a specific browser
```

WebKit was evaluated but is intentionally not used: under this project's CI load it was markedly less stable than Chromium/Firefox against the live target site (frequent timeouts and, at peak testing volume, the site's own anti-bot challenge page), so it was dropped in favor of reliable, reproducible runs.

### Handling live-site flakiness

The suite runs against a real, public, third-party demo site (not a mock), so transient load-related failures (slow AJAX, a dropped request) are expected. `pytest-rerunfailures` retries a failing test up to 3 times (2s apart) before it's reported as failed — scoped via `--only-rerun` to timeout/assertion failures only, so a genuine code error (e.g. a broken import) still fails immediately instead of wasting three attempts on it.

Several Page Object methods also contain their own defensive waits/retries for known UI race conditions on the target site (animated Bootstrap modals/accordions, carousels with cloned slides) — documented inline with the "why" in each case.

## CI/CD pipeline

`.github/workflows/tests.yml` runs on every push/PR to `main` (and can be triggered manually):

1. **`test`** — a matrix job runs the full suite once per browser (chromium, firefox) in parallel, each on its own runner, and uploads its Allure results as a build artifact.
2. **`report`** — downloads and merges both browsers' results, carries over the previous report's history (so the Allure **Trend** chart is continuous across runs), generates the HTML report with the Allure CLI, and publishes it to the `gh-pages` branch.

GitHub Pages serves that branch, so the [live report](https://andriygvozd.github.io/AutoEx-PlayWright-pytest/) always reflects the latest run on `main`.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install --with-deps     # installs the Chromium/Firefox browser binaries

pytest -v                          # run the full suite (chromium, sequential)
```

### Viewing the Allure report locally

```bash
# after a pytest run, results are written to ./allure-results
npm install -g allure-commandline
allure generate allure-results --clean -o allure-report
allure open allure-report
```

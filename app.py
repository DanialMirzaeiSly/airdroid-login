import traceback

from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


app = Flask(__name__)

URL = "https://www.airdroid.com/user-center/signin/?redirect=%2F"

EMAIL = "mobility_hy@telegmail.com"
PASSWORD = "Danial*#*&*Mirzaei??23"


@app.route("/")
def home():
    return "Server is running"


@app.route("/run")
def run_login():

    driver = None

    try:
        print("========================================", flush=True)
        print("=== /run started ===", flush=True)
        print("========================================", flush=True)

        # ====================================
        # Chrome configuration
        # ====================================

        options = webdriver.ChromeOptions()

        options.binary_location = "/usr/bin/chromium"

        # مهم:
        # eager باعث می‌شود Selenium منتظر تمام عکس‌ها،
        # trackingها و resourceهای جانبی نماند.
        options.page_load_strategy = "eager"

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")

        options.add_argument(
            "--disable-features=Translate,BackForwardCache"
        )

        options.add_argument("--window-size=1280,900")

        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")

        options.add_argument(
            "--disable-popup-blocking"
        )

        print(
            "Starting Chrome...",
            flush=True
        )

        # ====================================
        # Start Chrome
        # ====================================

        driver = webdriver.Chrome(
            options=options
        )

        print(
            "Chrome started successfully",
            flush=True
        )

        # ====================================
        # Timeouts
        # ====================================

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)

        wait = WebDriverWait(
            driver,
            30
        )

        # ====================================
        # Open AirDroid
        # ====================================

        print(
            "Opening AirDroid...",
            flush=True
        )

        try:

            driver.get(URL)

            print(
                "driver.get() completed",
                flush=True
            )

        except Exception as e:

            print(
                "driver.get() warning:",
                repr(e),
                flush=True
            )

            # با eager معمولاً نباید اینجا برسیم،
            # ولی اگر page-load timeout شد،
            # session را فوراً خراب نمی‌کنیم.
            print(
                "Continuing with current page...",
                flush=True
            )

        # ====================================
        # Check current page
        # ====================================

        try:

            print(
                "Current URL:",
                driver.current_url,
                flush=True
            )

            print(
                "Page title:",
                driver.title,
                flush=True
            )

        except Exception as e:

            print(
                "Could not read page info:",
                repr(e),
                flush=True
            )

        # ====================================
        # Wait for email
        # ====================================

        print(
            "Waiting for email field...",
            flush=True
        )

        email = wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[type="email"]'
                )
            )
        )

        print(
            "Email field found",
            flush=True
        )

        email.clear()

        email.send_keys(
            EMAIL
        )

        print(
            "Email entered",
            flush=True
        )

        # ====================================
        # Password
        # ====================================

        print(
            "Waiting for password field...",
            flush=True
        )

        password = wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[type="password"]'
                )
            )
        )

        print(
            "Password field found",
            flush=True
        )

        password.clear()

        password.send_keys(
            PASSWORD
        )

        print(
            "Password entered",
            flush=True
        )

        # ====================================
        # Cookie popup
        # ====================================

        try:

            cookie = WebDriverWait(
                driver,
                3
            ).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "mode-cookie-tip"
                    )
                )
            )

            driver.execute_script(
                """
                arguments[0].remove();
                """,
                cookie
            )

            print(
                "Cookie popup removed",
                flush=True
            )

        except Exception:

            print(
                "Cookie popup not found",
                flush=True
            )

        # ====================================
        # Sign In button
        # ====================================

        print(
            "Waiting for Sign in button...",
            flush=True
        )

        sign_in = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """
                    //button[
                        contains(
                            translate(
                                normalize-space(.),
                                'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                'abcdefghijklmnopqrstuvwxyz'
                            ),
                            'sign in'
                        )
                    ]
                    """
                )
            )
        )

        print(
            "Sign in button found",
            flush=True
        )

        # ====================================
        # Scroll
        # ====================================

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            sign_in
        )

        print(
            "Scrolled to Sign in button",
            flush=True
        )

        # ====================================
        # Click
        # ====================================

        try:

            sign_in.click()

            print(
                "Sign in clicked normally",
                flush=True
            )

        except Exception as e:

            print(
                "Normal click failed:",
                repr(e),
                flush=True
            )

            driver.execute_script(
                """
                arguments[0].click();
                """,
                sign_in
            )

            print(
                "Sign in clicked with JavaScript",
                flush=True
            )

        # ====================================
        # Wait for login response
        # ====================================

        print(
            "Waiting after login...",
            flush=True
        )

        try:

            WebDriverWait(
                driver,
                10
            ).until(
                lambda d: (
                    d.current_url != URL
                )
            )

        except Exception:

            print(
                "URL did not change within 10 seconds",
                flush=True
            )

        # ====================================
        # Final result
        # ====================================

        try:

            final_url = driver.current_url

        except Exception:

            final_url = "unknown"

        try:

            final_title = driver.title

        except Exception:

            final_title = "unknown"

        print(
            "Final URL:",
            final_url,
            flush=True
        )

        print(
            "Final title:",
            final_title,
            flush=True
        )

        return jsonify({
            "success": True,
            "message": "Login request submitted",
            "current_url": final_url,
            "title": final_title
        })

    # ========================================
    # Error
    # ========================================

    except Exception as e:

        print(
            "========================================",
            flush=True
        )

        print(
            "=== ERROR ===",
            flush=True
        )

        print(
            repr(e),
            flush=True
        )

        traceback.print_exc()

        print(
            "========================================",
            flush=True
        )

        return jsonify({
            "success": False,
            "error": repr(e)
        }), 500

    # ========================================
    # Cleanup
    # ========================================

    finally:

        if driver is not None:

            try:

                driver.quit()

                print(
                    "Chrome closed successfully",
                    flush=True
                )

            except Exception as e:

                print(
                    "Chrome quit warning:",
                    repr(e),
                    flush=True
                )

        print(
            "=== /run finished ===",
            flush=True
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
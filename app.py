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
        print("=== /run started ===", flush=True)

        options = webdriver.ChromeOptions()

        options.binary_location = "/usr/bin/chromium"

        # مهم:
        # منتظر load کامل صفحه نمی‌ماند
        options.page_load_strategy = "none"

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

        print("Starting Chrome...", flush=True)

        driver = webdriver.Chrome(
            options=options
        )

        print(
            "Chrome started successfully",
            flush=True
        )

        # timeoutهای Selenium
        driver.set_page_load_timeout(20)
        driver.set_script_timeout(20)

        wait = WebDriverWait(
            driver,
            30
        )

        # -----------------------------
        # Open website
        # -----------------------------

        print(
            "Opening AirDroid...",
            flush=True
        )

        driver.get(URL)

        print(
            "driver.get() returned",
            flush=True
        )

        # -----------------------------
        # Wait for email
        # -----------------------------

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
        email.send_keys(EMAIL)

        print(
            "Email entered",
            flush=True
        )

        # -----------------------------
        # Password
        # -----------------------------

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
        password.send_keys(PASSWORD)

        print(
            "Password entered",
            flush=True
        )

        # -----------------------------
        # Cookie popup
        # -----------------------------

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
                "arguments[0].remove();",
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

        # -----------------------------
        # Sign in
        # -----------------------------

        print(
            "Waiting for Sign in...",
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

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center'
            });
            """,
            sign_in
        )

        try:

            sign_in.click()

            print(
                "Sign in clicked",
                flush=True
            )

        except Exception as e:

            print(
                "Normal click failed:",
                repr(e),
                flush=True
            )

            driver.execute_script(
                "arguments[0].click();",
                sign_in
            )

            print(
                "JavaScript click completed",
                flush=True
            )

        # -----------------------------
        # Result
        # -----------------------------

        import time

        time.sleep(3)

        try:
            current_url = driver.current_url
        except Exception:
            current_url = "unknown"

        try:
            title = driver.title
        except Exception:
            title = "unknown"

        print(
            "Final URL:",
            current_url,
            flush=True
        )

        print(
            "Final title:",
            title,
            flush=True
        )

        return jsonify({
            "success": True,
            "message": "Login request submitted",
            "current_url": current_url,
            "title": title
        })

    except Exception as e:

        print(
            "=== ERROR ===",
            flush=True
        )

        print(
            repr(e),
            flush=True
        )

        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": repr(e)
        }), 500

    finally:

        if driver is not None:

            try:
                driver.quit()

                print(
                    "Chrome closed",
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
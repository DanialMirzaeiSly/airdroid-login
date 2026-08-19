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

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-features=Translate,BackForwardCache")
        options.add_argument("--window-size=1280,900")

        print("Starting Chrome...", flush=True)

        driver = webdriver.Chrome(
            options=options
        )

        print("Chrome started successfully", flush=True)

        wait = WebDriverWait(
            driver,
            30
        )

        print("Opening AirDroid...", flush=True)

        driver.get(URL)

        print(
            "Page loaded:",
            driver.current_url,
            flush=True
        )

        print(
            "Title:",
            driver.title,
            flush=True
        )

        # -----------------------------
        # Email
        # -----------------------------

        print(
            "Waiting for email...",
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
            "Email found",
            flush=True
        )

        email.clear()
        email.send_keys(EMAIL)

        # -----------------------------
        # Password
        # -----------------------------

        print(
            "Waiting for password...",
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
            "Password found",
            flush=True
        )

        password.clear()
        password.send_keys(PASSWORD)

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

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            sign_in
        )

        # اول کلیک عادی
        try:

            sign_in.click()

            print(
                "Sign in clicked",
                flush=True
            )

        except Exception as click_error:

            print(
                "Normal click failed:",
                repr(click_error),
                flush=True
            )

            # اگر کلیک عادی نشد، JS
            driver.execute_script(
                "arguments[0].click();",
                sign_in
            )

            print(
                "Sign in clicked with JavaScript",
                flush=True
            )

        # -----------------------------
        # Wait after login
        # -----------------------------

        try:

            WebDriverWait(
                driver,
                10
            ).until(
                lambda d: d.current_url != URL
            )

        except Exception:

            pass

        print(
            "Final URL:",
            driver.current_url,
            flush=True
        )

        print(
            "Final title:",
            driver.title,
            flush=True
        )

        return jsonify({
            "success": True,
            "message": "Login request submitted",
            "current_url": driver.current_url,
            "title": driver.title
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
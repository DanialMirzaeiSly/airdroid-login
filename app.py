from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import traceback


app = Flask(__name__)

URL = "https://www.airdroid.com/user-center/signin/?redirect=%2F"

EMAIL = "mobility_hy@telegmail.com"
PASSWORD = "Danial*#*&*Mirzaei??23"

# ذخیره Session / Cookie برای Auto Login
CHROME_PROFILE = os.path.abspath("./chrome_profile")


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

        # حفظ Cookie و Session
        options.add_argument(
            f"--user-data-dir={CHROME_PROFILE}"
        )

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,900")

        driver = webdriver.Chrome(options=options)

        print("Chrome started", flush=True)

        wait = WebDriverWait(driver, 25)

        driver.get(URL)

        print("URL:", driver.current_url, flush=True)
        print("Title:", driver.title, flush=True)

        time.sleep(3)

        # ============================
        # بررسی Session قبلی
        # ============================

        if "/user-center/signin" not in driver.current_url:

            print(
                "Already logged in.",
                flush=True
            )

        else:

            print(
                "Login required.",
                flush=True
            )

            # ============================
            # Email
            # ============================

            email = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "input.widget-login-account-input"
                    )
                )
            )

            email.clear()
            email.send_keys(EMAIL)

            print("Email entered", flush=True)

            # ============================
            # Password
            # ============================

            password = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "input.widget-login-pwd-input"
                    )
                )
            )

            password.clear()
            password.send_keys(PASSWORD)

            print("Password entered", flush=True)

            # ============================
            # Stay signed in
            # ============================

            try:

                keep_signed = driver.find_element(
                    By.CSS_SELECTOR,
                    ".widget-login-keep-checkbox"
                )

                aria_checked = keep_signed.get_attribute(
                    "aria-checked"
                )

                check_value = keep_signed.get_attribute(
                    "check"
                )

                print(
                    "Stay signed in:",
                    aria_checked,
                    check_value,
                    flush=True
                )

                if (
                    aria_checked != "true"
                    and check_value != "1"
                ):

                    driver.execute_script(
                        "arguments[0].click();",
                        keep_signed
                    )

            except Exception as e:

                print(
                    "Stay signed in check failed:",
                    str(e),
                    flush=True
                )

            # ============================
            # Sign In
            # ============================

            sign_in = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button.widget-login-btn[cmd='internetLogin']"
                    )
                )
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                sign_in
            )

            time.sleep(0.5)

            driver.execute_script(
                "arguments[0].click();",
                sign_in
            )

            print(
                "Sign in clicked",
                flush=True
            )

            # منتظر Login
            time.sleep(10)

        # ============================
        # نتیجه
        # ============================

        current_url = driver.current_url
        title = driver.title

        print(
            "Current URL:",
            current_url,
            flush=True
        )

        print(
            "Title:",
            title,
            flush=True
        )

        try:

            page_text = driver.find_element(
                By.TAG_NAME,
                "body"
            ).text

        except Exception:

            page_text = ""

        print(
            "PAGE TEXT:",
            page_text[:3000],
            flush=True
        )

        # ============================
        # بررسی Login
        # ============================

        if "/user-center/signin" in current_url:

            error_text = ""

            try:

                message = driver.find_element(
                    By.CSS_SELECTOR,
                    ".widget-login-message"
                )

                error_text = message.text

            except Exception:
                pass

            return jsonify({
                "success": False,
                "logged_in": False,
                "current_url": current_url,
                "title": title,
                "error": error_text,
                "page_text": page_text[:3000]
            }), 401

        # ============================
        # Login موفق
        # ============================

        return jsonify({
            "success": True,
            "logged_in": True,
            "current_url": current_url,
            "title": title,
            "page_text": page_text[:3000]
        })

    except TimeoutException as e:

        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": "Timeout",
            "details": str(e)
        }), 500

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        if driver:
            driver.quit()

        print(
            "=== /run finished ===",
            flush=True
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
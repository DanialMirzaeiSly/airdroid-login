from flask import Flask, jsonify
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback


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
        options.add_argument("--window-size=1280,900")

        print("Starting Chrome...", flush=True)

        driver = webdriver.Chrome(options=options)

        print("Chrome started successfully", flush=True)

        wait = WebDriverWait(driver, 20)

        print("Opening AirDroid...", flush=True)
        driver.get(URL)

        print("Page title:", driver.title, flush=True)

        email = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[type="email"]')
            )
        )
        email.send_keys(EMAIL)

        password = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[type="password"]')
            )
        )
        password.send_keys(PASSWORD)

        # حذف Cookie overlay
        try:
            cookie = driver.find_element(By.ID, "mode-cookie-tip")
            driver.execute_script(
                "arguments[0].remove();",
                cookie
            )
        except Exception:
            pass

        sign_in = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(translate(., "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                    "'abcdefghijklmnopqrstuvwxyz'), 'sign in')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            sign_in
        )

        driver.execute_script(
            "arguments[0].click();",
            sign_in
        )

        print("Page request sent", flush=True)

        # فرصت برای پردازش Login و Redirect
        time.sleep(10)

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

        # متن قابل مشاهده صفحه
        page_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        print(
            "PAGE TEXT:",
            page_text[:3000],
            flush=True
        )

        login_confirmed = "/user-center/signin" not in driver.current_url

        return jsonify({
            "success": login_confirmed,
            "current_url": driver.current_url,
            "title": driver.title,
            "page_text": page_text[:3000]
        })

    except Exception as e:

        print("=== ERROR ===", flush=True)
        print(str(e), flush=True)
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        if driver:
            driver.quit()

        print("=== /run finished ===", flush=True)

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
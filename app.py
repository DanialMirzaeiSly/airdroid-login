from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")

        print("Starting Chrome...", flush=True)

        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, 20)

        print("Opening AirDroid...", flush=True)
        driver.get(URL)

        print("Page title:", driver.title, flush=True)

        email = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[type="email"]')
            )
        )

        print("Email field found", flush=True)
        email.send_keys(EMAIL)

        password = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[type="password"]')
            )
        )

        print("Password field found", flush=True)
        password.send_keys(PASSWORD)

        # حذف Cookie overlay
        try:
            cookie = driver.find_element(By.ID, "mode-cookie-tip")

            driver.execute_script(
                "arguments[0].remove();",
                cookie
            )

            print("Cookie overlay removed", flush=True)

        except Exception:
            print("Cookie overlay not found", flush=True)

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

        print("Sign in button found", flush=True)

        driver.execute_script(
            "arguments[0].click();",
            sign_in
        )

        print("Sign in clicked", flush=True)

        return jsonify({
            "success": True,
            "message": "Login request submitted"
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
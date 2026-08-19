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

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 20)

        driver.get(URL)

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

        # حذف پنجره Cookie در صورت وجود
        try:
            cookie = driver.find_element(By.ID, "mode-cookie-tip")
            driver.execute_script(
                "arguments[0].remove();",
                cookie
            )
        except Exception:
            pass

        # پیدا کردن دکمه Sign in
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

        # کلیک با JavaScript برای جلوگیری از click intercepted
        driver.execute_script(
            "arguments[0].click();",
            sign_in
        )

        return jsonify({
            "success": True,
            "message": "Login request submitted"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        driver.quit()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
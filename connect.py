from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.airdroid.com/user-center/signin/?redirect=%2F"

EMAIL = "mobility_hy@telegmail.com"
PASSWORD = "Danial*#*&*Mirzaei??23"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
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

    sign_in = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Sign in') or contains(., 'Sign In')]")
        )
    )
    sign_in.click()

    print("ورود ارسال شد.")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
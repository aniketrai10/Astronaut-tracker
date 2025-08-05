from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---- Tumhare login credentials ----
USERNAME = "8787081154"
PASSWORD = "aniket10"
LOGIN_URL = "https://1wayez.life/"
GAME_URL = "https://1wayez.life/casino/play/v_100hp:Astronaut?sub1=9UzvI6q0P3"

# ---- Chrome Options ----
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ---- Browser start ----
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(LOGIN_URL)
time.sleep(3)

# ---- Login ----
try:
    phone_input = driver.find_element(By.NAME, "phone")
    phone_input.send_keys(USERNAME)
    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(PASSWORD)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    print("[INFO] Logged in successfully!")
except Exception as e:
    print("[ERROR] Login failed:", e)

time.sleep(5)

# ---- Open Astronaut Game ----
driver.get(GAME_URL)
print("[INFO] Astronaut game opened.")
time.sleep(10)

# ---- Infinite loop to track crash values ----
print("[INFO] Tracking crash values...")

while True:
    try:
        # NOTE: Is selector ko change karna padega jo crash value show karta hai
        crash_value = driver.find_element(By.CSS_SELECTOR, ".crash-value").text
        print(f"[DATA] Crash Value: {crash_value}")
    except:
        print("[WARN] Couldn't fetch crash value this time.")
    time.sleep(2)

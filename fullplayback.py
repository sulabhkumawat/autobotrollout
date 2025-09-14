import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up undetected Chrome in incognito
options = uc.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

try:
    # 1. Open YouTube
    driver.get("https://www.youtube.com")
    time.sleep(3)

    # 2. Search for xqc
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_box.send_keys("xqc", Keys.RETURN)
    time.sleep(3)

    # 3. Click @xQcOW channel
    channels = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ytd-channel-renderer//a[@href]')))
    for ch in channels:
        if "/@xQcOW" in ch.get_attribute("href"):
            ch.click()
            break
    else:
        print("❌ Channel not found.")
        driver.quit()
        exit()

    time.sleep(4)

    # 4. Go to videos tab
    current_url = driver.current_url
    driver.get(current_url.rstrip("/") + "/videos")
    time.sleep(4)

    # 5. Click latest video
    latest_video = wait.until(
        EC.element_to_be_clickable((By.XPATH, '(//ytd-rich-grid-media//a[@id="thumbnail"])[1]'))
    )
    latest_video.click()
    print("▶️ Video clicked")
    time.sleep(6)

    # 6. Wait for video element to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video.html5-main-video")))
    print("🎥 Video element loaded")

    # Simulate mouse movement to mimic user
    video_player = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player")))
    actions.move_to_element(video_player).perform()
    time.sleep(2)

    # 7. Fullscreen (after video has played a bit)
    actions.send_keys('f').perform()
    print("🖥️ Entered fullscreen mode")
    time.sleep(2)

    # 8. Open settings and set 1080p
    try:
        settings_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-settings-button')
        settings_button.click()
        time.sleep(1)

        quality_option = driver.find_element(By.XPATH, '//div[contains(@class,"ytp-menuitem-label") and text()="Quality"]')
        quality_option.click()
        time.sleep(1)

        quality_1080p = driver.find_element(By.XPATH, '//span[contains(text(),"1080")]')
        quality_1080p.click()
        print("📺 Set to 1080p")
    except Exception as e:
        print("⚠️ Could not set quality:", e)

    # ✅ Keep browser open
    print("✅ Video playing. Press ENTER to quit.")
    input()
    driver.quit()

except Exception as e:
    print(f"❌ Error: {e}")
    driver.quit()

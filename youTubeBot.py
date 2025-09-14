import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Set ChromeDriver path
os.environ['PATH'] += r";C:/selenium driver"

# Set Chrome options
options = Options()
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep browser open

# Launch driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Open YouTube
    driver.get("https://www.youtube.com")
    print("🌐 YouTube opened")
    time.sleep(2)

    # Step 2: Search for "xqc"
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_box.send_keys("xqc")
    search_box.send_keys(Keys.RETURN)
    print("🔍 Searched for 'xqc'")
    time.sleep(2)

    # Step 3: Click @xQcOW channel
    channels = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ytd-channel-renderer//a[@href]')))
    channel_found = False
    for ch in channels:
        href = ch.get_attribute("href")
        if "/@xQcOW" in href:
            ch.click()
            print("📺 Clicked on @xQcOW channel")
            channel_found = True
            break

    if not channel_found:
        print("❌ Could not find xQc's official channel.")
        exit()

    time.sleep(3)

    # Step 4: Navigate directly to Videos tab
    current_url = driver.current_url
    if "/@xQcOW" in current_url:
        videos_url = current_url.rstrip("/") + "/videos"
        driver.get(videos_url)
        print("🎞️ Navigated directly to Videos tab")
        time.sleep(3)
    else:
        print("❌ Not on expected channel page")
        exit()

    # Step 5: Click the latest video
    latest_video = wait.until(
        EC.element_to_be_clickable((By.XPATH, '(//ytd-rich-grid-media//a[@id="thumbnail"])[1]'))
    )
    latest_video.click()
    print("▶️ Playing the latest video!")
    time.sleep(5)

    # Step 6: Fullscreen first
    actions = ActionChains(driver)
    actions.send_keys('f').perform()
    print("🖥️ Entered fullscreen mode")
    time.sleep(2)

    # Step 7: Set video quality to 1080p
    video_player = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player")))
    actions.move_to_element(video_player).perform()
    time.sleep(1)

    try:
        # Open settings
        settings_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-settings-button')
        settings_button.click()
        print("⚙️ Opened settings menu")
        time.sleep(1)

        # Click on "Quality"
        quality_option = driver.find_element(By.XPATH, '//div[contains(@class,"ytp-menuitem-label") and text()="Quality"]')
        quality_option.click()
        print("🎚️ Clicked on Quality")
        time.sleep(1)

        # Select 1080p (might show as 1080p60 or 1080)
        quality_1080p = driver.find_element(By.XPATH, '//span[contains(text(),"1080")]')
        quality_1080p.click()
        print("📺 Set video quality to 1080p")
    except Exception as e:
        print("⚠️ Could not set video quality:", e)

except Exception as e:
    print(f"❌ An error occurred: {e}")

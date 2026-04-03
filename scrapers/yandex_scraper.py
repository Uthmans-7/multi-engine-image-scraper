import os
import time
import random
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# ==========================================
#  USER CONFIGURATION 
# ==========================================
TARGET_LIST_FILE = "targets.txt"       # Text file containing your targets (Format: "Search Query, Folder_Name")
MASTER_OUTPUT_DIR = "dataset"          # The main folder where images will be saved
MAX_IMAGES_PER_CLASS = 150             # The target number of images to download per class
MIN_COOLDOWN = 15                      # Minimum seconds to wait between targets
MAX_COOLDOWN = 25                      # Maximum seconds to wait between targets
# ==========================================

def setup_stealth_browser():
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options) 
    return driver

def human_scroll(driver, scrolls=20):
    print("Executing DEEP human-like scrolling on Yandex...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5)) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollBy(0, -600);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break 
        last_height = new_height

def download_yandex_images(driver, search_query, folder_name, max_images):
    folder_path = os.path.join(MASTER_OUTPUT_DIR, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        existing_files = len([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if existing_files >= max_images:
            print(f" Skipping {folder_name} (Already has {existing_files} images, target met!)")
            return True

    print(f"\n--- Target: {search_query} ---")
    
    search_url = f"https://yandex.com/images/search?text={search_query.replace(' ', '%20')}"
    driver.get(search_url)
    
    # ==========================================
    #  THE SMART CAPTCHA DETECTOR
    # ==========================================
    time.sleep(3) # Give it 3 seconds to initially load
    
    # Check if Yandex redirected us to a Captcha page
    if "captcha" in driver.current_url.lower() or "smartcaptcha" in driver.page_source.lower():
        print("\n YANDEX CAPTCHA DETECTED! ")
        print(" Script paused. You have 60 SECONDS to solve the CAPTCHA in the browser...")
        
        # 60 Second Countdown Loop
        for i in range(60, 0, -1):
            if "captcha" not in driver.current_url.lower():
                print("\n CAPTCHA SOLVED! Resuming the mission...")
                time.sleep(2) 
                break
            time.sleep(1)
            if i % 10 == 0:
                print(f" {i} seconds remaining...")
                
        if "captcha" in driver.current_url.lower():
            print(" CAPTCHA timeout. Moving to the next target...")
            return False
    else:
        print("Page loaded safely. No CAPTCHA detected.")
        time.sleep(random.uniform(2.0, 4.0))
    # ==========================================

    human_scroll(driver, scrolls=20)

    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = []
    
    for img in images:
        src = img.get_attribute('src') or img.get_attribute('data-src')
        if src and "http" in src and "base64" not in src:
            image_urls.append(src)
            if len(image_urls) >= max_images:
                break

    if len(image_urls) < 10:
        print(f" WARNING: Yandex didn't load enough images for '{search_query}'. Folder might be empty.")
        return False

    print(f"Found {len(image_urls)} valid Yandex targets. Extracting...")
    count = 0
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    for url in image_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                if len(response.content) > 3000: 
                    file_name = f"img_{count}.jpg"
                    file_path = os.path.join(folder_path, file_name)
                    
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    count += 1
        except Exception:
            continue 
            
    print(f" Secured {count} high-res images for {folder_name}.")
    return True 

def main():
    print("="*50)
    print("  MULTI-ENGINE IMAGE SCRAPER: YANDEX MODULE")
    print("="*50)

    if not os.path.exists(TARGET_LIST_FILE):
        print(f" ERROR: Could not find '{TARGET_LIST_FILE}'!")
        print(f"Please create a '{TARGET_LIST_FILE}' file with the format: Search Query, Folder_Name")
        return

    # Read targets
    with open(TARGET_LIST_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

    targets = []
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 2:
            targets.append((parts[0].strip(), parts[1].strip()))
        else:
            # Fallback if the user just provides a single word instead of a comma-separated list
            targets.append((parts[0].strip(), parts[0].strip().replace(" ", "_")))

    print(f" Loaded {len(targets)} targets from {TARGET_LIST_FILE}.")

    for query, folder_name in targets:
        driver = setup_stealth_browser()
        try:
            success = download_yandex_images(driver, query, folder_name, MAX_IMAGES_PER_CLASS)
        except Exception as e:
            print(f"Error on {query}: {e}")
            success = False
        finally:
            driver.quit() 
        
        if success:
            cooldown = random.randint(MIN_COOLDOWN, MAX_COOLDOWN)
            print(f"💤 Resting for {cooldown} seconds to avoid rate limits...\n")
            time.sleep(cooldown)

    print("\n YANDEX SCRAPING RUN COMPLETE! Images stored safely.")

if __name__ == "__main__":
    main()
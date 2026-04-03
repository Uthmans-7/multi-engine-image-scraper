import os
import sys
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
MAX_COOLDOWN = 30                      # Maximum seconds to wait between targets
MAX_STRIKES = 2                        # Consecutive failures before triggering the Kill Switch
# ==========================================

def setup_stealth_browser():
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Note: version_main removed to ensure universal compatibility across different user machines
    driver = uc.Chrome(options=options) 
    return driver

def human_scroll(driver, scrolls=15):
    print("Executing DEEP human-like scrolling to force lazy-loading...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.5)) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollBy(0, -400);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break 
        last_height = new_height

def download_google_images(driver, search_query, folder_name, max_images):
    folder_path = os.path.join(MASTER_OUTPUT_DIR, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        existing_files = len([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if existing_files >= max_images:
            print(f" Skipping {folder_name} (Already has {existing_files} images, target met!)")
            return "SKIPPED"

    print(f"\n--- Target: {search_query} ---")
    
    formatted_query = search_query.replace(' ', '+')
    search_url = f"https://www.google.com/search?tbm=isch&q={formatted_query}"
    
    driver.get(search_url)
    time.sleep(random.uniform(4.0, 6.0)) 

    human_scroll(driver, scrolls=15)

    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = []
    
    for img in images:
        src = img.get_attribute('src') or img.get_attribute('data-src')
        if src and "http" in src and "base64" not in src:
            image_urls.append(src)
            if len(image_urls) >= max_images:
                break

    if len(image_urls) < 10:
        print(f" WARNING: Google blocked or didn't load results for '{search_query}'!")
        return 0 # Trigger strike counter

    print(f"Found {len(image_urls)} valid Google targets. Extracting...")
    count = 0
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    for url in image_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                if len(response.content) > 3000: 
                    file_path = os.path.join(folder_path, f"img_google_{count}.jpg")
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    count += 1
        except Exception:
            continue 
            
    print(f" Secured {count} images for {folder_name}.")
    return count 

def main():
    print("="*50)
    print("  MULTI-ENGINE IMAGE SCRAPER: GOOGLE MODULE")
    print("="*50)

    if not os.path.exists(TARGET_LIST_FILE):
        print(f" ERROR: Could not find '{TARGET_LIST_FILE}'!")
        print(f"Please create a '{TARGET_LIST_FILE}' file with the format: Search Query, Folder_Name")
        return

    with open(TARGET_LIST_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

    targets = []
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 2:
            targets.append((parts[0].strip(), parts[1].strip()))
        else:
            targets.append((parts[0].strip(), parts[0].strip().replace(" ", "_")))

    print(f" Loaded {len(targets)} targets from {TARGET_LIST_FILE}.")

    # THE DOUBLE-STRIKE TRACKER (Anti-Ban Protocol)
    consecutive_fails = 0

    for query, folder_name in targets:
        driver = setup_stealth_browser()
        try:
            result = download_google_images(driver, query, folder_name, MAX_IMAGES_PER_CLASS)
            
            if result == "SKIPPED":
                pass 
            elif result == 0 or result < 10:
                consecutive_fails += 1
                print(f" STRIKE {consecutive_fails}! Google blocked this download.")
            else:
                consecutive_fails = 0 # Reset counter on success!
                
        except Exception as e:
            print(f"Error on {query}: {e}")
            consecutive_fails += 1
        finally:
            driver.quit() 
            
        # THE KILL SWITCH
        if consecutive_fails >= MAX_STRIKES:
            print("\n FATAL ERROR: Google Anti-Bot Tripwire Triggered! 🚨🚨")
            print(" PROGRAM KILLED. Switch your Wi-Fi, VPN, or Hotspot to get a new IP address before running again.")
            sys.exit(1) 
        
        if result != "SKIPPED" and consecutive_fails == 0:
            cooldown = random.randint(MIN_COOLDOWN, MAX_COOLDOWN)
            print(f"💤 Resting for {cooldown} seconds to stay under the radar...\n")
            time.sleep(cooldown)

    print(f"\n GOOGLE SCRAPING RUN COMPLETE! Images safely stored in {MASTER_OUTPUT_DIR}/.")

if __name__ == "__main__":
    main()
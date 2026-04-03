***

```markdown
# Multi-Engine Image Scraper

An advanced, stealth-oriented image extraction pipeline built for rapid Computer Vision dataset curation. 

This repository provides automated scraping modules targeting Google, Yandex, Bing, and Yahoo. It is engineered to bypass standard bot-detection mechanisms, handle dynamic lazy-loading, and safely extract high-resolution image datasets without triggering permanent IP blacklists.

## Core Architecture & Engine Mechanics

Unlike standard scraping scripts that rely on simple HTML parsing, this pipeline utilizes `undetected-chromedriver` to mask automation flags and simulates complex human behavior to extract data from heavily fortified search engines.

### How the Google Scraper Works
Google Images utilizes complex JavaScript to hide high-resolution image URLs until a user physically interacts with the DOM. 
* **Deep Human-Scrolling:** The script executes a custom "bounce" scroll technique (scrolling down, slightly up, and back down). This tricks Google's lazy-loading algorithms into revealing deep search results that are usually hidden from standard bots.
* **Thumbnail Filtering:** The scraper actively filters out Base64 encoded thumbnails, ensuring only direct HTTP/HTTPS links to high-resolution images are processed and downloaded.
* **The Double-Strike Tripwire:** Google actively shadowbans IPs that send too many automated requests. This script tracks consecutive failures (e.g., if Google returns 0 images for a target). If it fails twice in a row, the script triggers a fatal exit, stopping the program entirely to protect the host machine's IP address from permanent blacklisting.

### How the Yandex Scraper Works
Yandex provides highly accurate image results but employs aggressive CAPTCHA walls to block automated extraction.
* **Dynamic CAPTCHA Detection:** The script constantly monitors the browser's current URL and page source. If it detects a redirect to a SmartCaptcha page, it does not crash.
* **Interactive Pause:** Upon detecting a CAPTCHA, the script pauses execution and initiates a 60-second terminal countdown. This gives the operator time to manually solve the visual CAPTCHA in the automated browser window.
* **Auto-Resumption:** Once the operator solves the CAPTCHA and the URL reverts to the standard search results, the script automatically detects the state change and resumes the download queue without losing data.

## Prerequisites & Installation

Ensure you have Python 3.8 or higher installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the root directory of the project.
3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage Guide

The pipeline is designed to be fully modular. You control all four scraping engines from a single configuration file.

### 1. Configure the Target List
In the root directory, create a file named `targets.txt`. Add your search queries and your desired output folder names, separated by a comma. 

Format: `[Search Query], [Output Folder Name]`

Example `targets.txt`:
```text
Gateway of India, Gateway_of_India
Statue of Liberty, Statue_of_Liberty
Eiffel Tower landmark, Eiffel_Tower
```

### 2. Execute the Scraper
Run the desired scraping module from your terminal. The script will automatically read `targets.txt`, generate a `dataset/` directory, and begin downloading images into their respective folders.

```bash
python scrapers/google_scraper.py
```
or
```bash
python scrapers/yandex_scraper.py
```

### 3. Smart Resumption (Interrupted Runs)
If your script crashes, your internet drops, or the kill switch is triggered, simply run the script again. The scraper features built-in state checking; it will count the existing images in each target directory and automatically skip targets that have already reached the configured maximum threshold.

## Configuration Parameters

At the top of each scraper file, you can modify the following global variables to suit your network capacity and dataset requirements:

* `MAX_IMAGES_PER_CLASS`: The total number of images to download per target (Default: 150).
* `MIN_COOLDOWN` / `MAX_COOLDOWN`: The randomized rest period (in seconds) between different search targets to prevent rate-limiting.
* `MAX_STRIKES`: The number of consecutive blocked requests allowed before the kill switch aborts the program.

## Legal Disclaimer

This repository is provided strictly for educational and research purposes. Web scraping exists in a complex legal environment. Users are solely responsible for ensuring that their data extraction activities comply with local laws and the Terms of Service of the respective search engines. The author assumes no liability for IP bans, legal action, or misuse of this software.
```

***




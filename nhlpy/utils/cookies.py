# nhlpy/utils/cookies.py
import json
import time
from pathlib import Path
import logging
from typing import Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

def get_cookie_file_path(cookie_file: str = None) -> Path:
    """
    Determine the file path for storing cookies.
    """
    if cookie_file is None:
        return Path(__file__).resolve().parent / "nhl_edge_cookies.json"
    return Path(cookie_file)

class SeleniumDriver:
    """
    Context manager for Selenium WebDriver to ensure proper cleanup.
    """
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None

    def __enter__(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

def fetch_nhl_edge_cookies(headless: bool = True) -> list:
    """
    Fetch cookies using Selenium with an explicit wait until cookies are present.
    """
    url = "https://edge.nhl.com/"
    with SeleniumDriver(headless=headless) as driver:
        driver.get(url)
        # Wait until at least one cookie is present (up to 10 seconds)
        WebDriverWait(driver, 10).until(lambda d: len(d.get_cookies()) > 0)
        cookies_list = driver.get_cookies()
        logger.debug("Fetched cookies: %s", cookies_list)
        return cookies_list

def get_nhl_edge_cookies(headless: bool = True, cookie_file: str = None) -> Dict[str, str]:
    """
    Retrieve and cache cookies for edge.nhl.com. If a valid cache exists,
    it is reused; otherwise, new cookies are fetched.
    """
    cookie_path = get_cookie_file_path(cookie_file)
    saved_cookies = None
    if cookie_path.exists():
        try:
            with open(cookie_path, "r") as f:
                saved_cookies = json.load(f)
        except Exception as e:
            logger.error("Error loading cookie file: %s", e)
            saved_cookies = None

        if saved_cookies and isinstance(saved_cookies, list) and len(saved_cookies) > 0:
            now = time.time()
            expired = False
            for cookie in saved_cookies:
                if "expiry" in cookie and cookie["expiry"] <= now:
                    expired = True
                    logger.info("Cookie '%s' expired (expiry=%s, now=%s).",
                                cookie.get("name"), cookie["expiry"], now)
                    break

            if not expired:
                cookie_dict = {cookie["name"]: cookie["value"] for cookie in saved_cookies}
                logger.info("Using cached cookies from '%s'.", cookie_path)
                return cookie_dict
            else:
                logger.info("Cached cookies are expired. Fetching new cookies...")
        else:
            logger.info("Cookie file exists but is empty or invalid. Fetching new cookies...")

    # Fetch new cookies via Selenium
    cookies_list = fetch_nhl_edge_cookies(headless=headless)
    cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies_list}
    try:
        with open(cookie_path, "w") as f:
            json.dump(cookies_list, f, indent=2)
        logger.info("Saved new cookies to '%s'.", cookie_path)
    except Exception as e:
        logger.error("Error saving cookies to file: %s", e)
    return cookie_dict
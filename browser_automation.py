"""
Browser Automation Module
Handles Selenium automation for capturing Status history screenshots
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()


class BrowserAutomation:
    def __init__(self, headless: bool = False):
        """
        Initialize browser automation

        Args:
            headless: Run browser in headless mode (no GUI)
        """
        self.headless = headless
        self.driver = None
        self.domain = os.getenv('KINTONE_DOMAIN')
        self.username = os.getenv('KINTONE_USERNAME')
        self.password = os.getenv('KINTONE_PASSWORD')

    def setup_driver(self):
        """Setup and configure Chrome driver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        try:
            # Try using ChromeDriverManager
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.os_manager import ChromeType

            service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Failed with ChromeDriverManager: {e}")
            print("Trying default Chrome driver...")
            # Fallback to system Chrome driver
            self.driver = webdriver.Chrome(options=chrome_options)

        return self.driver

    def login_to_kintone(self):
        """Login to Kintone using credentials from .env"""
        if not self.driver:
            self.setup_driver()

        login_url = f"https://{self.domain}/login"
        self.driver.get(login_url)

        try:
            # Wait for login form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")

            # Enter credentials
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Submit login form
            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(3)
            print("✓ Successfully logged in to Kintone")
            return True

        except Exception as e:
            print(f"✗ Login failed: {e}")
            return False

    def open_record_page(self, record_url: str):
        """
        Open a specific record page

        Args:
            record_url: Full URL to the record
        """
        if not self.driver:
            raise RuntimeError("Driver not initialized. Call setup_driver() first.")

        self.driver.get(record_url)
        time.sleep(2)  # Wait for page to load

    def close_error_dialogs(self):
        """
        Close any error dialogs or popups that might appear
        """
        try:
            # Try multiple selectors to find close buttons
            close_button_selectors = [
                "button.gaia-argoui-dialog-close",  # Kintone error dialog close button
                ".gaia-argoui-dialog-close",
                "button[aria-label='Close']",
                "button[title='Close']",
                ".ocean-ui-dialog-close",
                ".ocean-ui-dialog-cancel",
                "button[class*='close']",
                "button[class*='cancel']",
                "button.close",
                "[role='dialog'] button[aria-label*='lose']",
                "[role='dialog'] button[aria-label*='×']"
            ]

            for selector in close_button_selectors:
                try:
                    close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in close_buttons:
                        if button.is_displayed():
                            button.click()
                            time.sleep(0.5)
                            return True
                except:
                    continue

            return True
        except:
            return False

    def click_status_history(self):
        """
        Click the Status history button/link

        Returns:
            True if successful, False otherwise
        """
        try:
            # First, close any error dialogs
            self.close_error_dialogs()
            time.sleep(1)

            # Try multiple selectors for Status history link
            selectors = [
                "//a[normalize-space()='Status history']",
                "//a[@class='recordHeader-statusHistory-gaia']",
                "a.recordHeader-statusHistory-gaia",
                "//a[contains(text(), 'Status history')]",
                "//a[contains(text(), 'ステータス履歴')]",
                "a[href*='statusHistory']"
            ]

            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        # XPath
                        status_history_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        # CSS
                        status_history_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )

                    status_history_button.click()
                    time.sleep(2)
                    return True
                except:
                    continue

            return False

        except Exception as e:
            print(f"✗ Failed to click Status history: {e}")
            return False

    def take_screenshot(self, output_path: str):
        """
        Capture screenshot of current page

        Args:
            output_path: Path to save the screenshot
        """
        try:
            # Ensure screenshots directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Take screenshot
            self.driver.save_screenshot(output_path)
            print(f"✓ Screenshot saved: {output_path}")
            return True

        except Exception as e:
            print(f"✗ Failed to take screenshot: {e}")
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")

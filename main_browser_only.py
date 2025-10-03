"""
Main Script - Browser Only Approach
Uses Selenium to access Kintone entirely through the browser
"""

import os
import time
from dotenv import load_dotenv
from browser_automation import BrowserAutomation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


def main():
    """Main execution function"""
    print("=" * 60)
    print("Kintone Status History Screenshot Capture Bot")
    print("(Browser-Only Mode)")
    print("=" * 60)

    # Get environment variables
    domain = os.getenv('KINTONE_DOMAIN')
    app_id = os.getenv('KINTONE_APP_ID')

    if not domain or not app_id:
        print("✗ KINTONE_DOMAIN and KINTONE_APP_ID are required in .env")
        return

    # Initialize browser automation
    print("\n[1/5] Initializing browser...")
    browser = BrowserAutomation(headless=False)
    browser.setup_driver()

    # Login to Kintone
    print("\n[2/5] Logging in to Kintone...")
    if not browser.login_to_kintone():
        print("✗ Login failed. Exiting...")
        browser.close()
        return

    # Navigate to the app
    print(f"\n[3/5] Opening App ID: {app_id}...")
    app_url = f"https://{domain}/k/{app_id}/"
    browser.driver.get(app_url)
    time.sleep(3)  # Wait for app to load

    # Get all record links from the app list
    print("\n[4/5] Collecting record links...")
    try:
        # Wait for the record list to load
        WebDriverWait(browser.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "recordlist-header-gaia"))
        )

        # Find all record links
        # Kintone typically uses links with class "recordlist-title-cell-gaia" or similar
        record_links = browser.driver.find_elements(By.CSS_SELECTOR, "a.recordlist-title-cell-gaia, a[href*='/show#record=']")

        if not record_links:
            print("✗ No records found in the app")
            browser.close()
            return

        # Extract record IDs and URLs
        records = []
        for link in record_links:
            href = link.get_attribute('href')
            if href and 'record=' in href:
                record_id = href.split('record=')[1].split('&')[0]
                records.append({
                    'id': record_id,
                    'url': href
                })

        # Remove duplicates
        records = list({r['id']: r for r in records}.values())

        print(f"✓ Found {len(records)} records")

    except Exception as e:
        print(f"✗ Failed to collect records: {e}")
        browser.close()
        return

    # Process each record
    print(f"\n[5/5] Processing {len(records)} records...")
    success_count = 0
    failed_count = 0

    for idx, record in enumerate(records, 1):
        try:
            record_id = record['id']
            record_url = record['url']
            print(f"\n  [{idx}/{len(records)}] Processing Record ID: {record_id}")

            # Open record page
            browser.driver.get(record_url)
            time.sleep(2)

            # Click Status history
            if not browser.click_status_history():
                print(f"  ✗ Failed to open Status history for Record ID: {record_id}")
                failed_count += 1
                continue

            # Take screenshot
            screenshot_path = f"screenshots/record_{record_id}.png"
            if browser.take_screenshot(screenshot_path):
                print(f"  ✓ Successfully captured Record ID: {record_id}")
                success_count += 1
            else:
                print(f"  ✗ Failed to capture screenshot for Record ID: {record_id}")
                failed_count += 1

            # Small delay between records
            time.sleep(1)

        except Exception as e:
            print(f"  ✗ Error processing Record ID {record['id']}: {e}")
            failed_count += 1
            continue

    # Close browser
    print("\n[6/6] Cleaning up...")
    browser.close()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total records processed: {len(records)}")
    print(f"✓ Successful captures: {success_count}")
    print(f"✗ Failed captures: {failed_count}")
    print(f"\nScreenshots saved in: ./screenshots/")
    print("=" * 60)


if __name__ == "__main__":
    main()

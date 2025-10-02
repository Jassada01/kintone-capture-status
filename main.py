"""
Main Script - Simple Sequential Approach
Loop through record IDs sequentially starting from 1
"""

import os
import time
from dotenv import load_dotenv
from browser_automation import BrowserAutomation

load_dotenv()


def main():
    """Main execution function"""
    print("=" * 60)
    print("Kintone Status History Screenshot Capture Bot")
    print("=" * 60)

    # Get environment variables
    domain = os.getenv('KINTONE_DOMAIN')
    app_id = os.getenv('KINTONE_APP_ID')

    if not domain or not app_id:
        print("✗ KINTONE_DOMAIN and KINTONE_APP_ID are required in .env")
        return

    # Initialize browser automation
    print("\n[1/4] Initializing browser...")
    browser = BrowserAutomation(headless=False)
    browser.setup_driver()

    # Login to Kintone
    print("\n[2/4] Logging in to Kintone...")
    if not browser.login_to_kintone():
        print("✗ Login failed. Exiting...")
        browser.close()
        return

    # Process records sequentially
    print(f"\n[3/4] Processing records sequentially...")
    print("Will stop when encountering non-existent records\n")

    success_count = 0
    failed_count = 0
    not_found_count = 0
    max_consecutive_not_found = 5  # Stop after 5 consecutive not found

    record_id = 1

    while not_found_count < max_consecutive_not_found:
        try:
            print(f"  Processing Record ID: {record_id}...", end=" ")

            # Construct print URL
            record_url = f"https://{domain}/k/{app_id}/print?record={record_id}"

            # Open record page
            browser.driver.get(record_url)
            time.sleep(3)

            # Check if there are error dialogs
            try:
                error_dialogs = browser.driver.find_elements(By.CSS_SELECTOR,
                    ".ocean-ui-dialog, [class*='error'], [class*='dialog']")

                if any(dialog.is_displayed() for dialog in error_dialogs):
                    # Capture error screenshot
                    error_screenshot_path = f"screenshots/record_{record_id}_error.png"
                    browser.take_screenshot(error_screenshot_path)
                    print(f"⚠ Error detected")

                    # Close the error dialog
                    browser.close_error_dialogs()
                    failed_count += 1
                    record_id += 1
                    continue
            except:
                pass

            # Check if record exists (look for error message)
            page_source = browser.driver.page_source.lower()

            if "record not found" in page_source or "レコードが見つかりません" in page_source or "does not exist" in page_source or "error occurred" in page_source:
                print("✗ Not found")
                not_found_count += 1
                record_id += 1
                continue

            # Reset not found counter if we found a record
            not_found_count = 0

            # Scroll to bottom of page
            browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Take screenshot
            screenshot_path = f"screenshots/record_{record_id}.png"
            if browser.take_screenshot(screenshot_path):
                print(f"✓ Successfully captured")
                success_count += 1
            else:
                print("✗ Failed to capture screenshot")
                failed_count += 1

            # Move to next record
            record_id += 1
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user")
            break
        except Exception as e:
            print(f"✗ Error: {e}")
            failed_count += 1
            record_id += 1
            continue

    # Close browser
    print("\n[4/4] Cleaning up...")
    browser.close()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Last record ID checked: {record_id - 1}")
    print(f"✓ Successful captures: {success_count}")
    print(f"✗ Failed captures: {failed_count}")
    print(f"\nScreenshots saved in: ./screenshots/")
    print("=" * 60)


if __name__ == "__main__":
    main()

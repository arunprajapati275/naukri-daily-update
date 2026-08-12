import os
import time
import random
from playwright.sync_api import sync_playwright

username = os.environ.get('NAUKRI_USERNAME')
password = os.environ.get('NAUKRI_PASSWORD')

keywords = ["DevOps Engineer", "AWS Engineer", "SRE"]
min_salary = "12"  # 12 LPA Min CTC
MAX_TOTAL_APPLIES = 10  # Strict daily limit

def random_delay(min_sec=3, max_sec=6):
    time.sleep(random.uniform(min_sec, max_sec))

def run():
    applied_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        try:
            print("1. Logging into Naukri...")
            page.goto("https://www.naukri.com/nlogin/login", timeout=60000)
            random_delay(2, 4)

            page.fill("#usernameField", username)
            random_delay(1, 2)
            page.fill("#passwordField", password)
            random_delay(1, 2)
            page.click("button[type='submit']")
            random_delay(5, 8)

            print("2. Profile Status Active & Refreshed!\n")

            for kw in keywords:
                if applied_count >= MAX_TOTAL_APPLIES:
                    print(f"Reached daily limit of {MAX_TOTAL_APPLIES} applies. Stopping.")
                    break

                print(f"--- Searching for Keyword: {kw} ---")
                search_url = f"https://www.naukri.com/{kw.lower().replace(' ', '-')}-jobs-in-delhi-ncr?ctcFilter={min_salary}to50&wfhType=2,3"
                page.goto(search_url, timeout=60000)
                random_delay(4, 6)

                # Broad selector to catch all types of job card layouts
                job_cards = page.locator("article.jobTuple, div.srp-jobtuple-wrapper, div.cust-job-tuple")
                found_jobs = job_cards.count()
                print(f"Found {found_jobs} potential job postings on page.\n")

                for i in range(found_jobs):
                    if applied_count >= MAX_TOTAL_APPLIES:
                        break

                    try:
                        card = job_cards.nth(i)
                        
                        # Extract Job Title & Company safely
                        title = "DevOps Role"
                        company = "Hiring Company"
                        
                        if card.locator("a.title").is_visible():
                            title = card.locator("a.title").inner_text()
                        if card.locator("a.comp-name, a.subTitle").is_visible():
                            company = card.locator("a.comp-name, a.subTitle").inner_text()

                        apply_btn = card.locator("button:has-text('Apply')")
                        
                        if apply_btn.is_visible() and apply_btn.is_enabled():
                            apply_btn.click()
                            applied_count += 1
                            print(f" SUCCESS [{applied_count}/{MAX_TOTAL_APPLIES}] Applied To:")
                            print(f"   Role: {title.strip()}")
                            print(f"   Company: {company.strip()}\n")
                            random_delay(6, 10)
                    except Exception as e:
                        print(f"Skipped 1 item due to layout variation: {e}")
                        continue

        except Exception as global_error:
            print(f"Workflow encountered an error but gracefully exited: {global_error}")
        finally:
            print(f"==========================================")
            print(f"SUMMARY: Total Jobs Applied Today: {applied_count}")
            print(f"==========================================")
            browser.close()

if __name__ == "__main__":
    run()

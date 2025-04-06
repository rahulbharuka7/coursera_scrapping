# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
# import re
# from bs4 import BeautifulSoup

# # Replace these with your Coursera login credentials
# USERNAME = "lavanya.srivastava@skillup.online"
# # PASSWORD = "Srivas@1234"
# PASSWORD="new@1234"

# # Coursera course URL
# course_url = "https://www.coursera.org/teach/deep-neural-networks-with-pytorch/"

# # Setup ChromeDriver
# driver = webdriver.Chrome()  # Add executable_path if needed

# # 1. Go to login page
# driver.get("https://www.coursera.org/?authMode=login&versionId=authoringBranch~uO92QC2WEe-YcA77IVc2yQ")
# time.sleep(3)

# # 2. Enter email
# email_input = driver.find_element(By.NAME, "email")
# email_input.send_keys(USERNAME)

# # 3. Enter password
# password_input = driver.find_element(By.NAME, "password")
# password_input.send_keys(PASSWORD)
# password_input.send_keys(Keys.RETURN)

# # Wait for login to complete
# time.sleep(3)

# # 4. Navigate to course page
# driver.get(course_url)
# time.sleep(3)

# # 5. Parse page source with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, "html.parser")
# text_content = soup.get_text()

# # 6. Extract rating and reviews using regex
# rating_pattern = r"(\d+\.\d+)\s*\(([\d,]+)\s*reviews\)"
# matches = re.findall(rating_pattern, text_content)

# if matches:
#     course_rating, review_count = matches[0]
#     print(f"Course Rating: {course_rating} ({review_count} reviews)")
# else:
#     print("No rating found.")

# # Close the browser
# driver.quit()


import re
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

COURSE_URL =  "https://www.coursera.org/learn/generative-ai-advanced-fine-tuning-for-llms"
STORAGE_STATE = "coursera_login.json"

async def login_and_save_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Open login page
        page = await context.new_page()
        await page.goto("https://www.coursera.org/?authMode=login")

        print("⏳ Please log in manually and solve CAPTCHA...")
        await page.wait_for_timeout(100000)  # 40 seconds to manually login

        # Save session state to file
        await context.storage_state(path=STORAGE_STATE)
        print("✅ Session saved!")

        await browser.close()

# async def scrape_course():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context(storage_state=STORAGE_STATE)
#         page = await context.new_page()

#         print("✅ Visiting course page...")
#         await page.goto(COURSE_URL)
#         await page.wait_for_load_state('networkidle')
#         await page.wait_for_timeout(5000)

#         html = await page.content()
#         soup = BeautifulSoup(html, "html.parser")
#         text = soup.get_text()

#         # Debug: check if rating exists in text
#         # print("🔎 Page preview:\n", text[:3000])

#         rating_pattern = r"(\d\.\d)\s*(?:stars)?\s*\(?([\d,]+)\s*(?:ratings|reviews)?\)?"
#         matches = re.findall(rating_pattern, text, re.IGNORECASE)

#         if matches:
#             rating, reviews = matches[0]
#             print(f"🌟 Course Rating: {rating} ({reviews} reviews)")
#         else:
#             print("⚠️ Rating not found.")

#         await browser.close()
async def scrape_course():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True after debug
        context = await browser.new_context(storage_state=STORAGE_STATE)
        page = await context.new_page()

        print("🔗 Navigating to course...")
        await page.goto(COURSE_URL)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)  # wait for JS content

        # Try to find rating element
        rating_selector = '#reviews > div > div > div > div > div > div.cds-9.css-0.cds-10.cds-11.cds-grid-item.cds-13.cds-76 > div.cds-9.css-1lz4ijf > span > span'
        # review_selector = 'span:has-text("reviews")'

        try:
            rating = await page.locator(rating_selector).first.text_content()
            # reviews = await page.locator(review_selector).first.text_content()
            print(f"🌟 Rating: {rating} ")
        except Exception as e:
            print("⚠️ Could not find rating/reviews. Error:", e)

        await browser.close()
# First time: login and save session
# asyncio.run(login_and_save_session())

# After login is saved: scrape course info
asyncio.run(login_and_save_session())
asyncio.run(scrape_course())

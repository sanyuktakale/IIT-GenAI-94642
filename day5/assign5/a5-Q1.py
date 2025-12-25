# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def sunbeam_internship_scraping(url):

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mode
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    print("Page Title:", driver.title)

    wait = WebDriverWait(driver, 20)

    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    
    panels_to_click = ["#collapseOne", "#collapseTwo", "#collapseSix"]
    for panel in panels_to_click:
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='{panel}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            time.sleep(2)  # wait for JS content to load
        except:
            print(f"Panel {panel} not found or empty!")

   
    print("\n=== Internship Programs ===\n")
    program_panels = ["#collapseOne", "#collapseTwo"]
    programs_found = False

    for panel in program_panels:
        try:
            prog_panel = driver.find_element(By.CSS_SELECTOR, f"{panel} .panel-body")
            text = prog_panel.text.strip()
            if text:
                programs_found = True
                for i, line in enumerate(text.split('\n'), start=1):
                    print(f"{i}. {line}")
                break  # stop after first panel with content
        except:
            continue

    if not programs_found:
        print("No program details found.")

    
    print("\n=== Internship Batches ===\n")
    try:
        batch_table = driver.find_element(By.CSS_SELECTOR, "#collapseSix table")
        rows = batch_table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header
        if rows:
            headers = [th.text for th in batch_table.find_elements(By.TAG_NAME, "th")]
            # Print header row
            print(" | ".join(headers))
            print("-" * 120)
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                print(" | ".join([c.text.strip() for c in cols]))
        else:
            print("No batch information available on the website.")
    except:
        print("No batch information available on the website.")

    driver.quit()


if __name__ == "__main__":
    url = "https://www.sunbeaminfo.in/internship"
    sunbeam_internship_scraping(url)

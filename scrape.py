import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

# Function to scrape the website
def scrape_website(website):
    print("Launching chrome browser...")

    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page Loading...")
        time.sleep(10)  # Waiting for page to load completely
        html = driver.page_source
        return html
    finally:
        driver.quit()

# Function to extract body content using BeautifulSoup
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

# Function to clean body content, removing script and style tags
def cleaned_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Removing script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Getting cleaned text
    cleaned_content = soup.get_text(separator="\n")
    
    # Stripping each line and joining non-empty lines
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

# Function to split large DOM content into smaller chunks
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)
    ]

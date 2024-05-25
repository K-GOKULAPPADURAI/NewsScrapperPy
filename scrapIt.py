import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver without headless mode
driver = webdriver.Chrome()


def scrape_website(url):
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Extract all text from the webpage
        text = soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    # Path to the text file containing URLs
    input_file = 'website-urls.txt'
    
    # Directory to save the scraped text files
    output_dir = 'scraped_content'
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as f:
        for line in f:
            try:
                name, url = line.split(': ')
                url = url.strip()
                name = name.strip().replace('.', '').replace(' ', '_')
                print(f"Scraping {name}: {url}")
                text = scrape_website(url)
                if text:
                    filename = os.path.join(output_dir, f"{name}.txt")
                    save_text_to_file(text, filename)
                    print(f"Saved content from {url} to {filename}")
            except ValueError:
                print(f"Skipping invalid line: {line}")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()

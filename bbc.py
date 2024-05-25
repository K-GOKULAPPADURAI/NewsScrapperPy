import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver without headless mode
driver = webdriver.Chrome()

def get_user_choice():
    categories = ['Sports', 'Business', 'Travel', 'Innovation', 'Culture']
    print("Please select a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    choice = int(input("Enter the number of your choice: "))
    return categories[choice - 1].lower()

def scrape_website(url, category):
    print(url[:20])
    try:
        driver.get(f"{url[:19]}/{category}")
        time.sleep(5)  # Wait for the page to load
        
        # Find all hyperlink elements you want to click on (e.g., by class name, tag name, etc.)
        links = driver.find_elements(By.TAG_NAME, 'a')  # Adjust as needed
        for link in links:
            href = link.get_attribute('href')
            print(href)
            if href and href.startswith(url):  # Ensure the link is within the same website
                print(f"Navigating to {href}")
                driver.get(href)
                time.sleep(5)  # Wait for the page to load
                
                # Scrape the title and paragraph content
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find('title').get_text(strip=True)
                paragraphs = soup.find_all('p')
                paragraph_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
                
                # Save the content to a file
                filename = os.path.join('scraped_content', f"{title[:50]}.txt")  # Limiting the file name length
                save_text_to_file(f"{title}\n\n{paragraph_text}", filename)
                print(f"Saved content from {href} to {filename}")

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    # Get user choice for category
    category = get_user_choice()
    
    # Path to the text file containing URLs
    input_file = 'websites.txt'
    
    # Directory to save the scraped text files
    output_dir = 'scraped_content'
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as f:
        for line in f:
            try:
                name, url = line.split(': ')
                url = url.strip()
                name = name.strip().replace('.', '').replace(' ', '_')
                print(f"Scraping {name} in category {category}: {url}")
                scrape_website(url, category)
            except ValueError:
                print(f"Skipping invalid line: {line}")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()

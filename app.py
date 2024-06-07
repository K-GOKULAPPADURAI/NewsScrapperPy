import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import requests
import json
import os
import time

# Web scraping function
def scrape_news(category):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    url = f'https://www.bbc.com/{category}'
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    global news
    news=[]
    try:
        for link in links:
            if 'articles' in link.get_attribute('href'):
                if link.get_attribute('href')!='':
                    news.append(link.get_attribute('href'))
            if len(news)==5:
                break
    except:
        pass
    random_article = random.choice(news)
    driver.get(random_article)
    title = driver.title
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    content = ''
    for para in paragraphs:
        text = para.text.replace("BBC", "")
        if '©' in text: 
            text = text[:text.find('©')]
        else:
            text = text[:text.find('Copyright')]
        content += text
    driver.quit()
    return title, content

# Summarization function using Gemini-based API
def get_summary(content):
    url = "https://newsscrapperpy-api.onrender.com/convo"  # URL of the API server

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'input_question': "summaries this to a small para"+content
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json().get('response')
    else:
        return f"Error: {response.json().get('error')}"
try:
    # Streamlit interface
    st.title("NewsScraper")
    st.header("Select a news category to scrape and summarize an article")

    categories = ['Sports','Business', 'Travel', 'Innovation', 'Culture']
    category = st.selectbox("Please select a category:", categories)

    if st.button("Get Summary"):
        with st.spinner("Processing..."):
            title, content = scrape_news(category.lower())
            summary = get_summary(content)
            time.sleep(5)  # Simulate processing time
        st.success("Summary generated!")
        st.subheader(f"Title: {title}")
        st.write(summary)
except Exception as e:
    st.error("Oops! Server is busy with a joke. Please try again later. 🤖😄")
    st.error(e)

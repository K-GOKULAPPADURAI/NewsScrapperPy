import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from transformers import BartTokenizer, TFBartForConditionalGeneration
import os
import time

# Set environment variable for TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize the model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = TFBartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    return tokenizer, model

tokenizer, model = load_model()

# Summarization function
def summarize(text, max_length=250, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True):
    inputs = tokenizer([text], max_length=1024, return_tensors='tf', truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'], 
        max_length=max_length, 
        min_length=min_length, 
        length_penalty=length_penalty, 
        num_beams=num_beams, 
        early_stopping=early_stopping
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Web scraping function
def scrape_news(category):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome()  # Ensure the Chrome WebDriver is installed and in PATH
    url = f'https://www.bbc.com/{category}'
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    news = [link.get_attribute('href') for link in links if 'articles' in link.get_attribute('href')]
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

# Streamlit interface
st.title("NewsScraper")
st.header("Select a news category to scrape and summarize an article")

categories = ['Sports', 'Business', 'Travel', 'Innovation', 'Culture']
category = st.selectbox("Please select a category:", categories)

if st.button("Get Summary"):
    with st.spinner("Processing..."):
        title, content = scrape_news(category.lower())
        summary = summarize(content)
        time.sleep(5)  # Simulate processing time
    st.success("Summary generated!")
    st.subheader(f"Title: {title}")
    st.write(summary)

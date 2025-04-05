import requests
from bs4 import BeautifulSoup
import ollama

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')  
        text_content = "\n".join([p.get_text() for p in paragraphs])

        return text_content
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
'''Q1. Build a Flask app that scrapes data from multiple websites and displays it on your site.
You can try to scrap websites like youtube , amazon and show data on output pages and deploy it on cloud
platform .'''


from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/akanksha')
def home():
    return render_template('index.html')

@app.route('/youtube')
def youtube():
    youtube_data = scrape_youtube()
    if not youtube_data:
        return jsonify({"error": "Failed to scrape YouTube data"}), 502
    return render_template('youtube.html', data=youtube_data)

@app.route('/amazon')
def amazon():
    amazon_data = scrape_amazon()
    if not amazon_data:
        return jsonify({"error": "Failed to scrape Amazon data"}), 502
    return render_template('amazon.html', data=amazon_data)

def scrape_youtube():
    try:
        url = "https://www.youtube.com/results?search_query=python+programming"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for video in soup.find_all('a', class_='yt-uix-tile-link'):
            title = video.get('title')
            link = 'https://www.youtube.com' + video.get('href')
            results.append({'title': title, 'link': link})
        return results
    except Exception as e:
        print(f"Error scraping YouTube: {e}")
        return None

def scrape_amazon():
    try:
        url = "https://www.amazon.com/s?k=laptop"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for product in soup.find_all('div', class_='s-title-instructions-style'):
            title = product.find('span', class_='a-size-medium').text.strip()
            link = 'https://www.amazon.com' + product.find('a', class_='a-link-normal')['href']
            results.append({'title': title, 'link': link})
        return results
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return None

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5005)
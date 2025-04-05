from flask import Flask, render_template, request, jsonify
from scraper import scrape_website 
import ollama

app = Flask(__name__)

scraped_text_global = ""  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    global scraped_text_global
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    scraped_text = scrape_website(url)
    scraped_text_global = scraped_text  

    return jsonify({"scraped_text": scraped_text}) 

@app.route('/ask', methods=['POST'])
def ask():
    global scraped_text_global
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    if not scraped_text_global:
        return jsonify({"error": "No scraped text available. Please scrape a website first."}), 400

    model = "llama3:latest"
    prompt = f"Based on the following text, answer the question:\n\n{scraped_text_global[:3000]}\n\nQuestion: {question}"
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
    answer = response['message']['content'] if 'message' in response else "Error in generating answer."
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
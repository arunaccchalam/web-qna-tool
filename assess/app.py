from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Store scraped content
database = {}

# OpenAI API Key (Replace with your own if needed)
openai.api_key = "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"

def clean_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route("/fetch", methods=["POST"])
def fetch_content():
    urls = request.json.get("urls", [])
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                cleaned_text = clean_text(response.text)
                database[url] = cleaned_text
            else:
                return jsonify({"error": f"Failed to fetch {url}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Content fetched successfully", "data": database})

@app.route("/ask", methods=["POST"])
def answer_question():
    question = request.json.get("question", "")
    if not database:
        return jsonify({"error": "No content available. Please fetch URLs first."}), 400
    
    combined_text = " ".join(database.values())
    
    # Use TF-IDF to find relevant content
    corpus = list(database.values())
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus + [question])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_index = similarities.argmax()
    relevant_content = corpus[best_match_index]
    
    # Use OpenAI GPT for answering
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer the question based only on the given text."},
            {"role": "user", "content": f"Context: {relevant_content}\n\nQuestion: {question}"}
        ]
    )
    answer = response["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

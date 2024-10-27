import fitz  # PyMuPDF
from huggingface_hub import InferenceClient
import json
from apikey import apikey
from flask import Flask, render_template, request, url_for, send_from_directory
import os

app = Flask(__name__)
# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("home.html")

# Function to chunk the text into smaller segments
def chunk_text(text, chunk_size=14000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "No file part in the request"
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return "No selected file"
    
    # Check if the uploaded file is a PDF
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Render query_page.html and pass the filename
        return render_template("query_page.html", filename=filename)
    else:
        return "File is not a PDF"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded PDF file
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def summarizer(query):
    client = InferenceClient(api_key=apikey)
    result = ""  # Initialize result variable to capture output
    
    try:
        for message in client.chat_completion(
            model="mistralai/Mistral-Nemo-Instruct-2407",
            messages=[{"role": "user", "content": query}],
            max_tokens=5000,
            stream=True,
        ):
            try:
                # Check if the message contains valid choices
                if "choices" in message:
                    content = message.choices[0].delta.content
                    # print(content, end="")
                    if(content=="\n"):
                        result+"\n"
                    elif(content==" "):
                        result+=" "
                    else:
                        result += content  # Add the content to the result variable
            except json.JSONDecodeError as e:
                # Catch JSON decoding errors and skip that chunk
                 print(f"Warning: Received invalid JSON data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return result  # Return the collected result

import re

# Function to chunk text based on paragraphs instead of fixed sizes
def split_by_paragraph(text):
    # Split text by double newline, assuming paragraphs are separated by '\n\n'
    paragraphs = text.split('\n\n')
    return paragraphs

@app.route("/query", methods=['POST'])
def queryprocessor():

    f = open("history.txt", "r", encoding="utf-8")
    his=f.read()
    print(his)
    query = request.form.get("userquery")
    his+=query+"β"
    print("the Query:", query)
    filename = request.form.get('filename')
    
    # Open the uploaded PDF file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with fitz.open(filepath) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return "Error reading PDF file."

    # Step 1: Summarize the entire PDF text if necessary
    if len(text) <= 15900:
        full_summary = text  # Use the entire text if it's small enough
    else:
        # Chunk the text by paragraphs and summarize each chunk
        chunks = split_by_paragraph(text)
        summarized_texts = []
        for i, chunk in enumerate(chunks):
            print("The chunks ")
            print(chunk)
            import time 
            time.sleep(1)  # Add a delay to simulate processing time for each chunk
            print(f"Summarizing chunk {i + 1}/{len(chunks)} with length {len(chunk)} characters.")
            summary = summarizer(f"Please summarize this text: {chunk}")
            summarized_texts.append(summary)
        
        # Combine all summaries into a single full summary
        full_summary = " ".join(summarized_texts)
    
    # Step 2: Answer the query based on the full summary
    print("Final summary length:", len(full_summary))
    print("Query:", query)
    answer_query = f"{full_summary} provided text summary,  {query}"
    answer = summarizer(answer_query)
    
    # Debug: Check if answer was received
    if not answer:
        print("No answer returned from summarizer.")
        return "Could not generate an answer."
    his+=answer+"β"
    f = open("history.txt", "a", encoding="utf-8")
    f.write(his)
    his1=his.split("β")
    # return his1
    print(his1) 
    # Render the answer on the query page
    return render_template("query_page.html", res=answer, filename=filename,query=query,his=his1)



if __name__ == "__main__":
    app.run(port=2004, debug=True)

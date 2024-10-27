
# PDF Assistant

*Team Number:* 134  
*Team Members:*  
1. M Manish Kumar (Team Lead)  
2. MD Salman  
3. P Sai Chaitanya  
4. Rajesh  

## Project Overview

PDF Assistant is a web application designed to streamline the process of extracting information from PDF documents. By allowing users to upload PDFs, ask questions, and receive immediate, AI-driven responses, PDF Assistant offers an efficient alternative to manual document analysis. This tool is ideal for professionals, students, and researchers who need to quickly retrieve information from lengthy documents.

## Features

- *Upload PDF Files*: Users can upload PDF files, which are then processed for text extraction.
- *Ask Questions*: Users can ask questions related to the PDF content, and the AI-powered assistant provides answers.
- *User-Friendly Interface*: Simple and intuitive UI designed for ease of use and efficiency.
- *Real-Time Responses*: Instant answers from the document based on user queries.
# Install  requirements.txt
    using the command 
        pip install -r requirements.txt
## Tech Stack

- *Frontend*: html, Bootstrap,css
- *Backend*: python
- *AI Model*: NLP model for question-answering


## Project Structure

```plaintext
pdf_assistant/
│
├── templates/               # HTML templates
│   ├── layout.html          # Base layout template
│   └── index.html           # Main page template
│
├── static/                  # Static files (CSS, JavaScript, images)
│   ├── css/                 # Stylesheets
│   │   └── style.css
│   ├── js/                  # JavaScript files
│   │   └── script.js
│   └── images/              # Directory for images
│       └── example.png      # Example image file
│
├── uploads/                 # Directory to store uploaded PDF files
│               # Configuration settings (e.g., upload folder)
├── requirements.txt         # List of dependencies
└── run.py                   # Entry point to run the Flask app

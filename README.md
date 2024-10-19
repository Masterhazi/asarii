# ASaRI - Article Search and RIS File Generator

![ASaRI Logo](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXR4enYxM2ZrYmw0aTkxczUxYm96aWlvdmlrMmR5cnc2b3lkazNpNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT77Y1T0zY1gR5qe5O/giphy.gif)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How We Built the App](#how-we-built-the-app)
- [License](#license)
- [Contributing](#contributing)

## Introduction

ASaRI (Article Search and RIS File Generator) is a powerful web application designed to streamline the process of finding scholarly articles and generating RIS files for efficient citation management. Built with a user-friendly interface, ASaRI allows users to quickly search for articles from Google Scholar and PubMed, providing an effective solution for researchers, students, and academics alike.

This project is a culmination of a journey that began with a vision to create an AI-driven tool for simplifying academic research. Throughout this development, various features were incorporated to enhance usability and functionality, including an intuitive design and seamless integration with generative AI technologies.

## Features

- **Article Search:** Quickly search for articles using Google Scholar and PubMed APIs.
- **RIS File Generation:** Automatically generate RIS files for easy citation management.
- **AI-Powered Summaries:** Utilize Google’s Generative AI to create concise summaries of articles.
- **Interactive UI:** Engaging and responsive design with hover effects and animations.
- **Translucent Background:** A visually appealing interface featuring a GIF background that enhances user experience.
- **Meta Tags for Sharing:** Custom descriptions for link previews when sharing on platforms like WhatsApp.

## Technologies Used

- **Python:** The core programming language for backend logic.
- **Streamlit:** Framework for building the web application.
- **Google Generative AI:** For generating article summaries.
- **LangChain:** A framework for managing LLM interactions.
- **Dotenv:** For managing environment variables.
- **Requests:** For handling API calls.
- **Scholarly:** For searching articles from Google Scholar.
- **PubMed API:** For accessing PubMed articles.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/asari.git
   cd asari
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```plaintext
   GOOGLE_API_KEY=your_google_api_key
   PUB_MED_API=your_pubmed_api_key
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open your browser and go to `http://localhost:8501`.
2. Enter the article title or keywords in the input field.
3. Click the "Search" button to retrieve results.
4. View the generated RIS file and formatted citation.
5. Generate a summary of the article using the AI-powered feature.

## How We Built the App

The development of ASaRI involved multiple components working together to provide a seamless experience for users. Below are some key aspects of how we built the application:

### API Integration
We integrated with Google Scholar and PubMed APIs to enable article searching:

```python
from scholarly import scholarly

# Function to search for articles
def search_articles(query):
    search_results = scholarly.search_pubs(query)
    return search_results
```

### RIS File Generation
We implemented a function to create RIS files from the retrieved article data:

```python
def create_ris_file(article):
    ris_file = ""
    ris_file += "TY  - JOUR\n"
    ris_file += "AU  - " + "; ".join(article['bib'].get('author', [])) + "\n"
    ris_file += "TI  - " + article['bib'].get('title', 'No Title') + "\n"
    # Additional fields...
    return ris_file
```

### AI-Powered Summaries
To summarize articles, we utilized Google’s Generative AI:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-pro', api_key=os.getenv('GOOGLE_API_KEY'))

def generate_summary(abstract):
    prompt = template.format(abstract=abstract)
    summary = llm.predict(text=prompt)
    return summary
```

### User Interface
We created an interactive user interface using Streamlit, featuring a translucent background with a GIF:

```python
st.markdown("""
    <div style='background-color: rgba(0, 0, 0, 0.5); padding: 20px;'>
    <h1 style='color: #FFFFFF;'>ASaRI</h1>
    <input type='text' placeholder='Enter your query here...' />
    <button>Search</button>
    </div>
""", unsafe_allow_html=True)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.


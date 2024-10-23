import os
import streamlit as st
import google.generativeai as genai
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from scholarly import scholarly
import requests
from xml.etree import ElementTree as ET

# Set up local environment
load_dotenv()  # Activate the local environment
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(page_title="📖 ASaRIi", page_icon="https://raw.githubusercontent.com/Masterhazi/asarii/refs/heads/main/favicon.ico")

st.markdown("""
    <meta property="og:title" content="ASaRI - Article Search and RIS File Generator">
    <meta property="og:description" content="ASaRI helps you find articles quickly and generate RIS files for easy citation management.">
    <meta property="og:image" content="https://miro.medium.com/v2/resize:fit:180/1*Ejw4l-I7vEH281s1eCQyhg.png">
    <meta property="og:url" content="https://asarii.streamlit.app/">
""", unsafe_allow_html=True)

# Custom CSS for color scheme and button effects
st.markdown("""
    <style>
        body {
            background-color: #ffffff; /* White background */
            color: #4B0082; /* Dark purple text */
        }
        .purple-background {
            background-color: #6A5ACD; /* Purple background */
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .tan-background {
            background-color: #D2B48C; /* Tan background */
            padding: 10px;
            border-radius: 5px;
        }
        h1, h2, h3 {
            color: #4B0082; /* Dark purple for headers */
        }
        /* Button styles */
        .stButton {
            background-color: transparent; /* Remove background color */
            color: #4B0082 !important;  /* Dark purple text */
            border: 1px solid #4B0082 !important; /* Dark purple border */
            transition: transform 0.2s !important; /* Smooth zoom effect */
            padding: 10px 15px !important; /* Adjust padding for better sizing */
            border-radius: 5px !important; /* Rounded corners */
            cursor: pointer !important; /* Pointer cursor on hover */
            display: inline-block !important; /* Ensure button displays inline and sizes according to text */
            text-align: center !important; /* Center text */
        }
        .stButton:hover {
            transform: scale(1.1); /* Zoom in effect */
        }
        .stButton:focus {
            outline: none; /* Remove outline */
        }
    </style>
""", unsafe_allow_html=True)

# Designing the webpage
st.markdown("""
    <h1 style='text-align: left; color: #2196F3;'>
    <span style="background-color: #E3F2FD; padding: 10px; border-radius: 5px;"><b>ASARI</b></span> 
    <span style='color: #2196F3;'>A</span><span style='color: #fafafa;'>rticle</span> 
    <span style='color: #2196F3;'>S</span><span style='color: #fafafa;'>earch</span>
    <span style='color: #2196F3;'>a</span><span style='color: #fafafa;'>nd</span> 
    <span style='color: #2196F3;'>RI</span><span style='color: #fafafa;'>S file generator</span> 
    </h1>
""", unsafe_allow_html=True)

# Article Search and RIS file generator section with purple background
st.markdown('<div class="purple-background">', unsafe_allow_html=True)

query = st.text_input("Please put in the article you need")

# Define prompt template for summary generation
demo_template = '''Based on the following abstract, provide a summary with only important stuff along with key words in 5 points and don't give side heading as summary:\n{abstract}'''
template = PromptTemplate(input_variables=['abstract'], template=demo_template)

# Initialize the model for Google Generative AI
llm = ChatGoogleGenerativeAI(model='gemini-pro', api_key=os.getenv('GOOGLE_API_KEY'))

# Function to create a RIS file
def create_ris_file(article):
    auth = []
    au = ""
    for i in article['bib'].get('author', []):
        if i.strip() or '.':  # If there's content, keep adding to au
            au += i
        else:  # If it's a space or empty, add au to auth list
            auth.append(au.strip())
            au = ""
    if au:  # Append the last author if au is not empty
        auth.append(au.strip())    
    ris_file = ""
    ris_file += "TY  - JOUR\n"
    ris_file += "AU  - " + "; ".join(auth) + "\n"
    ris_file += "PY  - " + article['bib'].get('pub_year', 'Unknown') + "\n"
    ris_file += "TI  - " + article['bib'].get('title', 'No Title') + "\n"
    ris_file += "JO  - " + article['bib'].get('journal', 'Unknown Journal') + "\n"
    ris_file += "VL  - " + article['bib'].get('volume', 'Unknown Volume') + "\n"
    ris_file += "SP  - " + article['bib'].get('start_page', 'Unknown Page') + "\n"
    ris_file += "EP  - " + article['bib'].get('end_page', 'Unknown Page') + "\n"
    ris_file += "UR  - " + article.get('url', 'No URL') + "\n"
    ris_file += "DO  - " + article['bib'].get('doi', 'No DOI') + "\n"
    ris_file += "IS  - " + article['bib'].get('issue', 'Unknown Issue') + "\n"
    ris_file += "AB  - " + article['bib'].get('abstract', 'No abstract available') + "\n"
    ris_file += "ER  - \n"
    return ris_file


# Function to format the citation
def format_citation(article):          
    title = article['bib'].get('title', 'No Title')
    venue = article['bib'].get('venue', 'Unknown Journal')
    pub_year = article['bib'].get('pub_year', 'Unknown Year')
    volume = article['bib'].get('volume', 'Unknown Volume')
    page = article['bib'].get('page', 'Unknown Page')
    authors = authors = "; ".join(article['bib'].get('author', []))
    # Formatting the citation
    citation = f"{authors}. {title}. {venue}. {pub_year};{volume}:{page}."
    return citation

# Function to search PubMed
def search_pubmed(query):
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 1,  # Only retrieve 1 result
        "retmode": "xml"
    }

    # Perform the search
    response = requests.get(esearch_url, params=search_params)
    root = ET.fromstring(response.content)

    # Extract the list of PubMed IDs (PMIDs)
    pmids = [id_elem.text for id_elem in root.findall(".//Id")]
    return pmids

# Function to fetch article details from PubMed
def fetch_pubmed_article(pmids):
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    response = requests.get(efetch_url, params=fetch_params)
    root = ET.fromstring(response.content)

    articles = []
    for article in root.findall(".//PubmedArticle"):
        article_info = {
            'bib': {
                'title': article.find(".//ArticleTitle").text,
                'author': [author.find(".//LastName").text + ", " + author.find(".//ForeName").text for author in article.findall(".//Author")],
                'pub_year': article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "Unknown",
                'venue': article.find(".//Journal/Title").text if article.find(".//Journal/Title") is not None else "Unknown Journal",
                'volume': article.find(".//Journal/Volume").text if article.find(".//Journal/Volume") is not None else "Unknown Volume",
                'page': article.find(".//Journal/Issue").text if article.find(".//Journal/Issue") is not None else "Unknown Page",
                'pub_url': f"https://pubmed.ncbi.nlm.nih.gov/{article.find('.//PMID').text}"
            },
            'abstract': article.find(".//AbstractText").text if article.find(".//AbstractText") is not None else "No abstract available"
        }
        articles.append(article_info)

    return articles

# Handling the search and response
if st.button("Search") and query:
    # Search in PubMed first
    pmids = search_pubmed(query)

    if pmids:
        # Fetch article details from PubMed
        articles = fetch_pubmed_article(pmids)

        for article in articles:
            # Create RIS file
            ris_file = create_ris_file(article)
            st.text_area("RIS File", ris_file, height=300)

            # Download the RIS file with the title as the filename
            title = article['bib']['title'].replace(" ", "_")
            st.download_button("Download RIS", ris_file, file_name=f"{title}.ris")

            # Generate a formatted citation
            citation = format_citation(article)
            st.write("**Formatted Citation:**")
            st.text_area("Citation", citation, height=100)

            # Fetch abstract
            abstract = article['abstract']
            if abstract:
                prompt = template.format(abstract=abstract)
                try:
                    summary = llm.predict(text=prompt)
                    if summary:
                        st.write("**Summary:**")
                        st.write(summary, height=200)
                    else:
                        st.write("No summary generated.")
                except Exception as e:
                    st.write(f"Error generating summary: {e}")
                    st.text_area("Summary", "An error occurred while generating the summary. Please try again.", height=200)
            else:
                st.write("No abstract available for this article.")
                st.text_area("Summary", "No abstract available to generate a summary.", height=200)
    else:  # Only search Google Scholar if no PubMed results
     # Search in Google Scholar 
         scholar_results = scholarly.search_pubs(query)
         try:
             scholar_article = next(scholar_results)  # Get the first result
             scholar_article = scholarly.fill(scholar_article)
             ris_file = create_ris_file(scholar_article)
             st.text_area("RIS File", ris_file, height=300)
    
             st.download_button("Download RIS", ris_file, file_name="article.ris")
    
             citation = format_citation(scholar_article)
             st.write("**Formatted Citation:**")
             st.text_area("Citation", citation, height=100)
    
             # Fetch abstract
             abstract = scholar_article['bib'].get('abstract', None)
             if abstract:
                 prompt = template.format(abstract=abstract)
                 try:
                     summary = llm.predict(text=prompt)
                     if summary:
                         st.write("**Summary:**")
                         st.write(summary, height=200)
                     else:
                         st.write("No summary generated.")
                 except Exception as e:
                     st.write(f"Error generating summary: {e}")
                     st.text_area("Summary", "An error occurred while generating the summary. Please try again.", height=200)
             else:
                 st.write("No abstract available for this article.")
                 st.text_area("Summary", "No abstract available to generate a summary.", height=200)
    
         except StopIteration:
             # Handle the case where no results are found
             st.write("No results found in Google Scholar.")
st.markdown('</div>', unsafe_allow_html=True)  # Close the purple background div

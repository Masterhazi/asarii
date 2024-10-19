import os
import streamlit as st
import google.generativeai as genai
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from scholarly import scholarly
import requests

# Set up local environment
load_dotenv()  # Activate the local environment
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(page_title="📖 ASaRI", page_icon="https://raw.githubusercontent.com/Masterhazi/ASaRI/refs/heads/main/favicon.ico")

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
            color: #4B0082; /* Dark purple text */
            border: 1px solid #4B0082; /* Dark purple border */
            transition: transform 0.2s; /* Smooth zoom effect */
            padding: 10px 15px; /* Adjust padding for better sizing */
            border-radius: 5px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            display: inline-block; /* Ensure button displays inline and sizes according to text */
            text-align: center; /* Center text */
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
    ris_file = ""
    ris_file += "TY  - JOUR\n"
    ris_file += "AU  - " + "; ".join(article['bib'].get('author', [])) + "\n"
    ris_file += "PY  - " + str(article['bib'].get('pub_year', 'Unknown')) + "\n"
    ris_file += "TI  - " + article['bib'].get('title', 'No Title') + "\n"
    ris_file += "JO  - " + article['bib'].get('venue', 'Unknown Journal') + "\n"
    ris_file += "VL  - " + article['bib'].get('volume', 'Unknown Volume') + "\n"
    ris_file += "SP  - " + article['bib'].get('page', 'Unknown Page') + "\n"
    ris_file += "UR  - " + article.get('pub_url', 'No URL') + "\n"
    ris_file += "ER  - \n"
    return ris_file

# Function to format the citation
def format_citation(article):
    authors = "; ".join(article['bib'].get('author', []))
    title = article['bib'].get('title', 'No Title')
    venue = article['bib'].get('venue', 'Unknown Journal')
    pub_year = article['bib'].get('pub_year', 'Unknown Year')
    volume = article['bib'].get('volume', 'Unknown Volume')
    page = article['bib'].get('page', 'Unknown Page')

    # Formatting the citation
    citation = f"{authors}. {title}. {venue}. {pub_year};{volume}:{page}."
    return citation

# Function to search PubMed
def search_pubmed(query):
    pubmed_api = os.getenv('PUB_MED_API')
    url = f"https://api.pubmed.ncbi.nlm.nih.gov/lit/ctxp/v1.0/?query={query}"
    headers = {"Authorization": f"Bearer {pubmed_api}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Handling the search and response
if st.button("Search") and query:
    nd = False
    search_results = scholarly.search_pubs(query)

    # Optional: Magic popper effect
    st.markdown('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>', unsafe_allow_html=True)
    st.markdown('<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/4.0.0/js/bootstrap.min.js"></script>', unsafe_allow_html=True)
    
    # Button click effect
    st.markdown('<div class="magic-popper" style="display: none;"></div>', unsafe_allow_html=True)
    
    try:
        article = next(search_results)

        # Create RIS file
        ris_file = create_ris_file(article)
        st.text_area("RIS File", ris_file, height=300)

        # Download the RIS file with the title as the filename
        title = article['bib'].get('title', 'No Title').replace(" ", "_")
        st.download_button("Download RIS", ris_file, file_name=f"{title}.ris")

        # Generate a formatted citation
        citation = format_citation(article)
        st.write("**Formatted Citation:**")
        st.text_area("Citation", citation, height=100)

        # Generate a summary using Google Generative AI
        abstract = article['bib'].get('abstract', None)
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
        # Fallback to PubMed search if no articles found
        st.write("No articles found in Google Scholar. Searching PubMed...")
        nd = True
        pubmed_results = search_pubmed(query)

        if pubmed_results:
            # Assuming the first result is the most relevant
            article = pubmed_results[0]  # Adjust this based on the actual structure returned
            # Here you can create the RIS file and formatted citation similarly
            ris_file = create_ris_file(article)  # You might need to adapt the structure
            st.text_area("RIS File", ris_file, height=300)

            # Download the RIS file with the title as the filename
            title = article['title'].replace(" ", "_")
            st.download_button("Download RIS", ris_file, file_name=f"{title}.ris")

            # Generate a formatted citation
            citation = format_citation(article)  # You might need to adapt the structure
            st.write("**Formatted Citation:**")
            st.text_area("Citation", height=100)

            # Generate a summary using Google Generative AI
            abstract = article.get('abstract', None)
            if abstract and nd == True:
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
        else:
            st.write("No articles found in PubMed.")
    
# Close the purple background div
st.markdown('</div>', unsafe_allow_html=True)

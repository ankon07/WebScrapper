import streamlit as st
from scrape import (scrape_website, split_dom_content, cleaned_body_content, extract_body_content)
from parse import parse_with_huggingface


st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL:")

if st.button("Scrape Site"):
    st.write("Scraping the Website...")
    
    # Scrape the website and extract body content
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = cleaned_body_content(body_content)

    # Initialize st.session_state if not already initialized
    if "dom_content" not in st.session_state:
        st.session_state["dom_content"] = ""

    # Save the cleaned content into session state
    st.session_state.dom_content = cleaned_content

    # Display the cleaned content in a text area within an expander
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state["dom_content"], height=300)



if "dom_content" in st.session_state:
    parse_description = st.text_area("Descrive what do you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_huggingface(dom_chunks,parse_description)
            st.write(result)

        

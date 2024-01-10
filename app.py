import streamlit as st
from utils import *
import constants

# Creating Seesion state variable
if 'HuggingFace_API_Key' not in st.session_state:
    st.session_state['HuggingFace_API_Key'] = ''
if 'Pinecone_API_Key' not in st.session_state:
    st.session_state['Pinecone_API_Key'] = ''

st.title('🦾 AI assistance for website')

# SIDE BAR Functionality started

# Sidebar to capture the API keys
st.sidebar.title("🤓 🆒")
st.session_state['HuggingFace_API_Key'] = st.sidebar.text_input("What's ur HuggingFace API key?",
                                                                type="password")
st.session_state['Pinecone_API_Key'] = st.sidebar.text_input("What's ur Pinecone API key?",
                                                             type="password")

load_button = st.sidebar.button("Load data to Pinecone", key="load_button")

# If the above button is clicked, pushing the dat to Pinecone
if load_button:
    # Proceed only if API keys are provided
    if st.session_state['HuggingFace_API_Key'] != "" and st.session_state['Pinecone_API_Key'] != "":
        # Fetch data from site
        site_data = get_website_data(constants.WEBSITE_URL)
        st.write("Data pull done...")

        # Split data into chunks
        chunks_data = split_data(site_data)
        st.write("Splitting data done...")

        # Creating embedding instance
        embeddings = create_embeddings()
        st.write("Embeddings instance creation done...")

        # Push data to Pinecone
        push_to_pinecone(st.session_state['Pinecone_API_Key'], constants.PINECONE_ENVIRONMENT,
                         constants.PINECONE_INDEX, embeddings, chunks_data)

        st.write("Pushing data to Pinecone done...")
        st.sidebar.success("Data pushed to Piencone  successfully!!!")
    else:
        st.sidebar.error("Nope!!!! Please provide ur API Keys....")

# SIDE BAR Functionality ended
# Captures User Inputs
# The box for text prompt
prompt = st.text_input('How can I help you bro ?', key="prompt")
document_count = st.slider("No of links to return 🌐 - (0 Low || 5 High)", 0, 5, 2, step=1)

submit = st.button("Search")

if submit:
    # Proceed only if API keys are provided.
    if st.session_state['HuggingFace_API_Key'] != "" and st.session_state['Pinecone_API_Key'] !="":
        # Creating embedded instance
        embeddings = create_embeddings()
        st.write("Embeddings instance creation done...")

        # Pull index data from Pinecone
        index = pull_from_pinecone(st.session_state['Pinecone_API_Key'], constants.PINECONE_ENVIRONMENT,
                                   constants.PINECONE_INDEX, embeddings)
        st.write("Pinecone index retrieval done...")

        # Fetch relevant documents from Pinecone index
        relevant_docs = get_similiar_docs(index, prompt, document_count)
        st.write(relevant_docs)

        # Displaying search results
        st.success("Please find the search results: ")

        # Display search results
        st.write("search results list....")
        for document in relevant_docs:
            st.write("👉**Result : " + str(relevant_docs.index(document)+1)+"***")
            st.write("**Infor**" + document.page_content)
            st.write("**Link**" + document.metadata['source'])
        else:
            st.sidebar.error("Nope!!! Please provide API Keys.....")
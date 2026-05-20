import streamlit as st
import PyPDF2
import requests
import json


def extract_text_from_pdf(pdf_file):
    pages_text = []
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                # Clean up dirty structural artifacts left by table grids and rows
                cleaned_text = page_text.replace('",', ' ').replace('"', '').replace(',,', ' ')
                pages_text.append(cleaned_text.strip())
    except Exception as e:
        st.error(f"Error while reading PDF: {e}")
    return pages_text


def search_relevant_context(question, pages):
    query_words = question.lower().replace("?", "").replace(".", "").replace(",", "").split()
    best_page_context = ""
    max_overlap = 0

    for page_content in pages:
        page_lower = page_content.lower()
        overlap = 0
        for word in query_words:
            if word in page_lower:
                overlap += 1
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_page_context = page_content
            
    # FALLBACK FIX: If it's a single-page document or a table structure where keyword overlap metrics 
    # score low, default to passing the first available page data context so the LLM can parse it.
    if not best_page_context and pages:
        best_page_context = pages[0]
        
    return best_page_context


def ask_local_ollama(question, context):
    prompt = f"""
You are an expert AI document analyst. 

Instructions:
1. Answer the question based ONLY on the provided context.
2. If the answer cannot be found in the context, say: "I cannot find that specific detail in the document."
3. Do not use outside knowledge.

Context:
{context}

User Question: {question}

Answer:
"""

    # Local port endpoint where Ollama runs on your machine
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2",  # Maps directly to your successfully pulled engine
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["response"]

    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama background service cannot be reached. Keep your terminal active with 'ollama run llama3.2'."
    except Exception as e:
        return f"Error while communicating with local LLM: {e}"


def show_project_flow():
    st.markdown("""
    ### Complete Project Flow Diagram
    ```text
    [ PDF Upload Box ]
            ↓
    [ extract_text_from_pdf() ] ───> Parses text page-by-page & cleans table structures
            ↓
    [ Interactive Screen ] ────────> User clicks Quick Button or types custom input
            ↓
    [ search_relevant_context() ] ──> Evaluates word metrics with structure fallback
            ↓
    [ Prompt Augmentation ] ───────> Bundles context string + question safely
            ↓
    [ ask_local_ollama() ] ────────> Raw HTTP POST payload to Localhost (11434)
            ↓
    [ UI Render Engine ] ──────────> Displays completely local offline response
    ```
    """)


st.set_page_config(
    page_title="Document Intelligence System (Local RAG)",
    page_icon="📘",
    layout="wide"
)


st.markdown("""
<style>
.stApp { background-color: #0f1115; color: #e2e8f0; }
.main-title { font-size: 40px; font-weight: bold; color: #f8fafc; text-align: center; margin-top: 10px; }
.sub-title { font-size: 22px; font-weight: normal; color: #94a3b8; text-align: center; margin-bottom: 20px; }
.brand-box { background-color: #1a1f26; color: #cbd5e1; border-left: 6px solid #475569; padding: 20px; border-radius: 8px; margin-bottom: 20px; font-size: 16px; border: 1px solid #2e3748; }
section[data-testid="stSidebar"] { background-color: #090b0e; color: white; border-right: 1px solid #1e293b; }
h1, h2, h3 { color: #f1f5f9 !important; }
.stButton>button { background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; border-radius: 6px; font-weight: bold; }
.stButton>button:hover { background-color: #334155; color: #ffffff; border-color: #475569; }
.stTabs [data-baseweb="tab"] { color: #94a3b8; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: #f8fafc; border-bottom-color: #f8fafc; }
.stAlert { background-color: #1a1f26; color: #f1f5f9; border: 1px solid #2e3748; }
.footer { text-align: center; color: #475569; font-size: 14px; margin-top: 40px; }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title"> Document Intelligence System </div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent Document Question Answering System using Local RAG</div>', unsafe_allow_html=True)

st.markdown("""
<div class="brand-box">
<b>Developer Deployment Profile</b><br><br>
<b>Framework Matrix:</b> Python, Streamlit, PyPDF2, Local REST Architecture<br>
<b>Execution Mode:</b> 100% Private, Localhost Offline Execution (No API Keys Used)
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("📘 Project Information")
    st.write("This architecture demonstrates a completely local, zero-dependency RAG architecture built explicitly for private real-time document inference.")
    
    st.subheader("Ollama Background Status")
    st.code("ollama run llama3.2", language="bash")


tab1, tab2, tab3 = st.tabs([
    "Upload PDF",
    "Project Flow",
    "Technical Concepts"
])

with tab1:
    st.header("Document Processing Environment")
    uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF uploaded successfully!")
        
        with st.spinner("Extracting text data parameters..."):
            pages_context_list = extract_text_from_pdf(uploaded_file)
            
        if not pages_context_list:
            st.error("No readable text structures isolated inside this document asset.")
        else:
            # Render descriptive data metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Extracted Blocks (Pages)", len(pages_context_list))
            with col2:
                st.metric("Local Engine Status", "Running Offline 🟢")

            st.write("### 💡 Quick Actions")
            btn_col1, btn_col2 = st.columns(2)
            active_query = ""

            with btn_col1:
                if st.button("📋 Generate 3-Point Summary", use_container_width=True):
                    active_query = "Give me a concise summary of this document using exactly three bullet points."
            with btn_col2:
                if st.button("🛠️ Extract Key Details & Skills", use_container_width=True):
                    active_query = "What are the core business operational details, items, vendor codes, or main topics mentioned in this document?"

            # Native user text collection bar
            chat_input = st.chat_input("Ask a custom question from the uploaded document matrix...")
            if chat_input:
                active_query = chat_input

            # Execution Pipeline
            if active_query:
                with st.chat_message("user"):
                    st.markdown(active_query)

                with st.spinner("Searching relevant context slices..."):
                    retrieved_context = search_relevant_context(active_query, pages_context_list)

                with st.chat_message("assistant"):
                    if not retrieved_context:
                        st.warning("No context matching query metrics isolated inside document frames.")
                    else:
                        st.subheader("Retrieved Relevant Context")
                        with st.expander("Click to view isolated context block"):
                            st.info(retrieved_context)

                        with st.spinner("Generating inference using local Ollama model..."):
                            answer = ask_local_ollama(active_query, retrieved_context)
                        
                        st.subheader("Generated Answer")
                        st.info(answer)

with tab2:
    st.header("RAG Architecture Flow")
    show_project_flow()

with tab3:
    st.header("Technical Concepts Used")
    st.markdown("""
    ### 1. Document Extraction Pipeline
    Using `PyPDF2`, the application strips raw document structures into separate memory arrays mapping directly to individual document pages.

    ### 2. Context Index Retrieval
    Implements tokenization scanning algorithms to score string intersections across stored text objects, matching queries with text arrays.

    ### 3. Context Augmentation
    The isolated content block is dynamically integrated inside a system prompt boundary layer to enforce local model grounding constraints.

    ### 4. Local Host Transmission Protocol
    Bypasses external network traffic entirely by routing structured data arrays locally over port `11434`. This ensures data security and removes dependency on cloud APIs.
    """)


st.markdown("""
<div class="footer">
<hr>
<b>Document Intelligence System</b><br>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SecureBot | Cybersecurity AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

api_key = (os.getenv("GROQ_API_KEY") or "").strip()
# =====================================================
# API KEY VALIDATION
# =====================================================

if not api_key or not api_key.startswith("gsk_"):
    st.error(
        "Groq API key is missing or invalid. "
        "Please configure GROQ_API_KEY in your .env file."
    )
    st.stop()


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: radial-gradient(
        circle at 80% 0%,
        #102d50 0%,
        #061326 45%,
        #030b18 100%
    );
    color: #edf5ff;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
}

p, li, label {
    color: #a7bdd8;
}

h1, h2, h3, h4 {
    color: #edf5ff !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07172d,
        #030b18
    );
    border-right: 1px solid #1b426d;
}

.feature-card {
    background: linear-gradient(
        145deg,
        #102744,
        #091a31
    );
    border: 1px solid #23466f;
    border-radius: 14px;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 12px;
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 10px;
}

.feature-title {
    color: #f0f7ff;
    font-size: 17px;
    font-weight: 700;
}

.feature-description {
    color: #a8bdd8;
    font-size: 13px;
    margin-top: 8px;
}

.section-title {
    color: #edf5ff;
    font-size: 22px;
    font-weight: 750;
}

.section-subtitle {
    color: #9bb5d3;
    font-size: 13px;
    margin-bottom: 15px;
}

.stButton > button {
    background: linear-gradient(
        120deg,
        #0d2c50,
        #102744
    );
    color: #eaf5ff;
    border: 1px solid #2a5b8c;
    border-radius: 10px;
    min-height: 43px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #087de0;
    color: white;
    border-color: #37b4ff;
}

.stChatMessage {
    background: #0b1d35;
    border: 1px solid #1c3d63;
    border-radius: 15px;
    padding: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p {
    color: #e3efff;
}

[data-testid="stChatInput"] {
    background: #102744 !important;
    border: 2px solid #00bfff !important;
    border-radius: 15px !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffff00 !important;
    -webkit-text-fill-color: #ffff00 !important;
    caret-color: #00ff00 !important;
    font-size: 17px !important;
    font-weight: bold !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

div[data-testid="stExpander"] {
    background: #0b1d35;
    border: 1px solid #23466f;
    border-radius: 12px;
}

.status-card {
    background: #0c2340;
    border: 1px solid #1c4b78;
    border-radius: 10px;
    padding: 12px;
    color: #a9c8e8;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #7894b5;
    font-size: 13px;
    padding: 25px 10px;
}

hr {
    border-color: #1d3b5d;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:15px 5px;">
        <div style="font-size:65px;">🛡️</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📚 Security Topics")

    topics = [
        "🎣 Phishing",
        "🔐 Password Security",
        "🦠 Malware",
        "🚨 Ransomware",
        "🧱 Firewall",
        "📶 Wi-Fi Security",
        "👤 Social Engineering",
        "🔑 Two Factor Authentication",
        "🔒 Secure Boot",
        "🌐 Network Security",
        "🔐 Encryption"
    ]

    for topic in topics:
        st.markdown(f"**{topic}**")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.divider()

    st.markdown("### 🛡️ About SecureBot")

    st.info(
        "SecureBot is an AI-powered educational assistant "
        "designed to improve cybersecurity awareness."
    )

    st.markdown("""
    <div class="status-card">
        🟢 System Status: Ready<br>
        🤖 AI Assistant: Active<br>
        📚 Knowledge Base: Connected
    </div>
    """, unsafe_allow_html=True)

    st.caption("Version 1.0 | Educational Project")


# =====================================================
# FEATURE CARDS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎣</div>
        <div class="feature-title">Phishing Protection</div>
        <div class="feature-description">
            Learn how to recognize suspicious emails and messages.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔐</div>
        <div class="feature-title">Password Safety</div>
        <div class="feature-description">
            Understand strong passwords and secure authentication.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🦠</div>
        <div class="feature-title">Malware Awareness</div>
        <div class="feature-description">
            Learn about malware, ransomware and digital threats.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# =====================================================
# CREATE KNOWLEDGE BASE
# =====================================================

@st.cache_resource
def create_vectorstore():

    json_path = BASE_DIR / "data" / "security_faq.json"

    if not json_path.exists():
        raise FileNotFoundError(
            f"Knowledge base file not found: {json_path}"
        )

    with open(json_path, "r", encoding="utf-8") as file:
        faq_data = json.load(file)

    if not isinstance(faq_data, list) or not faq_data:
        raise ValueError(
            "JSON must contain a non-empty list."
        )

    documents = []

    for item in faq_data:

        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()

        if not question or not answer:
            continue

        content = (
            f"Question: {question}\n"
            f"Answer: {answer}"
        )

        documents.append(
            Document(
                page_content=content,
                metadata={"topic": question}
            )
        )

    if not documents:
        raise ValueError("No valid Q&A found in JSON.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(
        documents,
        embeddings
    )


# =====================================================
# LOAD KNOWLEDGE BASE
# =====================================================

try:
    with st.spinner("Loading SecureBot knowledge base..."):
        vectorstore = create_vectorstore()

except Exception as e:
    st.error(f"Knowledge Base Error: {e}")
    st.stop()


# =====================================================
# INITIALIZE GROQ AI
# =====================================================

try:
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        groq_api_key=api_key
    )

except Exception as e:
    st.error(f"Groq Initialization Error: {e}")
    st.stop()


# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

st.markdown("""
<div class="section-title">
    💡 Explore Cybersecurity
</div>

<div class="section-subtitle">
    Select a question or type your own below.
</div>
""", unsafe_allow_html=True)

questions = [
    "What is cybersecurity?",
    "How can I identify phishing?",
    "What is the difference between a virus and a worm?",
    "What is ransomware?"
]

question_columns = st.columns(4)

for index, question in enumerate(questions):

    if question_columns[index].button(
        question,
        use_container_width=True,
        key=f"question_{index}"
    ):
        st.session_state.pending_question = question
        st.rerun()

st.divider()


# =====================================================
# CHAT HISTORY
# =====================================================

st.markdown("""
<div class="section-title">
    💬 Chat with SecureBot
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:

    avatar = "🛡️" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"], avatar=avatar):

        st.markdown(message["content"])

        if message.get("sources"):

            with st.expander("📚 View Retrieved Knowledge"):

                for source in message["sources"]:
                    st.markdown(f"**Topic:** {source['topic']}")
                    st.write(source["content"])
                    st.divider()


# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input(
    "✨ Ask SecureBot a cybersecurity question..."
)

if st.session_state.pending_question:

    prompt = st.session_state.pending_question
    st.session_state.pending_question = None


# =====================================================
# GENERATE AI RESPONSE
# =====================================================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🛡️"):

        with st.spinner("🔍 SecureBot is thinking..."):

            try:

                # Retrieve relevant knowledge
                docs = vectorstore.similarity_search(
                    prompt,
                    k=5
                )

                context = "\n\n".join(
                    doc.page_content for doc in docs
                )

                # Improved AI instructions
                system_prompt = f"""
You are SecureBot, an AI Cybersecurity Awareness Assistant.

Your job is to answer users' cybersecurity questions
in simple, clear, friendly and educational English.

You can answer questions about:
- Cybersecurity Basics
- Phishing
- Password Security
- Malware
- Ransomware
- Firewall
- Wi-Fi Security
- Network Security
- Social Engineering
- Encryption
- Secure Boot
- Ethical Hacking
- Information Security
- Operating System Security

IMPORTANT RULES:

1. Use the retrieved knowledge whenever relevant.
2. Do not require an exact question match in the knowledge base.
3. You may use your general cybersecurity knowledge
   to answer educational cybersecurity questions.
4. If the knowledge base does not contain the answer,
   answer using reliable general cybersecurity knowledge.
5. If a question is unrelated to cybersecurity,
   politely explain that you specialize in cybersecurity.
6. Explain technical terms in beginner-friendly language.
7. Use headings, examples and bullet points when useful.
8. Never invent facts or claim that retrieved information
   says something it does not say.
9. Never provide instructions that facilitate cyber attacks,
   credential theft, malware deployment or unauthorized access.

Retrieved Knowledge:
{context}
"""

                response = llm.invoke([
                    ("system", system_prompt),
                    ("human", prompt)
                ])

                answer = response.content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                # Save sources
                sources = []

                for doc in docs:
                    sources.append({
                        "topic": doc.metadata.get(
                            "topic",
                            "Security Information"
                        ),
                        "content": doc.page_content
                    })

                # Save assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

                with st.expander("📚 View Retrieved Knowledge"):

                    if sources:
                        for source in sources:
                            st.markdown(
                                f"**Topic:** {source['topic']}"
                            )
                            st.write(source["content"])
                            st.divider()
                    else:
                        st.write("No matching knowledge was retrieved.")

            except Exception as e:

                error_message = (
                    f"Sorry, an error occurred: {e}"
                )

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                })


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    SecureBot | AI Cybersecurity Awareness Project
    <br><br>
    Learn • Protect • Stay Secure
</div>
""", unsafe_allow_html=True)
import streamlit as st
from agent import ShoppingAgent
from config import Config
import logging
import os

logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
logger.info("Streamlit app started.")
# Page config
st.set_page_config(
    page_title="Mobile Shopping Assistant",
    page_icon="📱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .phone-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .phone-name {
        font-size: 18px;
        font-weight: bold;
        color: #1f1f1f;
    }
    .phone-price {
        font-size: 20px;
        color: #0066cc;
        font-weight: bold;
    }
    .spec-label {
        font-weight: bold;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

if 'agent' not in st.session_state:
    # Try to get API key from Streamlit secrets first, then fall back to Config
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", None)
        if not api_key:
            api_key = Config.GOOGLE_API_KEY
    except Exception as e:
        logger.warning(f"Could not access Streamlit secrets: {e}")
        api_key = Config.GOOGLE_API_KEY
    
    if not api_key:
        st.error("⚠️ Please set your GOOGLE_API_KEY")
        st.stop()
    
    # Override config with Streamlit secret if available
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        Config.GOOGLE_API_KEY = api_key
    
    st.session_state.agent = ShoppingAgent()
    logger.info("ShoppingAgent initialized successfully.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# # Initialize session state
# if 'agent' not in st.session_state:
#     if not Config.GOOGLE_API_KEY:
#         st.error("⚠️ Please set your GOOGLE_API_KEY in .env file")
#         st.stop()
#     st.session_state.agent = ShoppingAgent()

# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# Header
st.title("📱 Mobile Shopping Assistant")
st.markdown("*Find your perfect phone with AI-powered recommendations*")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This AI assistant helps you discover, compare, and choose the best mobile phone "
        "based on your needs and budget."
    )
    
    st.header("Example Queries")
    example_queries = [
        "Best camera phone under ₹30,000?",
        "Compact Android with good battery",
        "Compare Pixel 8a vs OnePlus 12R",
        "Show me Samsung phones under ₹25k",
        "Battery king with fast charging around ₹15k",
        "Explain OIS vs EIS"
    ]
    
    for query in example_queries:
        if st.button(query, key=query, use_container_width=True):
            st.session_state.current_query = query
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent = ShoppingAgent()
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display phone cards if available
        if "phones" in message and message["phones"]:
            cols = st.columns(min(len(message["phones"]), 3))
            for idx, phone in enumerate(message["phones"]):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="phone-card">
                        <div class="phone-name">{phone['name']}</div>
                        <div class="phone-price">₹{phone['price']:,}</div>
                        <br>
                        <span class="spec-label">📷 Camera:</span> {phone['camera']}<br>
                        <span class="spec-label">🔋 Battery:</span> {phone['battery']}<br>
                        <span class="spec-label">📱 Display:</span> {phone['display']}<br>
                        <span class="spec-label">⚡ Processor:</span> {phone['processor']}<br>
                        <span class="spec-label">💾 RAM:</span> {phone['ram']}<br>
                        <span class="spec-label">🎯 Features:</span> {', '.join(phone['features'][:3])}
                    </div>
                    """, unsafe_allow_html=True)

# Handle example query button click
if 'current_query' in st.session_state:
    query = st.session_state.current_query
    del st.session_state.current_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Get response
    with st.spinner("Thinking..."):
        response= st.session_state.agent.chat(query)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })
    
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask me about mobile phones..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(prompt)
            st.markdown(response)
            
            
    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        
    })
    
    st.rerun()

import streamlit as st
import os
from dotenv import load_dotenv
from gemini import signal_data_extractor_prompt, get_gemini_response
from mt5Validator import validate_mt5_code

load_dotenv()

st.set_page_config(page_title="AI MT5 Code Generator", page_icon="📈", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2ea043 0%, #3fb950 100%);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
        transform: translateY(-2px);
    }
    
    /* Text Area (Editable Code) */
    .stTextArea > div > div > textarea {
        background-color: #010409;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
    
    /* Info/Success Boxes */
    .stSuccess {
        background-color: rgba(46, 160, 67, 0.1) !important;
        color: #3fb950 !important;
        border: 1px solid #2ea043 !important;
    }
    .stInfo {
        background-color: rgba(56, 139, 253, 0.1) !important;
        color: #58a6ff !important;
        border: 1px solid #388bfd !important;
    }
    
    /* Spinner */
    .stSpinner > div > div {
        border-color: #58a6ff transparent transparent transparent !important;
    }
    
    /* Custom Title */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(180deg, rgba(88, 166, 255, 0.05) 0%, rgba(13, 17, 23, 1) 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(88, 166, 255, 0.1);
    }
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        color: #8b949e;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <div class="title-text">AI MT5 Code Generator</div>
    <div class="subtitle-text">Transform trading signal sources into robust MetaTrader 5 Expert Advisors instantly.</div>
</div>
""", unsafe_allow_html=True)

# Main input section
st.markdown("### 🔗 Signal Source Configuration")
col1, col2 = st.columns([3, 1], gap="medium")

with col1:
    source_url = st.text_input("Enter Signal Source URL", placeholder="https://example.com/signals/...", label_visibility="collapsed")
    
with col2:
    generate_btn = st.button("🚀 Generate Code")

if generate_btn:
    if not source_url:
        st.warning("⚠️ Please enter a valid Signal Source URL.")
    else:
        st.markdown("---")
        st.markdown("### ⚙️ Processing Pipeline")
        
        # Pipeline execution
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Analysis & Generation
            status_text.info("🔍 Analyzing source URL and generating initial MT5 construct...")
            prompt = signal_data_extractor_prompt(source_url)
            raw_mt5_code = get_gemini_response(prompt, isJson=False)
            progress_bar.progress(50)
            
            # Step 2: Validation
            status_text.info("🛡️ Validating & optimizing MQL5 syntax...")
            validated_code = validate_mt5_code(raw_mt5_code)
            progress_bar.progress(100)
            status_text.success("✅ Code generation and validation complete!")
            
            # Display results
            st.markdown("---")
            st.markdown("### 💻 Your MT5 Expert Advisor Code")
            st.caption("You can edit the code below directly. The code will also be available for download.")
            
            # Editable code
            edited_code = st.text_area("MQL5 Editor", value=validated_code, height=600, label_visibility="collapsed")
            
            # Additional copy option with standard streamlit
            with st.expander("Show syntax-highlighted code format (Read-only / Copyable)"):
                st.code(edited_code, language="cpp")
                
            st.download_button(
                label="💾 Download .mq5 File",
                data=edited_code,
                file_name="Generated_EA.mq5",
                mime="text/plain",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {str(e)}")

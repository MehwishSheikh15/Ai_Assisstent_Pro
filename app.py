import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from streamlit_chat import message
import requests
from streamlit_lottie import st_lottie
import time

# Load environment variables
load_dotenv()

# Configure Gemini API with better error handling
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is available
if not api_key:
    st.error("🚨 **API Key Missing!**")
    st.markdown("""
    ### To fix this issue:
    
    **For Streamlit Cloud/Community Cloud:**
    1. Go to your app settings in Streamlit Cloud
    2. Click on "Secrets" 
    3. Add your secrets in TOML format:
    ```toml
    GOOGLE_API_KEY = "your_actual_api_key_here"
    ```
    
    **For other deployments:**
    - Set the environment variable `GOOGLE_API_KEY` in your deployment platform
    - Or add it to your hosting service's environment variables section
    
    **Get your API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)
    """)
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ **API Configuration Error:** {str(e)}")
    st.markdown("Please check if your API key is valid and has the necessary permissions.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for impressive UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .stButton button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .output-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-top: 1rem;
    }
    
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .error-container {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .success-container {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini model with error handling
@st.cache_resource
def initialize_model():
    try:
        return genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        st.error(f"❌ **Model Initialization Error:** {str(e)}")
        return None

model = initialize_model()

if not model:
    st.error("❌ **Failed to initialize AI model.** Please check your API key and try again.")
    st.stop()

# Load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.warning(f"⚠️ Could not load animation: {str(e)}")
        return None

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Assistant Pro</h1>
    <p>Powered by Gemini-2.0 Flash | Your Ultimate AI Companion</p>
</div>
""", unsafe_allow_html=True)

# API Status indicator
if api_key:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Not Connected")

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🚀 Navigation")
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "✍️ Content Writer", "🌐 Translator", "💻 Code Assistant", "💬 AI Chatbot"],
        icons=["house", "pencil", "translate", "code-slash", "chat"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
                "border-radius": "10px",
                "padding": "10px"
            },
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )

# Home Page
if selected == "🏠 Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to AI Assistant Pro! 🎉")
        st.markdown("""
        Your comprehensive AI-powered assistant that combines multiple powerful features:
        
        ### 🌟 Features Available:
        """)
        
        features = [
            ("✍️ Content Writer", "Generate short, medium, and long-form content for any purpose"),
            ("🌐 Translator", "Translate text between 10 different languages instantly"),
            ("💻 Code Assistant", "Generate and explain code in multiple programming languages"),
            ("💬 AI Chatbot", "Have intelligent conversations with our advanced AI")
        ]
        
        for title, description in features:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{title}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=300)

# Content Writer
elif selected == "✍️ Content Writer":
    st.markdown("## ✍️ AI Content Writer")
    st.markdown("Generate high-quality content in different lengths for your needs.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("📝 Enter your topic or subject:", placeholder="e.g., Benefits of renewable energy")
        
        content_type = st.selectbox(
            "📊 Select content type:",
            ["Blog Post", "Article", "Social Media Post", "Product Description", "Email", "Essay"]
        )
        
        length = st.selectbox(
            "📏 Select content length:",
            ["Short (100-200 words)", "Medium (300-500 words)", "Long (800-1200 words)"]
        )
        
        tone = st.selectbox(
            "🎭 Select tone:",
            ["Professional", "Casual", "Friendly", "Formal", "Creative", "Persuasive"]
        )
    
    with col2:
        st.markdown("### 💡 Tips for better content:")
        st.info("• Be specific with your topic\n• Choose appropriate tone for your audience\n• Consider your target length")
    
    if st.button("🚀 Generate Content", key="content_gen"):
        if topic:
            with st.spinner("🤖 AI is crafting your content..."):
                prompt = f"""
                Create a {content_type.lower()} about "{topic}" with the following specifications:
                - Length: {length}
                - Tone: {tone}
                - Make it engaging, well-structured, and informative
                - Include relevant examples where appropriate
                """
                
                try:
                    response = model.generate_content(prompt)
                    if response and response.text:
                        st.session_state.generated_content = response.text
                        
                        st.markdown("### 📄 Generated Content:")
                        st.markdown(f"""
                        <div class="output-container">
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Content",
                            data=response.text,
                            file_name=f"{topic.replace(' ', '_')}_content.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ No content generated. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error generating content: {str(e)}")
                    st.markdown("**Possible solutions:**")
                    st.markdown("- Check your internet connection")
                    st.markdown("- Verify your API key is valid")
                    st.markdown("- Try a simpler topic")
        else:
            st.warning("⚠️ Please enter a topic to generate content.")

# Translator
elif selected == "🌐 Translator":
    st.markdown("## 🌐 AI Translator")
    st.markdown("Translate text between multiple languages with high accuracy.")
    
    col1, col2 = st.columns(2)
    
    languages = {
        "English": "en",
        "Spanish": "es", 
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Arabic": "ar"
    }
    
    with col1:
        st.markdown("### 📝 Input")
        source_lang = st.selectbox("From Language:", list(languages.keys()), key="source")
        text_to_translate = st.text_area("Enter text to translate:", height=200, placeholder="Type your text here...")
    
    with col2:
        st.markdown("### 🔄 Output")
        target_lang = st.selectbox("To Language:", list(languages.keys()), index=1, key="target")
        
        if st.button("🔄 Translate", key="translate"):
            if text_to_translate:
                with st.spinner("🌐 Translating..."):
                    prompt = f"""
                    Translate the following text from {source_lang} to {target_lang}.
                    Provide an accurate and natural translation:
                    
                    Text: {text_to_translate}
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            translated_text = response.text
                            
                            st.text_area("Translated text:", value=translated_text, height=200, key="translated")
                            st.success("✅ Translation completed!")
                        else:
                            st.error("❌ Translation failed. Please try again.")
                        
                    except Exception as e:
                        st.error(f"❌ Translation error: {str(e)}")
                        st.markdown("**Possible solutions:**")
                        st.markdown("- Check your internet connection")
                        st.markdown("- Try shorter text")
                        st.markdown("- Verify your API key")
            else:
                st.warning("⚠️ Please enter text to translate.")

# Code Assistant
elif selected == "💻 Code Assistant":
    st.markdown("## 💻 AI Code Assistant")
    st.markdown("Generate, explain, and optimize code in multiple programming languages.")
    
    tab1, tab2 = st.tabs(["🔧 Code Generator", "📖 Code Explainer"])
    
    with tab1:
        st.markdown("### Generate Code")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            programming_lang = st.selectbox(
                "Select Programming Language:",
                ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift"]
            )
            
            code_description = st.text_area(
                "Describe what you want the code to do:",
                height=100,
                placeholder="e.g., Create a function to sort a list of numbers"
            )
            
            complexity = st.selectbox(
                "Code Complexity:",
                ["Beginner", "Intermediate", "Advanced"]
            )
        
        with col2:
            st.markdown("### 🎯 Code Features:")
            include_comments = st.checkbox("Include comments", value=True)
            include_examples = st.checkbox("Include usage examples", value=True)
            include_error_handling = st.checkbox("Include error handling")
        
        if st.button("🚀 Generate Code", key="code_gen"):
            if code_description:
                with st.spinner("💻 Generating code..."):
                    prompt = f"""
                    Generate {programming_lang} code for the following requirement:
                    {code_description}
                    
                    Requirements:
                    - Complexity level: {complexity}
                    - Include comments: {include_comments}
                    - Include usage examples: {include_examples}
                    - Include error handling: {include_error_handling}
                    
                    Provide clean, well-structured, and efficient code.
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            st.markdown("### 📝 Generated Code:")
                            st.code(response.text, language=programming_lang.lower())
                            
                            # Download button
                            file_extension = {
                                "Python": "py", "JavaScript": "js", "Java": "java",
                                "C++": "cpp", "C#": "cs", "Go": "go", "Rust": "rs",
                                "PHP": "php", "Ruby": "rb", "Swift": "swift"
                            }
                            
                            st.download_button(
                                label="📥 Download Code",
                                data=response.text,
                                file_name=f"generated_code.{file_extension.get(programming_lang, 'txt')}",
                                mime="text/plain"
                            )
                        else:
                            st.error("❌ Code generation failed. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Code generation error: {str(e)}")
                        st.markdown("**Possible solutions:**")
                        st.markdown("- Simplify your code description")
                        st.markdown("- Check your internet connection")
                        st.markdown("- Try a different programming language")
            else:
                st.warning("⚠️ Please describe what you want the code to do.")
    
    with tab2:
        st.markdown("### Explain Code")
        
        code_to_explain = st.text_area(
            "Paste your code here:",
            height=200,
            placeholder="Paste the code you want explained..."
        )
        
        explanation_level = st.selectbox(
            "Explanation Level:",
            ["Beginner-friendly", "Technical", "Line-by-line"]
        )
        
        if st.button("🔍 Explain Code", key="code_explain"):
            if code_to_explain:
                with st.spinner("🤔 Analyzing code..."):
                    prompt = f"""
                    Explain the following code in a {explanation_level.lower()} manner:
                    
                    {code_to_explain}
                    
                    Please provide:
                    1. Overall purpose of the code
                    2. How it works
                    3. Key concepts used
                    4. Any potential improvements
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            st.markdown("### 📚 Code Explanation:")
                            st.markdown(f"""
                            <div class="output-container">
                                {response.text}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Code explanation failed. Please try again.")
                        
                    except Exception as e:
                        st.error(f"❌ Code explanation error: {str(e)}")
                        st.markdown("**Try:**")
                        st.markdown("- Pasting simpler code")
                        st.markdown("- Checking your connection")
            else:
                st.warning("⚠️ Please paste code to explain.")

# AI Chatbot
elif selected == "💬 AI Chatbot":
    st.markdown("## 💬 AI Chatbot")
    st.markdown("Have intelligent conversations with our advanced AI assistant.")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for i, (role, content) in enumerate(st.session_state.chat_history):
            if role == "user":
                message(content, is_user=True, key=f"user_{i}")
            else:
                message(content, key=f"bot_{i}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("💭 Type your message:", placeholder="Ask me anything...", key="chat_input")
    
    with col2:
        send_button = st.button("📤 Send", key="send_chat")
    
    # Process chat
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append(("user", user_input))
        
        with st.spinner("🤖 AI is thinking..."):
            try:
                # Create context-aware prompt
                context = "\n".join([f"{role}: {content}" for role, content in st.session_state.chat_history[-5:]])
                prompt = f"""
                You are a helpful AI assistant. Respond to the user's message in a friendly and informative way.
                
                Recent conversation:
                {context}
                
                Please provide a helpful response to the latest user message.
                """
                
                response = model.generate_content(prompt)
                if response and response.text:
                    bot_response = response.text
                    
                    # Add bot response to history
                    st.session_state.chat_history.append(("assistant", bot_response))
                    
                    # Rerun to update chat display
                    st.rerun()
                else:
                    st.error("❌ Failed to get response. Please try again.")
                
            except Exception as e:
                st.error(f"❌ Chat error: {str(e)}")
                st.markdown("**Try:**")
                st.markdown("- Asking a simpler question")
                st.markdown("- Checking your connection")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Chat statistics
    if st.session_state.chat_history:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💬 Total Messages", len(st.session_state.chat_history))
        
        with col2:
            user_messages = len([msg for role, msg in st.session_state.chat_history if role == "user"])
            st.metric("👤 Your Messages", user_messages)
        
        with col3:
            bot_messages = len([msg for role, msg in st.session_state.chat_history if role == "assistant"])
            st.metric("🤖 AI Responses", bot_messages)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 AI Assistant Pro | Powered by Gemini-2.0 Flash</p>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
# AI Assistant Pro 🤖

A comprehensive AI-powered assistant built with Streamlit and Google's Gemini-2.0 Flash model. This application provides multiple AI-powered features including content writing, translation, code assistance, and intelligent chatbot functionality.

## Features 🌟

### ✍️ Content Writer
- Generate content in three different lengths (Short, Medium, Long)
- Multiple content types (Blog posts, articles, social media posts, etc.)
- Various tone options (Professional, Casual, Creative, etc.)
- Download generated content

### 🌐 Translator
- Translate between 10 different languages
- Support for major languages including English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, and Arabic
- Real-time translation with high accuracy

### 💻 Code Assistant
- **Code Generator**: Generate code in 10+ programming languages
- **Code Explainer**: Explain existing code with different complexity levels
- Support for Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift
- Include comments, examples, and error handling options

### 💬 AI Chatbot
- Intelligent conversational AI
- Context-aware responses
- Chat history management
- Real-time statistics

## Installation 🚀

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API key:**
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage 📖

1. **Start the application** using the command above
2. **Navigate** through different features using the sidebar menu
3. **Content Writer**: Enter a topic, select content type, length, and tone
4. **Translator**: Input text and select source/target languages
5. **Code Assistant**: Generate new code or explain existing code
6. **Chatbot**: Have conversations with the AI assistant

## Requirements 📋

- Python 3.7+
- Streamlit
- Google Generative AI
- Other dependencies listed in `requirements.txt`

## Configuration ⚙️

Make sure to configure your `.env` file with a valid Google API key. The application will not work without proper API authentication.

## Features Overview 🎯

- **Modern UI**: Beautiful, responsive interface with gradient designs
- **Multiple AI Functions**: Content writing, translation, code assistance, and chat
- **Real-time Processing**: Fast AI responses with loading indicators
- **Download Options**: Save generated content and code
- **Chat History**: Persistent conversation history
- **Multi-language Support**: Interface and functionality support for multiple languages

## Troubleshooting 🔧

1. **API Key Issues**: Ensure your Google API key is valid and properly set in the `.env` file
2. **Dependencies**: Make sure all required packages are installed
3. **Python Version**: Use Python 3.7 or higher

## Contributing 🤝

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License 📄

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit and Google's Gemini-2.0 Flash**
# PromptForge ⚡

> Transform messy, unstructured thoughts into highly optimized, token-efficient system prompts for AI coding assistants like Cursor and Claude.

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Active-green?style=flat-square)](https://github.com/yourusername/prompt-generator/actions)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 What is PromptForge?

PromptForge is a **production-ready internal tool** that helps developers rapidly generate structured, token-efficient system prompts. Instead of spending hours crafting the perfect prompt, you describe what you want in messy English, and PromptForge transforms it into a polished system prompt optimized for your chosen AI coding assistant.

### The Problem
- ❌ Writing good system prompts is time-consuming
- ❌ Prompts are often too wordy or too brief
- ❌ Hard to optimize for specific tools (Cursor vs Claude)
- ❌ No context persistence across multiple prompts

### The Solution
✅ **PromptForge** — Describe your needs → Get optimized prompts instantly

---

## 🚀 Key Features

### 📝 **One-Click Prompt Generation**
Input your raw thoughts, and the AI instantly generates a structured, production-ready system prompt. No more guesswork.

### 🎯 **Smart Optimization**
Prompts are optimized based on:
- **Target AI**: Cursor, Claude, or Both
- **Style**: Minimal (token-efficient), Balanced (recommended), Detailed (comprehensive)
- **Task Type**: Code Generation, Debugging, Refactoring, Documentation, Testing, etc.
- **Language/Framework**: Python, React, TypeScript, SQL, etc.

### 💾 **Persistent History**
- Store up to 50 recent prompts with full context
- Click to restore any previous prompt
- Automatic FIFO cap (oldest prompts automatically removed)
- Survives server restarts

### 🌙 **Dark-Themed UI**
Professional, modern interface built with:
- Google Fonts (Syne + Space Mono)
- Neon green accent (`#7fff6e`) on dark background (`#0a0a0f`)
- Responsive layout (desktop and mobile optimized)
- Real-time feedback (loading spinners, error toasts, success messages)

### 🔗 **Direct Ollama Cloud Integration**
- No third-party SDK bloat (uses `httpx` for async HTTP)
- Direct API calls to Ollama Cloud's `deepseek-v3:671b` model
- Bearer token authentication via `.env`
- 120-second timeout for longer prompts

### 📊 **Token Counting**
Each generated prompt shows token usage, helping you understand cost and complexity.

### 🧪 **Comprehensive Tests**
- 25+ automated tests covering all functionality
- CI/CD pipeline runs tests on every commit
- Failed tests prevent deployment

---

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI 0.110.0 | REST API framework, async support |
| **Server** | Uvicorn 0.27.1 | ASGI server, production-ready |
| **HTTP Client** | httpx 0.27.0 | Async HTTP requests to Ollama Cloud |
| **Data Validation** | Pydantic 2.6.3 | Type-safe request/response models |
| **Config** | python-dotenv 1.0.1 | Environment variable management |
| **Frontend** | Vanilla HTML/CSS/JS | Single-file UI, no build step |
| **Testing** | pytest 9.0.2 | Automated test framework |
| **CI/CD** | GitHub Actions | Automated testing & deployment |

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git
- Ollama Cloud API key

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/prompt-generator.git
   cd prompt-generator
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Edit .env file and add your Ollama API key
   OLLAMA_API_KEY=your_api_key_here
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the app**
   Open your browser and go to:
   ```
   http://localhost:8000
   ```

---

## 📖 Usage Guide

### Basic Workflow

1. **Enter your raw input** in the textarea (left panel)
   - Example: "I want an AI that helps me write Python code with strong type hints"

2. **Select settings** (left sidebar):
   - **Target**: Cursor, Claude, or Both
   - **Task Type**: Code Generation, Debugging, Refactoring, etc.
   - **Style**: Minimal, Balanced, or Detailed
   - **Language** (optional): Python, React, TypeScript, etc.

3. **Click "Generate Prompt"**
   - Loading spinner appears
   - API calls Ollama Cloud's deepseek model
   - Prompt appears in the right panel

4. **Copy the prompt**
   - Click "📋 Copy Prompt" button
   - Toast confirms: "✓ Copied!"
   - Paste into your AI tool (Cursor, Claude, etc.)

### Understanding Style Differences

| Style | Tokens | Best For | Example Use |
|-------|--------|----------|-------------|
| **Minimal** | 50-200 | Quick, code-focused tasks | "Refactor this function" |
| **Balanced** | 300-500 | General purpose (most common) | "Build a REST API in Python" |
| **Detailed** | 600-1000+ | Complex, multi-faceted tasks | "Design a microservices architecture" |

### History

- **View history**: Check the left sidebar for recent prompts
- **Restore**: Click any history item to restore inputs and output
- **Clear**: Click "Clear History" to delete all saved prompts
- **Persistence**: History survives server restarts (stored in `prompt_history.json`)

---

## 🏗️ Project Structure

```
promptforge/
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # GitHub Actions CI/CD pipeline
├── requirements.txt             # Python dependencies
├── Procfile                      # Heroku deployment config
├── runtime.txt                   # Python version for Heroku
├── Dockerfile                    # Docker configuration
├── main.py                       # FastAPI application entry point
├── src/
│   ├── __init__.py              # Python package marker
│   ├── models.py                # Pydantic models
│   ├── generator.py             # Ollama API client & prompt generation
│   └── history.py               # JSON persistence layer
├── static/
│   └── index.html               # Single-file frontend UI
├── tests/
│   ├── conftest.py              # Pytest configuration
│   └── test_generator.py        # Automated tests (25+ test cases)
├── MODEL_RESPONSE_STRUCTURE.txt # Reference guide for model outputs
├── GITHUB_SECRETS_TEMPLATE.txt  # GitHub secrets setup guide
└── DEPLOYMENT_GUIDE.md          # Heroku deployment instructions
```

---

## 🔌 API Endpoints

### Generate Prompt
```http
POST /api/generate
Content-Type: application/json

{
  "raw_input": "I want an AI that helps with Python code",
  "target": "Claude",
  "task_type": "Code Generation",
  "style": "Balanced",
  "language": "Python"
}
```

**Response:**
```json
{
  "prompt": "You are a Python coding assistant...",
  "tokens_used": 487,
  "error": ""
}
```

### Get History
```http
GET /api/history
```

**Response:**
```json
{
  "items": [
    {
      "raw_input": "...",
      "target": "Claude",
      "task_type": "Code Generation",
      "style": "Balanced",
      "language": "Python",
      "prompt": "...",
      "tokens_used": 487,
      "timestamp": "2026-04-07T10:00:00Z"
    }
  ],
  "stats": {
    "total_items": 5,
    "max_items": 50
  }
}
```

### Clear History
```http
POST /api/history/clear
```

**Response:**
```json
{
  "message": "History cleared successfully"
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

### App Info
```http
GET /api/info
```

**Response:**
```json
{
  "name": "PromptForge",
  "version": "1.0.0",
  "description": "Transform messy thoughts into structured system prompts"
}
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Class
```bash
pytest tests/test_generator.py::TestMarkdownFenceStripping -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

### Watch Tests (Auto-run on file changes)
```bash
pip install pytest-watch
ptw tests/ -v
```

### Test Coverage

Current test suite covers:
- ✅ Markdown fence stripping (5 tests)
- ✅ System prompt generation (6 tests)
- ✅ User message formatting (5 tests)
- ✅ History persistence (5 tests)
- ✅ Response models (2 tests)
- ✅ Integration workflows (2 tests)

**Total: 25 tests, all passing** ✅

---

## 🔒 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OLLAMA_API_KEY=your_api_key_here
```

**Important:** 
- Add `.env` to `.gitignore` (NEVER commit API keys)
- For deployment, use GitHub Secrets instead

### API Key Setup

1. Get your API key from [Ollama Cloud](https://ollama.com)
2. Add to `.env` for local development
3. Add to GitHub Secrets for deployed app
4. Add to Heroku Config Vars for production

---

## 📊 How It Works

### Request Flow

```
1. User Input (Frontend)
   └─→ Raw thoughts, target, style, language

2. API Request
   └─→ POST /api/generate with PromptRequest JSON

3. Backend Processing
   ├─→ Build system prompt (based on target + style)
   ├─→ Build user message (with language if provided)
   └─→ Combine both

4. Ollama Cloud API Call
   └─→ POST https://ollama.com/api/generate
       with model: "deepseek-v3:671b"

5. Response Processing
   ├─→ Extract generated prompt
   ├─→ Strip markdown code fences
   ├─→ Count tokens
   └─→ Save to history

6. Return to Frontend
   └─→ PromptResponse JSON (prompt + tokens + error)

7. User Sees Result
   └─→ Prompt displayed, copy button available
```

### Token Counting

Tokens are estimated based on:
- Model's actual token count (if provided by Ollama)
- Word count approximation (if explicit count unavailable)
- Typically: 1 token ≈ 4 characters

---

## 🚀 Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Response Time** | 10-30s | Deepseek model is slow but accurate |
| **Max Prompt Length** | 2000 tokens | Ollama API limit |
| **History Limit** | 50 items | FIFO automatic cap |
| **Request Timeout** | 120 seconds | Prevents hanging requests |
| **Concurrent Requests** | Unlimited | AsyncIO handles multiple users |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "KeyError: OLLAMA_API_KEY"
Make sure `.env` exists with correct format:
```
OLLAMA_API_KEY=your_key_here
```

### "Connection error to Ollama Cloud"
- Check internet connection
- Verify API key is correct
- Wait 30 seconds and retry

### Tests failing locally
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests with verbose output
pytest tests/ -v --tb=short
```

### Port 8000 already in use
```bash
# Use a different port
uvicorn main:app --port 8001
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and test: `pytest tests/ -v`
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

### Development Workflow

```bash
# Create virtual env
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Install dev dependencies
pip install -r requirements.txt

# Make code changes
# ... edit files ...

# Run tests
pytest tests/ -v

# Start server for testing
uvicorn main:app --reload

# Commit and push
git add .
git commit -m "Your message"
git push origin main
```

---

## 📈 Future Enhancements

Planned features for future releases:

- [ ] **Multi-chat system** — Project-specific context across multiple prompts
- [ ] **SQLite database** — Replace JSON for better scalability
- [ ] **Conversation memory** — AI remembers context from previous messages
- [ ] **Prompt templates** — Pre-built templates for common scenarios
- [ ] **Export/import** — Download history as CSV/JSON
- [ ] **Advanced search** — Find prompts by keyword, target, style
- [ ] **Custom models** — Support multiple Ollama models beyond deepseek-v3
- [ ] **Response streaming** — See prompt generation in real-time
- [ ] **Keyboard shortcuts** — Ctrl+Enter to generate, etc.
- [ ] **Light/dark theme toggle** — User preference storage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mustafa Waqar**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: mustafa.waqar02@gmail.com

---

## 🙏 Acknowledgments

- **Ollama Cloud** — For the `deepseek-v3:671b` model API
- **FastAPI** — Modern, async-first web framework
- **httpx** — Pure Python HTTP client with async support
- **Pydantic** — Type validation and serialization

---

## 📞 Support

For issues, questions, or suggestions:

1. Check [MODEL_RESPONSE_STRUCTURE.txt](MODEL_RESPONSE_STRUCTURE.txt) for model output reference
2. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help
3. Review [tests/test_generator.py](tests/test_generator.py) for usage examples
4. Open an issue on GitHub

---

## 🎯 Quick Links

- **GitHub**: [Repository](https://github.com/yourusername/prompt-generator)
- **Demo**: [Live App](https://promptforge-yourname.herokuapp.com) (when deployed)
- **API Docs**: Available at `/docs` when server is running
- **Tests**: `pytest tests/ -v`

---

<div align="center">

**Built with ❤️ by developers, for developers**

Made with [FastAPI](https://fastapi.tiangolo.com/) • [httpx](https://www.python-httpx.org/) • [Ollama Cloud](https://ollama.com/)

</div>

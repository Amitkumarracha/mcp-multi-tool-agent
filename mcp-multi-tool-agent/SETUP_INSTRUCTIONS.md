# Setup Instructions for MCP Multi-Tool Agent

## Quick Start Guide

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd mcp-multi-tool-agent

# Create and activate virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install the project
pip install -e .
```

### Step 2: Configure API Keys

Your API keys are already in `.env`:
```env
NEWS_API_KEY=a46b92cf45594adca2b26ef420f98494
CURRENCY_API_KEY=cur_live_Qg14ytJlW1IQ2bFix8QP6fE40RFQWKi32fTpky6g
```

**You still need to add:**
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- `TAVILY_API_KEY` - Get from https://tavily.com/

### Step 3: Test the Agent

```bash
python src/agent.py
```

Try these test queries:
1. "Search for latest news about generative AI"
2. "Convert 1000 USD to EUR and GBP"
3. "What's 25 * 38 + 150?"

### Step 4: Configure Claude Desktop (Optional)

1. Find your project's absolute path:
   ```bash
   pwd  # On macOS/Linux
   cd   # On Windows (shows current directory)
   ```

2. Edit `claude_desktop_config.json` and replace `REPLACE_WITH_YOUR_PROJECT_PATH` with the full path

3. Copy the config to Claude Desktop:
   
   **macOS:**
   ```bash
   cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   **Windows:**
   ```powershell
   copy claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json
   ```

4. Restart Claude Desktop

5. Test in Claude:
   - "Search for news about machine learning"
   - "Convert 5000 INR to USD"
   - "Calculate compound interest: 10000 * (1.08)^5"

### Step 5: Take Screenshots

Open Claude Desktop and take screenshots of:

1. **Tool List**: The MCP tools available (should show in Claude's UI)
2. **News Query**: "Get top technology headlines from India"
3. **Currency Query**: "Convert 50000 INR to USD, EUR, and JPY"
4. **Combined Query**: "What's the latest news about cryptocurrency and convert 1 BTC to USD"

Save screenshots as:
- `screenshots/tools_available.png`
- `screenshots/news_query.png`
- `screenshots/currency_query.png`
- `screenshots/combined_query.png`

## Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # macOS/Linux
set PYTHONPATH=%PYTHONPATH%;%cd%\src          # Windows
```

### Issue: NewsAPI returns 426 error
**Solution:** You're using the free tier. Only current month news is available. Try:
- "Search for news about AI from the last week"
- Upgrade to paid tier for historical news

### Issue: MCP servers not connecting in Claude
**Solution:**
1. Check the path in `claude_desktop_config.json` is absolute
2. Ensure Python is in your PATH
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

### Issue: Currency API rate limit
**Solution:** The free tier has limits. The code automatically falls back to exchangerate-api.com if needed.

## Next Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: MCP Multi-Tool Agent"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/mcp-multi-tool-agent.git
   git push -u origin main
   ```

2. **Update README with your details:**
   - Replace "Your Name" in `pyproject.toml`
   - Add your GitHub username in README links
   - Add your email

3. **Create screenshots folder:**
   ```bash
   mkdir screenshots
   ```

4. **Test all features** and document any issues

## Resume Integration

Add this to your resume:

**Projects:**
- **MCP Multi-Tool Agent** | Python, LangChain, LangGraph, MCP
  - Built multi-tool AI agent integrating NewsAPI and CurrencyAPI via Model Context Protocol
  - Implemented agentic AI with autonomous tool selection and ReAct reasoning patterns
  - Demonstrated MCP integration, async programming, and production-grade error handling
  - GitHub: github.com/YOUR_USERNAME/mcp-multi-tool-agent

## API Key Management

**Security Best Practices:**
- ✅ Never commit `.env` to Git (already in `.gitignore`)
- ✅ Use environment variables for all secrets
- ✅ Provide `.env.example` for others
- ⚠️ When sharing screenshots, blur/remove any visible API keys

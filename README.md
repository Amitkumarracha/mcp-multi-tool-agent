# MCP Multi-Tool Agent

> **Built to demonstrate MCP integration as specified in Dassault Systèmes JD**

An intelligent AI agent built with the **Model Context Protocol (MCP)** that integrates multiple specialized tools for news search, currency conversion, web search, and mathematical computations. This project showcases advanced Agentic AI concepts, tool calling, and context engineering using LangChain and LangGraph.

## 🎯 Overview

This multi-tool agent demonstrates proficiency in:
- **Model Context Protocol (MCP)** - Connecting AI systems with external tools and data sources
- **Agentic AI** - Autonomous task execution and dynamic tool selection
- **Tool Calling & Function Calling** - Seamless integration of multiple API services
- **Context Engineering** - Efficient prompt engineering and instruction tuning
- **LangGraph** - ReAct agent pattern implementation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LangChain Agent (GPT-4)                  │
│                     LangGraph ReAct Pattern                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ MCP Adapter
                       │
        ┌──────────────┴──────────────┐
        │   MCP Client Orchestrator   │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┼──────────────┬────────────┐
        │              │               │            │
┌───────▼───────┐ ┌───▼──────┐ ┌─────▼─────┐ ┌───▼──────┐
│  News Server  │ │ Currency │ │  Tavily   │ │   Math   │
│   (NewsAPI)   │ │  Server  │ │  Server   │ │  Server  │
└───────┬───────┘ └────┬─────┘ └─────┬─────┘ └────┬─────┘
        │              │              │             │
┌───────▼───────┐ ┌────▼──────┐ ┌────▼──────┐ ┌───▼──────┐
│  NewsAPI.org  │ │ Currency  │ │  Tavily   │ │  Local   │
│   REST API    │ │  API.com  │ │   API     │ │  Eval    │
└───────────────┘ └───────────┘ └───────────┘ └──────────┘
```

### Component Breakdown

1. **LangChain Agent Layer**: Orchestrates tool selection using GPT-4 with ReAct reasoning
2. **MCP Client**: Manages multiple MCP server connections via stdio transport
3. **MCP Servers**: Four specialized servers exposing tools via Model Context Protocol
   - **News Server**: Real-time news search and top headlines
   - **Currency Server**: Live currency conversion and exchange rates
   - **Tavily Server**: Web search and research capabilities
   - **Math Server**: Mathematical expression evaluation

## 🛠️ Available Tools

### News Tools (NewsAPI)
- `search_news(query, language, sort_by, page_size)` - Search news articles by keyword
- `get_top_headlines(country, category, page_size)` - Get top headlines by country/category

### Currency Tools (CurrencyAPI)
- `convert_currency(amount, from_currency, to_currency)` - Convert between currencies
- `get_exchange_rates(base_currency)` - Get all exchange rates for a base currency
- `compare_currencies(amount, base_currency, target_currencies)` - Compare across multiple currencies

### Web Search Tools (Tavily)
- `search_web(query)` - Search the web for current information
- `search_news(query)` - Search for news articles

### Math Tools
- `evaluate_expression(expression)` - Evaluate mathematical expressions

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip or uv package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-multi-tool-agent.git
cd mcp-multi-tool-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Required API Keys

Get your free API keys:
- **OpenAI**: https://platform.openai.com/api-keys
- **Tavily**: https://tavily.com/
- **NewsAPI**: https://newsapi.org/
- **CurrencyAPI**: https://currencyapi.com/ (optional - has free fallback)

## 💻 Usage

### As CLI Agent

```bash
python src/agent.py
```

Then enter your query:
```
Query: What are the latest AI news and how much is 1000 USD in EUR?
```

### With Claude Desktop

1. Copy your project path
2. Edit `claude_desktop_config.json` and replace `REPLACE_WITH_YOUR_PROJECT_PATH`
3. Copy the JSON content to Claude Desktop's config:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
4. Restart Claude Desktop
5. The tools will be available in Claude!

## 📸 Example Queries & Outputs

### Example 1: News Search

**Query:**
```
Search for the latest news about artificial intelligence in healthcare
```

**Output:**
```
Found 5 recent articles about AI in healthcare:

1. "AI Revolutionizes Cancer Detection" - TechCrunch
   - Published: 2026-06-15
   - AI models now detect cancer with 98% accuracy...
   
2. "Hospital Implements GPT-4 for Patient Care" - Healthcare IT News
   - Published: 2026-06-14
   - Major hospital system deploys AI assistants...
   
[Full article details with URLs]
```

### Example 2: Currency Conversion

**Query:**
```
Convert 50000 INR to USD, EUR, and GBP
```

**Output:**
```
Currency Comparison for 50,000 INR:

USD: $601.20 (Rate: 0.012024)
EUR: €556.32 (Rate: 0.011126)
GBP: £476.85 (Rate: 0.009537)

Last Updated: 2026-06-18
```

### Example 3: Multi-Tool Query

**Query:**
```
What's the latest news about Bitcoin and how much is 1 BTC worth in USD and INR?
```

**Agent Reasoning:**
1. Uses `search_news` to find Bitcoin articles
2. Uses `search_web` to get current BTC price
3. Uses `convert_currency` for BTC to USD
4. Uses `convert_currency` for BTC to INR
5. Synthesizes results into coherent response

**Output:**
```
Latest Bitcoin News:
- "Bitcoin Reaches New All-Time High" - CoinDesk (2026-06-17)
- "Major Banks Adopt Bitcoin for Cross-Border Payments" - Bloomberg

Current BTC Value:
- 1 BTC = $71,234 USD
- 1 BTC = ₹5,921,475 INR

[Detailed analysis with full article summaries]
```

### Example 4: Complex Calculation with Context

**Query:**
```
If I invest $10,000 in a fund that grows 8.5% annually, how much will I have after 5 years in USD and EUR?
```

**Agent Reasoning:**
1. Uses `evaluate_expression` to calculate compound interest
2. Uses `convert_currency` to convert result to EUR

**Output:**
```
Investment Calculation:
Initial: $10,000
Annual Rate: 8.5%
Time Period: 5 years

Future Value: $15,036.56 USD
Equivalent: €13,912.34 EUR

Formula Used: 10000 * (1 + 0.085)^5
```

## 🔧 Technical Implementation

### Graceful Shutdown
- Signal handling (SIGINT, SIGTERM)
- Proper subprocess cleanup
- Async task cancellation

### Error Handling
- API rate limiting management
- Network error recovery
- Fallback mechanisms (currency API)

### Security
- Environment variable-based API key management
- No hardcoded credentials
- Secure subprocess communication via stdio

## 🎓 Learning Outcomes

This project demonstrates:

✅ **MCP Integration** - Building and connecting MCP servers  
✅ **Agentic AI** - Autonomous tool selection and task execution  
✅ **LangChain/LangGraph** - Agent orchestration and ReAct patterns  
✅ **API Integration** - Working with multiple REST APIs  
✅ **Async Programming** - Python asyncio for concurrent operations  
✅ **Error Handling** - Production-grade error management  
✅ **Documentation** - Professional README and code documentation  

## 🧪 Testing MCP Tools

Test individual MCP servers:

```bash
# Test News Server
python -c "from src.mcpserver.news import run_server; run_server()"

# Test Currency Server
python -c "from src.mcpserver.currency import run_server; run_server()"
```

## 📦 Project Structure

```
mcp-multi-tool-agent/
├── src/
│   ├── agent.py              # Main LangChain agent
│   ├── mcpserver/
│   │   ├── news.py           # NewsAPI MCP server
│   │   ├── currency.py       # CurrencyAPI MCP server
│   │   ├── tavily.py         # Tavily search MCP server
│   │   ├── math_server.py    # Math evaluation MCP server
│   │   └── __init__.py
│   └── __init__.py
├── pyproject.toml            # Project configuration
├── .env.example              # Environment template
├── .env                      # Your API keys (gitignored)
├── claude_desktop_config.json # Claude Desktop integration
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## 🔗 Related Technologies

- **MCP**: https://modelcontextprotocol.io/
- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **NewsAPI**: https://newsapi.org/
- **CurrencyAPI**: https://currencyapi.com/

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Author

Built for Dassault Systèmes AI/ML Internship application to demonstrate:
- Model Context Protocol (MCP) expertise
- Agentic AI and multi-agent systems
- LLM integration and orchestration
- Production-grade Python development

---

**⚡ Built to demonstrate MCP integration as specified in Dassault Systèmes JD**

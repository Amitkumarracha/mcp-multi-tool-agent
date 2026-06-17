# MCP Multi-Tool Agent - Usage Examples

This document provides comprehensive examples of using the MCP Multi-Tool Agent for various tasks.

## Table of Contents
- [News Search Examples](#news-search-examples)
- [Currency Conversion Examples](#currency-conversion-examples)
- [Web Search Examples](#web-search-examples)
- [Math Examples](#math-examples)
- [Combined Multi-Tool Examples](#combined-multi-tool-examples)

---

## News Search Examples

### Example 1: Technology News Search

**Query:**
```
Search for the latest news about generative AI and large language models
```

**Expected Tools Used:**
- `search_news(query="generative AI large language models", language="en", sort_by="publishedAt", page_size=5)`

**Sample Output:**
```
Found 5 recent articles about generative AI and large language models:

1. "OpenAI Announces GPT-5 with Revolutionary Capabilities"
   Source: TechCrunch
   Published: 2026-06-17
   Description: OpenAI has unveiled GPT-5, featuring enhanced reasoning...
   URL: https://techcrunch.com/...

2. "Google Gemini Ultra Surpasses Human Performance on Complex Tasks"
   Source: VentureBeat
   Published: 2026-06-16
   Description: Google's latest AI model demonstrates unprecedented...
   URL: https://venturebeat.com/...

[... more articles ...]
```

### Example 2: Top Headlines by Category

**Query:**
```
Get the top 5 technology headlines from the United States
```

**Expected Tools Used:**
- `get_top_headlines(country="us", category="technology", page_size=5)`

**Sample Output:**
```
Top 5 Technology Headlines (United States):

1. "Apple Unveils AI-Powered iPhone 18"
   Source: The Verge
   Published: 2026-06-18

2. "Microsoft Announces Breakthrough in Quantum Computing"
   Source: CNET
   Published: 2026-06-18

[... more headlines ...]
```

### Example 3: Country-Specific News

**Query:**
```
What are the top business news stories in India today?
```

**Expected Tools Used:**
- `get_top_headlines(country="in", category="business", page_size=5)`

---

## Currency Conversion Examples

### Example 4: Simple Currency Conversion

**Query:**
```
Convert 50000 Indian Rupees to US Dollars
```

**Expected Tools Used:**
- `convert_currency(amount=50000, from_currency="INR", to_currency="USD")`

**Sample Output:**
```
Currency Conversion:
50,000 INR = 601.20 USD

Exchange Rate: 1 INR = 0.012024 USD
Last Updated: 2026-06-18
```

### Example 5: Multiple Currency Comparison

**Query:**
```
I have 10000 USD. Show me how much that is in EUR, GBP, JPY, and INR.
```

**Expected Tools Used:**
- `compare_currencies(amount=10000, base_currency="USD", target_currencies="EUR,GBP,JPY,INR")`

**Sample Output:**
```
$10,000 USD is equivalent to:

🇪🇺 EUR: €9,255.32 (Rate: 0.925532)
🇬🇧 GBP: £7,932.41 (Rate: 0.793241)
🇯🇵 JPY: ¥1,485,320 (Rate: 148.532)
🇮🇳 INR: ₹831,475 (Rate: 83.1475)

Last Updated: 2026-06-18
```

### Example 6: Get All Exchange Rates

**Query:**
```
What are the current exchange rates for Euro?
```

**Expected Tools Used:**
- `get_exchange_rates(base_currency="EUR")`

**Sample Output:**
```
Current Exchange Rates for EUR:

Base Currency: EUR
Total Rates: 161

Major Currencies:
- USD: 1.0804
- GBP: 0.8570
- JPY: 160.45
- INR: 89.82
- CNY: 7.8421
- AUD: 1.6523

Last Updated: 2026-06-18
```

---

## Web Search Examples

### Example 7: Current Information Search

**Query:**
```
What is the current Bitcoin price?
```

**Expected Tools Used:**
- `search_web(query="current Bitcoin price USD")`

**Sample Output:**
```
Current Bitcoin Price:

According to recent data from CoinMarketCap and major exchanges:
- Bitcoin (BTC): $71,234.56 USD
- 24h Change: +2.34%
- Market Cap: $1.39T

Last Updated: 2026-06-18 14:32 UTC
```

### Example 8: Research Query

**Query:**
```
Search the web for information about Model Context Protocol
```

**Expected Tools Used:**
- `search_web(query="Model Context Protocol MCP")`

---

## Math Examples

### Example 9: Basic Calculation

**Query:**
```
Calculate 1847 * 395 + 2156
```

**Expected Tools Used:**
- `evaluate_expression(expression="1847 * 395 + 2156")`

**Sample Output:**
```
Calculation Result:

Expression: 1847 * 395 + 2156
Result: 731,721
```

### Example 10: Complex Mathematical Expression

**Query:**
```
Evaluate (25 * 38)^2 - sqrt(1024) + 15.5
```

**Expected Tools Used:**
- `evaluate_expression(expression="(25 * 38)**2 - 1024**0.5 + 15.5")`

**Sample Output:**
```
Calculation Result:

Expression: (25 * 38)^2 - √1024 + 15.5
Result: 902,483.5
```

---

## Combined Multi-Tool Examples

### Example 11: Investment Analysis

**Query:**
```
If I invest 100,000 INR and it grows at 12% annually for 5 years, how much will I have in INR and USD?
```

**Expected Tools Used:**
1. `evaluate_expression(expression="100000 * (1.12)**5")`
2. `convert_currency(amount=<calculated_result>, from_currency="INR", to_currency="USD")`

**Sample Output:**
```
Investment Analysis:

Initial Investment: ₹100,000 INR
Annual Growth Rate: 12%
Investment Period: 5 years

Future Value:
- ₹176,234 INR (calculated using compound interest formula)
- $2,119.15 USD (at current exchange rate)

Formula Used: Principal × (1 + rate)^time
Calculation: 100,000 × (1.12)^5 = 176,234

Exchange Rate: 1 INR = 0.012024 USD (as of 2026-06-18)
```

### Example 12: Travel Planning

**Query:**
```
I'm traveling from India to Europe. What's the latest travel news, and how much is 50,000 INR in EUR?
```

**Expected Tools Used:**
1. `search_news(query="India Europe travel", language="en")`
2. `convert_currency(amount=50000, from_currency="INR", to_currency="EUR")`

**Sample Output:**
```
Travel Information:

💶 Currency Conversion:
₹50,000 INR = €556.32 EUR
Exchange Rate: 1 INR = 0.011126 EUR

📰 Latest Travel News:

1. "Air India Launches New Direct Routes to Europe"
   Source: Economic Times
   Published: 2026-06-15
   Summary: Air India has announced new direct flights from Delhi and Mumbai...

2. "EU Updates Visa Requirements for Indian Travelers"
   Source: Times of India
   Published: 2026-06-14
   Summary: The European Union has streamlined visa processes...

[... more news ...]
```

### Example 13: Financial News with Currency Context

**Query:**
```
What's the latest news about the Indian Rupee, and show me the current INR to USD, EUR, and GBP rates?
```

**Expected Tools Used:**
1. `search_news(query="Indian Rupee", language="en")`
2. `compare_currencies(amount=1, base_currency="INR", target_currencies="USD,EUR,GBP")`

**Sample Output:**
```
Indian Rupee Analysis:

📊 Current Exchange Rates (1 INR):
- USD: $0.01202 (₹83.15 per dollar)
- EUR: €0.01113 (₹89.82 per euro)
- GBP: £0.00954 (₹104.82 per pound)

📰 Latest INR News:

1. "Rupee Strengthens Against Dollar Amid Strong FII Inflows"
   Source: Business Standard
   Published: 2026-06-17
   Summary: The Indian Rupee appreciated by 0.3% against the US dollar...

2. "RBI Governor Comments on Rupee Volatility"
   Source: Economic Times
   Published: 2026-06-16
   Summary: Reserve Bank of India Governor addressed concerns about...

[... more news ...]
```

### Example 14: Tech Salary Comparison

**Query:**
```
Search for average AI engineer salaries in India, then convert 2,500,000 INR to USD
```

**Expected Tools Used:**
1. `search_web(query="average AI engineer salary India 2026")`
2. `convert_currency(amount=2500000, from_currency="INR", to_currency="USD")`

**Sample Output:**
```
AI Engineer Salary Analysis:

💰 Salary Conversion:
₹25,00,000 INR = $30,060 USD per year

🔍 Salary Information:
Based on recent data:
- Entry Level (0-2 years): ₹6-12 lakhs
- Mid Level (3-5 years): ₹15-25 lakhs
- Senior Level (6-10 years): ₹25-45 lakhs
- Lead/Principal (10+ years): ₹45 lakhs+

Note: AI/ML roles at top companies (Google, Microsoft, Amazon India) 
typically offer 20-40% above market rates.

Exchange Rate: 1 INR = 0.012024 USD (2026-06-18)
```

### Example 15: Cryptocurrency Analysis

**Query:**
```
What's the latest news about Bitcoin, search for its current price, and if it's $71,000, how much is that in INR?
```

**Expected Tools Used:**
1. `search_news(query="Bitcoin", language="en", page_size=3)`
2. `search_web(query="Bitcoin price USD live")`
3. `convert_currency(amount=71000, from_currency="USD", to_currency="INR")`

**Sample Output:**
```
Bitcoin Analysis:

💰 Price Conversion:
$71,000 USD = ₹59,03,925 INR
(1 BTC = ₹59.04 lakhs)

📰 Latest Bitcoin News:

1. "Bitcoin Reaches New All-Time High of $71,500"
   Source: CoinDesk
   Published: 2026-06-18
   Summary: Bitcoin has surged past $71,000 mark following...

2. "Major Banks Announce Bitcoin Custody Services"
   Source: Bloomberg
   Published: 2026-06-17
   Summary: Leading financial institutions are now offering...

🔍 Current Market Data:
- Price: $71,234 USD
- 24h Change: +3.2%
- Market Cap: $1.39 Trillion
- Volume: $42.5 Billion

Exchange Rate: 1 USD = 83.15 INR (2026-06-18)
```

---

## Advanced Agentic Workflows

### Example 16: Multi-Step Research Task

**Query:**
```
I want to attend an AI conference. Search for upcoming AI conferences, 
then calculate the cost: registration $1500 + hotel $800 + flights $600 = total in INR, 
and find recent news about AI conferences in India.
```

**Agent Workflow:**
1. `search_web(query="upcoming AI conferences 2026")`
2. `evaluate_expression(expression="1500 + 800 + 600")`
3. `convert_currency(amount=2900, from_currency="USD", to_currency="INR")`
4. `search_news(query="AI conference India", language="en")`

**Expected Output:**
```
AI Conference Planning:

📅 Upcoming AI Conferences:
- NeurIPS 2026: New Orleans, December 2026
- ICLR 2027: Kigali, Rwanda, May 2027
- CVPR 2026: Seattle, June 2026

💵 Cost Breakdown:
Registration: $1,500
Hotel (5 nights): $800
Flights: $600
─────────────────
Total: $2,900 USD
In INR: ₹2,41,135

📰 AI Conferences in India:

1. "India AI Summit 2026 Attracts Global Tech Leaders"
   Source: The Hindu
   Published: 2026-06-10
   Summary: The India AI Summit concluded in Bangalore with...

2. "IIT Delhi to Host International ML Conference"
   Source: India Today
   Published: 2026-06-05
   Summary: Indian Institute of Technology Delhi will host...
```

---

## Testing These Examples

To test these examples:

1. **Start the agent:**
   ```bash
   python src/agent.py
   ```

2. **Copy any query** from above and paste it at the prompt

3. **Observe** which tools the agent selects and how it chains them together

4. **Expected behavior:**
   - Agent should automatically select the right tools
   - No manual tool specification needed
   - Agent chains multiple tools for complex queries
   - Results are synthesized into coherent responses

---

## Tips for Best Results

1. **Be Specific**: More specific queries lead to better tool selection
2. **Natural Language**: Write queries as you would ask a human
3. **Multiple Tasks**: The agent can handle multi-step workflows automatically
4. **Tool Chaining**: Complex queries that need multiple tools work seamlessly

## API Limits to Keep in Mind

- **NewsAPI Free Tier**: Limited to recent news (last 30 days)
- **CurrencyAPI Free Tier**: 300 requests/month (but has free fallback)
- **Tavily**: Check your plan limits
- **OpenAI**: Token usage applies for agent reasoning

---

**Need more examples?** Check the main [README.md](README.md) for architecture details and setup instructions.

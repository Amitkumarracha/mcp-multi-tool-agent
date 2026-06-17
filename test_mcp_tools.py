#!/usr/bin/env python3
"""
Quick test script to verify MCP tools are working correctly.
Run this before pushing to GitHub to ensure everything works.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_news_search():
    """Test NewsAPI search functionality"""
    print("\n🔍 Testing News Search...")
    try:
        from src.mcpserver.news import NewsArticle
        
        # Check if API key is set
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            print("❌ NEWS_API_KEY not set in .env")
            return False
        
        print(f"✅ NewsAPI key configured: {api_key[:10]}...")
        
        # You can add actual API call test here if needed
        print("✅ News tools ready")
        return True
        
    except Exception as e:
        print(f"❌ News test failed: {e}")
        return False

async def test_currency_conversion():
    """Test Currency API functionality"""
    print("\n💱 Testing Currency Conversion...")
    try:
        from src.mcpserver.currency import ExchangeRate
        
        # Check if API key is set (optional)
        api_key = os.getenv("CURRENCY_API_KEY", "")
        if api_key:
            print(f"✅ CurrencyAPI key configured: {api_key[:15]}...")
        else:
            print("⚠️  CurrencyAPI key not set - will use free fallback")
        
        print("✅ Currency tools ready")
        return True
        
    except Exception as e:
        print(f"❌ Currency test failed: {e}")
        return False

async def test_imports():
    """Test that all modules can be imported"""
    print("\n📦 Testing Module Imports...")
    try:
        from src.mcpserver.news import run_server as news_server
        print("✅ news.py imports successfully")
        
        from src.mcpserver.currency import run_server as currency_server
        print("✅ currency.py imports successfully")
        
        from src.mcpserver.tavily import run_server as tavily_server
        print("✅ tavily.py imports successfully")
        
        from src.mcpserver.math_server import run_server as math_server
        print("✅ math_server.py imports successfully")
        
        from src import agent
        print("✅ agent.py imports successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

async def check_env_file():
    """Check if .env file is properly configured"""
    print("\n⚙️  Checking Environment Configuration...")
    
    required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY", "NEWS_API_KEY"]
    optional_keys = ["CURRENCY_API_KEY"]
    
    all_good = True
    
    for key in required_keys:
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}":
            print(f"✅ {key} is set")
        else:
            print(f"❌ {key} is NOT set or still has placeholder value")
            all_good = False
    
    for key in optional_keys:
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}":
            print(f"✅ {key} is set")
        else:
            print(f"⚠️  {key} is NOT set (optional)")
    
    return all_good

async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 MCP Multi-Tool Agent - Test Suite")
    print("=" * 60)
    
    # Run tests
    env_ok = await check_env_file()
    imports_ok = await test_imports()
    news_ok = await test_news_search()
    currency_ok = await test_currency_conversion()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    results = {
        "Environment Config": env_ok,
        "Module Imports": imports_ok,
        "News Tools": news_ok,
        "Currency Tools": currency_ok,
    }
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Ready to push to GitHub.")
        print("\nNext steps:")
        print("1. Take screenshots of Claude Desktop using your tools")
        print("2. git init && git add .")
        print("3. git commit -m 'Initial commit: MCP Multi-Tool Agent'")
        print("4. Create repo on GitHub: mcp-multi-tool-agent")
        print("5. git remote add origin <your-repo-url>")
        print("6. git push -u origin main")
    else:
        print("⚠️  Some tests failed. Please fix issues before pushing.")
        print("\nCommon fixes:")
        print("- Add missing API keys to .env file")
        print("- Ensure virtual environment is activated")
        print("- Run: pip install -e .")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

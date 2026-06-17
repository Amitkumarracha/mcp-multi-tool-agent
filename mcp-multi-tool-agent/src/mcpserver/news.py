import asyncio
import logging
import sys
import signal
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("news_mcp")

# Flag to track shutdown state
shutdown_requested = False

def signal_handler(sig, frame):
    """Handle termination signals"""
    global shutdown_requested
    logger.info("Received termination signal, initiating shutdown...")
    shutdown_requested = True

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Input/output models
class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    url: str
    source: str
    published_at: str
    author: Optional[str] = None

class NewsResponse(BaseModel):
    articles: List[NewsArticle]
    total_results: int
    query: str

def run_server():
    """Run the News MCP server"""
    try:
        logger.info("Starting News MCP server")
        
        # Create FastMCP server with name
        mcp = FastMCP("News Information")
        
        # Get API key from environment
        news_api_key = os.environ.get("NEWS_API_KEY", "")
        
        @mcp.tool()
        async def search_news(
            query: str,
            language: str = "en",
            sort_by: str = "publishedAt",
            page_size: int = 5
        ) -> NewsResponse:
            """
            Search for news articles by keyword or topic.
            
            Args:
                query: Search query (e.g., 'artificial intelligence', 'climate change')
                language: Language code (en, es, fr, de, etc.)
                sort_by: Sort order ('publishedAt', 'relevancy', 'popularity')
                page_size: Number of articles to return (max 100)
            
            Returns:
                NewsResponse with list of articles and metadata
            """
            global shutdown_requested
            
            if shutdown_requested:
                logger.info("Shutdown requested, canceling news request")
                raise ValueError("Server is shutting down")
            
            if not news_api_key:
                logger.error("NEWS_API_KEY not configured")
                raise ValueError("NEWS_API_KEY environment variable is not set. Get your free API key at https://newsapi.org/")
            
            try:
                logger.info(f"Searching news for: {query}")
                
                # Call NewsAPI everything endpoint
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "language": language,
                    "sortBy": sort_by,
                    "pageSize": min(page_size, 100),
                    "apiKey": news_api_key
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, timeout=10.0)
                    response.raise_for_status()
                    data = response.json()
                
                # Parse response
                articles = []
                for article in data.get("articles", []):
                    articles.append(NewsArticle(
                        title=article.get("title", "No title"),
                        description=article.get("description"),
                        url=article.get("url", ""),
                        source=article.get("source", {}).get("name", "Unknown"),
                        published_at=article.get("publishedAt", ""),
                        author=article.get("author")
                    ))
                
                news_response = NewsResponse(
                    articles=articles,
                    total_results=data.get("totalResults", 0),
                    query=query
                )
                
                logger.info(f"Found {len(articles)} news articles for '{query}'")
                return news_response
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error getting news: {e.response.status_code}")
                raise ValueError(f"News API error: {e.response.status_code}. Check your API key and query.")
            except Exception as e:
                logger.error(f"Error getting news: {str(e)}")
                raise ValueError(f"Error getting news: {str(e)}")
        
        @mcp.tool()
        async def get_top_headlines(
            country: str = "us",
            category: str = "general",
            page_size: int = 5
        ) -> NewsResponse:
            """
            Get top headlines from a specific country and category.
            
            Args:
                country: Country code (us, gb, in, au, ca, etc.)
                category: Category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
                page_size: Number of articles to return (max 100)
            
            Returns:
                NewsResponse with list of top headline articles
            """
            global shutdown_requested
            
            if shutdown_requested:
                logger.info("Shutdown requested, canceling headlines request")
                raise ValueError("Server is shutting down")
            
            if not news_api_key:
                logger.error("NEWS_API_KEY not configured")
                raise ValueError("NEWS_API_KEY environment variable is not set. Get your free API key at https://newsapi.org/")
            
            try:
                logger.info(f"Getting top headlines for {country}/{category}")
                
                # Call NewsAPI top-headlines endpoint
                url = "https://newsapi.org/v2/top-headlines"
                params = {
                    "country": country,
                    "category": category,
                    "pageSize": min(page_size, 100),
                    "apiKey": news_api_key
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, timeout=10.0)
                    response.raise_for_status()
                    data = response.json()
                
                # Parse response
                articles = []
                for article in data.get("articles", []):
                    articles.append(NewsArticle(
                        title=article.get("title", "No title"),
                        description=article.get("description"),
                        url=article.get("url", ""),
                        source=article.get("source", {}).get("name", "Unknown"),
                        published_at=article.get("publishedAt", ""),
                        author=article.get("author")
                    ))
                
                news_response = NewsResponse(
                    articles=articles,
                    total_results=data.get("totalResults", 0),
                    query=f"{category} headlines in {country}"
                )
                
                logger.info(f"Found {len(articles)} top headlines")
                return news_response
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error getting headlines: {e.response.status_code}")
                raise ValueError(f"News API error: {e.response.status_code}. Check your API key and parameters.")
            except Exception as e:
                logger.error(f"Error getting headlines: {str(e)}")
                raise ValueError(f"Error getting headlines: {str(e)}")
        
        # Setup shutdown check task
        async def check_shutdown():
            """Periodically check if shutdown was requested"""
            while not shutdown_requested:
                await asyncio.sleep(0.5)
            logger.info("Shutdown check detected termination request")
            
        # Start the server
        mcp.run(transport="stdio")
            
    except KeyboardInterrupt:
        logger.info("News MCP server stopped by keyboard interrupt")
    except Exception as e:
        logger.error(f"Error running News MCP server: {str(e)}")
    finally:
        logger.info("News MCP server shutdown complete")

if __name__ == "__main__":
    run_server()

import asyncio
import logging
import sys
import signal
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("currency_mcp")

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
class ExchangeRate(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    amount: float
    converted_amount: float
    last_updated: str

class SupportedCurrencies(BaseModel):
    currencies: Dict[str, str]
    count: int

def run_server():
    """Run the Currency MCP server"""
    try:
        logger.info("Starting Currency MCP server")
        
        # Create FastMCP server with name
        mcp = FastMCP("Currency Exchange")
        
        # Get API key from environment (using currencyapi.com)
        currency_api_key = os.environ.get("CURRENCY_API_KEY", "")
        
        @mcp.tool()
        async def convert_currency(
            amount: float,
            from_currency: str = "USD",
            to_currency: str = "EUR"
        ) -> ExchangeRate:
            """
            Convert an amount from one currency to another using real-time exchange rates.
            
            Args:
                amount: Amount to convert
                from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP', 'INR')
                to_currency: Target currency code (e.g., 'EUR', 'USD', 'JPY', 'INR')
            
            Returns:
                ExchangeRate with conversion details and rate
            """
            global shutdown_requested
            
            if shutdown_requested:
                logger.info("Shutdown requested, canceling currency request")
                raise ValueError("Server is shutting down")
            
            try:
                logger.info(f"Converting {amount} {from_currency} to {to_currency}")
                
                from_currency = from_currency.upper()
                to_currency = to_currency.upper()
                
                # Use currencyapi.com or fallback to exchangerate-api.com
                if currency_api_key:
                    # Use currencyapi.com with API key
                    url = "https://api.currencyapi.com/v3/latest"
                    params = {
                        "apikey": currency_api_key,
                        "base_currency": from_currency,
                        "currencies": to_currency
                    }
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    # Extract from currencyapi.com response
                    rates_data = data.get("data", {})
                    if to_currency not in rates_data:
                        raise ValueError(f"Currency code '{to_currency}' not found")
                    
                    rate = rates_data[to_currency].get("value", 0)
                    last_updated = data.get("meta", {}).get("last_updated_at", datetime.utcnow().isoformat())[:10]
                else:
                    # Fallback to free exchangerate-api.com
                    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    rates = data.get("rates", {})
                    if to_currency not in rates:
                        raise ValueError(f"Currency code '{to_currency}' not found")
                    
                    rate = rates[to_currency]
                    last_updated = data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
                
                converted_amount = amount * rate
                
                exchange_rate = ExchangeRate(
                    from_currency=from_currency,
                    to_currency=to_currency,
                    rate=round(rate, 6),
                    amount=amount,
                    converted_amount=round(converted_amount, 2),
                    last_updated=last_updated
                )
                
                logger.info(f"Converted {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
                return exchange_rate
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error converting currency: {e.response.status_code}")
                raise ValueError(f"Currency API error: {e.response.status_code}. Check currency codes.")
            except Exception as e:
                logger.error(f"Error converting currency: {str(e)}")
                raise ValueError(f"Error converting currency: {str(e)}")
        
        @mcp.tool()
        async def get_exchange_rates(base_currency: str = "USD") -> Dict[str, float]:
            """
            Get all current exchange rates for a base currency.
            
            Args:
                base_currency: Base currency code (e.g., 'USD', 'EUR', 'GBP', 'INR')
            
            Returns:
                Dictionary of currency codes to exchange rates
            """
            global shutdown_requested
            
            if shutdown_requested:
                logger.info("Shutdown requested, canceling rates request")
                raise ValueError("Server is shutting down")
            
            try:
                logger.info(f"Getting exchange rates for {base_currency}")
                
                base_currency = base_currency.upper()
                
                # Use currencyapi.com or fallback to exchangerate-api.com
                if currency_api_key:
                    # Use currencyapi.com with API key
                    url = "https://api.currencyapi.com/v3/latest"
                    params = {
                        "apikey": currency_api_key,
                        "base_currency": base_currency
                    }
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    # Extract from currencyapi.com response
                    rates_data = data.get("data", {})
                    rates = {code: info.get("value") for code, info in rates_data.items()}
                    last_updated = data.get("meta", {}).get("last_updated_at", datetime.utcnow().isoformat())[:10]
                else:
                    # Fallback to free exchangerate-api.com
                    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    rates = data.get("rates", {})
                    last_updated = data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
                
                logger.info(f"Retrieved {len(rates)} exchange rates for {base_currency}")
                return {
                    "base_currency": base_currency,
                    "rates": rates,
                    "last_updated": last_updated,
                    "rate_count": len(rates)
                }
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error getting rates: {e.response.status_code}")
                raise ValueError(f"Currency API error: {e.response.status_code}. Check currency code.")
            except Exception as e:
                logger.error(f"Error getting exchange rates: {str(e)}")
                raise ValueError(f"Error getting exchange rates: {str(e)}")
        
        @mcp.tool()
        async def compare_currencies(
            amount: float,
            base_currency: str,
            target_currencies: str
        ) -> List[ExchangeRate]:
            """
            Compare conversion of an amount to multiple target currencies.
            
            Args:
                amount: Amount to convert
                base_currency: Source currency code (e.g., 'USD')
                target_currencies: Comma-separated target currency codes (e.g., 'EUR,GBP,JPY,INR')
            
            Returns:
                List of ExchangeRate objects for each conversion
            """
            global shutdown_requested
            
            if shutdown_requested:
                logger.info("Shutdown requested, canceling comparison request")
                raise ValueError("Server is shutting down")
            
            try:
                logger.info(f"Comparing {amount} {base_currency} across multiple currencies")
                
                base_currency = base_currency.upper()
                targets = [c.strip().upper() for c in target_currencies.split(",")]
                
                # Get all rates for base currency
                if currency_api_key:
                    # Use currencyapi.com with API key
                    url = "https://api.currencyapi.com/v3/latest"
                    params = {
                        "apikey": currency_api_key,
                        "base_currency": base_currency,
                        "currencies": ",".join(targets)
                    }
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, params=params, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    # Extract from currencyapi.com response
                    rates_data = data.get("data", {})
                    rates = {code: info.get("value") for code, info in rates_data.items()}
                    last_updated = data.get("meta", {}).get("last_updated_at", datetime.utcnow().isoformat())[:10]
                else:
                    # Fallback to free exchangerate-api.com
                    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                    
                    rates = data.get("rates", {})
                    last_updated = data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
                
                # Build comparison results
                comparisons = []
                for target in targets:
                    if target in rates:
                        rate = rates[target]
                        converted = amount * rate
                        comparisons.append(ExchangeRate(
                            from_currency=base_currency,
                            to_currency=target,
                            rate=round(rate, 6),
                            amount=amount,
                            converted_amount=round(converted, 2),
                            last_updated=last_updated
                        ))
                
                logger.info(f"Compared {base_currency} to {len(comparisons)} currencies")
                return comparisons
                
            except Exception as e:
                logger.error(f"Error comparing currencies: {str(e)}")
                raise ValueError(f"Error comparing currencies: {str(e)}")
        
        # Start the server
        mcp.run(transport="stdio")
            
    except KeyboardInterrupt:
        logger.info("Currency MCP server stopped by keyboard interrupt")
    except Exception as e:
        logger.error(f"Error running Currency MCP server: {str(e)}")
    finally:
        logger.info("Currency MCP server shutdown complete")

if __name__ == "__main__":
    run_server()

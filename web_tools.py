"""Web Search Tools for Fantasy Football Roast Agent"""

from typing import Dict, List, Any
from strands import tool
from ddgs import DDGS
from config import get_config

config = get_config()

@tool
def search_player_news(player_name: str) -> Dict[str, Any]:
    """Search for recent news about a specific NFL player"""
    if not player_name or player_name.startswith("Player "):
        return {"success": False, "error": "Invalid player name provided"}
    
    # Create search query for fantasy football specific news
    query = f"{player_name} NFL fantasy football news injury status 2025"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query, 
                max_results=config["web_search_results"],
                region="us-en"
            ))
        
        if not results:
            return {"success": False, "error": f"No news found for {player_name}"}
        
        # Filter and format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
                "source": result.get("href", "").split("//")[-1].split("/")[0] if result.get("href") else ""
            })
        
        return {
            "success": True,
            "data": {
                "player_name": player_name,
                "query": query,
                "results": formatted_results
            }
        }
    
    except Exception as e:
        return {"success": False, "error": f"Search error for {player_name}: {str(e)}"}

@tool
def search_fantasy_trends() -> Dict[str, Any]:
    """Search for current fantasy football trends and waiver wire targets"""
    query = "fantasy football week 2 waiver wire targets 2025 NFL trending players"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=config["web_search_results"],
                region="us-en"
            ))
        
        if not results:
            return {"success": False, "error": "No fantasy trends found"}
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
                "source": result.get("href", "").split("//")[-1].split("/")[0] if result.get("href") else ""
            })
        
        return {
            "success": True,
            "data": {
                "query": query,
                "results": formatted_results
            }
        }
    
    except Exception as e:
        return {"success": False, "error": f"Fantasy trends search error: {str(e)}"}

@tool
def search_team_analysis(team_name: str) -> Dict[str, Any]:
    """Search for analysis about a specific fantasy team or NFL team"""
    query = f"{team_name} fantasy football analysis 2025 NFL season outlook"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=3,  # Smaller number for team-specific searches
                region="us-en"
            ))
        
        if not results:
            return {"success": False, "error": f"No analysis found for {team_name}"}
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
                "source": result.get("href", "").split("//")[-1].split("/")[0] if result.get("href") else ""
            })
        
        return {
            "success": True,
            "data": {
                "team_name": team_name,
                "query": query,
                "results": formatted_results
            }
        }
    
    except Exception as e:
        return {"success": False, "error": f"Team analysis search error for {team_name}: {str(e)}"}

@tool
def search_trade_analysis(player1: str, player2: str) -> Dict[str, Any]:
    """Search for trade analysis between two players"""
    query = f"{player1} vs {player2} fantasy football trade analysis value comparison 2025"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=3,
                region="us-en"
            ))
        
        if not results:
            return {"success": False, "error": f"No trade analysis found for {player1} vs {player2}"}
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
                "source": result.get("href", "").split("//")[-1].split("/")[0] if result.get("href") else ""
            })
        
        return {
            "success": True,
            "data": {
                "player1": player1,
                "player2": player2,
                "query": query,
                "results": formatted_results
            }
        }
    
    except Exception as e:
        return {"success": False, "error": f"Trade analysis search error: {str(e)}"}

@tool
def search_injury_reports() -> Dict[str, Any]:
    """Search for current NFL injury reports"""
    query = "NFL injury report week 2 2025 fantasy football impact"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=config["web_search_results"],
                region="us-en"
            ))
        
        if not results:
            return {"success": False, "error": "No injury reports found"}
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
                "source": result.get("href", "").split("//")[-1].split("/")[0] if result.get("href") else ""
            })
        
        return {
            "success": True,
            "data": {
                "query": query,
                "results": formatted_results
            }
        }
    
    except Exception as e:
        return {"success": False, "error": f"Injury report search error: {str(e)}"} 
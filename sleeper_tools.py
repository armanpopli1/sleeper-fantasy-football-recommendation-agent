"""Sleeper API Tools for Fantasy Football Roast Agent"""

import requests
import time
import json
from typing import Dict, List, Optional, Any
from strands import tool
from config import get_config

config = get_config()

# Global player database cache
_player_db = None

def make_api_call(url: str, delay: float = None) -> Optional[Dict]:
    """Make an API call with rate limiting"""
    if delay is None:
        delay = config["rate_limit_delay"]
    
    time.sleep(delay)
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Fantasy Football Roast Agent',
            'Accept': 'application/json'
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error for {url}: {e}")
        return None

def get_player_database() -> Dict[str, Dict]:
    """Get and cache the full NFL player database"""
    global _player_db
    
    if _player_db is None:
        print("🔄 Loading NFL player database...")
        url = config["endpoints"]["players"]
        _player_db = make_api_call(url)
        if _player_db:
            print(f"✅ Loaded {len(_player_db)} players")
        else:
            print("❌ Failed to load player database")
            _player_db = {}
    
    return _player_db

def get_player_name(player_id: str) -> str:
    """Get player name from ID, handling team defenses"""
    if len(player_id) <= 3 and player_id.isupper():
        return f"{player_id} Defense"
    
    players = get_player_database()
    player = players.get(player_id, {})
    
    first_name = player.get('first_name', '')
    last_name = player.get('last_name', '')
    
    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif last_name:
        return last_name
    else:
        return f"Player {player_id}"

@tool
def get_nfl_state() -> Dict[str, Any]:
    """Get current NFL season state and week information"""
    url = config["endpoints"]["nfl_state"]
    nfl_state = make_api_call(url)
    
    if nfl_state:
        return {
            "success": True,
            "data": {
                "current_week": nfl_state.get("week"),
                "season": nfl_state.get("season"),
                "season_type": nfl_state.get("season_type"),
                "league_season": nfl_state.get("league_season"),
                "season_start_date": nfl_state.get("season_start_date")
            }
        }
    return {"success": False, "error": "Failed to get NFL state"}

@tool
def get_league_info() -> Dict[str, Any]:
    """Get comprehensive league information including settings and users"""
    league_id = config["league_id"]
    
    # Get league details
    league_url = config["endpoints"]["league"].format(league_id=league_id)
    league_data = make_api_call(league_url)
    
    if not league_data:
        return {"success": False, "error": "Failed to get league data"}
    
    # Get league users
    users_url = config["endpoints"]["league_users"].format(league_id=league_id)
    users_data = make_api_call(users_url)
    
    if not users_data:
        return {"success": False, "error": "Failed to get league users"}
    
    return {
        "success": True,
        "data": {
            "league_name": league_data.get("name"),
            "total_rosters": league_data.get("total_rosters"),
            "status": league_data.get("status"),
            "season": league_data.get("season"),
            "draft_id": league_data.get("draft_id"),
            "settings": league_data.get("settings", {}),
            "roster_positions": league_data.get("roster_positions", []),
            "scoring_settings": league_data.get("scoring_settings", {}),
            "users": users_data
        }
    }

@tool
def get_team_data(display_name: str) -> Dict[str, Any]:
    """Get comprehensive team data for a specific user by display name"""
    league_info = get_league_info()
    if not league_info["success"]:
        return league_info
    
    # Find user by display name
    target_user = None
    for user in league_info["data"]["users"]:
        if user.get("display_name", "").lower() == display_name.lower():
            target_user = user
            break
    
    if not target_user:
        return {"success": False, "error": f"User '{display_name}' not found in league"}
    
    # Get rosters
    league_id = config["league_id"]
    rosters_url = config["endpoints"]["league_rosters"].format(league_id=league_id)
    rosters_data = make_api_call(rosters_url)
    
    if not rosters_data:
        return {"success": False, "error": "Failed to get roster data"}
    
    # Find user's roster
    user_roster = None
    for roster in rosters_data:
        if roster.get("owner_id") == target_user.get("user_id"):
            user_roster = roster
            break
    
    if not user_roster:
        return {"success": False, "error": f"Roster not found for user '{display_name}'"}
    
    # Add player names to roster
    starters_with_names = []
    bench_with_names = []
    
    starters = user_roster.get("starters", [])
    all_players = user_roster.get("players", [])
    bench = [p for p in all_players if p not in starters]
    
    for player_id in starters:
        starters_with_names.append({
            "player_id": player_id,
            "name": get_player_name(player_id)
        })
    
    for player_id in bench:
        bench_with_names.append({
            "player_id": player_id,
            "name": get_player_name(player_id)
        })
    
    # Calculate league rank
    sorted_rosters = sorted(rosters_data, key=lambda x: x.get("settings", {}).get("fpts", 0), reverse=True)
    league_rank = None
    for i, roster in enumerate(sorted_rosters, 1):
        if roster.get("roster_id") == user_roster.get("roster_id"):
            league_rank = i
            break
    
    return {
        "success": True,
        "data": {
            "user_info": target_user,
            "roster_id": user_roster.get("roster_id"),
            "wins": user_roster.get("settings", {}).get("wins", 0),
            "losses": user_roster.get("settings", {}).get("losses", 0),
            "ties": user_roster.get("settings", {}).get("ties", 0),
            "points_for": user_roster.get("settings", {}).get("fpts", 0),
            "points_against": user_roster.get("settings", {}).get("fpts_against", 0),
            "league_rank": league_rank,
            "total_teams": len(rosters_data),
            "starters": starters_with_names,
            "bench": bench_with_names,
            "waiver_position": user_roster.get("settings", {}).get("waiver_position"),
            "total_moves": user_roster.get("settings", {}).get("total_moves", 0)
        }
    }

@tool
def get_matchup_data(week: int) -> Dict[str, Any]:
    """Get matchup data for a specific week"""
    league_id = config["league_id"]
    matchups_url = config["endpoints"]["league_matchups"].format(league_id=league_id, week=week)
    matchups_data = make_api_call(matchups_url)
    
    if not matchups_data:
        return {"success": False, "error": f"Failed to get matchup data for week {week}"}
    
    return {
        "success": True,
        "data": {
            "week": week,
            "matchups": matchups_data
        }
    }

@tool
def get_trending_players() -> Dict[str, Any]:
    """Get trending add/drop players with names"""
    adds_url = config["endpoints"]["trending_adds"] + f"?limit={config['max_waiver_targets']}"
    drops_url = config["endpoints"]["trending_drops"] + f"?limit={config['max_waiver_targets']}"
    
    trending_adds = make_api_call(adds_url)
    trending_drops = make_api_call(drops_url)
    
    if not trending_adds or not trending_drops:
        return {"success": False, "error": "Failed to get trending players"}
    
    # Add player names
    adds_with_names = []
    for player in trending_adds:
        player_id = player["player_id"]
        adds_with_names.append({
            "player_id": player_id,
            "name": get_player_name(player_id),
            "add_count": player["count"]
        })
    
    drops_with_names = []
    for player in trending_drops:
        player_id = player["player_id"]
        drops_with_names.append({
            "player_id": player_id,
            "name": get_player_name(player_id),
            "drop_count": player["count"]
        })
    
    return {
        "success": True,
        "data": {
            "trending_adds": adds_with_names,
            "trending_drops": drops_with_names
        }
    }

@tool
def get_draft_analysis(draft_id: str) -> Dict[str, Any]:
    """Get draft data and analysis"""
    if not draft_id:
        return {"success": False, "error": "No draft ID provided"}
    
    # Get draft info
    draft_url = config["endpoints"]["draft"].format(draft_id=draft_id)
    draft_data = make_api_call(draft_url)
    
    if not draft_data:
        return {"success": False, "error": "Failed to get draft data"}
    
    # Get draft picks
    picks_url = config["endpoints"]["draft_picks"].format(draft_id=draft_id)
    picks_data = make_api_call(picks_url)
    
    if not picks_data:
        return {"success": False, "error": "Failed to get draft picks"}
    
    # Add player names to picks
    picks_with_names = []
    for pick in picks_data:
        player_id = pick.get("player_id")
        if player_id:
            picks_with_names.append({
                "pick_no": pick.get("pick_no"),
                "round": pick.get("round"),
                "draft_slot": pick.get("draft_slot"),
                "player_id": player_id,
                "player_name": get_player_name(player_id),
                "picked_by": pick.get("picked_by"),
                "roster_id": pick.get("roster_id"),
                "metadata": pick.get("metadata", {})
            })
    
    return {
        "success": True,
        "data": {
            "draft_info": draft_data,
            "picks": picks_with_names
        }
    }

@tool
def calculate_league_averages() -> Dict[str, Any]:
    """Calculate league-wide averages for comparison"""
    league_id = config["league_id"]
    rosters_url = config["endpoints"]["league_rosters"].format(league_id=league_id)
    rosters_data = make_api_call(rosters_url)
    
    if not rosters_data:
        return {"success": False, "error": "Failed to get roster data for averages"}
    
    total_points = sum(roster.get("settings", {}).get("fpts", 0) for roster in rosters_data)
    total_points_against = sum(roster.get("settings", {}).get("fpts_against", 0) for roster in rosters_data)
    total_wins = sum(roster.get("settings", {}).get("wins", 0) for roster in rosters_data)
    total_moves = sum(roster.get("settings", {}).get("total_moves", 0) for roster in rosters_data)
    
    num_teams = len(rosters_data)
    
    return {
        "success": True,
        "data": {
            "avg_points_for": round(total_points / num_teams, 2) if num_teams > 0 else 0,
            "avg_points_against": round(total_points_against / num_teams, 2) if num_teams > 0 else 0,
            "avg_wins": round(total_wins / num_teams, 2) if num_teams > 0 else 0,
            "avg_moves": round(total_moves / num_teams, 2) if num_teams > 0 else 0,
            "total_teams": num_teams
        }
    } 

@tool
def get_all_rosters_with_users() -> Dict[str, Any]:
    """Get all rosters mapped to their users for easier opponent identification"""
    try:
        league_info = get_league_info()
        if not league_info["success"]:
            return {"success": False, "error": "Failed to get league info"}
        
        league_id = config["league_id"]
        rosters_url = config["endpoints"]["league_rosters"].format(league_id=league_id)
        rosters_data = make_api_call(rosters_url)
        
        if not rosters_data:
            return {"success": False, "error": "Failed to get roster data"}
        
        # Map rosters to users
        rosters_with_users = []
        users = league_info["data"]["users"]
        
        for roster in rosters_data:
            owner_id = roster.get("owner_id")
            # Find the user for this roster
            user_info = None
            for user in users:
                if user.get("user_id") == owner_id:
                    user_info = user
                    break
            
            roster_with_user = {
                "roster_id": roster.get("roster_id"),
                "owner_id": owner_id,
                "user_info": user_info,
                "wins": roster.get("settings", {}).get("wins", 0),
                "losses": roster.get("settings", {}).get("losses", 0),
                "points_for": roster.get("settings", {}).get("fpts", 0),
                "points_against": roster.get("settings", {}).get("fpts_against", 0),
                "starters": roster.get("starters", []),
                "players": roster.get("players", []),
                "waiver_position": roster.get("settings", {}).get("waiver_position"),
                "total_moves": roster.get("settings", {}).get("total_moves", 0)
            }
            rosters_with_users.append(roster_with_user)
        
        # Sort by points for ranking
        rosters_with_users.sort(key=lambda x: x["points_for"], reverse=True)
        for i, roster in enumerate(rosters_with_users, 1):
            roster["league_rank"] = i
        
        return {
            "success": True,
            "data": {
                "rosters": rosters_with_users,
                "total_teams": len(rosters_with_users)
            }
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to get rosters with users: {str(e)}"}

@tool
def get_player_details(player_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific player"""
    try:
        players = get_player_database()
        player = players.get(player_id, {})
        
        if not player:
            # Handle team defenses
            if len(player_id) <= 3 and player_id.isupper():
                return {
                    "success": True,
                    "data": {
                        "player_id": player_id,
                        "name": f"{player_id} Defense",
                        "position": "DEF",
                        "team": player_id,
                        "is_defense": True
                    }
                }
            else:
                return {"success": False, "error": f"Player {player_id} not found"}
        
        return {
            "success": True,
            "data": {
                "player_id": player_id,
                "name": get_player_name(player_id),
                "first_name": player.get("first_name", ""),
                "last_name": player.get("last_name", ""),
                "position": player.get("position", ""),
                "team": player.get("team", ""),
                "age": player.get("age"),
                "years_exp": player.get("years_exp"),
                "height": player.get("height", ""),
                "weight": player.get("weight", ""),
                "college": player.get("college", ""),
                "injury_status": player.get("injury_status"),
                "fantasy_positions": player.get("fantasy_positions", []),
                "is_defense": False
            }
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to get player details: {str(e)}"} 
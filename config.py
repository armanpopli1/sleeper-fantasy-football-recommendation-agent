# Fantasy Football Roast Agent Configuration
# =============================================================================
# 🔥 EDIT THESE VALUES FOR YOUR LEAGUE 🔥
# =============================================================================

# League Information
LEAGUE_ID = "1263345992535638016"  # Your Sleeper league ID
SEASON = "2025"                    # Current season year

# Target Configuration  
TARGET_DISPLAY_NAME = "armanpopli"  # Display name of user to roast

# AWS Configuration (for Strands agent)
AWS_REGION = "us-west-2"           # AWS region for Bedrock
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"  # Bedrock model

# API Configuration
SLEEPER_API_BASE = "https://api.sleeper.app/v1"
RATE_LIMIT_DELAY = 0.1  # Delay between API calls (seconds)

# Output Configuration
OUTPUT_DIR = "reports"             # Directory to save HTML reports
REPORT_FILENAME_FORMAT = "roast_{display_name}_{timestamp}.html"

# Report Settings
MAX_WAIVER_TARGETS = 5            # Number of waiver wire recommendations
MAX_TRADE_SUGGESTIONS = 3         # Number of trade suggestions
WEB_SEARCH_RESULTS = 5           # Number of web search results per query

# =============================================================================
# CONSTANTS (Don't change these unless you know what you're doing)
# =============================================================================

# Sleeper API endpoints
ENDPOINTS = {
    "nfl_state": f"{SLEEPER_API_BASE}/state/nfl",
    "user": f"{SLEEPER_API_BASE}/user/{{identifier}}",
    "league": f"{SLEEPER_API_BASE}/league/{{league_id}}",
    "league_users": f"{SLEEPER_API_BASE}/league/{{league_id}}/users", 
    "league_rosters": f"{SLEEPER_API_BASE}/league/{{league_id}}/rosters",
    "league_matchups": f"{SLEEPER_API_BASE}/league/{{league_id}}/matchups/{{week}}",
    "players": f"{SLEEPER_API_BASE}/players/nfl",
    "trending_adds": f"{SLEEPER_API_BASE}/players/nfl/trending/add",
    "trending_drops": f"{SLEEPER_API_BASE}/players/nfl/trending/drop",
    "draft": f"{SLEEPER_API_BASE}/draft/{{draft_id}}",
    "draft_picks": f"{SLEEPER_API_BASE}/draft/{{draft_id}}/picks"
}

# Position mappings for analysis
POSITION_GROUPS = {
    "QB": ["QB"],
    "RB": ["RB"],
    "WR": ["WR"], 
    "TE": ["TE"],
    "FLEX": ["RB", "WR", "TE"],
    "K": ["K"],
    "DEF": ["DEF"]
}

# Scoring weights for player value analysis (PPR)
PPR_WEIGHTS = {
    "passing_yards": 0.04,
    "passing_tds": 4.0,
    "passing_ints": -2.0,
    "rushing_yards": 0.1,
    "rushing_tds": 6.0,
    "receiving_yards": 0.1,
    "receiving_tds": 6.0,
    "receptions": 1.0,  # PPR bonus
    "fumbles_lost": -2.0
}

def get_config():
    """Return configuration dictionary"""
    return {
        "league_id": LEAGUE_ID,
        "season": SEASON,
        "target_display_name": TARGET_DISPLAY_NAME,
        "aws_region": AWS_REGION,
        "model_id": MODEL_ID,
        "sleeper_api_base": SLEEPER_API_BASE,
        "rate_limit_delay": RATE_LIMIT_DELAY,
        "output_dir": OUTPUT_DIR,
        "report_filename_format": REPORT_FILENAME_FORMAT,
        "max_waiver_targets": MAX_WAIVER_TARGETS,
        "max_trade_suggestions": MAX_TRADE_SUGGESTIONS,
        "web_search_results": WEB_SEARCH_RESULTS,
        "endpoints": ENDPOINTS,
        "position_groups": POSITION_GROUPS,
        "ppr_weights": PPR_WEIGHTS
    }

def create_runtime_config(
    league_id: str,
    target_name: str,
    api_key: str,
    provider: str = "anthropic",
    model: str = None,
    season: str = "2025"
):
    """
    Create configuration at runtime from user inputs (for Streamlit app)
    
    Args:
        league_id: Sleeper league ID
        target_name: Display name of user to roast
        api_key: Anthropic or OpenAI API key
        provider: "anthropic" or "openai"
        model: Optional model override (auto-selected if None)
        season: Season year (defaults to 2025)
    
    Returns:
        Configuration dictionary
    """
    # Auto-select model based on provider
    if model is None:
        model = "claude-3-7-sonnet-20250219" if provider == "anthropic" else "gpt-4o"
    
    # Start with base config
    base_config = get_config()
    
    # Override with runtime values
    base_config.update({
        "league_id": league_id,
        "target_display_name": target_name,
        "api_provider": provider,
        "api_key": api_key,
        "model_id": model,
        "season": season,
    })
    
    return base_config 
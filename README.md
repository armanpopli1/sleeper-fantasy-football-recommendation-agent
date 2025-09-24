# 🔥 Fantasy Football Roast Agent 🔥

The most savage fantasy football analyst ever created. This agent generates brutally honest, hilariously snarky fantasy football reports that will roast your team into oblivion while providing legitimate analysis.

## ✨ Features

- **Maximum Snark Mode**: No feelings are spared in the pursuit of truth
- **Real-time Data**: Uses Sleeper API for up-to-date league information
- **Web Search Integration**: Gets current player news and trends
- **Beautiful HTML Reports**: Visually stunning roast reports with timestamps
- **Comprehensive Analysis**: 7 detailed sections covering every aspect of your fantasy failures
- **Player Database**: Full NFL player name resolution (no more mysterious IDs)

## 📋 Report Sections

1. **📊 Team Snapshot** - Record, points, ranking + savage commentary
2. **📝 Draft Analysis** - Best/worst picks with maximum regret
3. **📈 Last Week Recap** - Optimal lineup analysis + missed opportunities  
4. **⚡ Next Matchup Preview** - Opponent scouting + brutal predictions
5. **🔄 Roster Recommendations** - Top waiver targets + trade suggestions
6. **🔮 League Prognosis** - Playoff chances + reality check
7. **📊 Final Score** - Overall team grade + devastating final thoughts

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- AWS credentials configured for Bedrock
- Access to Amazon Bedrock Claude models

### 2. Installation

```bash
# Clone or download the project
cd sleeper-fantasy-football-recommendation-agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Edit `config.py` with your league information:

```python
# League Information
LEAGUE_ID = "your_sleeper_league_id"     # Find this in your Sleeper app URL
SEASON = "2025"                          # Current season year

# Target Configuration  
TARGET_DISPLAY_NAME = "username_to_roast"  # Display name of victim

# AWS Configuration
AWS_REGION = "us-west-2"                 # Your AWS region
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"  # Bedrock model
```

### 4. Run the Roast

```bash
# Generate roast for user in config
python run_roast.py

# Roast a specific user
python run_roast.py --target "armanpopli"

# List all league members
python run_roast.py --list-users
```

## 🔧 Configuration Options

### League Settings

```python
LEAGUE_ID = "1263345992535638016"    # Your Sleeper league ID
SEASON = "2025"                      # Current season
TARGET_DISPLAY_NAME = "armanpopli"  # User to roast
```

### AWS Settings

```python
AWS_REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
```

### Report Settings

```python
OUTPUT_DIR = "reports"               # Where to save HTML reports
MAX_WAIVER_TARGETS = 5              # Number of waiver recommendations
MAX_TRADE_SUGGESTIONS = 3           # Number of trade ideas
WEB_SEARCH_RESULTS = 5             # Web search result limit
```

## 📁 Project Structure

```
sleeper-fantasy-football-recommendation-agent/
├── config.py              # Configuration settings
├── sleeper_tools.py        # Sleeper API integration tools
├── web_tools.py           # Web search tools
├── roast_agent.py         # Main roast agent logic
├── run_roast.py           # Runner script
├── report_template.html   # HTML template for reports
├── requirements.txt       # Python dependencies
├── reports/               # Generated reports (created automatically)
└── README.md             # This file
```

## 🛠️ How It Works

### 1. Data Collection
- **Sleeper API**: Gets real-time league data, rosters, matchups, drafts
- **Player Database**: Caches full NFL player database for name resolution
- **Web Search**: Finds current player news and fantasy trends

### 2. Analysis Engine
- **Team Performance**: Win-loss record, points, league ranking
- **Draft Analysis**: Identifies best/worst picks with hindsight
- **Matchup History**: Analyzes recent performance and optimal lineups
- **Roster Evaluation**: Suggests improvements and roasts current choices

### 3. Report Generation
- **Savage Commentary**: Maximum snark mode with no mercy
- **HTML Rendering**: Beautiful, responsive reports with custom styling
- **Timestamp Tracking**: Date-stamped reports for historical humiliation

## 🎯 Example Output

```
🔥 Fantasy Football Roast Report 🔥
Armtard and Co Re-Mastered | 2025 Season

📊 Team Snapshot
Your Team: armanpopli | Record: 1-0 | Current Rank: #6

Grade: C+

Your 1-0 record means you're mediocre, which is probably your ceiling. 
Your 145 points is above average, which is shocking given your decision-making. 
Being ranked #6 means you're temporarily fooling people into thinking you know what you're doing.

Your team name "armanpopli" is almost as disappointing as your performance this season...
```

## 🚨 Error Handling

The agent gracefully handles:
- Missing draft data (skips draft analysis)
- Unavailable matchup data (skips recent performance)
- API failures (continues with available data)
- Invalid user names (provides helpful error messages)

## 🔍 Advanced Usage

### Custom Player Analysis
```bash
# Focus on specific positions
python run_roast.py --target "username" --focus "QB,RB"

# Include injury analysis
python run_roast.py --target "username" --include-injuries
```

### Multiple Reports
```bash
# Generate reports for all league members
for user in $(python run_roast.py --list-users --names-only); do
    python run_roast.py --target "$user"
done
```

## 🐛 Troubleshooting

### Common Issues

**"Failed to get league data"**
- Check your `LEAGUE_ID` in config.py
- Ensure the league is public or you have access

**"User not found"**
- Use `--list-users` to see exact display names
- Display names are case-sensitive

**"AWS/Bedrock errors"**
- Verify AWS credentials are configured
- Check that you have Bedrock access in your region
- Ensure the model ID is correct

**"No player database"**
- Check internet connection (downloads ~5MB player database)
- Sleeper API may be temporarily down

### Debug Mode

Set environment variable for verbose logging:
```bash
export DEBUG=1
python run_roast.py --target "username"
```

## 🗂️ **Development Backlog**

### **🔥 High Priority Features**
- **League-Wide Reports** - Generate roast reports for entire league with cross-team analysis
- **Head-to-Head Analysis** - Detailed opponent research with historical matchup data
- **Advanced Trade Analysis** - Multi-player trade scenarios with value calculations
- **Playoff Bracket Predictions** - Simulate playoff scenarios with roast commentary
- **Season-Long Trending** - Track performance changes over multiple weeks

### **📊 Enhanced Analysis Features**
- **Waiver Wire Timing Analysis** - Roast users for picking up players too late
- **Injury Management Roasting** - Analyze how well users handle injured players
- **Lineup Optimization Scoring** - Calculate exactly how much points were left on bench
- **Draft Value Analysis** - Compare draft ADP to current season performance
- **Schedule Strength Analysis** - Factor in opponent difficulty for projections

### **🌐 Web Integration Enhancements**
- **Player News Integration** - Search for specific injury reports and news
- **Expert Rankings Comparison** - Compare user decisions to expert consensus
- **Reddit/Twitter Sentiment** - Find what fantasy community is saying about players
- **Trade Value Charts** - Integrate current trade value data for analysis

### **🎯 User Experience Improvements**
- **Multiple Target Reports** - Generate reports for multiple league members at once
- **Comparison Reports** - Side-by-side analysis of two teams
- **Historical Report Tracking** - Compare current performance to previous weeks
- **Interactive HTML Reports** - Clickable elements and dynamic content
- **PDF Export Options** - Professional-looking printable reports

### **🔧 Technical Enhancements**
- **Faster Player Database** - Cache and optimize NFL player data loading
- **Real-time Scoring** - Live updates during game days
- **Advanced Opponent Matching** - Better algorithm for finding actual opponents
- **Multi-league Support** - Analyze multiple leagues for same user
- **API Rate Limiting** - Smart throttling for large league analysis

## 🤝 Contributing

Want to make the roasts even more savage? Contributions welcome!

1. Fork the repository
2. Create a feature branch  
3. Pick an item from the backlog or add more brutal commentary
4. Submit a pull request

**Priority Areas:**
- League-wide analysis and cross-team roasting
- Better opponent identification and matchup analysis
- Enhanced web search integration for current player news
- More sophisticated trade and waiver wire analysis

## ⚠️ Disclaimer

This agent generates satirical content for entertainment purposes. Fantasy football roasting is an art form that requires thick skin and a sense of humor. Use responsibly and don't actually destroy friendships (unless they deserve it).

## 📜 License

MIT License - Roast responsibly.

---

**🔥 May your lineups be optimal and your opponents be terrible 🔥** 
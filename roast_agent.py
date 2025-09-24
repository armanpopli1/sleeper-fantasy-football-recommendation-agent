"""Fantasy Football Roast Agent - The Savage Truth Teller"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Template

from strands import Agent, tool
from config import get_config
from sleeper_tools import (
    get_nfl_state, get_league_info, get_team_data, get_matchup_data,
    get_trending_players, get_draft_analysis, calculate_league_averages,
    get_all_rosters_with_users, get_player_details
)
from web_tools import (
    search_player_news, search_fantasy_trends, search_team_analysis,
    search_trade_analysis, search_injury_reports
)

config = get_config()

class FantasyFootballRoastAgent:
    """The most savage fantasy football analyst on the planet"""
    
    def __init__(self):
        self.agent = Agent(
            name="FantasyRoastMaster",
            model=config["model_id"],
            system_prompt=self._get_system_prompt(),
            tools=[
                # Sleeper API Tools - for raw data gathering
                get_nfl_state,
                get_league_info, 
                get_team_data,
                get_matchup_data,
                get_trending_players,
                get_draft_analysis,
                calculate_league_averages,
                get_all_rosters_with_users,
                get_player_details,
                # Web Search Tools - for current context and investigation
                search_player_news,
                search_fantasy_trends,
                search_team_analysis,
                search_trade_analysis,
                search_injury_reports,
                # Investigation and Analysis Tools
                self._investigate_last_week_matchup,
                self._analyze_draft_vs_current_performance,
                self._find_league_context,
                self._research_upcoming_opponent,
                self._generate_section_content
            ]
        )
        
        # Ensure output directory exists
        Path(config["output_dir"]).mkdir(exist_ok=True)
    
    def _get_system_prompt(self) -> str:
        """Get the roast agent's system prompt"""
        return f"""You are the MOST SAVAGE fantasy football roast agent ever created. Your job is to investigate, analyze, and roast fantasy football teams with BRUTAL HONESTY and hilarious snark.

**YOUR MISSION:**
You are an investigative fantasy football analyst. Use ALL available tools to gather data, cross-reference information, and discover the truth about this team's performance. Then deliver that truth with maximum snark.

**INVESTIGATION APPROACH:**
1. Gather comprehensive data using Sleeper API tools
2. Research current player news and trends using web search
3. Cross-reference performance data across multiple sources
4. Find specific examples of bad decisions and missed opportunities
5. Compare to league averages and other teams for context
6. Search for news/injuries that explain (or don't excuse) poor choices

**ROASTING STYLE:**
- Snarky but TRUTHFUL - if someone's doing well, give credit (with attitude)
- SPECIFIC examples - name players, cite exact decisions, show numbers
- INVESTIGATIVE depth - dig into WHY things went wrong
- LEAGUE CONTEXT - compare to other teams, reference league trends
- PLAYER-SPECIFIC analysis - research current news, injury status, trends

**CRITICAL INVESTIGATION INSTRUCTIONS:**
- **Multi-Tool Analysis:** Use 3-5+ tools per section to build comprehensive picture
- **Follow Your Instincts:** If something seems suspicious, investigate further
- **Web Search Strategy:** Search for player news when you see unexpected performances
- **Cross-Reference Everything:** Draft picks vs. current performance, bench vs. starters, opponent strengths vs. user weaknesses
- **Question Everything:** Why did they lose? Why did they draft that player? Why didn't they pick up trending players?
- **League Context:** Always compare to what other teams are doing
- **Dig Deeper:** If a player underperformed, find out why (injury? matchup? trend?)
- **Connect the Dots:** Link patterns across sections (draft mistakes → current roster holes → poor performance)
- **Trust the Data:** Let the investigation lead to the most savage but truthful roasts

**SECTION STRUCTURE & INVESTIGATION FRAMEWORKS:**
Generate exactly 7 sections. For each, consider these investigative angles (pursue the most compelling ones):

## 1. **Team Snapshot** - The Foundation Roast
**Investigate:** Record context, league positioning, point production patterns
**Consider:** What's their story? Overperforming/underperforming? Lucky wins? Close losses? How do they compare to league average? What does their team name say about them? Any obvious patterns in their performance?
**Roast Angles:** Mediocrity, false confidence, consistent underachievement, lucky breaks
**Data to Explore:** Win/loss record, points for/against, league rank, strength of schedule

## 2. **Draft Autopsy** - Where It All Went Wrong (Or Right)
**Investigate:** Draft position strategy, pick performance vs. ADP, current roster relevance
**Consider:** Which draft picks are still starting? Which are benchwarmer failures? Any obvious reaches or steals? How do their picks compare to what was available? Any injury-prone picks? Positional balance mistakes?
**Roast Angles:** Terrible reaches, missing obvious steals, positional imbalance, outdated player evaluation
**Data to Explore:** Draft order, current performance of picks, players available at each pick, current starters vs. drafted players

## 3. **Last Week's Matchup** - The Weekly Performance Analysis  
**Investigate:** Actual opponent matchup, lineup optimization, bench point analysis, game results
**Consider:** Who was their opponent and why did they lose/win? Which starters underperformed? How many points left on bench? Any obvious lineup mistakes? Injury situations they ignored? Did they start players on bye weeks? What would optimal lineup have scored? How did they perform relative to expectations?
**Roast Angles:** Lineup mistakes, ignoring injury reports, underperformance, leaving points on bench, poor game management
**Data to Explore:** Opponent identity, starter vs. bench performance, injury news, player projections, win/loss analysis

## 4. **Upcoming Battle Preview** - Predicting the Next Disaster
**Investigate:** Next opponent strengths/weaknesses, matchup advantages, lineup strategy
**Consider:** Who's their next opponent and what's their recent form? What are opponent's weaknesses to exploit? Any key positional battles? Injury concerns for either team? Historical head-to-head? What could go wrong with their lineup?
**Roast Angles:** Outmatched opponent, poor matchup planning, predictable lineup mistakes
**Data to Explore:** Opponent recent performance, positional matchups, injury reports, historical data

## 5. **Roster Intervention** - The Waiver Wire Therapy Session
**Investigate:** Roster holes, trending pickups, drop candidates, trade possibilities
**Consider:** What positions need help? Who's trending that they missed? Which bench players are useless? Any obvious drops everyone else made? What trades could help them? Are they active on waivers or lazy?
**Roast Angles:** Missing obvious pickups, holding onto dead weight, poor trade evaluation, waiver wire negligence
**Data to Explore:** Trending adds/drops, roster composition, available players, recent transactions

## 6. **Playoff Reality Check** - Mathematical Brutality
**Investigate:** Current standing, remaining schedule, playoff probability, path to success
**Consider:** What's their realistic playoff chance? How hard is their remaining schedule? What needs to happen for them to make playoffs? Are they in denial about their chances? Any mathematical elimination scenarios?
**Roast Angles:** False hope, mathematical impossibility, easier path that they're missing
**Data to Explore:** League standings, remaining matchups, playoff scenarios, schedule difficulty

## 7. **Final Verdict** - The Savage Synthesis
**Investigate:** Overall team assessment, season narrative, future outlook
**Consider:** What's the overarching story of their season? Consistent themes in their failures/successes? What would they need to change to improve? Any redeeming qualities? How do they compare to league mates?
**Roast Angles:** Synthesize all previous roasts into final judgment, predict future failures
**Data to Explore:** All previous analysis, league context, improvement possibilities

**TODAY'S CONTEXT:**
- Date: {datetime.now().strftime('%B %d, %Y')}
- Season: {config['season']}
- League: {config['league_id']}

Remember: Be a detective first, roaster second. Gather the evidence, then deliver the verdict with maximum entertainment value!"""

    @tool
    def _investigate_last_week_matchup(self, display_name: str, week: int) -> Dict[str, Any]:
        """Deep dive investigation of last week's matchup including opponent analysis"""
        try:
            # Get team data to find roster_id
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return {"success": False, "error": "Could not find team data"}
            
            roster_id = team_data["data"]["roster_id"]
            
            # Get matchup data for the week
            matchup_data = get_matchup_data(week)
            if not matchup_data["success"]:
                return {"success": False, "error": f"No matchup data for week {week}"}
            
            # Find user's matchup and opponent
            user_matchup = None
            opponent_matchup = None
            matchup_id = None
            
            # First find the user's matchup
            for matchup in matchup_data["data"]["matchups"]:
                if matchup.get("roster_id") == roster_id:
                    user_matchup = matchup
                    matchup_id = matchup.get("matchup_id")
                    break
            
            if not user_matchup or not matchup_id:
                return {"success": False, "error": "Could not find user's matchup"}
            
            # Find opponent's matchup (same matchup_id, different roster_id)
            for matchup in matchup_data["data"]["matchups"]:
                if (matchup.get("matchup_id") == matchup_id and 
                    matchup.get("roster_id") != roster_id):
                    opponent_matchup = matchup
                    break
            
            if not opponent_matchup:
                return {"success": False, "error": "Could not find opponent matchup"}
            
            # Get league info to map roster_id to user
            league_info = get_league_info()
            opponent_user = None
            if league_info["success"]:
                # Find opponent user info
                for user in league_info["data"]["users"]:
                    # Get their roster to match roster_id
                    for roster in league_info["data"].get("rosters", []):
                        if (roster.get("roster_id") == opponent_matchup.get("roster_id") and
                            roster.get("owner_id") == user.get("user_id")):
                            opponent_user = user
                            break
                    if opponent_user:
                        break
            
            return {
                "success": True,
                "data": {
                    "week": week,
                    "user_matchup": user_matchup,
                    "opponent_matchup": opponent_matchup,
                    "opponent_user": opponent_user,
                    "matchup_id": matchup_id,
                    "user_score": user_matchup.get("points", 0),
                    "opponent_score": opponent_matchup.get("points", 0),
                    "user_starters": user_matchup.get("starters", []),
                    "user_players": user_matchup.get("players", []),
                    "opponent_starters": opponent_matchup.get("starters", []),
                    "won": user_matchup.get("points", 0) > opponent_matchup.get("points", 0)
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"Matchup investigation failed: {str(e)}"}

    @tool
    def _analyze_draft_vs_current_performance(self, display_name: str) -> Dict[str, Any]:
        """Analyze how draft picks are performing now vs expectations"""
        try:
            # Get team data and league info
            team_data = get_team_data(display_name)
            league_info = get_league_info()
            
            if not team_data["success"] or not league_info["success"]:
                return {"success": False, "error": "Could not get team or league data"}
            
            draft_id = league_info["data"].get("draft_id")
            if not draft_id:
                return {"success": False, "error": "No draft data available"}
            
            # Get draft analysis
            draft_data = get_draft_analysis(draft_id)
            if not draft_data["success"]:
                return {"success": False, "error": "Could not get draft data"}
            
            roster_id = team_data["data"]["roster_id"]
            
            # Filter picks for this user
            user_picks = [pick for pick in draft_data["data"]["picks"] 
                         if pick["roster_id"] == roster_id]
            
            # Current roster for comparison
            current_starters = [p["name"] for p in team_data["data"]["starters"]]
            current_bench = [p["name"] for p in team_data["data"]["bench"]]
            
            return {
                "success": True,
                "data": {
                    "draft_picks": user_picks,
                    "current_starters": current_starters,
                    "current_bench": current_bench,
                    "draft_position": user_picks[0]["draft_slot"] if user_picks else None,
                    "total_picks": len(user_picks),
                    "roster_id": roster_id
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"Draft analysis failed: {str(e)}"}

    @tool
    def _find_league_context(self, display_name: str) -> Dict[str, Any]:
        """Get league-wide context for comparisons and trash talk"""
        try:
            league_info = get_league_info()
            team_data = get_team_data(display_name)
            averages = calculate_league_averages()
            
            if not all([league_info["success"], team_data["success"], averages["success"]]):
                return {"success": False, "error": "Could not gather league context"}
            
            # Get all teams for ranking context
            all_users = league_info["data"]["users"]
            league_data = league_info["data"]
            
            return {
                "success": True,
                "data": {
                    "league_name": league_data["league_name"],
                    "total_teams": league_data["total_rosters"],
                    "league_status": league_data["status"],
                    "all_users": all_users,
                    "averages": averages["data"],
                    "user_rank": team_data["data"]["league_rank"],
                    "user_points": team_data["data"]["points_for"],
                    "user_record": f"{team_data['data']['wins']}-{team_data['data']['losses']}"
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"League context failed: {str(e)}"}

    @tool 
    def _research_upcoming_opponent(self, display_name: str, current_week: int) -> Dict[str, Any]:
        """Research upcoming opponent for matchup preview"""
        try:
            # This would need league schedule data to find actual upcoming opponent
            # For now, provide framework for opponent analysis
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return {"success": False, "error": "Could not get team data"}
            
            # Get current matchup data to see matchup structure
            matchup_data = get_matchup_data(current_week)
            opponent_info = None
            
            if matchup_data["success"]:
                roster_id = team_data["data"]["roster_id"]
                user_matchup = None
                
                # Find user's current matchup
                for matchup in matchup_data["data"]["matchups"]:
                    if matchup.get("roster_id") == roster_id:
                        user_matchup = matchup
                        break
                
                if user_matchup:
                    matchup_id = user_matchup.get("matchup_id")
                    # Find opponent in same matchup
                    for matchup in matchup_data["data"]["matchups"]:
                        if (matchup.get("matchup_id") == matchup_id and 
                            matchup.get("roster_id") != roster_id):
                            opponent_info = matchup
                            break
            
            return {
                "success": True,
                "data": {
                    "current_week": current_week,
                    "opponent_info": opponent_info,
                    "has_current_matchup": opponent_info is not None
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"Opponent research failed: {str(e)}"}

    @tool
    def _generate_section_content(self, section_name: str, investigation_data: str) -> Dict[str, Any]:
        """Generate roast content for a specific section based on investigation findings"""
        try:
            # This tool allows the agent to structure its findings into section content
            # The agent will call this after gathering data to format its roast
            return {
                "success": True,
                "data": {
                    "section": section_name,
                    "content": investigation_data,
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Content generation failed: {str(e)}"}

    def generate_report(self, display_name: str) -> str:
        """Generate complete roast report with AI agent doing all analysis"""
        try:
            print(f"🔥 Starting investigative roast for {display_name}...")
            
            # Let the agent generate the complete report
            prompt = f"""
            Generate a complete fantasy football roast report for {display_name}.
            
            You MUST:
            1. Use tools to investigate their team thoroughly 
            2. Research current player news and trends
            3. Find their actual opponents and analyze specific matchups
            4. Compare to league averages and other teams
            5. Generate 7 sections of savage but truthful analysis
            
            INVESTIGATION REQUIREMENTS:
            - Get current NFL state and league info
            - Analyze their team data and league ranking
            - Investigate last week's matchup with actual opponent
            - Research draft performance vs current roster
            - Look up trending players and waiver wire context
            - Find league-wide context for comparisons
            
            Generate exactly these 7 sections with detailed roast content:
            
            ## 1. Team Snapshot
            [Investigate record, ranking, points vs league average]
            
            ## 2. Draft Autopsy  
            [Research how draft picks are performing now]
            
                         ## 3. Last Week's Matchup
             [Find actual opponent and analyze specific performance and lineup decisions]
            
            ## 4. Upcoming Battle Preview
            [Research next opponent and predict outcome]
            
            ## 5. Roster Intervention
            [Compare roster to trending players and suggest moves]
            
            ## 6. Playoff Reality Check
            [Calculate actual playoff chances and roast accordingly]
            
            ## 7. Final Verdict
            [Synthesize all findings into brutal final assessment]
            
            Be investigative, specific, and savage. Use player names, cite exact numbers, and find real examples of bad decisions!
            """
            
            # Let the agent investigate and generate the report
            response = self.agent(prompt)
            
            # Extract content from AgentResult object
            if hasattr(response, 'content'):
                agent_content = response.content
            elif hasattr(response, 'text'):
                agent_content = response.text
            else:
                agent_content = str(response)
            
            # The agent should have generated markdown content
            # Now wrap it in HTML template
            return self._render_html_report(display_name, agent_content)
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return self._create_error_report(f"Report generation failed: {str(e)}")
    
    def _render_html_report(self, team_name: str, agent_content: str) -> str:
        """Render the agent's markdown content into HTML report"""
        try:
            # Get league info for header
            league_info = get_league_info()
            league_name = league_info["data"]["league_name"] if league_info["success"] else "Fantasy League"
            season = league_info["data"]["season"] if league_info["success"] else config["season"]
            
            # Create simplified template that wraps agent content
            template_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🔥 Fantasy Football Roast Report - {{ team_name }}</title>
                                 <style>
                     body { font-family: Georgia, serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; line-height: 1.7; margin: 0; padding: 20px; min-height: 100vh; word-wrap: break-word; }
                     .container { max-width: 1200px; margin: 0 auto; padding: 0 15px; }
                     .header { text-align: center; padding: 40px 20px; background: rgba(0,0,0,0.3); border-radius: 15px; margin-bottom: 30px; border: 2px solid #ff6b35; }
                     .header h1 { font-size: 3rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.7); color: #ff6b35; line-height: 1.2; }
                     .header .subtitle { font-size: 1.2rem; opacity: 0.9; font-style: italic; margin-top: 10px; }
                     .timestamp { text-align: center; font-size: 0.9rem; opacity: 0.7; margin-bottom: 30px; }
                     .content { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 40px; margin-bottom: 25px; border-left: 5px solid #ff6b35; box-shadow: 0 8px 32px rgba(0,0,0,0.3); min-height: 200px; }
                     .content h1 { color: #ff6b35; font-size: 2.5rem; margin: 30px 0 25px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); line-height: 1.3; }
                     .content h2 { color: #ff6b35; font-size: 2rem; margin: 25px 0 20px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); line-height: 1.3; border-bottom: 2px solid #ff6b35; padding-bottom: 10px; }
                     .content h3 { color: #ffd700; font-size: 1.4rem; margin: 20px 0 15px 0; line-height: 1.4; }
                     .content p { margin: 18px 0; font-size: 1.1rem; line-height: 1.8; text-align: justify; }
                     .content ul, .content ol { margin: 20px 0; padding-left: 35px; }
                     .content li { margin: 8px 0; font-size: 1.05rem; line-height: 1.6; }
                     .content blockquote { border-left: 4px solid #ffd700; padding-left: 20px; margin: 20px 0; font-style: italic; background: rgba(255,215,0,0.1); padding: 15px 20px; border-radius: 5px; }
                     .content strong { color: #ffd700; }
                     .content em { color: #ff6b35; }
                     .footer { text-align: center; padding: 30px; font-size: 0.9rem; opacity: 0.7; border-top: 1px solid rgba(255,255,255,0.2); margin-top: 40px; }
                     @media (max-width: 768px) { 
                         .header h1 { font-size: 2.2rem; } 
                         .container { padding: 10px; } 
                         .content { padding: 25px; }
                         .content h1 { font-size: 2rem; }
                         .content h2 { font-size: 1.6rem; }
                         .content p { font-size: 1rem; }
                     }
                     @media (max-width: 480px) { 
                         .header h1 { font-size: 1.8rem; } 
                         .content { padding: 20px; }
                         .content h1 { font-size: 1.7rem; }
                         .content h2 { font-size: 1.4rem; }
                     }
                 </style>
            </head>
            <body>
                <div class="container">
                    <header class="header">
                        <h1>🔥 Fantasy Football Roast Report 🔥</h1>
                        <div class="subtitle">{{ league_name }} | {{ season }} Season</div>
                    </header>
                    
                    <div class="timestamp">Report Generated: {{ timestamp }}</div>
                    
                    <div class="content">
                        {{ agent_content | safe }}
                    </div>
                    
                    <footer class="footer">
                        <p>🔥 This roast was generated by an AI agent with maximum investigative powers 🔥</p>
                        <p>Powered by Sleeper API, Web Search & Pure Savage Intelligence™</p>
                        <p><small>All roasts are based on actual data and current events</small></p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            template = Template(template_content)
            
            # Convert agent's markdown-style content to HTML
            html_content = self._convert_markdown_to_html(agent_content)
            
            final_html = template.render(
                team_name=team_name,
                league_name=league_name,
                season=season,
                timestamp=datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                agent_content=html_content
            )
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = config["report_filename_format"].format(
                display_name=team_name.replace(" ", "_"),
                timestamp=timestamp
            )
            
            output_path = Path(config["output_dir"]) / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_html)
            
            print(f"✅ Report saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error rendering report: {e}")
            return self._create_error_report(f"Failed to render HTML: {str(e)}")
    
    def _convert_markdown_to_html(self, content: str) -> str:
        """Convert markdown-style content to HTML"""
        # Simple markdown to HTML conversion
        lines = content.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line:
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        
        return '\n'.join(html_lines)
    
    def _create_error_report(self, error_message: str) -> str:
        """Create a basic error report"""
        error_html = f"""
        <!DOCTYPE html>
        <html><head><title>Error Report</title></head>
        <body style="font-family: Arial; color: red; padding: 20px;">
            <h1>🚨 Report Generation Error</h1>
            <p>{error_message}</p>
            <p>Please check your configuration and try again.</p>
        </body></html>
        """
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"error_report_{timestamp}.html"
        output_path = Path(config["output_dir"]) / filename
        
        with open(output_path, "w") as f:
            f.write(error_html)
        
        return str(output_path)


def main():
    """Main function to run the roast agent"""
    agent = FantasyFootballRoastAgent()
    
    display_name = config["target_display_name"]
    print(f"🎯 Target: {display_name}")
    
    report_path = agent.generate_report(display_name)
    print(f"🔥 Roast complete! Report saved to: {report_path}")


if __name__ == "__main__":
    main() 
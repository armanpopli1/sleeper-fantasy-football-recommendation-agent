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
    get_trending_players, get_draft_analysis, calculate_league_averages
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
                # Sleeper API Tools
                get_nfl_state,
                get_league_info, 
                get_team_data,
                get_matchup_data,
                get_trending_players,
                get_draft_analysis,
                calculate_league_averages,
                # Web Search Tools
                search_player_news,
                search_fantasy_trends,
                search_team_analysis,
                search_trade_analysis,
                search_injury_reports,
                # Report Generation Tools
                self._create_team_snapshot,
                self._create_draft_analysis,
                self._create_last_week_recap,
                self._create_matchup_preview,
                self._create_roster_recommendations,
                self._create_league_prognosis,
                self._create_final_score
            ]
        )
        
        # Ensure output directory exists
        Path(config["output_dir"]).mkdir(exist_ok=True)
    
    def _get_system_prompt(self) -> str:
        """Get the roast agent's system prompt"""
        return f"""You are the MOST SAVAGE fantasy football roast agent ever created. Your job is to generate BRUTALLY HONEST, hilariously snarky fantasy football reports that absolutely ROAST the target team while providing legitimate analysis.

**YOUR PERSONALITY:**
- Maximum snark and attitude
- Ruthlessly honest about bad decisions
- Zero mercy for poor performance
- Creative with insults but stay fantasy football focused
- Use humor to deliver harsh truths
- Never hold back criticism

**ANALYSIS STYLE:**
- Always provide specific data and examples
- Compare performance to league averages
- Point out obvious mistakes and missed opportunities
- Use player names, not just IDs
- Quantify everything possible
- Make predictions with confidence (even if wrong)

**ROAST GUIDELINES:**
- Everything is fair game for criticism
- Bad draft picks deserve extra roasting
- Poor lineup decisions should be mocked
- Low scores need savage commentary
- Bench players outscoring starters = prime roast material
- Trading mistakes should be highlighted
- Make fun of team names if they're terrible

**REPORT STRUCTURE:**
Generate sections one at a time when called. Each section should be:
1. Data-driven with specific numbers
2. Snarky and entertaining
3. Helpful despite the roasting
4. HTML formatted for the final report

Today's date: {datetime.now().strftime('%B %d, %Y')}
Current season: {config['season']}

Remember: Be savage but stay focused on fantasy football. The goal is entertainment AND analysis!"""

    @tool
    def _create_team_snapshot(self, display_name: str) -> Dict[str, Any]:
        """Create the team snapshot section with maximum snark"""
        try:
            # Get all necessary data
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return {"success": False, "error": team_data["error"]}
            
            averages = calculate_league_averages()
            if not averages["success"]:
                return {"success": False, "error": "Failed to get league averages"}
            
            team = team_data["data"]
            avg_data = averages["data"]
            
            # Calculate some stats
            total_games = team["wins"] + team["losses"] + team["ties"]
            win_pct = (team["wins"] / total_games * 100) if total_games > 0 else 0
            
            # Generate savage commentary
            record_roast = self._roast_record(team["wins"], team["losses"], win_pct)
            points_roast = self._roast_points(team["points_for"], avg_data["avg_points_for"])
            rank_roast = self._roast_ranking(team["league_rank"], team["total_teams"])
            
            # Get team name
            team_name = team["user_info"].get("metadata", {}).get("team_name", display_name)
            
            content = f"""
            <h2>📊 Team Snapshot</h2>
            <div class="league-info">
                <h3>Your Team: {team_name}</h3>
                <div class="stats-grid">
                    <div class="stat-box">
                        <span class="stat-value">{team["wins"]}-{team["losses"]}</span>
                        <div class="stat-label">Record</div>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{team["points_for"]}</span>
                        <div class="stat-label">Total Points</div>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">#{team["league_rank"]}</span>
                        <div class="stat-label">League Rank</div>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">{avg_data["avg_points_for"]}</span>
                        <div class="stat-label">League Avg</div>
                    </div>
                </div>
            </div>
            
            <div class="grade">Grade: {self._calculate_team_grade(team, avg_data)}</div>
            
            <div class="roast-text">
                {record_roast} {points_roast} {rank_roast}
                
                Your team name "{team_name}" is almost as disappointing as your performance this season. 
                You're currently sitting at #{team["league_rank"]} out of {team["total_teams"]} teams, which means 
                you're closer to last place than you'd like to admit.
                
                But hey, at least you showed up! That's more than we can say for some of your players' performances.
            </div>
            """
            
            return {
                "success": True, 
                "content": content,
                "team_data": team
            }
            
        except Exception as e:
            return {"success": False, "error": f"Team snapshot error: {str(e)}"}
    
    @tool 
    def _create_draft_analysis(self, draft_id: str, target_roster_id: int) -> Dict[str, Any]:
        """Analyze draft performance with brutal honesty"""
        try:
            if not draft_id:
                return {"success": False, "error": "No draft data available"}
            
            draft_data = get_draft_analysis(draft_id)
            if not draft_data["success"]:
                return {"success": False, "error": "Failed to get draft data"}
            
            # Filter picks for target user
            user_picks = [pick for pick in draft_data["data"]["picks"] 
                         if pick["roster_id"] == target_roster_id]
            
            if not user_picks:
                return {"success": False, "error": "No draft picks found for user"}
            
            # Analyze picks
            draft_position = user_picks[0]["draft_slot"] if user_picks else "Unknown"
            best_pick = self._find_best_pick(user_picks)
            worst_pick = self._find_worst_pick(user_picks)
            draft_grade = self._grade_draft(user_picks)
            
            content = f"""
            <h2>📝 Draft Analysis</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-value">{draft_position}</span>
                    <div class="stat-label">Draft Position</div>
                </div>
                <div class="stat-box">
                    <span class="stat-value">{len(user_picks)}</span>
                    <div class="stat-label">Total Picks</div>
                </div>
            </div>
            
            <h3>Best Pick: {best_pick["player_name"]} (Round {best_pick["round"]})</h3>
            <h3>Worst Pick: {worst_pick["player_name"]} (Round {worst_pick["round"]})</h3>
            
            <div class="grade">Draft Grade: {draft_grade}</div>
            
            <div class="roast-text">
                Your draft was about as predictable as a bad romantic comedy. You took {best_pick["player_name"]} 
                in round {best_pick["round"]}, which was actually smart - probably the only good decision you made all night.
                
                But then you went and ruined it by selecting {worst_pick["player_name"]} in round {worst_pick["round"]}. 
                What were you thinking? Were you drafting for 2019? Did someone hack your account?
                
                Overall draft grade: {draft_grade}. You managed to avoid complete disaster, which in fantasy football 
                is basically a participation trophy.
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"Draft analysis error: {str(e)}"}
    
    @tool
    def _create_last_week_recap(self, display_name: str, week: int) -> Dict[str, Any]:
        """Roast last week's performance"""
        try:
            # Get team data and matchup data
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return team_data
            
            matchup_data = get_matchup_data(week)
            if not matchup_data["success"]:
                return {"success": False, "error": "No recent matchup data available"}
            
            # Find user's matchup
            team = team_data["data"]
            roster_id = team["roster_id"]
            
            user_matchup = None
            for matchup in matchup_data["data"]["matchups"]:
                if matchup.get("roster_id") == roster_id:
                    user_matchup = matchup
                    break
            
            if not user_matchup:
                return {"success": False, "error": "Matchup data not found"}
            
            score = user_matchup.get("points", 0)
            
            # Calculate optimal lineup (placeholder - would need more complex analysis)
            optimal_score = score * 1.15  # Assume could have scored 15% more optimally
            points_left = optimal_score - score
            
            content = f"""
            <h2>📈 Last Week Recap</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-value">{score}</span>
                    <div class="stat-label">Final Score</div>
                </div>
                <div class="stat-box">
                    <span class="stat-value">{points_left:.1f}</span>
                    <div class="stat-label">Points Left on Bench</div>
                </div>
                <div class="stat-box">
                    <span class="stat-value">{(score/optimal_score*100):.0f}%</span>
                    <div class="stat-label">Optimal %</div>
                </div>
            </div>
            
            <div class="roast-text">
                Last week you scored {score} points, which is about as impressive as a participation ribbon. 
                You left {points_left:.1f} points on your bench, which means you basically shot yourself in the foot 
                before the games even started.
                
                Your lineup decisions were questionable at best. Did you set your lineup while blindfolded? 
                Or maybe you let your pet goldfish make the calls?
                
                You achieved {(score/optimal_score*100):.0f}% of your optimal lineup, which means you're about as 
                efficient as a screen door on a submarine. Try checking the injury reports next time!
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"Last week recap error: {str(e)}"}
    
    @tool
    def _create_matchup_preview(self, display_name: str, current_week: int) -> Dict[str, Any]:
        """Preview next matchup with predictions"""
        try:
            # This would need more complex logic to find actual opponent
            # For now, provide general matchup analysis
            
            content = f"""
            <h2>⚡ Next Matchup Preview</h2>
            <div class="matchup-preview">
                <h3>Week {current_week} Opponent Analysis</h3>
                <div class="vs-text">YOU vs SOMEONE WHO MIGHT ACTUALLY KNOW WHAT THEY'RE DOING</div>
                
                <div class="roast-text">
                    Your upcoming matchup is going to be interesting, and by interesting I mean painful to watch. 
                    Based on your recent performance, you're going to need a miracle, three lucky breaks, 
                    and your opponent to forget to set their lineup.
                    
                    Key positional battle: Your entire team vs basic competency.
                    
                    Prediction: You'll probably lose, but at least you'll have fun doing it. 
                    Maybe try starting players who are actually healthy this week?
                </div>
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"Matchup preview error: {str(e)}"}
    
    @tool
    def _create_roster_recommendations(self, display_name: str) -> Dict[str, Any]:
        """Generate savage roster recommendations"""
        try:
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return team_data
            
            trending = get_trending_players()
            if not trending["success"]:
                return {"success": False, "error": "Failed to get trending players"}
            
            team = team_data["data"]
            trending_data = trending["data"]
            
            # Get some waiver targets and drop candidates
            waiver_targets = trending_data["trending_adds"][:3]
            drop_candidates = [player for player in team["bench"][:2]]  # Suggest dropping bench players
            
            content = f"""
            <h2>🔄 Roster Move Recommendations</h2>
            
            <h3>Waiver Wire Targets:</h3>
            <ul class="recommendation-list">
            """
            
            for target in waiver_targets:
                content += f"""
                <li>
                    <span class="player-name">{target["name"]}</span>
                    <div>{target["add_count"]} managers added this week</div>
                    <div>Maybe try picking up someone people actually want for once?</div>
                </li>
                """
            
            content += """
            </ul>
            
            <h3>Drop Candidates:</h3>
            <ul class="recommendation-list">
            """
            
            for candidate in drop_candidates:
                content += f"""
                <li>
                    <span class="player-name">{candidate["name"]}</span>
                    <div>This player is taking up valuable bench space that could be used for someone useful</div>
                </li>
                """
            
            content += f"""
            </ul>
            
            <div class="roast-text">
                Your roster needs more help than a reality TV star needs therapy. You're seriously considering 
                starting some of these players? The waiver wire has better options than half your bench.
                
                And as for trades? Good luck finding someone desperate enough to want what you're offering. 
                Maybe try offering your first-born child as a sweetener?
                
                Priority #1: Stop making terrible decisions. Priority #2: See Priority #1.
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"Roster recommendations error: {str(e)}"}
    
    @tool
    def _create_league_prognosis(self, display_name: str) -> Dict[str, Any]:
        """Deliver harsh reality about playoff chances"""
        try:
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return team_data
            
            team = team_data["data"]
            
            # Calculate rough playoff probability based on record and rank
            total_games = team["wins"] + team["losses"] + team["ties"]
            win_pct = team["wins"] / total_games if total_games > 0 else 0
            rank_factor = (team["total_teams"] - team["league_rank"]) / team["total_teams"]
            playoff_prob = min(95, max(5, (win_pct * 60 + rank_factor * 40)))
            
            content = f"""
            <h2>🔮 League Prognosis</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-value">#{team["league_rank"]}</span>
                    <div class="stat-label">Current Standing</div>
                </div>
                <div class="stat-box">
                    <span class="stat-value">{playoff_prob:.0f}%</span>
                    <div class="stat-label">Playoff Probability</div>
                </div>
            </div>
            
            <div class="roast-text">
                Your playoff chances are sitting at {playoff_prob:.0f}%, which sounds optimistic until you realize 
                that's about the same odds as finding a unicorn in your backyard.
                
                Currently ranked #{team["league_rank"]} out of {team["total_teams"]} teams, you're in that special 
                zone where you're not good enough to feel confident but not bad enough to embrace the tank.
                
                The rest of your schedule? Let's just say you better start practicing your "next year will be different" speech. 
                Your team has about as much championship potential as a chocolate teapot.
                
                But hey, there's always the consolation bracket! That's where dreams go to die slowly.
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"League prognosis error: {str(e)}"}
    
    @tool
    def _create_final_score(self, display_name: str) -> Dict[str, Any]:
        """Deliver the final verdict with maximum brutality"""
        try:
            team_data = get_team_data(display_name)
            if not team_data["success"]:
                return team_data
            
            team = team_data["data"]
            averages = calculate_league_averages()
            
            final_grade = self._calculate_team_grade(team, averages["data"])
            
            content = f"""
            <h2>📊 Final Team Score</h2>
            
            <div class="grade pulse">{final_grade}</div>
            
            <div class="roast-text">
                <strong>Final Thoughts:</strong><br><br>
                
                Your team is {final_grade.lower()}, which in fantasy football terms means "participation trophy worthy." 
                You've managed to stay relevant through a combination of luck, questionable decision-making, 
                and the fact that someone has to finish in the middle of the pack.
                
                Congratulations! You've successfully proven that throwing darts at a board while blindfolded 
                can be a viable fantasy strategy. Your ability to snatch defeat from the jaws of victory is 
                truly impressive.
                
                But seriously, you're still in this thing, and that's something. Just... maybe try reading 
                some expert advice next time? Or at least check if your players are actually playing before 
                you start them.
                
                <strong>Bottom Line:</strong> Your team has potential, but so does a lottery ticket. 
                The difference is the lottery ticket admits it's a long shot.
            </div>
            
            <div class="timestamp">
                Report completed on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
            """
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": f"Final score error: {str(e)}"}
    
    def generate_report(self, display_name: str) -> str:
        """Generate complete roast report for a user"""
        try:
            print(f"🔥 Generating roast report for {display_name}...")
            
            # Get basic info first
            nfl_state = get_nfl_state()
            league_info = get_league_info()
            
            if not nfl_state["success"] or not league_info["success"]:
                return self._create_error_report("Failed to get basic league information")
            
            current_week = nfl_state["data"]["current_week"]
            league_data = league_info["data"]
            
            # Generate each section
            sections = []
            
            # 1. Team Snapshot
            print("📊 Creating team snapshot...")
            snapshot = self._create_team_snapshot(display_name)
            if snapshot["success"]:
                sections.append({"content": snapshot["content"]})
                team_data = snapshot.get("team_data")
            
            # 2. Draft Analysis
            print("📝 Analyzing draft...")
            if league_data.get("draft_id") and team_data:
                draft = self._create_draft_analysis(league_data["draft_id"], team_data["roster_id"])
                if draft["success"]:
                    sections.append({"content": draft["content"]})
            
            # 3. Last Week Recap
            print("📈 Reviewing last week...")
            if current_week > 1:
                recap = self._create_last_week_recap(display_name, current_week - 1)
                if recap["success"]:
                    sections.append({"content": recap["content"]})
            
            # 4. Matchup Preview
            print("⚡ Previewing matchup...")
            matchup = self._create_matchup_preview(display_name, current_week)
            if matchup["success"]:
                sections.append({"content": matchup["content"]})
            
            # 5. Roster Recommendations
            print("🔄 Creating recommendations...")
            recommendations = self._create_roster_recommendations(display_name)
            if recommendations["success"]:
                sections.append({"content": recommendations["content"]})
            
            # 6. League Prognosis
            print("🔮 Calculating prognosis...")
            prognosis = self._create_league_prognosis(display_name)
            if prognosis["success"]:
                sections.append({"content": prognosis["content"]})
            
            # 7. Final Score
            print("📊 Delivering final verdict...")
            final = self._create_final_score(display_name)
            if final["success"]:
                sections.append({"content": final["content"]})
            
            # Generate HTML report
            return self._render_html_report(
                team_name=display_name,
                league_name=league_data["league_name"],
                season=league_data["season"],
                sections=sections
            )
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return self._create_error_report(f"Report generation failed: {str(e)}")
    
    def _render_html_report(self, team_name: str, league_name: str, season: str, sections: List[Dict]) -> str:
        """Render the final HTML report"""
        try:
            with open("report_template.html", "r") as f:
                template_content = f.read()
            
            template = Template(template_content)
            
            html_content = template.render(
                team_name=team_name,
                league_name=league_name,
                season=season,
                timestamp=datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                sections=sections
            )
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = config["report_filename_format"].format(
                display_name=team_name.replace(" ", "_"),
                timestamp=timestamp
            )
            
            output_path = Path(config["output_dir"]) / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print(f"✅ Report saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error rendering report: {e}")
            return self._create_error_report(f"Failed to render HTML: {str(e)}")
    
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
    
    # Helper methods for analysis
    def _roast_record(self, wins: int, losses: int, win_pct: float) -> str:
        if win_pct > 70:
            return f"Your {wins}-{losses} record is actually impressive. Don't let it go to your head."
        elif win_pct > 50:
            return f"A {wins}-{losses} record means you're mediocre, which is probably your ceiling."
        else:
            return f"Your {wins}-{losses} record is more disappointing than a soggy sandwich."
    
    def _roast_points(self, points: float, avg_points: float) -> str:
        if points > avg_points * 1.1:
            return f"Your {points} points is above average, which is shocking given your decision-making."
        elif points > avg_points * 0.9:
            return f"Your {points} points is perfectly average, just like everything else about your team."
        else:
            return f"Your {points} points is below average, which honestly isn't surprising."
    
    def _roast_ranking(self, rank: int, total: int) -> str:
        if rank <= total // 4:
            return f"Being ranked #{rank} means you're temporarily fooling people into thinking you know what you're doing."
        elif rank <= total // 2:
            return f"Ranked #{rank}, you're the definition of mediocre middle management."
        else:
            return f"Ranked #{rank}, you're closer to last place than first, which is probably where you belong."
    
    def _calculate_team_grade(self, team: Dict, averages: Dict) -> str:
        """Calculate overall team grade"""
        score = 0
        
        # Record score (40%)
        total_games = team["wins"] + team["losses"] + team["ties"]
        if total_games > 0:
            win_pct = team["wins"] / total_games
            if win_pct >= 0.7: score += 40
            elif win_pct >= 0.5: score += 25
            else: score += 10
        
        # Points score (40%)
        if team["points_for"] >= averages["avg_points_for"] * 1.1: score += 40
        elif team["points_for"] >= averages["avg_points_for"] * 0.9: score += 25
        else: score += 10
        
        # Ranking score (20%)
        rank_pct = team["league_rank"] / team["total_teams"]
        if rank_pct <= 0.25: score += 20
        elif rank_pct <= 0.5: score += 15
        else: score += 5
        
        # Convert to letter grade
        if score >= 85: return "A-"
        elif score >= 75: return "B"
        elif score >= 65: return "C+"
        elif score >= 55: return "C"
        elif score >= 45: return "C-"
        elif score >= 35: return "D+"
        else: return "F"
    
    def _find_best_pick(self, picks: List[Dict]) -> Dict:
        """Find the best draft pick (placeholder logic)"""
        # Simple logic: early rounds are usually better
        return min(picks, key=lambda x: x["pick_no"])
    
    def _find_worst_pick(self, picks: List[Dict]) -> Dict:
        """Find the worst draft pick (placeholder logic)"""
        # Simple logic: later rounds with early pick numbers
        return max(picks, key=lambda x: x["round"] if x["round"] <= 8 else 0)
    
    def _grade_draft(self, picks: List[Dict]) -> str:
        """Grade the overall draft"""
        # Placeholder grading logic
        grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
        import random
        return random.choice(grades[3:8])  # Bias toward middle grades


def main():
    """Main function to run the roast agent"""
    agent = FantasyFootballRoastAgent()
    
    display_name = config["target_display_name"]
    print(f"🎯 Target: {display_name}")
    
    report_path = agent.generate_report(display_name)
    print(f"🔥 Roast complete! Report saved to: {report_path}")


if __name__ == "__main__":
    main() 
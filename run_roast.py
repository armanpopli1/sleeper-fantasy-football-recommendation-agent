#!/usr/bin/env python3
"""
Fantasy Football Roast Agent Runner
🔥 Generate savage fantasy football roast reports 🔥
"""

import sys
import os
from pathlib import Path
import argparse
from roast_agent import FantasyFootballRoastAgent
from config import get_config

def main():
    parser = argparse.ArgumentParser(
        description="🔥 Generate a savage fantasy football roast report 🔥",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_roast.py                    # Use config file target
  python run_roast.py --target "username" # Roast specific user
  python run_roast.py --list-users       # Show available users
        """
    )
    
    parser.add_argument(
        "--target", 
        type=str, 
        help="Display name of user to roast (overrides config file)"
    )
    
    parser.add_argument(
        "--list-users",
        action="store_true",
        help="List all users in the league"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory to save report (overrides config)"
    )
    
    args = parser.parse_args()
    
    try:
        config = get_config()
        
        # Create output directory if specified
        if args.output_dir:
            Path(args.output_dir).mkdir(parents=True, exist_ok=True)
            config["output_dir"] = args.output_dir
        
        # Initialize the roast agent
        print("🤖 Initializing Fantasy Football Roast Agent...")
        agent = FantasyFootballRoastAgent()
        
        # List users if requested
        if args.list_users:
            print("👥 Available users in league:")
            from sleeper_tools import get_league_info
            league_info = get_league_info()
            
            if league_info["success"]:
                users = league_info["data"]["users"]
                for i, user in enumerate(users, 1):
                    display_name = user.get("display_name", "Unknown")
                    team_name = user.get("metadata", {}).get("team_name", "No team name")
                    print(f"  {i:2d}. {display_name} (Team: {team_name})")
            else:
                print("❌ Failed to get league users")
            return
        
        # Determine target user
        target_user = args.target or config["target_display_name"]
        
        if not target_user or target_user == "your_target_here":
            print("❌ Error: No target user specified!")
            print("   Either set TARGET_DISPLAY_NAME in config.py or use --target flag")
            print("   Use --list-users to see available users")
            sys.exit(1)
        
        print(f"🎯 Target: {target_user}")
        print(f"🏆 League: {config['league_id']}")
        print(f"📁 Output: {config['output_dir']}")
        print()
        
        # Generate the roast report
        print("🔥 Generating maximum snark roast report...")
        print("⚠️  Warning: No feelings will be spared in this process")
        print()
        
        report_path = agent.generate_report(target_user)
        
        print()
        print("✅ Roast report generated successfully!")
        print(f"📄 Report saved to: {report_path}")
        print("🔥 May the fantasy football gods have mercy on their soul")
        
        # Try to open the report
        try:
            import webbrowser
            webbrowser.open(f"file://{Path(report_path).absolute()}")
            print("🌐 Opening report in browser...")
        except:
            print("💡 Open the HTML file in your browser to view the full roast")
        
    except KeyboardInterrupt:
        print("\n🛑 Roast interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Fantasy Football Roast Generator - Streamlit Web App
🔥 Generate savage roast reports with AI-powered investigation 🔥
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
from roast_agent import FantasyFootballRoastAgent
from config import create_runtime_config

# Page configuration
st.set_page_config(
    page_title="Fantasy Football Roast Generator",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .stButton>button {
        background-color: #ff6b35;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
    }
    .stButton>button:hover {
        background-color: #ff8c5a;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.title("🔥 Roast Configuration")
    st.markdown("---")
    
    # API Provider selection
    st.subheader("AI Configuration")
    provider = st.selectbox(
        "AI Provider",
        ["Anthropic", "OpenAI"],
        help="Choose your AI provider. You'll need an API key from the selected provider."
    )
    
    api_key = st.text_input(
        f"{provider} API Key",
        type="password",
        help=f"Enter your {provider} API key. Get one at {'console.anthropic.com' if provider == 'Anthropic' else 'platform.openai.com'}",
        placeholder=f"sk-ant-... or sk-..." if provider == "Anthropic" else "sk-..."
    )
    
    st.markdown("---")
    
    # League details
    st.subheader("League Information")
    league_id = st.text_input(
        "Sleeper League ID",
        help="Find this in your Sleeper league URL: sleeper.com/leagues/<LEAGUE_ID>",
        placeholder="1263345992535638016"
    )
    
    target_user = st.text_input(
        "Target Username",
        help="Enter the exact Sleeper display name of the user to roast",
        placeholder="armanpopli"
    )
    
    season = st.text_input(
        "Season Year",
        value="2025",
        help="The fantasy football season year"
    )
    
    st.markdown("---")
    
    # Advanced settings (collapsed)
    with st.expander("⚙️ Advanced Settings"):
        model_override = st.text_input(
            "Model Override (Optional)",
            placeholder="claude-3-7-sonnet-20250219 or gpt-4o",
            help="Leave blank to use default model for selected provider"
        )
    
    st.markdown("---")
    
    # Generate button
    generate_btn = st.button("🔥 Generate Roast", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("💡 **How to use:**")
    st.caption("1. Get an API key from Anthropic or OpenAI")
    st.caption("2. Find your Sleeper League ID")
    st.caption("3. Enter the target username")
    st.caption("4. Click Generate and prepare for maximum snark!")

# Main content area
st.title("🔥 Fantasy Football Roast Generator")
st.markdown("### Enter your league details and prepare for **maximum snark**")
st.markdown("---")

# Info boxes at the top
col1, col2, col3 = st.columns(3)
with col1:
    st.info("📊 **Investigative Analysis**\nAI agent searches player stats, news, and trends")
with col2:
    st.info("🎯 **Savage but Truthful**\nBased on real data from Sleeper API")
with col3:
    st.info("📥 **Download Options**\nGet your roast as Markdown or HTML")

st.markdown("---")

# Initialize session state for caching results
if 'markdown_content' not in st.session_state:
    st.session_state.markdown_content = None
if 'target_user' not in st.session_state:
    st.session_state.target_user = None

# Generate roast when button is clicked
if generate_btn:
    # Validation
    if not all([api_key, league_id, target_user]):
        st.error("⚠️ Please fill in all required fields (API Key, League ID, and Target Username)")
    else:
        try:
            # Create runtime configuration
            runtime_config = create_runtime_config(
                league_id=league_id,
                target_name=target_user,
                api_key=api_key,
                provider=provider.lower(),
                model=model_override if model_override else None,
                season=season
            )
            
            # Initialize agent with runtime config
            agent = FantasyFootballRoastAgent(config_override=runtime_config)
            
            # Generate roast with progress indication
            with st.spinner("🔍 Investigating team failures... This may take 1-2 minutes..."):
                progress_text = st.empty()
                
                progress_text.text("📡 Fetching league data from Sleeper API...")
                markdown_content = agent.generate_markdown_report(target_user)
                
                progress_text.text("✅ Roast generation complete!")
            
            # Store in session state
            st.session_state.markdown_content = markdown_content
            st.session_state.target_user = target_user
            
            st.success("🎉 Roast report generated successfully!")
            
        except Exception as e:
            st.error(f"💥 Error generating roast: {str(e)}")
            with st.expander("🔍 View error details"):
                st.exception(e)

# Display roast if available
if st.session_state.markdown_content:
    st.markdown("---")
    st.markdown("## 📄 Your Roast Report")
    
    # Download buttons at the top
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.download_button(
            label="📥 Download Markdown",
            data=st.session_state.markdown_content,
            file_name=f"roast_{st.session_state.target_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        # Generate HTML version for download
        try:
            agent = FantasyFootballRoastAgent()  # Use default config for HTML conversion
            html_content = agent.markdown_to_html(
                st.session_state.markdown_content,
                st.session_state.target_user
            )
            
            # Read the generated HTML file
            st.download_button(
                label="📥 Download HTML",
                data=html_content,
                file_name=f"roast_{st.session_state.target_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        except:
            pass  # HTML download is optional
    
    st.markdown("---")
    
    # Display the markdown content
    st.markdown(st.session_state.markdown_content, unsafe_allow_html=True)

else:
    # Show placeholder when no roast has been generated
    st.info("👈 Enter your league details in the sidebar and click 'Generate Roast' to get started!")
    
    st.markdown("### 🎯 What to Expect")
    st.markdown("""
    This AI-powered roast generator will:
    - 📊 Analyze your team's performance vs. league averages
    - 🔍 Investigate your draft decisions (the good and the terrible)
    - 📉 Roast your lineup mistakes from last week
    - 🔮 Preview your upcoming matchup disaster
    - 💊 Prescribe waiver wire therapy
    - 📈 Calculate your (probably dismal) playoff chances
    - ⚖️ Deliver the final savage verdict
    
    All based on **real data** from the Sleeper API and current NFL news!
    """)
    
    st.markdown("### 📝 Example Report Sections")
    with st.expander("See what a roast report looks like"):
        st.markdown("""
        **📊 Team Snapshot**
        > Your 1-2 record screams "autodraft gone wrong"
        
        | Stat | You | League Avg | Yikes Factor |
        |------|-----|------------|--------------|
        | Points | 319 | 373.5 | -54.5 😱 |
        | Rank | 9th | 5.5 | Bottom tier |
        
        **🎯 Draft Autopsy**
        Your first-round pick lasted 2 weeks before getting injured...
        
        **And 5 more sections of savage analysis!**
        """)

st.markdown("---")
st.caption("Powered by Sleeper API • DuckDuckGo Search • Anthropic/OpenAI AI")
st.caption("Made with 🔥 by a fantasy football roast agent that shows no mercy")

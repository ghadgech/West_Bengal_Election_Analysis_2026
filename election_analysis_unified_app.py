#!/usr/bin/env python3
"""
India Election Analysis 2026 - Unified Chatbot
Supports: Tamil Nadu & West Bengal
Users can switch between state analyses
"""

import streamlit as st
import os
from anthropic import Anthropic

# ============================================================================
# TAMIL NADU KNOWLEDGE BASE
# ============================================================================
TN_KNOWLEDGE_BASE = """
TAMIL NADU 2026 ELECTIONS - AI-DRIVEN PREDICTION

KEY FACTS:
- Total Assembly Seats: 234
- Majority Threshold: 118 seats (50% + 1)
- Supermajority (2/3): 156 seats
- Incumbent: DMK Alliance (led by MK Stalin)
- 2021 DMK Alliance Seats: 159 (2/3 majority)
- 2021 AIADMK Seats: 66
- New Entrant: TVK (Vijay's party) - founded 2023

THREE MAIN SCENARIOS:

Scenario A - DMK Retains Power (60-70% probability):
- DMK: 49-160 seats (Likely: 81)
- AIADMK: 11-70 seats (Likely: 26)
- TVK: 0-50 seats (Likely: 30)
- TVK as Kingmaker: 70-85% probability

Scenario B - TVK as Kingmaker (70-85% probability):
- If TVK wins 40-70 seats, no party has 118 alone
- DMK + TVK = possible coalition
- AIADMK + TVK = possible coalition
- TVK as CM: 10-20% probability (only if 90+ seats)

Scenario C - AIADMK Comeback (Unlikely, <15% probability):
- AIADMK declining trend 2016→2021 (-54 seats)
- Would need major surprise to recover to 66 seats

234 ASSEMBLY SEATS BREAKDOWN:
- DMK Safe: 49 seats (strongest incumbency)
- AIADMK Safe: 11 seats (weakest position)
- Contested: 174 seats (74% of all seats genuinely contested)

TVK THE DISRUPTER:
- Brand new party (founded 2023, first election 2026)
- Zero historical vote share data
- No surveys to predict vote share
- But: 152/234 seats (65%) flagged as TVK-disrupted
- Meaning: 2021 incumbent won but margin thin enough TVK could change dynamics
- 3-way race dynamics (only 33% needed to win)

METHODOLOGY:
- Constituency vulnerability assessment (margin <45% in 2021)
- Disruption Index: identifies seats vulnerable to TVK entry
- Zone-based analysis shows regional patterns
- No survey data used (independent analysis)

CONFIDENCE LEVELS:
[HIGH 95%] DMK remains largest party
[HIGH 70%] DMK crosses 118 majority
[MEDIUM 80%] TVK emerges as significant force
[MEDIUM 75%] TVK becomes kingmaker
[LOW 20%] TVK wins outright
[LOW 15%] AIADMK recovers to 2021 baseline
"""

# ============================================================================
# WEST BENGAL KNOWLEDGE BASE
# ============================================================================
WB_KNOWLEDGE_BASE = """
WEST BENGAL 2026 ELECTIONS - AI-DRIVEN PREDICTION WITH ZONE-BASED ANALYSIS

KEY FACTS:
- Total Assembly Seats: 294
- Majority Threshold: 148 seats (50% + 1)
- Incumbent: Trinamool Congress (TMC)
- 2021 TMC Seats: 215 (73.1%)
- 2021 BJP Seats: 77 (26.2%)

GEOGRAPHIC ZONES:
- North: 27 seats (9.2%) - Cooch Behar, Darjeeling, Jalpaiguri. BJP stronghold (67% vulnerable).
- East: 107 seats (36.4%) - Kolkata, Howrah, 24 Parganas. Battleground (54% vulnerable).
- West: 69 seats (23.5%) - Hooghly, Nadia, Uttar Dinajpur. TMC fortress (33% vulnerable).
- South: 91 seats (31.0%) - Malda, Murshidabad, Birbhum, Bankura. Balanced (57% vulnerable).

THREE SCENARIOS:
Scenario A - TMC Retains Power (60% probability):
- TMC: 185-235 seats (Likely: 210)
- BJP: 80-130 seats (Likely: 100-110)
- Winner: TMC with possible allies

Scenario B - BJP Consolidates (30% probability):
- TMC: 140-180 seats (Likely: 160)
- BJP: 100-150 seats (Likely: 120-130)
- Winner: Contested, might need coalition

Scenario C - Fractured Assembly (10% probability):
- TMC: 140-160 seats
- BJP: 100-130 seats
- Others: 10-20 seats
- Winner: Unclear, alliances needed

LIKELY OUTCOME:
- North: TMC 10 + BJP 17 (27)
- East: TMC 42 + BJP 43 + Others 22 (107)
- West: TMC 55 + BJP 8 + Others 6 (69)
- South: TMC 42 + BJP 35 + Others 14 (91)
TOTAL: TMC 149 + BJP 103 + Others 42 = 294

BJP CONSOLIDATION:
- 2016: 3 seats (1.0%)
- 2021: 77 seats (26.2%) = +74 seats
- 2026 Expected: 100-115 seats = +23-38 seats

DATA CLEANING:
- Cleaned 588 records (294 constituencies x 2 elections)
- Parsed 1,176 candidate records for 2026
- Resolved 19 district name variations
- Used AC_Number as immutable primary key

METHODOLOGY:
1. Historical Trend Analysis: 123/294 constituencies (42%) changed hands 2016-2021
2. Margin-Based Vulnerability: Constituencies with <45% winning share = vulnerable
3. Zone Classification: 19 districts into 4 geographic zones
4. Consolidation Index: Party-specific gains calculated by zone
5. Scenario Modeling: 3 outcome scenarios with probability weights

CONFIDENCE LEVELS:
[HIGH 95%] TMC remains largest single party
[HIGH 70%] TMC crosses 148 majority
[MEDIUM 80%] BJP consolidates to 100+ seats
[MEDIUM 75%] BJP growth costs TMC 10-30 seats
[LOW 10%] Hung Assembly
[LOW 25%] BJP forms government
"""

# Streamlit page config
st.set_page_config(
    page_title="India Election Analysis 2026",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        max-width: 1000px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        padding: 20px 0;
        border-bottom: 3px solid #1f77b4;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .state-selector {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🗳️ India Election Analysis 2026</h1>
    <p><strong>AI-Driven Predictions for Tamil Nadu & West Bengal</strong></p>
    <p style="color: #666; font-size: 14px;">Ask any question about predictions, zones, methodology, or confidence levels</p>
</div>
""", unsafe_allow_html=True)

# State selector
st.markdown("### 🌏 Choose State:")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🔴 Tamil Nadu", use_container_width=True, key="tn_btn"):
        st.session_state.selected_state = "Tamil Nadu"

with col2:
    if st.button("🟢 West Bengal", use_container_width=True, key="wb_btn"):
        st.session_state.selected_state = "West Bengal"

# Initialize session state
if "selected_state" not in st.session_state:
    st.session_state.selected_state = "Tamil Nadu"

if "messages" not in st.session_state:
    st.session_state.messages = {}

if "client" not in st.session_state:
    st.session_state.client = None

# Get current state
current_state = st.session_state.selected_state

# Initialize messages for current state
if current_state not in st.session_state.messages:
    st.session_state.messages[current_state] = []

# Select knowledge base
if current_state == "Tamil Nadu":
    knowledge_base = TN_KNOWLEDGE_BASE
    state_emoji = "🔴"
    color = "#ff6b6b"
else:
    knowledge_base = WB_KNOWLEDGE_BASE
    state_emoji = "🟢"
    color = "#51cf66"

# Sidebar with state info
with st.sidebar:
    st.markdown(f"### {state_emoji} {current_state}")

    if current_state == "Tamil Nadu":
        st.metric("Total Seats", "234")
        st.metric("Majority", "118")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("DMK (2021)", "159")
        with col2:
            st.metric("AIADMK (2021)", "66")
        st.info("""
        **Key Point:** TVK is NEW party
        - Likely 30+ seats (kingmaker)
        - 70-85% probability of kingmaker role
        """)
    else:
        st.metric("Total Seats", "294")
        st.metric("Majority", "148")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("TMC (2021)", "215")
        with col2:
            st.metric("BJP (2021)", "77")
        st.info("""
        **Key Point:** Zone-based analysis
        - 149 seats contested (50.7%)
        - East Zone = battleground
        """)

    st.markdown("### 🔐 API Key Setup")
    st.caption("Get free API key from https://console.anthropic.com")

# Initialize Anthropic client
def get_api_key():
    """Get API key from environment or user input"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
        except:
            pass
    return api_key

# Initialize client
if st.session_state.client is None:
    api_key = get_api_key()
    if api_key:
        st.session_state.client = Anthropic(api_key=api_key)

# Main content
st.markdown(f"### 💬 Ask Questions About {current_state}")
st.markdown(
    f'<div class="info-box">Ask anything about {current_state} 2026 election predictions, analysis, methodology, or confidence levels. The chatbot uses comprehensive analysis knowledge base.</div>',
    unsafe_allow_html=True
)

# Clear chat button
if st.button("🔄 Clear Chat", use_container_width=False):
    st.session_state.messages[current_state] = []
    st.rerun()

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages[current_state]:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"])

# Chat input
if st.session_state.client:
    user_input = st.chat_input(
        f"Ask about {current_state} 2026 elections...",
        key="chat_input"
    )

    if user_input:
        # Add user message to history
        st.session_state.messages[current_state].append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # Get response from Claude
        try:
            with st.spinner("Thinking..."):
                system_prompt = f"""You are an expert on India 2026 election analysis.
You are currently answering questions about {current_state} 2026 elections.
You have access to comprehensive knowledge base with detailed analysis and predictions.

KNOWLEDGE BASE FOR {current_state.upper()}:
{knowledge_base}

Answer questions based on this knowledge base. Be specific, cite data points, acknowledge uncertainty.
Keep responses concise but informative."""

                response = st.session_state.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages[current_state]
                    ]
                )

                assistant_message = response.content[0].text

                # Add assistant message to history
                st.session_state.messages[current_state].append({
                    "role": "assistant",
                    "content": assistant_message
                })

                # Display assistant message
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(assistant_message)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure your API key is valid. Get one from https://console.anthropic.com")

else:
    # API key input
    st.warning("⚠️ API key required")

    with st.expander("📝 Enter your Claude API Key"):
        api_key_input = st.text_input(
            "Enter Claude API Key (starts with sk-)",
            type="password",
            key="api_key_input"
        )

        if api_key_input:
            if api_key_input.startswith("sk-"):
                os.environ["ANTHROPIC_API_KEY"] = api_key_input
                st.session_state.client = Anthropic(api_key=api_key_input)
                st.success("✓ API key set! Refresh to start chatting.")
                st.rerun()
            else:
                st.error("❌ Invalid API key format. Should start with 'sk-'")

    st.info("""
    **How to get an API key:**
    1. Go to https://console.anthropic.com
    2. Sign up or log in
    3. Create a new API key
    4. Copy and paste it above
    5. Start asking questions!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>India Election Analysis 2026 | Tamil Nadu & West Bengal | AI-Powered Q&A</p>
    <p>Knowledge base from detailed statistical analysis of historical election data</p>
    <p>🗳️ Choose state above to ask questions</p>
</div>
""", unsafe_allow_html=True)

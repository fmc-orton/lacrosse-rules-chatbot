import streamlit as st
from openai import OpenAI

# Configure the page
st.set_page_config(
    page_title="Women's Lacrosse Rules Assistant",
    page_icon="🥍",
    layout="centered"
)
st.markdown("""
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js');
        }
    </script>
""", unsafe_allow_html=True)

# Connect to OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# The rulebook knowledge embedded in the AI
SYSTEM_PROMPT = """You are an expert assistant for the 2025-2026 World Lacrosse Women's Field Lacrosse Official Playing Rules (Version 1.1, January 2025).

CRITICAL RULES KNOWLEDGE:

FIELD & GAME BASICS:
- Field: 91.4-100m long, 50-60m wide
- Game: 4 x 15-minute quarters
- Team: Up to 10 players on field
- Goal-Circle: 3m radius from goal-line center
- Restraining-Lines: 22m from each goal-line

MAJOR FOULS (Rule 20):
- Check to Head: MANDATORY CARD
- Dangerous Follow Through: MANDATORY CARD
- Dangerous Propel: MANDATORY CARD
- Swipe: MANDATORY CARD
- Shooting Space: blocking shooting lane in 15m MA
- Three Seconds: defender in 11m Fan >3 seconds without marking
- Charge, Block, Detain, Illegal Contact

MINOR FOULS (Rule 19):
- Illegal Draw, Offside, Illegal Equipment
- Empty Crosse Check, Hand Ball
- Withholding Ball, Delay of Game

GOAL-CIRCLE RULES (Rule 17):
- Attack CANNOT enter circle
- Only goalkeeper may stay in circle when attack has possession
- Goalkeeper has 5 seconds to clear ball

ADVANTAGE FLAG (Rule 21):
- Raised when defense fouls during attack's scoring play
- Play continues until shot/turnover/attack foul

WARNING CARDS (Rule 23):
- Yellow: 2 minutes
- Yellow/Red: 5 minutes + ejection
- Red: 10 minutes + ejection

SHOT CLOCK (Rule 24 - STARTS JAN 2027):
- 80 seconds per possession

When answering:
1. Cite rule numbers (e.g., "Rule 20.A.19")
2. Explain practical application
3. Use clear language
4. If uncertain, say so"""

# Initialize chat history (stores conversation)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page title
st.title("🥍 Women's Lacrosse Rules Assistant")
st.markdown("""
**2025-2026 Official World Lacrosse Rules**

Ask me anything about the rules!
""")

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask about the rules..."):
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                stream=True,
                temperature=0.3,
                max_tokens=1000
            )
            
            # Stream the response (shows typing effect)
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Check your OpenAI API key in secrets.")

# Sidebar
with st.sidebar:
    st.markdown("### Quick Reference")
    st.markdown("""
    **Major Fouls:**
    - Check to Head (card)
    - Dangerous Follow Through (card)
    - Swipe (card)
    - Shooting Space
    - Three Seconds
    
    **Key Rules:**
    - 4 x 15 min quarters
    - Shot clock: 80 sec (2027)
    - Up to 10 players on field
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Version 1.1 • January 2025")
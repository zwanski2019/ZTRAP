import streamlit as st
import json

def load_encyclopedia():
    # This reads the elite dictionary we just generated
    with open('red_team_dictionary.json', 'r') as f:
        return json.load(f)

def render_dictionary():
    st.title("🛡️ Zwanski Tech: Red-Core Encyclopedia")
    data = load_encyclopedia()
    
    # Advanced Search Filter
    query = st.text_input("QUERY MASTER REPOSITORY...", placeholder="e.g. Neural Hijacking")
    
    for entry in data:
        if query.lower() in entry['term'].lower() or query.lower() in entry['category'].lower():
            with st.expander(f"🔴 {entry['term']} | {entry['category']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Technical Definition:**\n{entry['definition']}")
                    st.markdown(f"**Advanced TTPs:**\n{entry['advanced_ttp']}")
                with col2:
                    st.markdown(f"**2026 Trends:**\n{entry['emerging_trend_2026']}")
                    st.warning(f"**THE UNKNOWN FACTOR:**\n{entry['the_unknown_factor']}")
                st.code(entry['command'], language='bash')
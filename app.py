import streamlit as st
import pandas as pd

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Skin Consultant", layout="centered")

# Minimalist CSS for centered layout and clean separators
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { background-color: #000; color: #fff; border-radius: 8px; height: 3.5em; width: 100%; }
    .time-header { padding: 10px 0; border-bottom: 2px solid #000; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
    .product-info { padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Load your Indian Skincare Dataset
    df = pd.read_csv('indian_skincare_dataset.csv')
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- 2. AI Logic: Classification & Selection ---
def get_step_type(product_name):
    name = product_name.lower()
    if any(x in name for x in ["wash", "cleanser", "soap"]): return "Cleanse"
    if any(x in name for x in ["serum", "gel", "tonic", "oil"]): return "Treat"
    if any(x in name for x in ["cream", "moisturizer", "lotion"]): return "Moisturize"
    if any(x in name for x in ["sunscreen", "spf"]): return "Protect"
    return "Treat"

# --- 3. Main UI (Centered Inputs) ---
st.title("🤖 AI Skin Consultant")
st.write("Complete your profile to generate your professional 24-hour routine.")

# Centered Input Section
col1, col2 = st.columns(2)
with col1:
    stype = st.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Normal", "Sensitive"])
with col2:
    sconcern = st.selectbox("Primary Concern", ["Acne", "Pigmentation", "Hydration", "Sun protection", "Pimples"])

allergy = st.text_input("🚫 Allergy Guard", placeholder="Enter ingredients to avoid (e.g. Alcohol)")

if st.button("Generate My Routine"):
    # 1. Filter Logic
    filtered = df[
        (df['Skin type'].str.contains(stype, case=False, na=False)) & 
        (df['Concern'].str.contains(sconcern, case=False, na=False))
    ]

    # 2. Allergy Guard (Negative Constraint)
    if allergy:
        filtered = filtered[~filtered['Product'].str.contains(allergy, case=False, na=False)]

    if not filtered.empty:
        df['Step'] = df['Product'].apply(get_step_type)
        
        # Chronological Routine Plan
        routine_schedule = [
            {"label": "☀️ Morning Routine", "steps": ["Cleanse", "Treat", "Protect"]},
            {"label": "🌆 Evening Routine", "steps": ["Cleanse", "Treat", "Moisturize"]},
            {"label": "🌙 Night Routine", "steps": ["Cleanse", "Moisturize"]}
        ]

        for schedule in routine_schedule:
            st.markdown(f"<div class='time-header'><h3>{schedule['label']}</h3></div>", unsafe_allow_html=True)
            
            for step_name in schedule['steps']:
                # Find matching product for this specific step
                match = filtered[df['Step'] == step_name]
                
                if not match.empty:
                    product = match.iloc[0]
                    with st.container():
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.image(product['product_pic'], use_container_width=True)
                        with c2:
                            st.write(f"#### {step_name}")
                            st.write(f"**{product['Product']}**")
                            st.caption(f"Reason: Targeted for {product['Concern']}")
                            st.link_button("View Details ↗", product['product_url'])
                        st.divider() # THE NEW SEPARATOR
                else:
                    st.info(f"No specific {step_name} found matching your profile.")
    else:
        st.error("No products match your criteria. Please adjust your concerns or allergy guard.")

st.caption("Developed as an AI Principles Project | Knowledge-Based Expert System")
import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime

# Set page config for a polished dark theme
st.set_page_config(page_title="AI Supplier Matching Agent", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark theme with white text (unchanged)
st.markdown("""
    <style>
    .main {background-color: #1e1e1e; color: #ffffff;}
    .stButton>button {
        background-color: #4CAF50;
        color: #ffffff;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>label, .stNumberInput>label, .stSelectbox>label {
        font-weight: bold;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2c2c2c;
        padding: 10px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3a3a3a;
    }
    .stSuccess {
        background-color: #2d6a4f;
        color: #ffffff;
        border-radius: 5px;
    }
    .stError {
        background-color: #6b2d2d;
        color: #ffffff;
        border-radius: 5px;
    }
    .stMarkdown, .stWrite, .stDataFrame {
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>select {
        background-color: #3a3a3a;
        color: #ffffff;
        border: 1px solid #555555;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("Agentic AI for Supplier Matching")
st.subheader("An Interactive Prototype for Autonomous Supplier Matching")
st.write("This prototype simulates an AI agent that autonomously matches buyers with suppliers based on real-world constraints.")

# Tabs (including Tech Stack tab)
tab1, tab2, tab3 = st.tabs(["🔍 Prototype", "🧠 Core Components", "⚙️ Tech Stack (AI PM)"])

# Simulated Supplier Data (unchanged)
suppliers = pd.DataFrame({
    "Name": ["Supplier A", "Supplier B", "Supplier C", "Supplier D"],
    "Region": ["EU", "EU", "US", "Asia"],
    "Cost_per_Unit": [45.0, 48.0, 40.0, 52.0],
    "Delivery_Days": [5, 8, 6, 10],
    "Reliability": [0.9, 0.95, 0.85, 0.88],
    "Min_Order_Value": [400000, 300000, 500000, 450000],
    "Compliance_Score": [0.95, 0.85, 0.98, 0.90],
    "Sustainability_Rating": [0.8, 0.9, 0.7, 0.85]
})

# Tab 1: Prototype (unchanged)
with tab1:
    st.header("Supplier Matching Prototype")
    st.write("Enter your requirements below to see the AI agent in action!")
    with st.form(key="buyer_form"):
        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input("Quantity (e.g., 10000)", min_value=1, value=10000)
            item = st.text_input("Item (e.g., aluminum alloy)", value="aluminum alloy")
            max_cost = st.number_input("Max Cost per Unit ($)", min_value=1.0, value=50.0)
        with col2:
            delivery_days = st.number_input("Max Delivery Days", min_value=1, value=7)
            region = st.selectbox("Region", ["EU", "US", "Asia"], index=0)
            compliance_priority = st.checkbox("Prioritize Regulatory Compliance", value=True)
        submit = st.form_submit_button(label="Find Supplier")
    if submit:
        st.subheader("AI Agent Workflow")
        progress_bar = st.progress(0)
        st.write("**1. Perception**: Parsing and validating your input...")
        st.info(f"Request: {quantity} units of {item}, max ${max_cost}/unit, delivered in {delivery_days} days, {region} region.")
        time.sleep(1)
        progress_bar.progress(25)
        st.write("**2. Data Retrieval**: Querying supplier database...")
        filtered_suppliers = suppliers[suppliers["Region"] == region]
        st.dataframe(filtered_suppliers.style.format({"Cost_per_Unit": "${:.2f}"}))
        time.sleep(1)
        progress_bar.progress(50)
        st.write("**3. Decision-Making**: Scoring suppliers...")
        valid_suppliers = filtered_suppliers[
            (filtered_suppliers["Cost_per_Unit"] <= max_cost) &
            (filtered_suppliers["Delivery_Days"] <= delivery_days) &
            (filtered_suppliers["Min_Order_Value"] <= quantity * max_cost)
        ]
        if not valid_suppliers.empty:
            weights = {"cost": 0.4, "delivery": 0.3, "reliability": 0.2, "compliance": 0.1}
            if compliance_priority:
                weights["compliance"] = 0.3
                weights["cost"] = 0.3
            scores = (
                weights["cost"] * (max_cost - valid_suppliers["Cost_per_Unit"]) / max_cost +
                weights["delivery"] * (delivery_days - valid_suppliers["Delivery_Days"]) / delivery_days +
                weights["reliability"] * valid_suppliers["Reliability"] +
                weights["compliance"] * valid_suppliers["Compliance_Score"]
            )
            valid_suppliers["Score"] = scores
            best_supplier = valid_suppliers.loc[valid_suppliers["Score"].idxmax()]
            st.write("**Best Supplier Match**:")
            st.markdown(f"""
            - **Name**: {best_supplier['Name']}  
            - **Cost per Unit**: ${best_supplier['Cost_per_Unit']:.2f}  
            - **Delivery Days**: {best_supplier['Delivery_Days']}  
            - **Reliability**: {best_supplier['Reliability']*100:.0f}%  
            - **Compliance Score**: {best_supplier['Compliance_Score']*100:.0f}%  
            - **Score**: {best_supplier['Score']:.2f}
            """)
            with st.expander("View Raw Data (JSON)"):
                st.json(best_supplier.to_dict())
        else:
            st.error("No suppliers meet your conditions.")
        time.sleep(1)
        progress_bar.progress(75)
        if not valid_suppliers.empty:
            st.write("**4. Action**: Executing the match...")
            st.success(f"Selected {best_supplier['Name']}. Initiating purchase order and smart contract...")
            st.write("API Call: `POST /supplier/{best_supplier['Name']}/order`")
        time.sleep(1)
        progress_bar.progress(100)

# Tab 2: Core Components (unchanged)
with tab2:
    st.header("Core Components")
    st.write("How the AI agent perceives, decides, and acts.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Perception Tools")
        st.write("- **Historical Data**: Past transactions (Coupa DB)")
        st.write("- **Market Intelligence**: Real-time pricing (APIs)")
        st.write("- **Jurisdictional Constraints**: Compliance checks")
    with col2:
        st.subheader("Decision Framework")
        st.write("- **Multi-modal Fusion**: Combines data inputs")
        st.write("- **Scoring**: Weighted supplier evaluation")
        st.write("- **Optimization**: Best match selection")
    st.subheader("Action & Execution")
    st.write("- **API Integration**: Internal (Coupa) + External (Suppliers)")
    st.write("- **Smart Contracts**: Blockchain-based execution")

# Tab 3: Tech Stack from an AI Product Manager Perspective
with tab3:
    st.header("Tech Stack: An AI Product Manager’s Perspective")
    st.write("As an AI PM for Coupa, the tech stack drives **user value, enterprise scalability, and competitive differentiation**. It must solve procurement pain points—supplier risk, cost optimization, and compliance—while delivering an intuitive experience.")

    # Data Layer
    st.subheader("1. Data Layer")
    st.write("**Goal**: Power AI with real-time, reliable supplier data.")
    st.markdown("""
    - **Apache Kafka**: Streams **real-time supplier updates** (e.g., price changes, risks). Users get instant insights, not stale data.
    - **Snowflake**: Centralized warehouse for **cross-org supplier visibility**. Enables seamless buyer-supplier collaboration.
    - **Neo4j**: Graph DB to uncover **hidden supplier relationships**. Differentiates us with fraud detection and trust scoring.
    """)
    st.write("**AI PM Rationale**: Data is the foundation—low-latency Kafka and Snowflake ensure users trust the AI’s recommendations.")

    # AI/ML Layer
    st.subheader("2. AI & Machine Learning")
    st.write("**Goal**: Deliver intelligent, actionable procurement insights.")
    st.markdown("""
    - **Google Vertex AI**: Managed ML for **fast supplier matching models**. Speeds up MVP delivery to procurement teams.
    - **Databricks**: Unified analytics for **spend optimization**. Turns raw data into a user-facing ROI story.
    - **Hugging Face Transformers**: NLP to flag **contract risks**. Users avoid legal headaches with minimal effort.
    - **Pinecone**: Vector search for **instant supplier lookups**. Enhances UX with speed and relevance.
    """)
    st.write("**AI PM Rationale**: Vertex AI and Databricks balance innovation with usability; Pinecone ensures the AI feels snappy and smart.")

    # Integration Layer
    st.subheader("3. Integration & APIs")
    st.write("**Goal**: Embed AI into Coupa’s ecosystem for a cohesive experience.")
    st.markdown("""
    - **GraphQL + gRPC**: High-speed APIs for **real-time supplier data**. Users expect responsiveness, not delays.
    - **FastAPI**: Lightweight microservices for **AI-driven features**. Quick iterations keep us ahead of competitors.
    - **Coupa APIs**: Tap into **existing procurement workflows**. Reduces adoption friction for current Coupa users.
    """)
    st.write("**AI PM Rationale**: Seamless integration via APIs ensures the AI feels native, not bolted-on—key for user retention.")

    # Security & Deployment
    st.subheader("4. Deployment & Security")
    st.write("**Goal**: Scale globally while protecting enterprise data.")
    st.markdown("""
    - **Kubernetes (GKE)**: Multi-cloud orchestration for **AI scalability**. Handles millions of users without breaking.
    - **HashiCorp Vault**: Secures **sensitive procurement data**. Builds trust with compliance-focused enterprises.
    - **AWS Macie**: AI to detect **data leaks**. Proactively addresses user concerns about privacy.
    """)
    st.write("**AI PM Rationale**: Security isn’t optional—Vault and Macie turn compliance into a selling point; Kubernetes ensures reliability.")

    # Why This Stack?
    st.subheader("Why This Stack?")
    st.write("""
    - **User Value**: Fast, smart supplier matching (Pinecone, Vertex AI) saves time and money.
    - **Differentiation**: Graph-based insights (Neo4j) and contract analysis (Transformers) set us apart.
    - **Scalability**: Kafka and Kubernetes handle global enterprise growth.
    - **Trust**: Security (Vault, Macie) and Coupa integration build user confidence.
    """)
    st.write("**AI PM Takeaway**: This stack turns procurement into an AI-powered superpower—users get efficiency, execs get ROI, and Coupa stays ahead of the curve.")

# Footer (unchanged)
st.markdown("---")
st.write("Built by Keerthi Raghavendra | Feb 21, 2025")
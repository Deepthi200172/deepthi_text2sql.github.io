import streamlit as st
import pandas as pd
import json
from backend import process_user_question  # Assuming your backend code is in backend.py

# Page configuration
st.set_page_config(
    page_title="SQL Query Generator",
    page_icon=":mag:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
    }
    h1 {
        color: #2c3e50;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .result-box {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# App title and description
st.title("🔍 Natural Language to SQL Query Generator")
st.markdown("""
    This application converts your natural language questions about the data into SQL queries, 
    executes them, and displays the results. Simply type your question in plain English!
    """)

# Sidebar with dataset information
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Sample Dataset Information:**
    - This demo uses job card/service record data
    - Contains fields like Odometer, Warranty Cost, Complaint Group, etc.
    - Try questions like:
        - "Top 20 defects by failure count"
        - "Average warranty cost by complaint group"
        - "Vehicles with odometer under 500 miles"
    """)
    
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("""
    1. Type your question in natural language
    2. The AI generates and validates a SQL query
    3. The query executes against the database
    4. Results are displayed in a structured format
    """)
    
    st.markdown("---")
    st.markdown("Created by [Your Name]")
    st.markdown("[GitHub Repository](https://github.com/yourusername/sql-query-generator)")

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    # User input
    user_question = st.text_area(
        "Ask your question about the data:",
        placeholder="e.g., 'Show me the top 20 defects by failure count'",
        height=100
    )
    
    # Submit button
    if st.button("Generate SQL Query"):
        if user_question.strip() == "":
            st.warning("Please enter a question")
        else:
            with st.spinner("Generating and executing query..."):
                try:
                    # Process the user question using the backend
                    json_response = process_user_question(user_question)
                    response_data = json.loads(json_response)
                    
                    # Display results
                    st.session_state.response_data = response_data
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

with col2:
    st.markdown("**Example Questions:**")
    st.markdown("""
    - "Top 25 records by warranty cost"
    - "Count of vehicles by complaint group"
    - "Average odometer reading by model year"
    - "Most common defects by failure count"
    - "Total warranty cost by region"
    """)

# Display results if available
if 'response_data' in st.session_state:
    response_data = st.session_state.response_data
    
    st.markdown("---")
    st.subheader("Results")
    
    # Display SQL Query
    with st.expander("View Generated SQL Query"):
        st.code(response_data['sql_query'], language='sql')
    
    # Display Results
    if response_data['result']:
        # Convert to DataFrame for nice display
        df = pd.DataFrame(response_data['result'])
        
        # Show data
        st.dataframe(df)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name='query_results.csv',
            mime='text/csv'
        )
    else:
        st.info("No results found for this query.")
    
    # Raw JSON view
    with st.expander("View Raw JSON Response"):
        st.json(response_data)

# Footer
st.markdown("---")
st.markdown("""
    *Note: This is a demo application. Query accuracy depends on the AI model's understanding of your question and the database schema.*
""")
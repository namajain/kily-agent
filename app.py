import streamlit as st
import pandas as pd
import os
from advanced_qna_agent import AdvancedQnAAgent
from dotenv import load_dotenv
import tempfile
import io
import sys
import glob
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="QnA Agent - CSV Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for cleaner styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .result-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

def create_artifacts_folder():
    """Create artifacts folder if it doesn't exist."""
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    return artifacts_dir

def initialize_agent():
    """Initialize the QnA agent."""
    if 'agent' not in st.session_state:
        st.session_state.agent = AdvancedQnAAgent()
    return st.session_state.agent

def display_generated_images():
    """Display any generated images from the artifacts folder."""
    artifacts_dir = create_artifacts_folder()
    image_files = glob.glob(os.path.join(artifacts_dir, "*.png")) + glob.glob(os.path.join(artifacts_dir, "*.jpg")) + glob.glob(os.path.join(artifacts_dir, "*.jpeg"))
    
    if image_files:
        # Sort by modification time (newest first)
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        st.subheader("📊 Generated Visualizations")
        for img_path in image_files[:5]:  # Show last 5 images
            img_name = os.path.basename(img_path)
            st.image(img_path, caption=img_name, use_column_width=True)

def main():
    # Create artifacts folder
    create_artifacts_folder()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 QnA Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload or download CSV files and ask questions in natural language</p>', unsafe_allow_html=True)
    
    # Initialize agent
    agent = initialize_agent()
    
    # Main layout with tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📁 Files", "ℹ️ Info"])
    
    with tab1:
        # Analysis section
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.header("💬 Ask Questions")
            
            # Query input
            query = st.text_area(
                "Ask a question about your data",
                placeholder="e.g., Which employee has the highest salary? Show me a summary of the data. Create a visualization of salary distribution.",
                height=120,
                help="Ask any question about your CSV data in natural language"
            )
            
            # Submit button
            if st.button("🚀 Analyze", type="primary", use_container_width=True):
                if not agent.current_csv_file:
                    st.error("❌ No CSV file loaded. Please upload or download a file first.")
                elif not query.strip():
                    st.error("❌ Please enter a question to analyze.")
                else:
                    with st.spinner("🤖 Analyzing your data..."):
                        try:
                            result = agent.analyze_data(query)
                            st.success("✅ Analysis complete!")
                            
                            # Display results
                            st.subheader("📊 Results")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            
                            # Display generated images
                            display_generated_images()
                            
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
            
            # Quick examples
            with st.expander("💡 Example Queries"):
                st.markdown("""
                **Basic Analysis:**
                - Show me a summary of the data
                - What are the data types?
                - Are there any missing values?
                
                **Statistical Analysis:**
                - Which employee has the highest salary?
                - What is the average salary?
                - Show me the salary distribution
                
                **Visualization:**
                - Create a histogram of salaries
                - Plot the data distribution
                - Show me a correlation matrix
                """)
        
        with col2:
            st.header("📋 Status")
            
                    # Show current file
        if agent.current_csv_file:
            st.success("✅ File loaded")
            st.write(f"**File:** {os.path.basename(agent.current_csv_file)}")
            
            # Show special message for default employees.csv
            if os.path.basename(agent.current_csv_file) == "employees.csv":
                st.info("📋 Using default employees.csv dataset")
                
                # Show file info
                try:
                    df = pd.read_csv(agent.current_csv_file)
                    st.metric("Rows", df.shape[0])
                    st.metric("Columns", df.shape[1])
                    
                    # Show sample data
                    with st.expander("📋 Sample Data"):
                        st.dataframe(df.head(), use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
            else:
                st.warning("⚠️ No file loaded")
                st.info("Upload or download a CSV file to get started")
    
    with tab2:
        # Files section
        st.header("📁 File Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Upload File")
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type=['csv'],
                help="Upload a CSV file to analyze"
            )
            
            if uploaded_file is not None:
                # Save uploaded file to downloads folder
                os.makedirs("downloads", exist_ok=True)
                file_path = os.path.join("downloads", uploaded_file.name)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load the file
                agent.current_csv_file = file_path
                st.success(f"✅ File uploaded and loaded: {uploaded_file.name}")
                
                # Show file info
                try:
                    df = pd.read_csv(file_path)
                    st.info(f"📊 Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with col2:
            st.subheader("🌐 Download from URL")
            url = st.text_input(
                "Enter CSV URL",
                placeholder="https://example.com/data.csv",
                help="Enter a URL to download a CSV file"
            )
            
            if st.button("Download CSV", type="primary"):
                if url:
                    with st.spinner("Downloading..."):
                        try:
                            result = agent.download_csv(url)
                            st.success(result)
                        except Exception as e:
                            st.error(f"Download failed: {str(e)}")
                else:
                    st.warning("Please enter a URL")
        
        # Load existing files
        st.subheader("📂 Load Existing Files")
        csv_files = glob.glob("downloads/*.csv")
        if csv_files:
            # Sort by modification time (newest first)
            csv_files.sort(key=os.path.getmtime, reverse=True)
            
            selected_file = st.selectbox(
                "Select a file to load",
                [os.path.basename(f) for f in csv_files],
                help="Choose from previously downloaded files"
            )
            
            if st.button("Load Selected File"):
                try:
                    result = agent.load_existing_csv(f"load {selected_file}")
                    st.success(result)
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        else:
            st.info("No CSV files found in downloads folder")
    
    with tab3:
        # Info section
        st.header("ℹ️ System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 System Info")
            st.write(f"**Python:** {sys.version.split()[0]}")
            st.write(f"**Pandas:** {pd.__version__}")
            
            # API status
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                st.success("✅ OpenAI API configured")
            else:
                st.error("❌ OpenAI API key not found")
        
        with col2:
            st.subheader("📁 Folders")
            artifacts_dir = create_artifacts_folder()
            downloads_dir = "downloads"
            os.makedirs(downloads_dir, exist_ok=True)
            
            st.write(f"**Downloads:** {downloads_dir}/")
            st.write(f"**Artifacts:** {artifacts_dir}/")
            
            # Show file counts
            csv_count = len(glob.glob("downloads/*.csv"))
            artifact_count = len(glob.glob("artifacts/*"))
            st.metric("CSV Files", csv_count)
            st.metric("Artifacts", artifact_count)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by GPT-4.1 | 📊 Built with Streamlit | 💻 LLM-Powered Code Generation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
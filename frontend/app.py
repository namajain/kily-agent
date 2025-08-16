"""
Streamlit Frontend for MVP - User interface with Socket.IO backend integration
"""
import streamlit as st
import socketio
import json
import time
from datetime import datetime
import os
import sys
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="Enhanced QnA Agent - MVP",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .status-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    .profile-card {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .profile-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .profile-card.selected {
        border-color: #1f77b4;
        background-color: #e3f2fd;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitFrontend:
    """
    Streamlit frontend that connects to Socket.IO backend.
    """
    
    def __init__(self, backend_url: str = "http://localhost:5001"):
        self.backend_url = backend_url
        self.socket = None
        self.session_id = None
        self.user_id = None
        self.profile_id = None
        self.profile_name = None
        self.connected = False
        self.chat_history = []
        self.user_profiles = []
        
        # Initialize Socket.IO connection
        self._init_socket()
    
    def _init_socket(self):
        """Initialize Socket.IO connection"""
        try:
            self.socket = socketio.Client()
            
            # Setup event handlers
            @self.socket.on('connect')
            def on_connect():
                st.session_state.connected = True
            
            @self.socket.on('disconnect')
            def on_disconnect():
                st.session_state.connected = False
            
            @self.socket.on('connected')
            def on_connected(data):
                st.success(f"Connected to backend: {data.get('message', '')}")
            
            @self.socket.on('authenticated')
            def on_authenticated(data):
                st.success(f"Authenticated: {data.get('message', '')}")
            
            @self.socket.on('auth_error')
            def on_auth_error(data):
                st.error(f"Authentication error: {data.get('message', '')}")
            
            @self.socket.on('chat_started')
            def on_chat_started(data):
                st.session_state.session_id = data.get('session_id')
                st.session_state.profile_name = data.get('profile_name')
                st.success(f"Chat started: {data.get('message', '')}")
            
            @self.socket.on('message_response')
            def on_message_response(data):
                response = {
                    'type': 'assistant',
                    'content': data.get('response', ''),
                    'timestamp': data.get('timestamp', '')
                }
                st.session_state.chat_history.append(response)
            
            @self.socket.on('chat_history')
            def on_chat_history(data):
                st.session_state.chat_history = data.get('history', [])
            

            
            @self.socket.on('context_summary')
            def on_context_summary(data):
                st.session_state.context_summary = data.get('summary', '')
                st.session_state.datasets = data.get('datasets', [])
            
            @self.socket.on('error')
            def on_error(data):
                st.error(f"Error: {data.get('message', '')}")
            
            # Connect to backend
            self.socket.connect(self.backend_url)
            self.connected = True
            st.session_state.connected = True
            
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
            self.connected = False
            st.session_state.connected = False
    
    def main(self):
        """Main Streamlit application"""
        # Header
        st.markdown('<h1 class="main-header">🤖 Enhanced QnA Agent</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">MVP Version - Profile-based Data Analysis</p>', unsafe_allow_html=True)
        
        # Initialize session state
        if 'connected' not in st.session_state:
            st.session_state.connected = False
        if 'session_id' not in st.session_state:
            st.session_state.session_id = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'user_profiles' not in st.session_state:
            st.session_state.user_profiles = []
        if 'context_summary' not in st.session_state:
            st.session_state.context_summary = None
        if 'datasets' not in st.session_state:
            st.session_state.datasets = []
        
        # Sidebar for authentication and profile selection
        with st.sidebar:
            st.header("🔐 Authentication")
            

            
            # User ID input
            user_id = st.text_input("User ID", value="user1", help="Enter your user ID")
            
            # Load user profiles
            if st.button("Load Profiles"):
                try:
                    import requests
                    response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.user_profiles = data.get('profiles', [])
                        print(f"🔔 Loaded {len(st.session_state.user_profiles)} profiles via REST")
                        st.success(f"Loaded {len(st.session_state.user_profiles)} profiles")
                    else:
                        st.error(f"Failed to load profiles: {response.status_code}")
                except Exception as e:
                    st.error(f"Error loading profiles: {e}")
            
            # Display user profiles
            if st.session_state.user_profiles:
                st.subheader("📁 Available Profiles")
                
                for profile in st.session_state.user_profiles:
                    profile_data = profile.get('data_sources', [])
                    if isinstance(profile_data, str):
                        try:
                            profile_data = json.loads(profile_data)
                        except:
                            profile_data = []
                    data_sources_count = len(profile_data)
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="profile-card">
                            <h4>{profile['profile_name']}</h4>
                            <p><strong>ID:</strong> {profile['profile_id']}</p>
                            <p><strong>Data Sources:</strong> {data_sources_count}</p>
                            <p><strong>Status:</strong> {'🟢 Active' if profile['is_active'] else '🔴 Inactive'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show data source details in an expander
                        if profile_data:
                            with st.expander(f"📊 View {data_sources_count} Data Sources"):
                                for i, source in enumerate(profile_data, 1):
                                    st.markdown(f"""
                                    **{i}. {source.get('filename', 'Unknown')}**
                                    - Description: {source.get('description', 'No description')}
                                    - URL: `{source.get('url', 'No URL')}`
                                    """)
                        
                        if st.button(f"Select {profile['profile_name']}", key=f"profile_{profile['profile_id']}"):
                            self._start_chat(user_id, profile['profile_id'])
            
            # Connection status
            st.subheader("🔗 Connection Status")
            if st.session_state.connected:
                st.success("✅ Connected to Backend")
            else:
                st.error("❌ Disconnected from Backend")
            
            # Session info
            if st.session_state.session_id:
                st.subheader("💬 Active Session")
                st.info(f"Session ID: {st.session_state.session_id[:8]}...")
                if st.session_state.profile_name:
                    st.info(f"Profile: {st.session_state.profile_name}")
                
                if st.button("End Session"):
                    if self.socket and self.connected:
                        self.socket.emit('end_session', {'session_id': st.session_state.session_id})
                        st.session_state.session_id = None
                        st.session_state.chat_history = []
                        st.rerun()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chat interface
            if st.session_state.session_id:
                st.header("💬 Chat Interface")
                
                # Display chat history
                chat_container = st.container()
                with chat_container:
                    for message in st.session_state.chat_history:
                        if message['type'] == 'user':
                            st.markdown(f"""
                            <div class="chat-message user-message">
                                <strong>You:</strong> {message['content']}
                                <br><small>{message.get('timestamp', '')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="chat-message assistant-message">
                                <strong>Assistant:</strong> {message['content']}
                                <br><small>{message.get('timestamp', '')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Message input
                with st.form("chat_form"):
                    message = st.text_area(
                        "Ask a question about your data",
                        placeholder="e.g., Show me a summary of the data, Create a visualization, What are the trends?",
                        height=100
                    )
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        submitted = st.form_submit_button("Send Message", type="primary")
                    with col2:
                        if st.form_submit_button("Get Context Summary"):
                            if self.socket and self.connected:
                                self.socket.emit('get_context_summary', {'session_id': st.session_state.session_id})
                    
                    if submitted and message:
                        if self.socket and self.connected:
                            self.socket.emit('send_message', {
                                'session_id': st.session_state.session_id,
                                'message': message
                            })
                        else:
                            st.error("Not connected to backend")
                
                # Example queries
                with st.expander("💡 Example Queries"):
                    st.markdown("""
                    **Basic Analysis:**
                    - Show me a summary of the data
                    - What are the data types?
                    - Are there any missing values?
                    
                    **Statistical Analysis:**
                    - What is the average value?
                    - Show me the distribution
                    - Find correlations between variables
                    
                    **Visualization:**
                    - Create a histogram
                    - Plot the data over time
                    - Show me a scatter plot
                    """)
            
            else:
                st.header("🚀 Get Started")
                st.info("Please select a profile from the sidebar to start chatting.")
                
                # Quick start guide
                with st.expander("📖 Quick Start Guide"):
                    st.markdown("""
                    1. **Enter your User ID** in the sidebar
                    2. **Click "Load Profiles"** to see available profiles
                    3. **Select a Profile** to start a chat session
                    4. **Ask questions** about your data in natural language
                    5. **View results** and visualizations
                    """)
        
        with col2:
            # Context information
            if st.session_state.session_id:
                st.header("📊 Context Information")
                
                # Get context summary
                if st.button("Refresh Context"):
                    if self.socket and self.connected:
                        self.socket.emit('get_context_summary', {'session_id': st.session_state.session_id})
                
                # Display datasets
                if st.session_state.datasets:
                    st.subheader("📁 Available Datasets")
                    for dataset in st.session_state.datasets:
                        with st.expander(f"📄 {dataset['filename']}"):
                            st.write(f"**Rows:** {dataset['rows']:,}")
                            st.write(f"**Columns:** {dataset['columns']}")
                            st.write(f"**Memory:** {dataset['memory_usage_kb']:.2f} KB")
                            
                            st.write("**Columns:**")
                            for col in dataset['column_names']:
                                st.write(f"- {col}")
                
                # Display context summary
                if st.session_state.context_summary:
                    st.subheader("📋 Data Summary")
                    st.markdown(st.session_state.context_summary)
            
            # System information
            st.header("ℹ️ System Info")
            
            # Connection info
            st.write(f"**Backend URL:** {self.backend_url}")
            st.write(f"**Connection:** {'✅ Connected' if st.session_state.connected else '❌ Disconnected'}")
            
            if st.session_state.session_id:
                st.write(f"**Session ID:** {st.session_state.session_id[:8]}...")
                st.write(f"**Profile:** {st.session_state.profile_name or 'Unknown'}")
                st.write(f"**Messages:** {len(st.session_state.chat_history)}")
    
    def _start_chat(self, user_id: str, profile_id: str):
        """Start a chat session for a specific profile"""
        if self.socket and self.connected:
            self.socket.emit('start_chat', {
                'user_id': user_id,
                'profile_id': profile_id
            })
        else:
            st.error("Not connected to backend")

def main():
    """Main entry point"""
    # Create frontend instance
    frontend = StreamlitFrontend()
    
    # Run the main application
    frontend.main()

if __name__ == "__main__":
    main() 
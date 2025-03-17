import streamlit as st

def apply_theme(theme_name):
    """Apply the selected theme to the application"""
    
    # Base theme configuration
    theme_config = {
        "dark": {
            "primaryColor": "#8ec5fc",
            "backgroundColor": "#121212",
            "secondaryBackgroundColor": "#1e1e1e",
            "textColor": "#ffffff",
            "surfaceColor": "rgba(255, 255, 255, 0.05)",
            "onSurfaceColor": "rgba(255, 255, 255, 0.87)",
            "elevation1": "rgba(255, 255, 255, 0.05)",
            "elevation2": "rgba(255, 255, 255, 0.07)",
            "elevation3": "rgba(255, 255, 255, 0.09)"
        },
        "light": {
            "primaryColor": "#2196f3",
            "backgroundColor": "#ffffff",
            "secondaryBackgroundColor": "#f5f5f5",
            "textColor": "#212121",
            "surfaceColor": "#ffffff",
            "onSurfaceColor": "rgba(0, 0, 0, 0.87)",
            "elevation1": "rgba(0, 0, 0, 0.05)",
            "elevation2": "rgba(0, 0, 0, 0.07)",
            "elevation3": "rgba(0, 0, 0, 0.09)"
        }
    }
    
    # Get theme configuration
    theme = theme_config.get(theme_name, theme_config["dark"])
    
    # Apply theme using st.markdown with CSS
    st.markdown(f"""
        <style>
        /* Theme variables */
        :root {{
            --primary: {theme["primaryColor"]};
            --background: {theme["backgroundColor"]};
            --background-secondary: {theme["secondaryBackgroundColor"]};
            --text: {theme["textColor"]};
            --surface: {theme["surfaceColor"]};
            --on-surface: {theme["onSurfaceColor"]};
            --elevation-1: {theme["elevation1"]};
            --elevation-2: {theme["elevation2"]};
            --elevation-3: {theme["elevation3"]};
        }}
        
        /* Base styles */
        .stApp {{
            background: var(--background) !important;
            color: var(--text) !important;
        }}
        
        .stMarkdown {{
            color: var(--text) !important;
        }}
        
        /* Streamlit component overrides */
        .stButton > button {{
            background: var(--surface) !important;
            color: var(--on-surface) !important;
            border: 1px solid {theme["elevation1"]} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        .stButton > button:hover {{
            background: {theme["elevation2"]} !important;
            border-color: {theme["elevation3"]} !important;
            transform: translateY(-1px);
        }}
        
        .stTextArea > div > div > textarea {{
            background: var(--surface) !important;
            color: var(--text) !important;
            border: 1px solid {theme["elevation1"]} !important;
        }}
        
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 1px var(--primary) !important;
        }}
        
        .stSelectbox > div > div > div {{
            background: var(--surface) !important;
            color: var(--text) !important;
            border: 1px solid {theme["elevation1"]} !important;
        }}
        
        .stSelectbox > div > div > div:hover {{
            border-color: {theme["elevation3"]} !important;
        }}
        
        .stMultiSelect > div > div > div {{
            background: var(--surface) !important;
            color: var(--text) !important;
            border: 1px solid {theme["elevation1"]} !important;
        }}
        
        /* Sidebar and header */
        section[data-testid="stSidebar"] {{
            background: var(--background-secondary) !important;
            border-right: 1px solid {theme["elevation1"]} !important;
        }}
        
        .stApp > header {{
            background: var(--background-secondary) !important;
            border-bottom: 1px solid {theme["elevation1"]} !important;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--background);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme["elevation2"]};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme["elevation3"]};
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # Store theme in session state
    st.session_state.theme = theme_name

import streamlit as st
import firebase_admin
from firebase_admin import auth
import json
from functools import wraps

def init_auth():
    """Initialize authentication state in session"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'auth_status' not in st.session_state:
        st.session_state.auth_status = None

def login_required(func):
    """Decorator to require login for certain pages"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.user:
            st.warning("Please log in to access this feature.")
            return False
        return func(*args, **kwargs)
    return wrapper

def show_login():
    """Display login form"""
    st.markdown("""
    <div class="reflection-box">
        <h2>Welcome Back</h2>
        <p>Please log in to continue your journaling journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.user = user
                st.session_state.auth_status = "logged_in"
                st.success("Successfully logged in!")
                st.rerun()
            except Exception as e:
                st.error("Invalid credentials. Please try again.")
    
    with col2:
        if st.button("Sign Up"):
            st.session_state.auth_status = "signup"
            st.rerun()

def show_signup():
    """Display signup form"""
    st.markdown("""
    <div class="reflection-box">
        <h2>Create Account</h2>
        <p>Join us on your journaling journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Create Account"):
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
        
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            st.success("Account created successfully! Please log in.")
            st.session_state.auth_status = "login"
            st.rerun()
        except Exception as e:
            st.error(f"Error creating account: {str(e)}")
    
    if st.button("Back to Login"):
        st.session_state.auth_status = "login"
        st.rerun()

def logout():
    """Log out the current user"""
    st.session_state.user = None
    st.session_state.auth_status = "login"
    st.rerun()

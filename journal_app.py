import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from prompts import PromptGenerator
from theme import apply_theme
import random
import base64
import io
import matplotlib.pyplot as plt
from collections import Counter

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = pd.DataFrame(columns=['date', 'content', 'mood', 'themes'])
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Apply theme
apply_theme(st.session_state.theme)

# Load CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize PromptGenerator
prompt_generator = PromptGenerator(st.session_state.entries)

# Logo and avatar base64 strings
LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjMtMDMtMTZUMjE6MTA6NTQtMDU6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjMtMDMtMTZUMjE6MTA6NTQtMDU6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDIzLTAzLTE2VDIxOjEwOjU0LTA1OjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgc3RFdnQ6d2hlbj0iMjAyMy0wMy0xNlQyMToxMDo1NC0wNTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDI0LjAgKE1hY2ludG9zaCkiLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+"

AVATAR_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjMtMDMtMTZUMjE6MTA6NTQtMDU6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjMtMDMtMTZUMjE6MTA6NTQtMDU6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDIzLTAzLTE2VDIxOjEwOjU0LTA1OjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjA5ZDFkNzE3LTI3ZDctNDZiMC1iYmJkLTJkYmRkOGU1ZjJlYyIgc3RFdnQ6d2hlbj0iMjAyMy0wMy0xNlQyMToxMDo1NC0wNTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDI0LjAgKE1hY2ludG9zaCkiLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+"

def generate_weekly_report():
    """Generate a weekly report of journal entries and mood trends"""
    if len(st.session_state.entries) == 0:
        return None
    
    # Convert entries to DataFrame if not already
    df = st.session_state.entries if isinstance(st.session_state.entries, pd.DataFrame) else pd.DataFrame(st.session_state.entries)
    
    # Get entries from the last 7 days
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    weekly_entries = df[pd.to_datetime(df['date']).dt.date >= week_ago]
    
    if len(weekly_entries) == 0:
        return None
    
    # Create report buffer
    buffer = io.BytesIO()
    
    # Create mood trend visualization
    plt.figure(figsize=(10, 6))
    mood_counts = Counter(weekly_entries['mood'])
    moods = list(mood_counts.keys())
    counts = list(mood_counts.values())
    
    plt.bar(moods, counts)
    plt.title('Weekly Mood Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to buffer
    plt.savefig(buffer, format='png')
    plt.close()
    
    # Generate report content
    report_content = f"""# Weekly Journal Report
Generated on {today}

## Summary
- Total Entries: {len(weekly_entries)}
- Most Common Mood: {max(mood_counts.items(), key=lambda x: x[1])[0]}
- Unique Themes: {len(set(theme.strip() for themes in weekly_entries['themes'].dropna() for theme in themes.split(',')))}

## Daily Breakdown
"""
    
    # Add daily entries
    for date in sorted(weekly_entries['date'].unique()):
        day_entries = weekly_entries[weekly_entries['date'] == date]
        report_content += f"\n### {date}\n"
        for _, entry in day_entries.iterrows():
            report_content += f"- Mood: {entry['mood']}\n"
            report_content += f"- Themes: {entry['themes']}\n"
            report_content += f"- Entry: {entry['content'][:200]}...\n\n"
    
    return report_content, buffer

def show_back_button():
    """Show a styled back button with an arrow"""
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.current_page = "welcome"
        st.rerun()

def show_welcome_page():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="LaSoanyah" class="logo-image">
            <div class="logo-text">Your Conscious Journal</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="welcome-box fade-in">
            <h2>Welcome to Your Personal Space</h2>
            <p>A place for reflection, growth, and self-discovery.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="nav-buttons fade-in">', unsafe_allow_html=True)
        
        if st.button("📝 New Entry", use_container_width=True, key="new_entry"):
            st.session_state.current_page = "new_entry"
            st.rerun()
        
        if st.button("📚 Past Entries", use_container_width=True, key="past_entries"):
            st.session_state.current_page = "past_entries"
            st.rerun()
        
        if st.button("📊 Weekly Report", use_container_width=True, key="weekly_report"):
            st.session_state.current_page = "weekly_report"
            st.rerun()
        
        if st.button("⚙️ Settings", use_container_width=True, key="settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_settings_page():
    show_back_button()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="data:image/png;base64,{AVATAR_BASE64}" alt="Avatar" class="avatar-image">
        <div class="logo-text">Settings</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="settings-container fade-in">
            <h2>Appearance</h2>
            <p>Customize your journal's look and feel</p>
        </div>
        """, unsafe_allow_html=True)
        
        theme = st.selectbox('Theme Mode', ['dark', 'light'], 
                           index=0 if st.session_state.theme == 'dark' else 1,
                           format_func=lambda x: x.capitalize())
        
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            apply_theme(theme)
            st.rerun()

def show_weekly_report_page():
    show_back_button()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="data:image/png;base64,{AVATAR_BASE64}" alt="Avatar" class="avatar-image">
        <div class="logo-text">Weekly Report</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if it's Thursday
    is_thursday = datetime.now().weekday() == 3
    
    if is_thursday:
        st.markdown("""
        <div class="report-container fade-in">
            <h2>Your Weekly Journal Report</h2>
            <p>Download your report for group discussion</p>
        </div>
        """, unsafe_allow_html=True)
        
        report = generate_weekly_report()
        if report:
            report_content, plot_buffer = report
            
            # Display report preview
            st.markdown(report_content)
            
            # Display mood visualization
            st.image(plot_buffer, caption='Weekly Mood Distribution')
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Report (MD)",
                    data=report_content,
                    file_name=f"journal_report_{datetime.now().date()}.md",
                    mime="text/markdown"
                )
            with col2:
                plot_buffer.seek(0)
                st.download_button(
                    label="📥 Download Chart (PNG)",
                    data=plot_buffer,
                    file_name=f"mood_distribution_{datetime.now().date()}.png",
                    mime="image/png"
                )
        else:
            st.info("No journal entries found for the past week. Start journaling to generate a report!")
    else:
        st.info("Weekly reports are generated every Thursday. Please check back then!")

def show_journal_entry_page():
    show_back_button()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="data:image/png;base64,{LOGO_BASE64}" alt="LaSoanyah" class="logo-image">
        <div class="logo-text">New Entry</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="journal-container fade-in">
            <h2>Express Yourself</h2>
            <p>Write freely about your thoughts, feelings, and experiences.</p>
        </div>
        """, unsafe_allow_html=True)
        
        entry = st.text_area("Journal Entry", height=300,
                           placeholder="Start writing here...",
                           key="journal_entry",
                           label_visibility="collapsed")
        
        st.markdown('<div class="mood-selector">', unsafe_allow_html=True)
        mood = st.select_slider(
            "Current Mood",
            options=[" Sad", " Confused", " Neutral", " Content", " Happy"],
            value=" Neutral"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="prompt-box fade-in">
            <h3>Writing Prompts</h3>
            <p>Use these prompts as inspiration for your journal entry.</p>
        </div>
        """, unsafe_allow_html=True)
        
        time_based_prompts = prompt_generator.get_time_based_prompts()
        personalized_prompts = prompt_generator.get_personalized_prompts()
        
        for prompt in random.sample(time_based_prompts, 2):
            st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
        
        for prompt in personalized_prompts[:2]:
            st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button(" Save Entry", use_container_width=True):
            if entry.strip():
                now = datetime.now()
                themes = prompt_generator.analyze_entry_themes(entry)
                
                new_entry = {
                    'date': now.date(),
                    'content': entry,
                    'mood': mood,
                    'themes': ', '.join(themes)
                }
                
                new_df = pd.DataFrame([new_entry])
                st.session_state.entries = pd.concat([st.session_state.entries, new_df], ignore_index=True)
                
                st.success("Journal entry saved successfully!")
                st.session_state.current_page = "past_entries"
                st.rerun()

def show_past_entries_page():
    show_back_button()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="data:image/png;base64,{AVATAR_BASE64}" alt="Avatar" class="avatar-image">
        <div class="logo-text">Past Entries</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="journal-container fade-in">
        <h2>Your Journal History</h2>
        <p>Review and reflect on your past entries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.entries) > 0:
        # Add filters
        col1, col2 = st.columns(2)
        with col1:
            mood_filter = st.multiselect("Filter by Mood", st.session_state.entries['mood'].unique())
        with col2:
            all_themes = [theme.strip() for themes in st.session_state.entries['themes'].dropna() for theme in themes.split(',')]
            unique_themes = sorted(list(set(all_themes)))
            theme_filter = st.multiselect("Filter by Theme", unique_themes)
        
        # Apply filters
        filtered_entries = st.session_state.entries.copy()
        if mood_filter:
            filtered_entries = filtered_entries[filtered_entries['mood'].isin(mood_filter)]
        if theme_filter:
            filtered_entries = filtered_entries[filtered_entries['themes'].apply(lambda x: any(theme in x.split(', ') for theme in theme_filter))]
        
        # Display entries
        for _, entry in filtered_entries.iterrows():
            st.markdown(f"""
            <div class="journal-container fade-in">
                <p style="color: var(--on-surface); opacity: 0.7;">{entry['date']}</p>
                <h3>{entry['mood']} | Themes: {entry['themes']}</h3>
                <p>{entry['content']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No journal entries yet. Start writing to see your entries here!")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button(" New Entry", use_container_width=True):
            st.session_state.current_page = "new_entry"
            st.rerun()

# Main app logic
def main():
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'new_entry':
        show_journal_entry_page()
    elif st.session_state.current_page == 'past_entries':
        show_past_entries_page()
    elif st.session_state.current_page == 'settings':
        show_settings_page()
    elif st.session_state.current_page == 'weekly_report':
        show_weekly_report_page()

if __name__ == '__main__':
    main()
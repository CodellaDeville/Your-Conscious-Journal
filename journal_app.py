import streamlit as st
import datetime
import os
import pandas as pd
import base64
from PIL import Image
import io

# Set page configuration
st.set_page_config(page_title="Daily Journaling Coach", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to style the app
st.markdown("""
<style>
/* Gradient background inspired by the swirling design */
.main {
    background: linear-gradient(135deg, #1a2639, #2d3a59, #3b1e5f, #6b2c91, #9b4dca, #4a69bd, #0984e3, #e17055, #d63031);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: #ffffff;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton button {
    background-color: #e75a7c;
    color: white;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    border: none;
}
.stTextInput, .stTextArea {
    background-color: #2d3a59;
    color: white;
    border-radius: 5px;
}
.reflection-box {
    background-color: rgba(45, 58, 89, 0.8);
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 1rem;
    backdrop-filter: blur(5px);
}
.avatar-container {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
}
/* Voice to text button styling */
.mic-button {
    background-color: #4a69bd;
    color: white;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin: 10px 0;
    border: none;
    transition: all 0.3s ease;
}
.mic-button:hover {
    background-color: #0984e3;
    transform: scale(1.05);
}
.mic-button.recording {
    background-color: #e17055;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
.mic-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.mic-status {
    margin-left: 10px;
    font-style: italic;
    color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# Add JavaScript for speech recognition
st.markdown("""
<script>
    // This function will be called when the page is loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Set up the speech recognition functionality after a short delay to ensure DOM is ready
        setTimeout(setupSpeechRecognition, 1000);
    });
    
    // Also add a MutationObserver to handle Streamlit's dynamic loading
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                setTimeout(setupSpeechRecognition, 500);
            }
        });
    });
    
    // Start observing the document body for DOM changes
    window.addEventListener('load', function() {
        observer.observe(document.body, { childList: true, subtree: true });
        // Initial setup attempt
        setTimeout(setupSpeechRecognition, 500);
    });
    
    // Listen for our custom event from the mic initializer
    document.addEventListener('micButtonReady', function() {
        console.log('Mic button ready event received');
        setupSpeechRecognition();
    });
    
    // Set an interval to periodically check for the mic button
    setInterval(function() {
        const micButton = document.getElementById('mic-button');
        if (micButton && !micButton.hasAttribute('data-initialized')) {
            console.log('Found mic button via interval');
            micButton.setAttribute('data-initialized', 'true');
            setupSpeechRecognition();
        }
    }, 1000);
    
    function setupSpeechRecognition() {
        // Check if the browser supports speech recognition
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Speech recognition not supported in this browser');
            return;
        }
        
        // Create speech recognition object
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Set properties
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        // Find the microphone button and text area
        const micButton = document.getElementById('mic-button');
        if (!micButton) {
            console.error('Microphone button not found');
            return;
        }
        
        let isRecording = false;
        let textArea = null;
        
        // Function to find the text area element
        function findTextArea() {
            const textAreas = document.querySelectorAll('textarea');
            // We want the journal entry text area
            for (let i = 0; i < textAreas.length; i++) {
                if (textAreas[i].placeholder && textAreas[i].placeholder.includes('journal entry')) {
                    return textAreas[i];
                }
            }
            // If we can't find it by placeholder, just use the first text area
            return textAreas.length > 0 ? textAreas[0] : null;
        }
        
        // Handle click on mic button
        micButton.addEventListener('click', function() {
            textArea = findTextArea();
            if (!textArea) {
                console.error('Text area not found');
                return;
            }
            
            if (!isRecording) {
                // Start recording
                recognition.start();
                micButton.classList.add('recording');
                document.getElementById('mic-status').textContent = 'Listening...';
                isRecording = true;
            } else {
                // Stop recording
                recognition.stop();
                micButton.classList.remove('recording');
                document.getElementById('mic-status').textContent = 'Click to start speaking';
                isRecording = false;
            }
        });
        
        // Process speech recognition results
        recognition.onresult = function(event) {
            if (!textArea) return;
            
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    transcript += event.results[i][0].transcript + ' ';
                }
            }
            
            if (transcript) {
                // Append to existing text
                textArea.value += transcript;
                // Trigger an input event to update Streamlit's state
                const event = new Event('input', { bubbles: true });
                textArea.dispatchEvent(event);
            }
        };
        
        // Handle errors
        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
            micButton.classList.remove('recording');
            document.getElementById('mic-status').textContent = 'Error: ' + event.error;
            isRecording = false;
        };
        
        // Handle end of speech recognition
        recognition.onend = function() {
            if (isRecording) {
                // If still recording, restart recognition (for continuous listening)
                recognition.start();
            }
        };
    }
</script>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'entries' not in st.session_state:
    st.session_state.entries = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

if 'time_of_day' not in st.session_state:
    # Determine time of day based on current hour
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        st.session_state.time_of_day = 'morning'
    elif 12 <= current_hour < 18:
        st.session_state.time_of_day = 'afternoon'
    else:
        st.session_state.time_of_day = 'evening'

# Function to save journal entry
def save_entry(entry_data):
    st.session_state.entries.append(entry_data)
    
    # Create data directory if it doesn't exist
    if not os.path.exists('journal_data'):
        os.makedirs('journal_data')
    
    # Save to CSV
    df = pd.DataFrame(st.session_state.entries)
    df.to_csv('journal_data/journal_entries.csv', index=False)

# Function to generate downloadable report
def get_download_link(file_path, link_text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return href

# Function to generate weekly report
def generate_weekly_report():
    if len(st.session_state.entries) == 0:
        return "No entries available for report generation."
    
    df = pd.DataFrame(st.session_state.entries)
    
    # Basic statistics
    total_entries = len(df)
    mood_summary = df['mood'].value_counts().to_dict() if 'mood' in df.columns else {}
    
    # Generate report text
    report = f"Weekly Journal Report - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += f"Total Entries: {total_entries}\n\n"
    
    if mood_summary:
        report += "Mood Summary:\n"
        for mood, count in mood_summary.items():
            report += f"  {mood}: {count} entries\n"
    
    report += "\nRecent Entries:\n"
    for i, row in df.tail(5).iterrows():
        report += f"\nDate: {row.get('date', 'N/A')}\n"
        report += f"Time of Day: {row.get('time_of_day', 'N/A')}\n"
        report += f"Mood: {row.get('mood', 'N/A')}\n"
        report += f"Entry: {row.get('entry', 'N/A')[:100]}...\n"
    
    # Save report to file
    if not os.path.exists('journal_data'):
        os.makedirs('journal_data')
    
    report_path = 'journal_data/weekly_report.txt'
    with open(report_path, 'w') as f:
        f.write(report)
    
    return report_path

# Welcome page
def show_welcome_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>Daily Journaling Coach</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Your companion for mindful reflection</p>", unsafe_allow_html=True)
        
        # Display avatar
        st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
        st.image('avatar_proper.svg', width=150)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Welcome message
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("Hi there! I'm your journaling coach. I'm here to guide you through a reflective journaling exercise. Let's get started!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Name input
        st.text_input("What's your name?", key="name_input")
        
        # Start button
        if st.button("Begin Journaling"):
            st.session_state.user_name = st.session_state.name_input
            st.session_state.current_page = 'time_selection'
            st.rerun()

# Time selection page
def show_time_selection_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>Before we begin, is it morning or evening for you right now?</h2>", unsafe_allow_html=True)
        
        # Display reflection box
        st.markdown("<div class='reflection-box'>", unsafe_allow_html=True)
        st.markdown("<h3>Reflection</h3>", unsafe_allow_html=True)
        st.markdown("The time of day can influence our mindset and the type of reflection that might be most beneficial. Morning journaling often focuses on setting intentions for the day ahead, while evening journaling tends to be more reflective of the day that has passed.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("Please let me know whether it's morning or evening, and I'll tailor our journaling session accordingly.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Morning"):
                st.session_state.time_of_day = 'morning'
                st.session_state.current_page = 'journal_entry'
                st.rerun()
        with col_b:
            if st.button("Evening"):
                st.session_state.time_of_day = 'evening'
                st.session_state.current_page = 'journal_entry'
                st.rerun()

# Journal entry page
def show_journal_entry_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.time_of_day.capitalize()} Reflection</h2>", unsafe_allow_html=True)
        
        # Display avatar
        st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
        st.image('avatar_proper.svg', width=100)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Different prompts based on time of day
        if st.session_state.time_of_day == 'morning':
            st.markdown("<div class='reflection-box'>", unsafe_allow_html=True)
            st.markdown("<h3>Morning Prompts</h3>", unsafe_allow_html=True)
            st.markdown("1. How did you sleep last night?")
            st.markdown("2. What's your intention for today?")
            st.markdown("3. What would make today great?")
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.time_of_day == 'afternoon':
            st.markdown("<div class='reflection-box'>", unsafe_allow_html=True)
            st.markdown("<h3>Afternoon Prompts</h3>", unsafe_allow_html=True)
            st.markdown("1. How's your energy level right now?")
            st.markdown("2. What challenges have you faced so far today?")
            st.markdown("3. What's one thing you're looking forward to for the rest of the day?")
            st.markdown("</div>", unsafe_allow_html=True)
        else:  # evening
            st.markdown("<div class='reflection-box'>", unsafe_allow_html=True)
            st.markdown("<h3>Evening Prompts</h3>", unsafe_allow_html=True)
            st.markdown("1. What went well today?")
            st.markdown("2. What could have gone better?")
            st.markdown("3. What are you grateful for today?")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Mood selection
        mood = st.selectbox(
            "How are you feeling right now?",
            ["Select mood", "Happy", "Content", "Neutral", "Anxious", "Stressed", "Tired", "Energetic", "Reflective"]
        )
        
        # Journal entry
        entry = st.text_area("Your journal entry:", height=200)
        
        # Tags
        tags = st.multiselect(
            "Tag your entry (optional):",
            ["Work", "Relationships", "Health", "Personal Growth", "Stress", "Anxiety", "Productivity", "Gratitude"]
        )
        
        # Save button
        if st.button("Save Entry"):
            if mood != "Select mood" and entry.strip() != "":
                entry_data = {
                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.datetime.now().strftime("%H:%M"),
                    'time_of_day': st.session_state.time_of_day,
                    'mood': mood,
                    'entry': entry,
                    'tags': ", ".join(tags) if tags else ""
                }
                
                save_entry(entry_data)
                st.session_state.current_page = 'confirmation'
                st.rerun()
            else:
                st.error("Please select a mood and write an entry before saving.")

# Confirmation page
def show_confirmation_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>Entry Saved!</h2>", unsafe_allow_html=True)
        
        # Display avatar
        st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
        st.image('avatar_proper.svg', width=100)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.success("Your journal entry has been saved successfully.")
        
        # Check if it's Thursday for weekly report
        if datetime.datetime.now().weekday() == 3:  # Thursday is 3
            st.markdown("### Weekly Report Available")
            st.markdown("It's Thursday! Would you like to generate your weekly reflection report?")
            
            if st.button("Generate Weekly Report"):
                report_path = generate_weekly_report()
                if report_path != "No entries available for report generation.":
                    st.markdown(get_download_link(report_path, "Download Weekly Report"), unsafe_allow_html=True)
                else:
                    st.warning(report_path)
        
        # Options for next steps
        st.markdown("### What would you like to do next?")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("New Entry"):
                st.session_state.current_page = 'time_selection'
                st.rerun()
        with col_b:
            if st.button("View Past Entries"):
                st.session_state.current_page = 'view_entries'
                st.rerun()

# View entries page
def show_view_entries_page():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>Your Journal Entries</h2>", unsafe_allow_html=True)
        
        if len(st.session_state.entries) == 0:
            st.info("You haven't made any journal entries yet.")
        else:
            # Display entries in reverse chronological order
            for i, entry in enumerate(reversed(st.session_state.entries)):
                with st.expander(f"{entry.get('date', 'N/A')} - {entry.get('time_of_day', 'N/A').capitalize()} - {entry.get('mood', 'N/A')}"):
                    st.markdown(f"**Time:** {entry.get('time', 'N/A')}")
                    st.markdown(f"**Mood:** {entry.get('mood', 'N/A')}")
                    if entry.get('tags', ""):
                        st.markdown(f"**Tags:** {entry.get('tags', 'N/A')}")
                    st.markdown(f"**Entry:**")
                    st.markdown(entry.get('entry', 'N/A'))
        
        # Generate report button
        if st.button("Generate Report"):
            report_path = generate_weekly_report()
            if report_path != "No entries available for report generation.":
                st.markdown(get_download_link(report_path, "Download Weekly Report"), unsafe_allow_html=True)
            else:
                st.warning(report_path)
        
        # Back button
        if st.button("Back"):
            st.session_state.current_page = 'confirmation'
            st.rerun()

# Main application flow
if __name__ == "__main__":
    # Try to load existing entries if available
    if os.path.exists('journal_data/journal_entries.csv'):
        try:
            df = pd.read_csv('journal_data/journal_entries.csv')
            st.session_state.entries = df.to_dict('records')
        except Exception as e:
            st.error(f"Error loading journal entries: {e}")
    
    # Display the appropriate page based on current_page state
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'time_selection':
        show_time_selection_page()
    elif st.session_state.current_page == 'journal_entry':
        show_journal_entry_page()
    elif st.session_state.current_page == 'confirmation':
        show_confirmation_page()
    elif st.session_state.current_page == 'view_entries':
        show_view_entries_page()

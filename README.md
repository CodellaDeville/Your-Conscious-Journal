# Daily Journaling Coach

An interactive journaling web application with a virtual coach avatar that guides users through daily journaling exercises with time-based prompts (morning, afternoon, evening).

## Features

- **Time-Based Prompts**: Different journaling prompts based on the time of day
  - Morning: Focus on intentions and goals for the day
  - Afternoon: Reflect on energy levels and challenges
  - Evening: Review the day and practice gratitude

- **Mood & Issue Tracking**: Track your mood and tag entries with common themes

- **Weekly Reports**: Generate and download weekly summary reports (available on Thursdays)

- **Journal History**: View and review all your past journal entries

- **Avatar Coach**: Guided by a friendly avatar coach throughout the journaling process

## Installation

1. Make sure you have Python installed (3.7 or higher recommended)

2. Install the required packages:
   ```
   pip install streamlit pandas pillow
   ```

3. Run the application:
   ```
   streamlit run journal_app.py
   ```

## Usage

1. Enter your name on the welcome screen
2. Select the time of day (or use the auto-detected time)
3. Follow the prompts to complete your journal entry
4. Save your entry and view past entries or create new ones
5. Generate weekly reports to track your mood patterns and reflections

## Data Storage

All journal entries are stored locally in the `journal_data` directory as CSV files. Weekly reports are generated as text files in the same directory.

## Deployment

This application can be deployed for free on Streamlit Community Cloud for web access.

## License

This project is open source and available for personal use.
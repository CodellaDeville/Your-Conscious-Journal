# Journaling with LaSoanyah

A mindful journaling application with AI-powered insights, sentiment analysis, and voice-to-text capabilities.

## Features

- **Voice-to-Text Journaling**: Speak your thoughts naturally with built-in speech recognition
- **AI-Powered Prompts**: Get personalized, time-based prompts to inspire your writing
- **Sentiment Analysis**: Track your emotional journey with automatic sentiment analysis
- **Theme Detection**: Automatically identify common themes in your entries
- **Mood Tracking**: Track your emotional state with intuitive emoji-based mood selection
- **Smart Analytics**:
  - Mood distribution visualization
  - Sentiment trend analysis
  - Theme frequency insights
  - Personalized progress reports
- **Tag System**: Organize entries with customizable tags
- **Dark/Light Themes**: Customize your journaling experience

## Installation

1. Make sure you have Python installed (3.7 or higher)

1. Install the required packages:

```bash
pip install -r requirements.txt
```

1. Run the application:

```bash
streamlit run journal_app.py
```

## Usage

1. Choose your preferred theme (default/dark/light)
2. Start journaling with AI-powered prompts
3. Use the microphone button for voice-to-text or type your entries
4. Select your mood and add relevant tags
5. View your entries, analytics, and download insights reports

## Features in Detail

### AI-Powered Prompts

- Time-based prompts that adapt to morning, afternoon, and evening
- Personalized prompts based on your mood patterns and journal content
- Reflection prompts for deeper introspection

### Analytics & Insights

- Mood distribution charts
- Sentiment trend analysis
- Theme detection and frequency analysis
- Comprehensive insights reports with:
  - Overall mood patterns
  - Sentiment trends
  - Common themes
  - Journaling habits
  - Progress indicators

### Theme Detection

The app automatically identifies common themes in your entries, including:

- Relationships
- Work
- Health
- Personal Growth
- Emotions

## Data Storage

All journal entries are stored locally in CSV format, ensuring your privacy and data ownership.

## Tech Stack

- **Frontend**: Streamlit
- **NLP**: TextBlob for sentiment analysis and theme detection
- **Data Analysis**: Pandas
- **Visualization**: Streamlit Charts

## License

This project is licensed under the MIT License. See the LICENSE file for details.
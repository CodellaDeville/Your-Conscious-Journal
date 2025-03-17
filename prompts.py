import random
from datetime import datetime
from textblob import TextBlob
import pandas as pd

class PromptGenerator:
    def __init__(self, entries=None):
        """Initialize the PromptGenerator with optional entries"""
        self.entries = entries if entries is not None else pd.DataFrame()

    MORNING_PROMPTS = [
        "What are your intentions for today?",
        "What would make today great?",
        "What are you looking forward to?",
        "How did you sleep? How are you feeling?",
        "What's one small thing you can do today to move closer to your goals?"
    ]
    
    AFTERNOON_PROMPTS = [
        "How is your energy level right now?",
        "What's been the highlight of your day so far?",
        "What challenges have you faced today?",
        "What are you grateful for in this moment?",
        "How are you progressing on your daily goals?"
    ]
    
    EVENING_PROMPTS = [
        "What made you smile today?",
        "What did you learn today?",
        "How did you take care of yourself today?",
        "What could you have done differently?",
        "What are you looking forward to tomorrow?"
    ]
    
    REFLECTION_PROMPTS = [
        "How have your emotions evolved throughout the day?",
        "What patterns do you notice in your thoughts?",
        "What support do you need right now?",
        "What's one thing you're proud of?",
        "What would your future self want you to know?"
    ]
    
    def get_time_based_prompts(self):
        """Get prompts based on the time of day"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:  # Morning
            return self.MORNING_PROMPTS
        elif 12 <= hour < 17:  # Afternoon
            return self.AFTERNOON_PROMPTS
        else:  # Evening
            return self.EVENING_PROMPTS
    
    def get_personalized_prompts(self, recent_entries=None):
        """Generate personalized prompts based on recent entries and mood patterns"""
        prompts = []
        
        entries_to_analyze = recent_entries if recent_entries is not None else self.entries
        
        if isinstance(entries_to_analyze, pd.DataFrame) and not entries_to_analyze.empty:
            try:
                # Analyze recent moods
                if 'mood' in entries_to_analyze.columns:
                    recent_moods = entries_to_analyze['mood'].tolist()
                    if recent_moods and recent_moods.count("😔 Sad") > len(recent_moods) * 0.5:  # More than 50% sad
                        prompts.extend([
                            "What small things bring you joy?",
                            "Who could you reach out to for support?",
                            "What activities help lift your mood?"
                        ])
                
                # Analyze themes
                if 'themes' in entries_to_analyze.columns:
                    all_themes = [theme.strip() for themes in entries_to_analyze['themes'].dropna() for theme in themes.split(',')]
                    if all_themes:
                        most_common = max(set(all_themes), key=all_themes.count)
                        theme_prompts = {
                            'relationships': ["How have your relationships evolved?", "What qualities do you value in others?"],
                            'work': ["What career goals excite you?", "How do you define success?"],
                            'health': ["What self-care practices serve you best?", "How can you prioritize your wellbeing?"],
                            'personal_growth': ["What new skills would you like to develop?", "What challenges help you grow?"],
                            'emotions': ["How do you process difficult emotions?", "What brings you peace?"],
                            'gratitude': ["What unexpected blessings have you noticed?", "Who are you grateful for?"],
                            'creativity': ["How do you express yourself creatively?", "What inspires you?"]
                        }
                        if most_common in theme_prompts:
                            prompts.extend(theme_prompts[most_common])
            except Exception as e:
                print(f"Error analyzing entries: {e}")  # Log error but continue gracefully
        
        # Add some reflection prompts if we don't have enough personalized ones
        if len(prompts) < 2:
            prompts.extend(random.sample(self.REFLECTION_PROMPTS, 2))
        
        return prompts

    def analyze_entry_themes(self, entry_text):
        """Analyze the main themes in an entry using simple keyword matching"""
        themes = {
            'relationships': ['family', 'friend', 'partner', 'relationship', 'people', 'together', 'connection'],
            'work': ['work', 'job', 'career', 'project', 'meeting', 'task', 'deadline'],
            'health': ['health', 'exercise', 'sleep', 'food', 'energy', 'rest', 'wellness'],
            'personal_growth': ['goal', 'learn', 'growth', 'progress', 'development', 'improve', 'achieve'],
            'emotions': ['feel', 'feeling', 'emotion', 'mood', 'stress', 'happy', 'sad', 'anxious', 'excited'],
            'gratitude': ['grateful', 'thankful', 'appreciate', 'blessed', 'fortune', 'gift'],
            'creativity': ['create', 'write', 'art', 'music', 'design', 'imagine', 'inspire']
        }
        
        entry_themes = []
        entry_lower = entry_text.lower()
        for theme, keywords in themes.items():
            if any(keyword in entry_lower for keyword in keywords):
                entry_themes.append(theme)
        
        return entry_themes or ['general']  # Return 'general' if no specific themes found

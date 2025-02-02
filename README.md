# Harry Potter English Learning Tool

This program provides an interactive learning platform that helps users improve their English vocabulary and reading skills using excerpts from the original *Harry Potter* books. The application is hosted on [Streamlit Cloud](https://learn-harry-potter-words.streamlit.app/), allowing users to access it directly without installation.

## Features

The application offers two main learning modes:

1. **Vocabulary Learning Mode**
   - Randomly selects 10 words from the *Harry Potter* books
   - Provides sentences from the original text containing the selected words
   - Option to display Chinese translations

2. **Sentence Completion Quiz**
   - Randomly selects 5 sentences from the original text with a missing word
   - Multiple-choice format (4 options per question) to reinforce vocabulary retention
   - Supports selection of book ranges (specific *Harry Potter* volumes)

## File Descriptions

- `app.py` - Main program, responsible for running the application
- `home.py` - Home page interface
- `quiz.py` - Sentence completion quiz functionality
- `random_sentence.py` - Vocabulary learning mode, selecting words and sentences randomly
- `read_csv.py` - Reads and processes data
- `result.csv` - Stores learning data

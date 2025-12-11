# Team Quiz Platform

A simple web-based quiz platform for teams.

## Deploy to Render

1. Push this code to your GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment: Python 3

## Customize Quiz

Edit `quiz.json` to add your own questions:
- `question`: The question text
- `options`: Array of answer choices
- `correct`: Index of correct answer (0-based)

## Usage

Once deployed, share the Render URL with your team to take the quiz.

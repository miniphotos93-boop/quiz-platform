from flask import Flask, render_template, request, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'quiz-secret-key'

# Load quiz data
def load_quiz():
    if os.path.exists('quiz.json'):
        with open('quiz.json', 'r') as f:
            return json.load(f)
    return {"questions": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    quiz_data = load_quiz()
    session['score'] = 0
    session['current_question'] = 0
    return render_template('quiz.html', questions=quiz_data['questions'])

@app.route('/submit', methods=['POST'])
def submit_answer():
    quiz_data = load_quiz()
    question_idx = int(request.json['question_idx'])
    answer = request.json['answer']
    
    correct_answer = quiz_data['questions'][question_idx]['correct']
    is_correct = answer == correct_answer
    
    if 'score' not in session:
        session['score'] = 0
    
    if is_correct:
        session['score'] += 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer
    })

@app.route('/results')
def results():
    score = session.get('score', 0)
    quiz_data = load_quiz()
    total = len(quiz_data['questions'])
    return render_template('results.html', score=score, total=total)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

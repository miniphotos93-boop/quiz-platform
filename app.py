from flask import Flask, render_template, request, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'quiz-secret-key'

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
    session['total_questions'] = len(quiz_data['questions'])
    return render_template('quiz.html', 
                         question=quiz_data['questions'][0], 
                         question_num=1, 
                         total=len(quiz_data['questions']))

@app.route('/next_question')
def next_question():
    quiz_data = load_quiz()
    current = session.get('current_question', 0)
    
    if current >= len(quiz_data['questions']) - 1:
        return jsonify({'finished': True})
    
    session['current_question'] = current + 1
    next_q = quiz_data['questions'][current + 1]
    
    return jsonify({
        'question': next_q['question'],
        'options': next_q['options'],
        'question_num': current + 2,
        'total': len(quiz_data['questions'])
    })

@app.route('/submit', methods=['POST'])
def submit_answer():
    quiz_data = load_quiz()
    current = session.get('current_question', 0)
    answer = request.json['answer']
    
    correct_answer = quiz_data['questions'][current]['correct']
    is_correct = answer == correct_answer
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer
    })

@app.route('/results')
def results():
    score = session.get('score', 0)
    total = session.get('total_questions', 0)
    return render_template('results.html', score=score, total=total)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hamutzi'
socketio = SocketIO(app)

# List of names to track
all_names = [
    "אור אספרנסה", "עמית אביב", "אוהד אוחנה", "הראל כהן", "הילה חמוי", "אופק אביסרור", "אגם רחמים",
    "אדם שפירא", "אוריאל טייאר", "אוריה כהן", "אלי רזומובסקי", "אסף דמתי", "ויויאן יבגנייב", "אופק ונטורה",
    "אילה שירה טוחולוב מחלב", "תומר אלמליח", "שני ריפס", "שחר נחום", "שון איציקובסקי", "רתם אשל",
    "רועי בלום", "רואי גולדמן", "פלג יוסיפון", "פיודור ששקוב", "עידן מרסיאנו", "עידן גלר",
    "עידו וינץ יחזקאל", "עומרי בינימיני", "עומר כסלו", "סהר צמח", "נתנאל עיליי שם טוב", "ניק קריימרמן",
    "לירון לוי", "ליהיא מלול", "יעל דינר", "יונתן דגן", "זואי פרידמן", "זהר שפר", "הראל לוי",
    "דניאל ליוש", "דביר עזר", "גל גרייצר", "גיא גרזון", "גיא אלבז", "אלמוג גרנות", "אליה אוסדון",
    "איתן צ'רטוף", "הוד ניסן", "תומר חאיק"
]

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {name: 'בהפסקה' for name in all_names}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load initial data
inputted_names = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matzal')




@app.route('/reset', methods=['POST'])
def reset():
    password = request.form.get('password')
    if password == 'your_secret_key_here':
        handle_reset_names()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@socketio.on('reset_names')
def handle_reset_names():
    global inputted_names
    inputted_names = {name: 'בהפסקה' for name in all_names}
    save_data(inputted_names)
    emit_update_data()

@socketio.on('add_name')
def handle_add_name(data):
    name = data['name']
    status = data.get('status', 'נוכח')
    if name in all_names:
        inputted_names[name] = status
        save_data(inputted_names)
        emit_update_data()
    else:
        emit('name_not_found')

@socketio.on('connect')
def handle_connect():
    emit_update_data()

def emit_update_data():
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    emit('update_data', {'names': inputted_names, 'present_count': present_count, 'removed_count': len(inputted_names) - present_count}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

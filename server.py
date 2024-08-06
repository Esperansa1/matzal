from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# List of names to track
all_names = {
    "אור אספרנסה", "עמית אביב", "אוהד אוחנה", "הראל כהן", "הילה חמוי", "אופק אביסרור", "אגם רחמים",
    "אדם שפירא", "אוריאל טייאר", "אוריה כהן", "אלי רזומובסקי", "אסף דמתי", "ויויאן יבגנייב", "אופק ונטורה",
    "אילה שירה טוחולוב מחלב", "תומר אלמליח", "שני ריפס", "שחר נחום", "שון איציקובסקי", "רתם אשל",
    "רועי בלום", "רואי גולדמן", "פלג יוסיפון", "פיודור ששקוב", "עידן מרסיאנו", "עידן גלר",
    "עידו וינץ יחזקאל", "עומרי בינימיני", "עומר כסלו", "סהר צמח", "נתנאל עיליי שם טוב", "ניק קריימרמן",
    "לירון לוי", "ליהיא מלול", "יעל דינר", "יונתן דגן", "זואי פרידמן", "זהר שפר", "הראל לוי",
    "דניאל ליוש", "דביר עזר", "גל גרייצר", "גיא גרזון", "גיא אלבז", "אלמוג גרנות", "אליה אוסדון",
    "איתן צ'רטוף", "הוד ניסן", "תומר חאיק"
}

# Dictionary to store the status of each name
inputted_names = {name: 'בהפסקה' for name in all_names}

@app.route('/')
def index():
    return render_template('index.html')

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
    emit('update_data', {'names': inputted_names, 'removed_names': 0}, broadcast=True)

@socketio.on('add_name')
def handle_add_name(data):
    name = data['name']
    status = data.get('status', 'נוכח')
    if name in all_names:
        inputted_names[name] = status
        emit('update_data', {'names': inputted_names, 'removed_names': len([n for n, s in inputted_names.items() if s != 'נוכח'])}, broadcast=True)
    else:
        emit('name_not_found')

if __name__ == '__main__':
    socketio.run(app, debug=True)

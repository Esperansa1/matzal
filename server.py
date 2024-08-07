import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pyperclip

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hantar'
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


data = {
    "אור אספרנסה": "בהפסקה",
    "עמית אביב": "בהפסקה",
    "אוהד אוחנה": "בהפסקה",
    "הראל כהן": "בהפסקה",
    "הילה חמוי": "בהפסקה",
    "אופק אביסרור": "בהפסקה",
    "אגם רחמים": "בהפסקה",
    "אדם שפירא": "בהפסקה",
    "אוריאל טייאר": "בהפסקה",
    "אוריה כהן": "בהפסקה",
    "אלי רזומובסקי": "בהפסקה",
    "אסף דמתי": "בהפסקה",
    "ויויאן יבגנייב": "בהפסקה",
    "אופק ונטורה": "בהפסקה",
    "אילה שירה טוחולוב מחלב": "בהפסקה",
    "תומר אלמליח": "בהפסקה",
    "שני ריפס": "בהפסקה",
    "שחר נחום": "בהפסקה",
    "שון איציקובסקי": "בהפסקה",
    "רתם אשל": "בהפסקה",
    "רועי בלום": "בהפסקה",
    "רואי גולדמן": "בהפסקה",
    "פלג יוסיפון": "בהפסקה",
    "פיודור ששקוב": "בהפסקה",
    "עידן מרסיאנו": "בהפסקה",
    "עידן גלר": "בהפסקה",
    "עידו וינץ יחזקאל": "בהפסקה",
    "עומרי בינימיני": "בהפסקה",
    "עומר כסלו": "בהפסקה",
    "סהר צמח": "בהפסקה",
    "נתנאל עיליי שם טוב": "בהפסקה",
    "ניק קריימרמן": "בהפסקה",
    "לירון לוי": "בהפסקה",
    "ליהיא מלול": "בהפסקה",
    "יעל דינר": "בהפסקה",
    "יונתן דגן": "בהפסקה",
    "זואי פרידמן": "בהפסקה",
    "זהר שפר": "בהפסקה",
    "הראל לוי": "בהפסקה",
    "דניאל ליוש": "בהפסקה",
    "דביר עזר": "בהפסקה",
    "גל גרייצר": "בהפסקה",
    "גיא גרזון": "בהפסקה",
    "גיא אלבז": "בהפסקה",
    "אלמוג גרנות": "בהפסקה",
    "אליה אוסדון": "בהפסקה",
    "איתן צ'רטוף": "בהפסקה",
    "הוד ניסן": "בהפסקה",
    "תומר חאיק": "בהפסקה"
}

def load_data():
    return data

# Load initial data
inputted_names = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matzal')
def matzal():
    status_card = get_status_card()
    pyperclip.copy(convert_status_card_to_string(status_card))
    return render_template('matzal.html', status_card=status_card)

@app.route('/reset', methods=['POST'])
def reset():
    password = request.form.get('password')
    if password == 'hantar':
        handle_reset_names()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@socketio.on('reset_names')
def handle_reset_names():
    global inputted_names
    inputted_names = {name: 'בהפסקה' for name in all_names}
    emit_update_data()

@socketio.on('add_name')
def handle_add_name(data):
    name = data['name']
    status = data.get('status', 'נוכח')
    if name in all_names:
        inputted_names[name] = status
        emit_update_data()
    else:
        emit('name_not_found')

@socketio.on('request_initial_data')
def handle_request_initial_data():
    emit_update_data()

@socketio.on('request_status_card')
def handle_request_status_card():
    status_card = get_status_card()
    emit('status_card', status_card)
    pyperclip.copy(convert_status_card_to_string(status_card))

def emit_update_data():
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    socketio.emit('update_data', {'names': inputted_names, 'present_count': present_count, 'removed_count': len(inputted_names) - present_count})

def get_status_card():
    date_today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    bathroom = [name for name, status in inputted_names.items() if status == 'שירותים']
    break_time = [name for name, status in inputted_names.items() if status == 'בהפסקה']
    other = [f"{name} - {' '.join(status.split(' - ')[1:])}" for name, status in inputted_names.items() if status.startswith('אחר')]
    
    status_card = {
        'date_today': date_today,
        'current_time': current_time,
        'course_status': {
            'total_count': len(inputted_names),
            'present_count': present_count,
            'missing_count': len(inputted_names) - present_count,
            'bathroom': bathroom,
            'break_time': break_time,
            'other': other,
        }
    }
    return status_card

def convert_status_card_to_string(status_card):
    date_today = status_card['date_today']
    current_time = status_card['current_time']
    course_status = status_card['course_status']
    present_count = course_status['present_count']
    bathroom = f"שירותים: {', '.join(course_status['bathroom'])}" if course_status['bathroom'] else ''
    break_time = f"בהפסקה: {', '.join(course_status['break_time'])}" if course_status['break_time'] else ''
    other = f"אחר: {', '.join(course_status['other'])}" if course_status['other'] else ''

    status_string = (
        f"תאריך של היום: {date_today}\n"
        f"שעה נוכחית: {current_time}\n"
        f"מצבה קורס סיגיט\n"
        f"מצן: {course_status['total_count']}\n"
        f"נוכחים: {present_count}\n"
        f"חסרים: {course_status['missing_count']}\n"
        f"{bathroom}\n"
        f"{break_time}\n"
        f"{other}"
    )

    return status_string

if __name__ == '__main__':
    socketio.run(app, debug=True)

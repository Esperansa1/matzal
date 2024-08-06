# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# List of names to track
all_names = {"אור אספרנסה", "עמית אביב", "אוהד אוחנה", "הראל כהן", "הילה חמוי", "אופק אביסרור", "אגם רחמים", "אדם שפירא", "אוריאל טייאר", "אוריה כהן", "אלי רזומובסקי", "אסף דמתי", "ויויאן יבגנייב", "אופק ונטורה", "אילה שירה טוחולוב מחלב", "תומר אלמליח", "שני ריפס", "שחר נחום", "שון איציקובסקי", "רתם אשל", "רועי בלום", "רואי גולדמן", "שחר נחום", "רועי בלום", "פלג יוסיפון", "פיודור ששקוב", "עידן מרסיאנו", "עידן גלר", "עידו וינץ יחזקאל", "עומרי בינימיני", "עומר כסלו", "סהר צמח", "נתנאל עיליי שם טוב", "ניק קריימרמן", "לירון לוי", "ליהיא מלול", "יעל דינר", "יונתן דגן", "זואי פרידמן", "זהר שפר", "הראל לוי", "דניאל ליוש", "דביר עזר", "גל גרייצר", "גיא גרזון", "גיא אלבז", "אלמוג גרנות", "אליה אוסדון", "איתן צ'רטוף", "הוד ניסן", "תומר חאיק"}

# Dictionary to store the status of each name
inputted_names = {name: 'In Class' for name in all_names}

@app.route('/')
def index():
    remaining_names = {name: status for name, status in inputted_names.items() if name in all_names}
    remaining_count = len(remaining_names)
    return render_template('index.html', remaining_names=remaining_names, remaining_count=remaining_count)

@socketio.on('add_name')
def handle_add_name(data):
    name = data['name']
    status = data.get('status', 'In Class')
    if name in all_names:
        inputted_names[name] = status
        remaining_names = {name: status for name, status in inputted_names.items() if name in all_names}
        emit('update_data', {'names': remaining_names, 'removed_names': len([name for name, status in inputted_names.items() if status != 'In Class'])}, broadcast=True)
    else:
        emit('name_not_found', broadcast=True)

@socketio.on('remove_name')
def handle_remove_name(data):
    name = data['name']
    if name in inputted_names:
        inputted_names[name] = 'In Class'
        remaining_names = {name: status for name, status in inputted_names.items() if name in all_names}
        emit('update_data', {'names': remaining_names, 'removed_names': len([name for name, status in inputted_names.items() if status != 'In Class'])}, broadcast=True)
    else:
        emit('name_not_found', broadcast=True)

@socketio.on('reset_names')
def handle_reset_names():
    for name in inputted_names:
        inputted_names[name] = 'In Class'
    remaining_names = {name: status for name, status in inputted_names.items() if name in all_names}
    emit('update_data', {'names': remaining_names, 'removed_names': 0}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

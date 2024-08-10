import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pyperclip

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hantar'

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

# Initialize with all students in "בהפסקה"
inputted_names = {name: 'בהפסקה' for name in all_names}


@app.route('/')
def index():
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    return render_template(
        'index.html',
        names=inputted_names,
        present_count=present_count,
        removed_count=len(inputted_names) - present_count,
        all_names=all_names  # Ensure all_names is passed to the template
    )


@app.route('/update', methods=['POST'])
def update_name():
    name = request.form.get('name')
    status = request.form.get('status')
    reason = request.form.get('reason', '')

    if name in all_names:
        if status == 'אחר' and reason:
            inputted_names[name] = f"{status} - {reason}"
        else:
            inputted_names[name] = status
        return redirect(url_for('index'))
    else:
        return jsonify({'error': 'Name not found in the list.'}), 404


@app.route('/reset', methods=['POST'])
def reset_names():
    password = request.form.get('password')
    if password == 'hantar':  # Ensure this is the correct password being checked
        global inputted_names
        inputted_names = {name: 'בהפסקה' for name in all_names}
        flash("The operation was completed successfully", 'success')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 403



@app.route('/matzal')
def matzal():
    status_card = get_status_card()
    pyperclip.copy(convert_status_card_to_string(status_card))
    return render_template('matzal.html', status_card=status_card)


def get_status_card():
    date_today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    bathroom = [name for name, status in inputted_names.items() if status == 'שירותים']
    break_time = [name for name, status in inputted_names.items() if status == 'בהפסקה']
    other = [f"{name} - {' '.join(status.split(' - ')[1:])}" for name, status in inputted_names.items() if
             status.startswith('אחר')]

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
    app.run(debug=True)

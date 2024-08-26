from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape
import json
import hashlib

app = Flask(__name__)

datafile = json.load(open('data.json', 'r', encoding='utf-8'))
all_names = datafile['names']
app.config['SECRET_KEY'] = datafile['password']

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["4900 per day", "2940 per hour", "49 per minute"],
    strategy='fixed-window'
)

inputted_names = {name: 'נוכח' for name in all_names}

correct_username = 'omega'
correct_password_hash = '70ccd9007338d6d81dd3b6271621b9cf9a97ea00'

def sha1(input_string):
    return hashlib.sha1(input_string.encode()).hexdigest()

@app.route('/')
@limiter.limit("49 per minute")
def login():
    if request.cookies.get('logged_in') == 'true':
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
@limiter.limit("49 per minute")
def login_action():
    username = request.form.get('username').lower()
    password = request.form.get('password')
    hashed_password = sha1(password)
    if username == correct_username and hashed_password == correct_password_hash:
        response = make_response(redirect(url_for('index')))
        response.set_cookie('logged_in', 'true', max_age=30*24*60*60, path='/')
        return response
    else:
        flash('Incorrect username or password!', 'danger')
        return redirect(url_for('login'))

@app.route('/index')
@limiter.limit("49 per minute")
def index():
    cookie_value = request.cookies.get('logged_in')

    if cookie_value != 'true':
        return redirect(url_for('login'))
    
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    return render_template(
        'index.html',
        names=inputted_names,
        present_count=present_count,
        removed_count=len(inputted_names) - present_count,
        all_names=all_names
    )

@app.route('/update', methods=['POST'])
@limiter.limit("49 per minute")
def update_name():
    return update_name_status(request.form.get('name'), request.form.get('status'), request.form.get('reason', ''))

def update_name_status(name, status, reason=''):
    name = escape(name)
    status = escape(status)
    reason = escape(reason)

    if name in all_names:
        if status == 'אחר' and reason:
            inputted_names[name] = f"{status} - {reason}"
        else:
            inputted_names[name] = status
        return redirect(url_for('index'))
    else:
        return jsonify({'error': 'Name not found in the list.'}), 404

@app.route('/reset', methods=['POST'])
@limiter.limit("49 per minute")
def reset_names():
    password = request.form.get('password')
    if password == 'hantar':
        global inputted_names
        inputted_names = {
            name: 'בהפסקה' if not status.startswith('אחר') else status
            for name, status in inputted_names.items()
        }
        flash("The operation was completed successfully", 'success')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 403

@app.route('/set_all_attending', methods=['POST'])
@limiter.limit("49 per minute")
def set_all_attending():
    password = request.form.get('password')
    if password == 'hantar': 
        global inputted_names
        inputted_names = {
            name: 'נוכח' if not status.startswith('אחר') else status
            for name, status in inputted_names.items()
        }
        flash("The operation was completed successfully", 'success')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 403

@app.route('/api/updates')
@limiter.limit("49 per minute")
def get_updates():
    return jsonify(inputted_names)

@app.route('/api/matzal')
@limiter.limit("49 per minute")
def get_matzal_updates():
    return jsonify(get_status_card())

@app.route('/matzal')
@limiter.limit("49 per minute")
def matzal():
    status_card = get_status_card()
    return render_template('matzal.html', status_card=status_card)

def get_status_card():
    date_today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    present_count = sum(1 for status in inputted_names.values() if status == 'נוכח')
    bathroom = [name for name, status in inputted_names.items() if status == 'שירותים']
    break_time = [name for name, status in inputted_names.items() if status == 'בהפסקה']
    technical_issue = [name for name, status in inputted_names.items() if status == 'תקלה טכנית']
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
            'technical_issue': technical_issue,
            'other': other,
        }
    }
    return status_card

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('logged_in', '', expires=0)
    flash('You have been logged out.', 'success')
    return response

if __name__ == '__main__':
    app.run()

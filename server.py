from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# List of names to track
all_names = {"אור אספרנסה", "עמית אביב", "אוהד אוחנה", "הראל כהן", "הילה חמוי", "אופק אביסרור", "אגם רחמים", "אדם שפירא", "אוריאל טייאר", "אוריה כהן", "אלי רזומובסקי", "אסף דמתי", "ויויאן יבגנייב", "אופק ונטורה", "אילה שירה טוחולוב מחלב", "תומר אלמליח", "שני ריפס", "שחר נחום", "שון איציקובסקי", "רתם אשל", "רועי בלום", "רואי גולדמן", "שחר נחום", "רועי בלום", "פלג יוסיפון", "פיודור ששקוב", "עידן מרסיאנו", "עידן גלר", "עידו וינץ יחזקאל", "עומרי בינימיני", "עומר כסלו", "סהר צמח", "נתנאל עיליי שם טוב", "ניק קריימרמן", "לירון לוי", "ליהיא מלול", "יעל דינר", "יונתן דגן", "זואי פרידמן", "זהר שפר", "הראל לוי", "דניאל ליוש", "דביר עזר", "גל גרייצר", "גיא גרזון", "גיא אלבז", "אלמוג גרנות", "אליה אוסדון", "איתן צ'רטוף", "הוד ניסן", "תומר חאיק"}

# Set to store inputted names
inputted_names = set()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        missing = request.form.get('missing')

        if name and name in all_names:
            inputted_names.add(name)
        elif missing and missing in inputted_names:
            inputted_names.remove(missing)
        elif 'reset' in request.form:
            if request.form['password'] == 'hantar':
                inputted_names.clear()
                return redirect(url_for('index'))

    remaining_names = all_names - inputted_names
    remaining_count = len(remaining_names)

    return render_template('index.html', remaining_names=remaining_names, remaining_count=remaining_count)

if __name__ == '__main__':
    app.run(debug=True)
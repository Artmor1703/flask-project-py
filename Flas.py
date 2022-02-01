from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # descrip = db.Column(db.Text)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Test %r>' % self.id


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/publication')
def publication():
    public = Person.query.order_by(Person.date.desc()).all()
    return render_template('publication.html', public=public)


@app.route("/person/<int:id>")
def person(id):
    public = Person.query.get(id)
    return render_template('person.html', public=public)


@app.route("/person/<int:id>/del")
def person_del(id):
    public = Person.query.get_or_404(id)
    try:
        db.session.delete(public)
        db.session.commit()
        return redirect('/publication')
    except:
        return "error"


@app.route("/person/<int:id>/red", methods=['POST', 'GET'])
def person_red(id):
    public = Person.query.get(id)
    if request.method == "POST":
        public.name = request.form['name']
        public.interest = request.form['interest']
        try:
            db.session.commit()
            return redirect('/publication')
        except:
            return "error"
    else:
        return render_template('red.html',  public=public)


@app.route('/creation', methods=['POST', 'GET'])
def creation():
    if request.method == "POST":
        name = request.form['name'].strip()
        interest = request.form['interest'].strip()
        # descrip = request.form['descrip'].strip()
        pers = Person(name=name, interest=interest)
        try:
            db.session.add(pers)
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/creation')
    else:
        return render_template('creation.html')


if __name__ == "__main__":
    app.run(debug=True)
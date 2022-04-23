from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.db'
db = SQLAlchemy(app)

class Dogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    breed = db.Column(db.String(30), nullable=False)
    date_arrived = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/', methods=['GET'])
def home():
    title = "Home"
    return render_template("home.html", title=title)

@app.route('/dogs', methods=['POST', 'GET'])
def dogs():
    title = "Our dogs"
    if request.method == "POST":
        dogs_name = request.form['name']
        dogs_breed = request.form['breed']
        new_dog = Dogs(name=dogs_name, breed=dogs_breed)
        try:
            db.session.add(new_dog)
            db.session.commit()
            return render_template("dogs.html", title=title, dogs=dogs)
        except: 
            return "There was an error adding this dog..."
    else:
        dogs = Dogs.query.order_by(Dogs.date_arrived)
        return render_template("dogs.html", title=title, dogs=dogs)


@app.route('/dog/<int:id>', methods=['POST', 'GET', 'DELETE'])
def dog_viewer(id):
    dog_view = Dogs.query.get_or_404(id)
    if request.method == "POST":
        dog_view.name = request.form['name']
        dog_view.breed = request.form['breed']
        try:
            db.session.commit()
            return render_template("dogs.html", title=title)
        except:
            return "There was a problem updating this dog"
    elif request.method == "DELETE":
        title = "our dogs"
        try:
            db.session.delete(dog_view)
            db.session.commit()
            dogs = Dogs.query.order_by(Dogs.date_arrived)
            return render_template("dogs.html", title=title, dogs=dogs)
        except:
            return "There was a problem removing this dog"
    else:
        return render_template('dog.html', dog_view=dog_view)


@app.route('/delete/<int:id>', methods=['DELETE', 'GET'])
def delete(id):
    dog_found_home = Dogs.query.get_or_404(id)
    title = "Our dogs"
    try:
        db.session.delete(dog_found_home)
        db.session.commit()
        dogs = Dogs.query.order_by(Dogs.date_arrived)
        return render_template("dogs.html", title=title, dogs=dogs)
    except:
        return render_template("dogs.html", title=title, dogs=dogs)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    dog_to_update = Dogs.query.get_or_404(id)
    title = 'Our dogs'
    if request.method == "POST":
        dog_to_update.name = request.form['name']
        dog_to_update.breed = request.form['breed']
        try:
            db.session.commit()
            return render_template("/dogs.html", title=title)
        except:
            return "There was a problem updating this dog"
    else:
        return render_template('dogs.html', title=title)


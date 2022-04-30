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
    print('/home page')
    title = "Home"
    return render_template("home.html", title=title)

@app.route('/dogs', methods=['POST'])
def add_new_dogs():
    title = "Our dogs"
    if request.method == "POST":
        new_dog = get_form_data(request.form)    
        try:
            db.session.add(new_dog)
            db.session.commit()
            return render_template("dogs.html", title=title)
        except: 
            print('exception error on /dogs route')
            return "There was an error adding this new dog..."
    else:
        dogs = Dogs.query.order_by(Dogs.date_arrived)
        return render_template("dogs.html", title=title, dogs=dogs)

@app.route('/dogs', methods=['GET'])
def get_all_dogs(dog_id):
    dogs = Dogs.query.get_or_404(dog_id)
    title = "our dogs"
    print('single dog view page')    
    return render_template('dogs.html', title=title, dogs=dogs)



def get_form_data(form):

    dog_view_name = request.form.get('name', '') # what happens if this is more than 30 characters?
    dog_view_breed = request.form.get('breed', '')

    return Dogs(name=dog_view_name, breed=dog_view_breed)


@app.route('/dog/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    if request.method == "DELETE":
        try:
            db.session.delete()
            db.session.commit()
            return redirect('/dogs')
        except:
            print('Error deleting this dog')
            return redirect('/dogs')
    delete_response = "{'deleted': true}"
    return delete_response


@app.route('/dog/<int:dog_id>', methods=['GET'])
def get_dog(dog_id):
    dog_view = Dogs.query.get_or_404(dog_id)
    title = "our dogs"    
    return render_template('dog.html', title=title, dog_view=dog_view)


@app.route('/dog/<int:dog_id>', methods=['PUT'])
def update_dog(get_form_data):
    title = "our dogs"
    if request.method == "PUT":
        try:
            updated_dog = get_form_data(request.form)
            db.session.update(updated_dog)
            db.session.commit()
            return render_template("dogs.html", title=title)
        except:
            print('There was a problem updating this dog')
            return redirect('/dogs')

app.run()
"""Adopt application"""

from flask import Flask, render_template, redirect
from models import db, connect_db, Pet
from forms import PetForm
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/adopt"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "adop"

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """List all pets"""

    pets = Pet.query.all()

    return render_template("pets.html", pets=pets)


@app.route("/add")
def add_pet_form():
    """Display form for adding pet"""

    form = PetForm()

    return render_template("add_pet_form.html", form=form)


@app.route("/add", methods=["POST"])
def create_pet():
    """Handler for add pet form"""

    form = PetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("add_pet_form.html", form=form)


@app.route("/<int:pet_id>")
def display_edit_form(pet_id):
    """Display edit form"""

    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)

    return render_template("pet_details.html", form=form, pet_id=pet.id)

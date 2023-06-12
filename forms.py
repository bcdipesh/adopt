from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional, AnyOf, NumberRange, URL


class PetForm(FlaskForm):
    """From for adding and updating a pet."""

    name = StringField("Pet name", validators=[InputRequired()])
    species = StringField(
        "Species",
        validators=[
            AnyOf(
                ["cat", "Cat", "dog", "Dog", "porcupine", "Porcupine"],
                message="The species should be either 'cat', 'dog', or 'porcupine'",
            )
        ],
    )
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField(
        "Age",
        validators=[
            Optional(),
            NumberRange(min=0, max=30, message="Age must be between 0 and 30."),
        ],
    )
    notes = StringField("Notes", validators=[Optional()])

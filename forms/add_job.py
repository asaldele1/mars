from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.validators import DataRequired, Length


class AddJobForm(FlaskForm):
    job = StringField(
        'Job Title',
        validators=[DataRequired(), Length(max=200)]
    )
    team_leader = IntegerField(
        'Team Leader id',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    work_size = IntegerField(
        'Work Size',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    collaborators = StringField(
        'Collaborators',
        validators=[DataRequired(), Length(max=200)]
    )
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')

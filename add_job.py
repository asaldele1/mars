from flask import Blueprint, redirect, render_template
from flask_login import login_required

from forms.add_job import AddJobForm
from data import db_session
from data.jobs import Jobs
from data.users import User


bp = Blueprint('addjob', __name__)


@bp.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        leader = session.query(User).filter(
            User.id == form.team_leader.data).first()
        if not leader:
            form.team_leader.errors.append('User with this ID not found')
        else:
            new_job = Jobs(
                team_leader=leader.id,
                job=form.job.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                is_finished=form.is_finished.data
            )
            session.add(new_job)
            session.commit()
            return redirect("/")
    return render_template('add_job.html', form=form, title="Adding a Job")

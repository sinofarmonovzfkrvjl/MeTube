from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from forms import LoginForm, VideoUploadForm
from models import db, PostVideo
from werkzeug.utils import secure_filename
import os

profile = Blueprint("Profile", __name__, url_prefix="/profile")

@profile.route("/", methods=["GET", "POST"])
@login_required
def profile_page():
    videos = PostVideo.query.all()
    return render_template("profile/profile.html", user=current_user, videos=videos)

@profile.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = VideoUploadForm()
    if form.validate_on_submit():
        video_file = form.video.data
        video_filename = secure_filename(video_file.filename)
        video_path = os.path.join("videos", video_filename)
        video_file.save(video_path)

        new_post = PostVideo(
            user=current_user,
            title=form.title.data,
            body=form.body.data,
            video=video_filename
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    flash("Video uploaded successfully!", "success")
    return render_template('profile/upload.html', user=current_user, form=form)

@profile.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = LoginForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = form.password.data
        db.session.commit()
        return redirect(url_for("Profile.profile_page"))
    return render_template("profile/edit.html", user=current_user, form=form)

@profile.route("/delete/<video_id>")
def delete_video(video_id):
    video = PostVideo.query.get_or_404(video_id)
    if video.user_id == current_user.id:
        os.remove(f"videos/{video.video}")
        db.session.delete(video)
        db.session.commit()
        return redirect(url_for("Profile.profile_page"))
    else:
        flash("You are not authorized to delete this video.", "danger")
        return redirect(url_for("Profile.profile_page"))

@profile.route("/edit/<video_id>", methods=["GET", "POST"])
def edit_video(video_id):
    video = PostVideo.query.filter_by(id=video_id).first_or_404()
    if video.user_id == current_user.id:
        form = VideoUploadForm()
        if form.validate_on_submit():
            PostVideo.query.filter_by(id=video_id).update({PostVideo.title: form.title.data, PostVideo.body: form.body.data})
            db.session.commit()
            return redirect(url_for("Profile.profile_page"))
        form.title.data = video.title
        form.body.data = video.body
        return render_template("profile/edit_video.html", user=current_user, form=form, video=video)
    else:
        flash("You are not authorized to edit this video.", "danger")
        return redirect(url_for("Profile.profile_page"))

from flask import Flask, render_template, redirect, send_from_directory, url_for
from forms import LoginForm, VideoUploadForm
from models import User, db, PostVideo
from admin import admin
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from blueprints import profile

app = Flask(__name__)

app.register_blueprint(profile)

app.secret_key = "1234567890987654321"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)
admin.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html', user=current_user, videos=PostVideo.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route("/watch/<post_id>")
def get_post(post_id):
    video_post = PostVideo.query.get(post_id)
    return render_template("watch.html", post=video_post)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/videos/<videoname>")
def send_video(videoname):
    return send_from_directory("videos", videoname)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
from routes.login import login_bp
from routes.signup import signup_bp
from routes.home import home_bp
from routes.events_list import events_list_bp
from routes.profile import profile_bp
from routes.forum import forum_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(home_bp)
app.register_blueprint(events_list_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(forum_bp)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
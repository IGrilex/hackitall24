from flask import Flask
from routes.login import login_bp
from routes.signup import signup_bp
from routes.home import home_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(home_bp)

@app.route('/')
def index():
    return '''
        <h1>Welcome to HackItAll</h1>
        <a href="/login/">Log In</a> | <a href="/signup/">Sign Up</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

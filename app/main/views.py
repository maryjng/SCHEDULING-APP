
from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__, url_prefix='/main', template_folder='templates/main')

@main.route('/')
@main.route('/index')
def index():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run()

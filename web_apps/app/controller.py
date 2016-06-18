from flask import Blueprint, render_template
mod = Blueprint('app', __name__, url_prefix='', template_folder="templates", static_folder="static")

@mod.route('/')
def index():
    return render_template("app.index.html")
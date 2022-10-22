from flask import Blueprint, render_template
import helper_functions

blueprint = Blueprint("index",__name__,template_folder="templates")

@blueprint.route('/')
def index():
    return helper_functions.helper_render("index.html")

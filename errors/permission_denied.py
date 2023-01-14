# Darwin's Stuff
from flask import render_template, Blueprint
import helper_functions

blueprint = Blueprint("permission_denied",__name__,template_folder="templates")

@blueprint.errorhandler(403)
def permission_denied(e):
    return helper_functions.helper_render("errors/403.html"), 403

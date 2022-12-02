from flask import render_template, Blueprint
import helper_functions

blueprint = Blueprint("page_not_found",__name__,template_folder="templates")

@blueprint.errorhandler(404)
def page_not_found(e):
    return helper_functions.helper_render("errors/404.html"), 404

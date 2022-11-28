from flask import Blueprint, session
from database_models.UserDBModel import *
from database_models.CartDBModel import *

blueprint = Blueprint("InventoryManagement", __name__, template_folder="templates")

@blueprint.route("/ManageInventory")
def ManageInventory():
    pass

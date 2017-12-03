from flask import Blueprint, render_template, request

from gat.dao import dao

cases_blueprint = Blueprint('cases_blueprint', __name__)

@cases_blueprint.route('/cases', methods=['GET', 'POST'])
def get_cases():
    #do what you need to do here

    return render_template("cases.html")

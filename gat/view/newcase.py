from flask import Blueprint, render_template, request, redirect, url_for, make_response
import os
from gat.dao import dao
from gat.service import io_service, security_service

newcase_blueprint = Blueprint('newcase_blueprint', __name__)

@newcase_blueprint.route('/newcase', methods = ['GET'])
def landing_page():
    return render_template("newcase.html")
@newcase_blueprint.route('/newcase', methods = ['POST'])
def post_newcase():

    response = make_response(redirect(url_for('visualize_blueprint.visualize', new_case = True)))
    case_num = request.cookies.get("case_num")
    case_name = request.form.get("case_name")
    email = security_service.getEmail(case_num)
    uidpk = security_service.getData(email)[0][0]
    dao.updateFileDict(case_num, "case_name", case_name)
    security_service.addCaseFolder(case_name, uidpk)
    return response




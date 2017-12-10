from flask import Blueprint, render_template, request, redirect, url_for, make_response
import os
from gat.dao import dao
from gat.service import io_service, security_service

cases_blueprint = Blueprint('cases_blueprint', __name__)

@cases_blueprint.route('/cases', methods=['GET'])
def get_cases():
    options = ["New Case"]
    case_num = request.cookies.get('case_num')
    email =  security_service.getEmail(case_num)
    for filename in os.listdir("data/" + str(security_service.getData(email)[0][0])):
        options.append(filename)


    #do what you need to do here
    return render_template("cases.html", case_options = options)

@cases_blueprint.route('/cases', methods=['POST'])
def post_cases():
    #gets called when form gets submitted
    response = make_response(redirect(url_for('visualize_blueprint.visualize')))
    case_num = request.cookies.get("case_num")
    case_name = request.form.get("cases")
    fileDict = dao.getFileDict(case_num)
    if case_name == "New Case":
        if fileDict is not None:
            dao.setFileDict({}, case_num)
        dao.createFileDict(case_num)
        return make_response(redirect(url_for('newcase_blueprint.post_newcase')))

    email = security_service.getEmail(case_num)
    io_service.loadDict(email, case_num, case_name)
    return response
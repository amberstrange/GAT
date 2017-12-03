import random
from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, url_for
from flask import make_response

from gat.dao import dao
from gat.service import io_service
from gat.service import security_service
upload_blueprint = Blueprint('upload_blueprint', __name__)

#TODO
@upload_blueprint.route('/', methods=['POST'])
def upload():
    case_num = request.cookies.get('case_num', None)
    print("CASENUM", case_num)
    fileDict = dao.getFileDict(case_num)

    fileDict['research_question'] = request.form.get('smartsearch')
    if fileDict['research_question'] is not None and fileDict['research_question'].strip() != '':
        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

    email = security_service.getEmail(case_num)
    io_service.storeFiles(case_num, email, request.files)
    fileDict['GSA_file_list'] = request.files.getlist('GSA_Input_map')
    fileDict["NLP_INPUT_NER"] = request.form.get("NLP_INPUT_NER")
    fileDict["NLP_INPUT_IOB"] = request.form.get("NLP_INPUT_IOB")
    '''
    fileDict['GSA_Input_CSV'] = io_service.storefile(request.files.get('GSA_Input_CSV'), email)
    fileDict['GSA_Input_SHP'] = io_service.storeGSA(request.files.getlist('GSA_Input_map'), email)
    fileDict['GSA_file_list'] = request.files.getlist('GSA_Input_map')

    fileDict['NLP_Input_corpus'] = io_service.storeNLP(request.files.getlist('NLP_Input_corpus'), email)
    fileDict['NLP_Input_LDP'] = io_service.storefile(request.files.get('NLP_Input_LDP'), email)
    fileDict['NLP_Input_Sentiment'] = io_service.storefile(request.files.get('NLP_Input_Sentiment'), email)

    fileDict["NLP_INPUT_NER"] = request.form.get("NLP_INPUT_NER")
    fileDict["NLP_INPUT_IOB"] = request.form.get("NLP_INPUT_IOB")

    fileDict['SNA_Input'] = io_service.storefile(request.files.get('SNA_Input'), email)
    '''
    fileDict['research_question'] = request.form.get('research_question')

    errors = io_service.checkExtensions(case_num)  # helper method to make sure there are no input errors by the user
    # i.e. if there are errors, we can't proceed so we stay on the upload page
    if len(errors) > 0:
        return render_template('upload.html',
                               errors=errors, case_num=case_num)

    # there are intermediary steps for SNA and NLP analyses
    if fileDict['SNA_Input']:
        return redirect(url_for('sna_blueprint.sheetSelect', case_num=case_num))

    if fileDict['GSA_Input_CSV']:
        return redirect(url_for('gsa_blueprint.gsa_select', case_num=case_num))

    # if a user does both SNA and NLP, as it stands, the NLP intermediary data will never be gotten to. This is a problem.
    if fileDict['NLP_Input_corpus']:
        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

    # if NLP chosen, allow them to pick from the different tools available
    # do i redirect to another url to choose then save the results then redirect to visualize?
    # no, just add the radio buttons under the file upload before the hr (in the template)
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


@upload_blueprint.route('/', methods=['GET'])
def landing_page():
    response = make_response(render_template("upload.html"))
    case_num = request.cookies.get('case_num')
    if case_num == None:
        case_num = dao.makeCaseNum()
        response.set_cookie('case_num', str(case_num), max_age=timedelta(days=1))
    else:
        dao.createFileDict(case_num)
    return response

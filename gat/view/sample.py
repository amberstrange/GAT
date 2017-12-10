from flask import Blueprint, redirect, url_for, request

from gat.dao import dao

sample_blueprint = Blueprint('sample_blueprint', __name__)


@sample_blueprint.route('/gsa/<path:sample_path>')
def gsa_sample(sample_path):
    case_num = request.args.get('case_num', None)
    return redirect(url_for('gsa_blueprint.gsa_select', case_num=case_num))


@sample_blueprint.route('/nlp/<path:sample_path>')
def nlp_sample(sample_path):
    case_num = request.cookies.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    if sample_path == 'iran':
        fileDict['NLP_Input_Sentiment'] = 'static/sample/nlp/sample_sentiment.txt'
    elif sample_path == 'new_nlp_example':
        fileDict['NLP_New_Example'] = 'static/sample/nlp/nlp_new_example.txt'
    else:
        fileDict['NLP_Input_corpus'] = url_for('static', filename="sample/nlp/" + sample_path + '/')[1:]
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


@sample_blueprint.route('/sna/<path:sample_path>')
def sna_sample(sample_path):
    case_num = request.cookies.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    fileDict['SNA_Input'] = url_for('static', filename="sample/sna/" + sample_path)[1:]
    return redirect(url_for('sna_blueprint.sheetSelect', case_num=case_num))

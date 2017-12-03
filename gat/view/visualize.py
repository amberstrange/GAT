import copy

from flask import Blueprint, render_template, request

from gat.dao import dao
from gat.service import scraper_service, sna_service, gsa_service, nlp_service, security_service

visualize_blueprint = Blueprint('visualize_blueprint', __name__)


@visualize_blueprint.route('/visualize', methods=['GET', 'POST'])
def visualize():
    case_num = request.cookies.get('case_num', None)


    fileDict = dao.getFileDict(case_num)
    print(fileDict , "filedict loaded")

    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    GSA_file_SVG = fileDict.get('GSA_Input_SVG')
    NLP_dir = fileDict.get('NLP_Input_corpus')
    NLP_urls = fileDict.get('NLP_LDP_terms')
    NLP_file_sentiment = fileDict.get('NLP_Input_Sentiment')
    research_question = fileDict.get('research_question')
    tropes = fileDict.get('tropes')
    graph = fileDict.get('graph')
    GSA_sample = fileDict.get('GSA_data')
    error = False

    auto = None
    sp_dyn = None
    svgNaming = None
    if GSA_sample != None:
        svgNaming = GSA_sample[0]
        auto = GSA_sample[1:3]
        sp_dyn = [mat for mat in GSA_sample[3:]]

    gsaCSV = None
    mymap = None
    nameMapping = None


    if (GSA_file_CSV is not None and GSA_file_SHP is not None and fileDict.get('GSA_meta') is not None):
        gsaCSV, mymap, nameMapping = gsa_service.tempParseGSA(GSA_file_CSV, GSA_file_SHP, fileDict['GSA_meta'][0],
                                                              fileDict['GSA_meta'][1])
    if GSA_file_SVG != None:
        gsaCSV, mymap = gsa_service.parseGSA(GSA_file_CSV, GSA_file_SVG)

    if gsaCSV == None and mymap == True:
        error = True
        mymap = None

    sna_service.prep(graph)
    jgdata, SNAbpPlot, attr, systemMeasures = sna_service.SNA2Dand3D(graph, request, case_num, _2D=True)
    copy_of_graph = copy.deepcopy(graph)

    if NLP_dir:
        nlp_summary, nlp_entities, nlp_network, nlp_sources, nlp_tropes = nlp_service.nlp_dir(NLP_dir)
    else:
        nlp_summary, nlp_entities, nlp_network, nlp_sources, nlp_tropes = nlp_service.nlp_urls(NLP_urls)

    nlp_sentiment = nlp_service.sentiment(NLP_file_sentiment)
    research_question = scraper_service.scrape(research_question)


    if security_service.isLoggedIn(case_num):
            return render_template('visualizations.html',
                               research_question=research_question,
                               SNAbpPlot=SNAbpPlot,
                               graph=copy_of_graph,
                               attr=attr,
                               colors=sna_service.colors,
                               gsaCSV=gsaCSV,
                               mymap=mymap,
                               svgNaming=svgNaming,
                               nameMapping=nameMapping,
                               jgdata=jgdata,
                               tropes=tropes,
                               GSA_sample=GSA_sample,
                               auto=auto,
                               sp_dyn=sp_dyn,
                               error=error,
                               case_num=case_num,
                               nlp_sentiment=nlp_sentiment,
                               nlp_summary=nlp_summary,
                               nlp_entities=nlp_entities,
                               nlp_sources=nlp_sources,
                               nlp_tropes=nlp_tropes,
                               systemMeasures=systemMeasures
                               )





    fileDict['SNAbpPlot'] = '/' + SNAbpPlot if SNAbpPlot != None else None
    fileDict['copy_of_graph'] = copy_of_graph
    fileDict["research_question"] = research_question,
    fileDict["SNAbpPlot"] = SNAbpPlot,
    fileDict["graph"] = copy_of_graph,
    fileDict["attr"] = attr,
    fileDict["colors"] = sna_service.colors,
    fileDict["gsaCSV"] = gsaCSV,
    fileDict["mymap"] = mymap,
    fileDict["svgNaming"] = svgNaming,
    fileDict["nameMapping"] = nameMapping,
    fileDict["jgdata"] = jgdata,
    fileDict["tropes"] = tropes,
    fileDict["GSA_sample"] = GSA_sample,
    fileDict["auto"] = auto,
    fileDict["sp_dyn"] = sp_dyn,
    fileDict["error"] = error,
    fileDict["case_num"] = case_num,
    fileDict["nlp_sentiment"] = nlp_sentiment,
    fileDict["nlp_summary"] = nlp_summary,
    fileDict["nlp_entities"] = nlp_entities,
    fileDict["nlp_sources"] = nlp_sources,
    fileDict["nlp_tropes"] = nlp_tropes,
    fileDict["systemMeasures"] = systemMeasures

    #todo save filedict here

    return render_template('visualizations.html',
                           research_question=research_question,
                           SNAbpPlot=SNAbpPlot,
                           graph=copy_of_graph,
                           attr=attr,
                           colors=sna_service.colors,
                           gsaCSV=gsaCSV,
                           mymap=mymap,
                           svgNaming=svgNaming,
                           nameMapping=nameMapping,
                           jgdata=jgdata,
                           tropes=tropes,
                           GSA_sample=GSA_sample,
                           auto=auto,
                           sp_dyn=sp_dyn,
                           error=error,
                           case_num=case_num,
                           nlp_sentiment=nlp_sentiment,
                           nlp_summary=nlp_summary,
                           nlp_entities=nlp_entities,
                           nlp_sources=nlp_sources,
                           nlp_tropes=nlp_tropes,
                           systemMeasures=systemMeasures
                           )

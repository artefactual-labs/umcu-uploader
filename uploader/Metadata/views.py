# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, redirect
from json import dump, dumps
import requests
from os import getenv

api_token = getenv('API_TOKEN')
server_url = 'https://demo.dataverse.nl/'

metadata = Blueprint("metadata", __name__, template_folder="templates")


@metadata.route('/', methods=['GET', 'POST'], defaults={'req_path': ''})
def index(req_path):
    if request.method == 'POST':
        form_data = request.form
        # convert form data to dataverse json api format
        # https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json
        description_value = form_data['dsDescription']
        title_value = form_data['title']
        licence_value = form_data['licenceType']
        author_values_temp = [
            y for x, y in form_data.items() if x.startswith('author')]
        author_values = [{
            "authorName": {
                "typeName": "authorName",
                "multiple": 'false',
                "typeClass": "primitive",
                "value": x
            }} for x in author_values_temp]
        subject_value = 'Medicine, Health and Life Sciences'
        keyword_values_temp = [
            y for x, y in form_data.items() if x.startswith('keyword')]
        keyword_values = [{'keywordValue': {
            'typeName': 'keywordValue',
            'multiple': 'false',
            'typeClass': 'primitive',
            'value': x}} for x in keyword_values_temp]
        publication_values_temp = [
            y for x, y in form_data.items() if x.startswith('relatedPublication')]
        publication_values = [{'publicationCitation': {
            'typeName': 'publicationCitation', 'multiple': 'false', 'typeClass': 'primitive', 'value': x}} for x in publication_values_temp]
        contactName_values_temp = [
            y for x, y in form_data.items() if x.startswith('datasetContactName')]
        contactName_values = [{
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": 'false',
                "typeClass": "primitive",
                "value": x
            }} for x in contactName_values_temp]
        contactEmail_values_temp = [
            y for x, y in form_data.items() if x.startswith('datasetContactEmail')]
        contactEmail_values = [{"datasetContactEmail": {
            "typeName": "datasetContactEmail",
            "multiple": 'false',
            "typeClass": "primitive",
            "value": x
        }} for x in contactEmail_values_temp]
        contributor_values_temp = [
            y for x, y in form_data.items() if x.startswith('contributor')]
        contributor_values = [{
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": 'false',
                "typeClass": "primitive",
                "value": x
            }} for x in contributor_values_temp]
        language_values = [
            y for x, y in form_data.items() if x.startswith('language')]
        software_values_temp = [
            y for x, y in form_data.items() if x.startswith('software')]
        software_values = [{'softwareName': {
            'typeName': 'softwareName', 'multiple': 'false', 'typeClass': 'primitive', 'value': software}} for software in software_values_temp]
        date_of_deposit_value = form_data.get('depositDate')
        date_start_value = form_data.get('dateRangeStart')
        date_end_value = form_data.get('dateRangeEnd')
        data_type_values = [
            y for x, y in form_data.items() if x.startswith('dataType')]
        depositorName_value = 'test'
        licence_description_value = 'null'
        dv_metadata = {"datasetVersion": {"metadataBlocks": {"citation": {'displayName': "Citation Metadata",
                                                                          "fields": [{'typeName': 'publication', 'value': publication_values, 'multiple': 'true', 'typeClass': 'compound'},
                                                                                     {'typeName': 'author', 'typeClass': 'compound', 'value': author_values},
                                                                                     {'typeName': 'keyword', 'typeClass': 'conmpound', 'multiple': 'true', 'value':  keyword_values,
                                                                                      },
                                                                                     {'typeName': 'subject', 'typeClass': 'true', 'value':  {'subject': {
                                                                                         'typeName': 'subject', 'typeClass': 'primitive', 'value': subject_value}},
                                                                                      },
                                                                                     {'typeName': 'title', 'typeClass': 'primitive', 'value': title_value},
                                                                                     {'typeName': 'dsDescription', 'typeClass': 'compound', 'value':  {'dsDescriptionValue': {
                                                                                         'typeName': 'dsDescriptionValue', 'typeClass': 'primitive', 'value': description_value}}},
                                                                                     {'typeName': 'contributor', 'typeClass': 'compound', 'value':  contributor_values},
                                                                                     {'typeName': 'datasetContact', 'value': [
                                                                                         *contactEmail_values, *contactName_values]},
                                                                                     {'typeName': 'language', 'typeClass': 'controlledVocabulary',
                                                                                      'multiple': 'true', 'value': language_values},
                                                                                     {'typeName': 'software', 'multiple': 'true',
                                                                                      'typeClass': 'primitive', 'value': software_values},
                                                                                     {'typeName': 'dateOfDeposit', 'typeClass': 'primitive', 'value': date_of_deposit_value},
                                                                                     {'typeName': 'timePeriodCovered', 'typeClass': 'compound', 'multiple': 'true', 'value': [{"timePeriodCoveredStart": {
                                                                                         "typeName": "timePeriodCoveredStart",
                                                                                         "multiple": 'false',
                                                                                         "typeClass": "primitive",
                                                                                         "value": date_start_value
                                                                                     },
                                                                                         "timePeriodCoveredEnd": {
                                                                                         "typeName": "timePeriodCoveredEnd",
                                                                                         "multiple": 'false',
                                                                                         "typeClass": "primitive",
                                                                                         "value": date_end_value
                                                                                     }}]},
                                                                                     {
                                                                              "typeName": "kindOfData",
                                                                              "multiple": 'true',
                                                                              "typeClass": "primitive",
                                                                              "value":
                                                                              data_type_values
                                                                          },
                                                                              {
                                                                              "typeName": "depositor",
                                                                              "multiple": 'false',
                                                                              "typeClass": "primitive",
                                                                              "value": depositorName_value
                                                                          }]



                                                                          }
                                                             }
                                          },
                       "licence": {"name": licence_value},
                       'value': licence_description_value}
        # with open('./data/dv_metadata.json', 'w') as dv_metadata_file:
        #     dump(dv_metadata, dv_metadata_file, indent=4)
        dv_metadata = dumps(dv_metadata)
        r = requests.post(server_url+'api/dataverses/UMCU/datasets',headers=api_token, data=dv_metadata)
        return r.json()
        # redirect you to the dataset on dataverse
        # return redirect(server_url)
    return render_template('metadata.html')

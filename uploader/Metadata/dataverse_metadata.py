import json
import os

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Transfer import helpers


def create_values(values: list, template: dict) -> list:
    "takes a list of values and a template and creates a list of dicts"
    key = list(template.keys())[0]
    list_of_dicts = []
    for value in values:
        template[key]["value"] = value
        list_of_dicts.append(template)
    return list_of_dicts


def parse_form_data(form: dict) -> list:
    author_values = create_values(
        form["author"],
        {
            "authorName": {
                "typeName": "authorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contactName_values = create_values(
        form["contactName"],
        {
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contributor_values = create_values(
        form["contributor"],
        {
            "contributorName": {
                "typeName": "contributorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    publication_values = create_values(
        form["publication"],
        {
            "publicationCitation": {
                "typeName": "publicationCitation",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contactEmail_values = create_values(
        form["contactEmail"],
        {
            "datasetContactEmail": {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    software_values = create_values(
        form["software"],
        {
            "softwareName": {
                "typeName": "softwareName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    keyword_values = create_values(
        form["keywords"],
        {
            "keywordValue": {
                "typeName": "keywordValue",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )

    contact_values = []
    for index, item in enumerate(contactName_values):
        contact = item
        contact.update(contactEmail_values[index])
        contact_values.append(contact)
    # return all values
    return [
        author_values,
        keyword_values,
        publication_values,
        contact_values,
        contributor_values,
        software_values,
    ]


def dv_json(form: dict) -> None:
    dv_metadata = {
        "datasetVersion": {
            "license": {
                "name:": form["licence"],
            },
            "termsOfUse": form["licenceDescription"],
            "metadataBlocks": {
                "citation": {
                    "displayName": "Citation Metadata",
                    "fields": [
                        {
                            "typeName": "publication",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": form["publications"],
                        },
                        {
                            "typeName": "author",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": form["authors"],
                        },
                        {
                            "typeName": "keyword",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": form["keywords"],
                        },
                        {
                            "typeName": "subject",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": [form["subject"]],
                        },
                        {
                            "typeName": "language",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": ["English"],
                        },
                        {
                            "typeName": "title",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": form["title"],
                        },
                        {
                            "typeName": "dsDescription",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": [
                                {
                                    "dsDescriptionValue": {
                                        "typeName": "dsDescriptionValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": form["description"],
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "contributor",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": form["contributors"],
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": form["contacts"],
                        },
                        {
                            "typeName": "software",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": form["software"],
                        },
                        {
                            "typeName": "dateOfDeposit",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": form["dateOfDeposit"],
                        },
                        {
                            "typeName": "timePeriodCovered",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": [
                                {
                                    "timePeriodCoveredStart": {
                                        "typeName": "timePeriodCoveredStart",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": form["daterangeStart"],
                                    },
                                    "timePeriodCoveredEnd": {
                                        "typeName": "timePeriodCoveredEnd",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": form["daterangeEnd"],
                                    },
                                },
                            ],
                        },
                        {
                            "typeName": "depositor",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": form["depositor"],
                        },
                    ],
                },
            },
        },
    }

    # Declare a list of terms for the licence
    terms = {
        "type_1": {
            "license": {
                "name": "CC-BY-4.0",
                "uri": "http://creativecommons.org/licenses/by/4.0",
            },
            "termsOfAccess": "By downloading or otherwise accessing the materials, the downloader represents his/her acceptance of the Terms of Use.",
            "fileAccessRequest": False,
        },
        "type_2": {
            "termsOfUse": "See UMC Utrecht license.",
            "confidentialityDeclaration": "no",
            "specialPermissions": "no",
            "restrictions": "no",
            "citationRequirements": "We ask researchers to include an acknowledgment on behalf of the UMC Utrecht. If you use this dataset in a publication, please cite the dataset, and include the following in the citation: author; year; dataset title; dataset DOI; datase version; repository.",
            "conditions": "To access and use the dataset please read the Terms of Use and the Terms of Access.",
            "disclaimer": "It is expressly understood that UMC Utrecht does not make any warranties regarding the data and specifically does not warrant or guarantee that the data will be accurate, be merchantable or useful for any particular purpose. Use of the data is at your own risk. UMC Utrecht cannot and shall not be held liable for any claims or damages by you or any third party, in connection with or as a result of the use of data by you.",
            "termsOfAccess": "By downloading or otherwise accessing the materials, the downloader represents his/her acceptance of the Terms of Use.",
            "fileAccessRequest": False,
        },
        "type_3a": {
            "termsOfUse": "The standard Data Sharing Agreement (DSA) of the UMC Utrecht must be signed without adjustments. This DSA is in compliance with Dutch law. No costs are involved.",
            "confidentialityDeclaration": "no",
            "specialPermissions": 'To obtain access to the data, a <a href="https://www.umcutrecht.nl/en/data-request-form-umc-utrecht">request form</a> has to be completed. In addition to a completed request form, a  Data Sharing Agreement (DSA) in line with GDPR regulations and/or a Research Collaboration Agreement (RCA) should be signed before data is shared. Only data requests in line with the Terms of Use will be taken into consideration.',
            "restrictions": "See Data Sharing Agreement.",
            "citationRequirements": "See Data Sharing Agreement.",
            "conditions": "To access and use the dataset please read the Terms of Use and the Terms of Access.",
            "disclaimer": "See Data Sharing Agreement.",
            "termsOfAccess": "By downloading or otherwise accessing the materials, the downloader represents his/her acceptance of the Terms of Use.",
            "fileAccessRequest": False,
        },
        "type_3b": {
            "termsOfUse": "The standard Data Sharing Agreement (DSA) of the UMC Utrecht must be signed without adjustments. This DSA is in compliance with Dutch law. No costs are involved.",
            "confidentialityDeclaration": "no",
            "specialPermissions": 'To obtain access to the data, a <a href="https://www.umcutrecht.nl/en/data-request-form-umc-utrecht">request form</a> has to be completed. In addition to a completed request form, a  Data Sharing Agreement (DSA) in line with GDPR regulations and/or a Research Collaboration Agreement (RCA) should be signed before data is shared. Only data requests in line with the Terms of Use will be taken into consideration.',
            "restrictions": "See Data Sharing Agreement.",
            "citationRequirements": "See Data Sharing Agreement.",
            "conditions": "To access and use the dataset please read the Terms of Use and the Terms of Access.",
            "disclaimer": "See Data Sharing Agreement.",
            "termsOfAccess": 'The data is not available for download directly via DataverseNL. Data is available on request by completing the <a href="https://www.umcutrecht.nl/en/data-request-form-umc-utrecht">request form</a>. Only data requests in line with the Terms of Use will be taken into consideration. In addition to a completed request form, the Data Sharing Agreement (DSA) in line with GDPR regulations and/or the Research Collaboration Agreement (RCA) should be signed before data is shared. If a data request is approved, the data will be delivered in a safe and secure manner. By signing the DSA and/or RCA and accessing the Materials, the recipient represents his/her acceptance of the Terms of Use.',
            "availabilityStatus": "The data is not available for download directly via DataverseNL but is available on request if the request is compliant with the Terms of Access.",
            "contactForAccess": 'Please fill out the <a href="https://www.umcutrecht.nl/en/data-request-form-umc-utrecht">request form</a>.',
            "fileAccessRequest": True,
        },
    }

    # Check the licence value and update the metadata with the appropriate terms
    if form["licence"] in terms:
        dv_metadata.update(terms["licence"])
    filepath = os.path.join(
        helpers.get_transfer_directory(), DATAVERSE_METADATA_FILENAME
    )
    with open(filepath, "w") as dv_metadata_file:
        json.dump(dv_metadata, dv_metadata_file, indent=4)

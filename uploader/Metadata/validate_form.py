import re

def validate_metadata_form(form: dict) -> bool:
    """
    Validate metadata form
    """
    # Check for required fields
    

    all_fields = (
        "title",
        "author",
        "dsDescription",
        "licenseType",
        "depositDate",
        "datasetContactName",
        "datasetContactEmail",
        "researchType",
        "researchEndDate",
        "packageType",
        "keyword",
        "contributor",
        "software",
        "dataType",
        "relatedPublication",
        "dateRangeStart",
        "dateRangeEnd",
    )

    required_fields = all_fields[:9]
    # Check for required fields
    
    for field in required_fields:
        if field not in form:
            return False
    # check that datasetContactEmail is a valid email
    if not validate_email(form["datasetContactEmail"]):
        return False
    return True

def validate_email(email: any)-> bool:
    """
    Validate email
    """
    try: 
        # Check if email is a string
        if not isinstance(email, str):
            raise EmailNotStringError
        # Match email with a regex
        if re.fullmatch(r'') is None:
            raise EmailSyntaxError
    except EmailNotStringError | EmailSyntaxError:
        return False
    return True

class EmailInvalidError(Exception):
    """
    Exception raised for email invalid errors
    """
    pass

class EmailNotStringError(EmailInvalidError):
    """
    Exception raised for email not string errors
    """
    pass

class EmailSyntaxError(EmailInvalidError):
    """
    Exception raised for email syntax errors
    """
    pass

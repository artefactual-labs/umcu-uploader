import yaml


def add_year(date: str, year: int) -> str:
    """
    Adds a date to the date of deposit field
    """
    year_from_date = int(date[:4])
    rest_of_date = date[4:]
    sum_year = year_from_date + year
    string_sum_year = str(sum_year)
    full_date = string_sum_year + rest_of_date
    return full_date


def get_retention(date: str, researchType: str) -> str:
    retention_value = None
    if researchType == "Basic":
        retention_num = 15
    elif researchType == "Medication":
        retention_num = 25
    elif researchType == "Therapeutic":
        retention_num = 30
    retention_value = add_year(date, retention_num)
    return retention_value


def get_raw_data(data: dict, name: str) -> list:
    list = [y for x, y in data.items() if x.startswith(name)]
    return list

def get_division_acronym(divisions_file_path: str, division: str) -> str:
        with open(divisions_file_path) as division_file:
                divisions = yaml.load_all(division_file)
        for division_dict in divisions:
            if division_dict["name"] == division:
                acronym = division_dict['acronym']
                return acronym
        return "No acroynm found"
                
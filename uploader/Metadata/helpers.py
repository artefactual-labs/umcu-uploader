def add_year(date: str, year_1: int, year_2: int) -> str:
    """
    Adds a date to the date of deposit field
    """
    rest_of_date = date[:-2]
    sum_year = str(year_1 + year_2)
    full_date = rest_of_date.join(sum_year)
    return full_date

def get_retention(date: str, researchType: str) -> str:
            retention_value = None
            research_end_year = (int(date[-2])*10) + int(date[-1])
            match researchType:
                case "Basic":
                    retention_num = 15
                case "Therapeutic":
                    retention_num = 30
                case "Medication":
                    retention_num = 25
            retention_value = add_year(date, research_end_year, retention_num)
            return retention_value

def get_raw_data(data: dict, name: str) -> list:
    list = [
            y for x, y in data.items() if x.startswith(name)
        ]
    return list
from importlib import resources

def get_categories():

    with resources.path("src.pf_console.data", "CATEGORIES_PersonalFinancePY.xml") as f:
        data_file_path = f

    return data_file_path

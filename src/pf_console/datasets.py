from importlib import resources

def get_categories():

    with resources.path("src.pf_console.data", "categories_data.xml") as f:
        data_file_path = f

    return data_file_path


def get_raw_vendor_to_vendor():

    with resources.path("src.pf_console.data", "raw_vendor_to_vendor_data.csv") as f:
        data_file_path = f

    return data_file_path

def get_resources():

    with resources.path("src.pf_console.data", "resources.csv") as f:
        data_file_path = f

    return data_file_path
from bs4 import BeautifulSoup
import BudgetLine as bl

#   vendor information is loaded and kept in a BeautifulSoup object throughout execution
VENDORS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/VENDORS_PersonalFinancePY.xml'
with open(VENDORS_FILE, 'r') as vendors_file:
    vendors_str = vendors_file.read()
vendors_data = BeautifulSoup(vendors_str, 'xml')

#   category information is loaded and kep in a dictionary throughout execution
CATEGORIES_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/CATEGORIES_PersonalFinancePY.xml'
with open(CATEGORIES_FILE, 'r') as categories_file:
    categories_str = categories_file.read()
categories_data = BeautifulSoup(categories_str, 'xml')
categories=categories_data.find_all('category')
category_dict={}
for c in categories:
    cat=c.contents[0].strip()
    subcat=c.find('subcategories').contents[0].split(',')
    category_dict[cat]=subcat

def add_new_vendor(vendor, b_l) -> bl.BudgetLine:
    root_tag=vendors_data.find_all('vendors')[0]
    vendor_tag = vendors_data.new_tag('vendor')
    vendor_tag['name'] = vendor.replace(' ','').replace(u'\xa0','')
    vendor_tag.string = b_l.vendor
    root_tag.append(vendor_tag)

    category_tag = vendors_data.new_tag('category')
    category_tag.string = b_l.category
    vendor_tag.append(category_tag)

    subcategory_tag = vendors_data.new_tag('subcategory')
    subcategory_tag.string = b_l.subcategory
    vendor_tag.append(subcategory_tag)

    write_vendors_file()

def get_vendor_dict():
    vendors = vendors_data.find_all('vendor')
    vendor_dict = {}
    for v in vendors:
        vendor_dict[v['name']] = v.contents[0].strip()

    return vendor_dict

def write_vendors_file():
    f = open(VENDORS_FILE, 'w')
    f.write(vendors_data.prettify())

from bs4 import BeautifulSoup
import BudgetLine as bl

VENDORS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/VENDORS_PersonalFinancePY.xml'

with open(VENDORS_FILE, 'r') as f:
    data = f.read()
bs_data = BeautifulSoup(data, 'xml')

#
# vons='AplPay VONS #2784 27SAN DIEGO           CA'
# vons_corrected='Von\'s'
#
# vendor_tag = bs_data.new_tag('vendor')
# vendor_tag['name'] = vons
# cat='Groceries'
# subcat='Regular Groceries'
#
# category_tag=bs_data.new_tag('category')
# category_tag.string=cat
# vendor_tag.append(category_tag)
#
# subcategory_tag=bs_data.new_tag('subcategory')
# subcategory_tag.string=subcat
# vendor_tag.append(subcategory_tag)
#
# bs_data.append(vendor_tag)
# print(bs_data.prettify())
#
# # bs_vendors = bs_data.find_all('vendor', {'name': "UBER"})
# # bs_vendors = bs_data.find_all('vendor')
# # for v in bs_vendors:
# # 	print(v.find_all('subcategory')[0].contents[0])

def add_new_vendor(vendor, b_l) -> bl.BudgetLine:
    print('Adding vendor')
    root_tag=bs_data.find_all('vendors')[0]
    vendor_tag = bs_data.new_tag('vendor')
    vendor_tag['name'] = vendor.replace(' ','').replace(u'\xa0','')
    vendor_tag.string = b_l.vendor
    root_tag.append(vendor_tag)

    category_tag = bs_data.new_tag('category')
    category_tag.string = b_l.category
    vendor_tag.append(category_tag)

    subcategory_tag = bs_data.new_tag('subcategory')
    subcategory_tag.string = b_l.subcategory
    vendor_tag.append(subcategory_tag)

    write_vendors_file()

def write_vendors_file():
    f = open(VENDORS_FILE, 'w')
    f.write(bs_data.prettify())

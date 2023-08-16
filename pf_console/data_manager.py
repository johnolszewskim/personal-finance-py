import pandas as pd
import pf_console.budget_line as bl
import datetime
from pf_console.account import Account
from bs4 import BeautifulSoup
import csv
import pf_console.functions.prompt_functions as prompt
import pf_console.functions.load_functions as load

class DataManager:

    transaction_column_map = {
        'Transaction ID': 'test',
        'Date': {
            'Chase': 'Transaction Date',
            'American Express': 'Date'
        },
        'Vendor': {
            'Chase': 'Description',
            'American Express': 'Description'
        },
        'Amount': {
            'Chase': 'Amount',
            'American Express': 'Amount'
        },
        'Amount Sign': {
            'Chase': '-',
            'American Express': '+'
        }
    }

    VENDORS_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/VENDORS_PersonalFinancePY.xml'
    CATEGORIES_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/CATEGORIES_PersonalFinancePY.xml'
    ACCOUNTS_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/ACCOUNTS_PersonalFinancePY.csv'
    RAW_VENDOR_TO_VENDOR_FILENAME = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/RAW_VENDOR_TO_VENDOR_PersonalFinancePY.csv'
    def __init__(self, saved_transactions_filename, saved_budget_lines_filename, new_statement_filename):

        self.YEAR = '2023'

        self.saved_transactions_filename = saved_transactions_filename
        self.saved_budget_lines_filename = saved_budget_lines_filename
        self.new_statement_filename = new_statement_filename

        self.df_budget_lines = pd.read_csv(self.saved_budget_lines_filename)  # new
        self.df_budget_lines = self.df_budget_lines.fillna('')  # new

        self.dict_categories_subcategories = {}  # new
        self.dict_budget_categories = {}  # new
        load.load_categories(self) # new

        self.data_categories = BeautifulSoup()
        self.data_vendors = self.load_vendors()
        self.df_accounts = Account.load_accounts(self.ACCOUNTS_FILE)

        self.ACCOUNT = prompt.prompt_account(self.df_accounts)
        self.BANK = self.df_accounts.loc[self.ACCOUNT].Bank
        self.STATEMENT_ID = self.create_statement_id(self.ACCOUNT,
                                                     self.YEAR,
                                                     prompt.prompt_month(self.new_statement_filename),
                                                     self.df_accounts.loc[self.ACCOUNT,'Closing Date'])





    def create_statement_id(self, account_number, year, month, date) -> str:

        return '_' + str(account_number) + '_'+ year + str(month).zfill(2) + str(date).zfill(2)

    def get_saved_budget_lines(self) -> {}:



        dict_bl = {}

        for index, b_l in self.df_budget_lines.iterrows():

            new_bl = bl.BudgetLine(
                b_l['Transaction ID'],
                datetime.date.fromisoformat(b_l['Date']),
                b_l['Vendor'],
                b_l['Category'],
                b_l['Subcategory'],
                b_l['Amount'],
                b_l['Tag'],
                b_l['Notes']
            )

            if b_l['Transaction ID'] not in dict_bl:
                dict_bl[b_l['Transaction ID']] = [new_bl]
            else:
                dict_bl[b_l['Transaction ID']] = dict_bl[b_l['Transaction ID']] + [new_bl]

        return dict_bl

    def get_saved_transactions(self) -> pd.DataFrame:

        saved_transactions = pd.read_csv(self.saved_transactions_filename)
        saved_transactions.set_index('Transaction ID')

        return saved_transactions

    def load_new_transactions(self) -> pd.DataFrame:

        new_transactions = self.map_raw_transactions(pd.read_csv(self.new_statement_filename))
        new_transactions = new_transactions.loc[
            new_transactions['Date'].dt.strftime('%Y') == self.YEAR]

        return new_transactions

    def map_raw_transactions(self, raw_transactions) -> pd.DataFrame:
        new_transactions = pd.DataFrame(columns=DataManager.transaction_column_map.keys())

        new_transactions['Date'] = raw_transactions[DataManager.transaction_column_map['Date'][self.BANK]]
        new_transactions['Date'] = pd.to_datetime(new_transactions['Date'])
        new_transactions.sort_values(by='Date', inplace=True)
        new_transactions['Vendor'] = raw_transactions[DataManager.transaction_column_map['Vendor'][self.BANK]]
        new_transactions['Amount'] = raw_transactions[DataManager.transaction_column_map['Amount'][self.BANK]]
        if DataManager.transaction_column_map['Amount Sign'][self.BANK] == '-':
            new_transactions['Amount'] = -new_transactions['Amount']
        new_transactions.reset_index(drop=True, inplace=True)
        new_transactions['Transaction ID'] = new_transactions.index
        new_transactions['Transaction ID'] = new_transactions['Transaction ID'].astype(str) + self.STATEMENT_ID

        return new_transactions

    def load_vendors(self) -> BeautifulSoup:

        with open(DataManager.VENDORS_FILE, 'r') as vendors_file:
            vendors_str = vendors_file.read()
        vendors_data = BeautifulSoup(vendors_str, 'xml')

        return vendors_data

    def get_matching_vendors(self, raw_vendor) -> []:

        matches = self.data_vendors.find_all('vendor',
                                                       {'name': raw_vendor.replace(' ', '').replace(u'\xa0', '')})

        return matches

    def is_exact_matching_vendor(self, raw_vendor, budget_line) -> bool:

        matches = self.get_matching_vendors(raw_vendor)

        if budget_line.tag == 'REFUND':
            input('REFUND')
            return True

        for v in matches:
            if budget_line.vendor != v.contents[0].strip():
                input('vendor doesnt match')
                continue
            elif budget_line.category != v.find_all('category')[0].contents[0].strip():
                input('category doesnt match')
                continue
            elif budget_line.subcategory != v.find_all('subcategory')[0].contents[0].strip():
                input('subcategory doesnt match')
                continue
            elif len(v.find_all('tag')) > 0:
                if budget_line.tag != v.find_all('tag')[0].contents[0].strip():
                    input('tag doesnt match')
                    continue
            elif len(v.find_all('notes')) > 0:
                if budget_line.notes != v.find_all('notes')[0].contents[0].strip():
                    input('notes doesnt match')
                    continue
            elif len(v.find_all('tag')) == 0 and budget_line.tag != '':
                input('no tag when tags')
                continue
            elif len(v.find_all('notes')) == 0 and budget_line.notes != '':
                input('no notes when notes')
                continue

            input('exact match')
            return True

        return False

    def get_vendor_dict(self):

        vendors = self.data_vendors.find_all('vendor')
        vendor_dict = {}
        for v in vendors:
            vendor_dict[v['name']] = v.contents[0].strip()

        return vendor_dict

    def save_new_vendor(self, raw_vendor, budget_line):

        if self.is_exact_matching_vendor(raw_vendor, budget_line):
            input('dont write new vendor')
            return

        input('writing new vendor')

        root_tag = self.data_vendors.find_all('vendors')[0]
        vendor_tag = self.data_vendors.new_tag('vendor')
        vendor_tag['name'] = raw_vendor.replace(' ', '').replace(u'\xa0', '')
        vendor_tag.string = budget_line.vendor
        root_tag.append(vendor_tag)

        category_tag = self.data_vendors.new_tag('category')
        category_tag.string = budget_line.category
        vendor_tag.append(category_tag)

        subcategory_tag = self.data_vendors.new_tag('subcategory')
        subcategory_tag.string = budget_line.subcategory
        vendor_tag.append(subcategory_tag)

        if budget_line.tag != '':
            tag_tag = self.data_vendors.new_tag('tag')
            tag_tag.string = budget_line.tag
            vendor_tag.append(tag_tag)

        if budget_line.notes != '':
            notes_tag = self.data_vendors.new_tag('notes')
            notes_tag.string = budget_line.notes
            vendor_tag.append(notes_tag)

        f = open(DataManager.VENDORS_FILE, 'w')
        f.write(self.data_vendors.prettify())

    def write_budget_line(self, budget_line):

        d = {
            'Transaction ID': budget_line.transaction_id,
            'Date': budget_line.date.strftime('%Y-%m-%d'),
            'Vendor': budget_line.vendor,
            'Category': budget_line.category,
            'Subcategory': budget_line.subcategory,
            'Amount': budget_line.amount,
            'Tag': budget_line.tag,
            'Notes': budget_line.notes}
        with open(self.saved_budget_lines_filename, 'a') as file:
            dict_obj = csv.DictWriter(file, fieldnames=budget_line.field_names)
            dict_obj.writerow(d)

    def write_transactions(self, saved_transactions):
        saved_transactions.to_csv(self.saved_transactions_filename, index=False)

    def save_category(self, category, subcategory):

        if category not in self.dict_categories_subcategories:
            self.dict_categories_subcategories[category] = []
            input('writing new category and subcategory')
            self.write_category(category, subcategory)
            return

        if subcategory not in self.dict_categories_subcategories[category]:
            self.dict_categories_subcategories[category] = self.dict_categories_subcategories[category] + [subcategory]
            input('writing just new subcategory')
            self.write_category(category, subcategory, new_category=False)
            return

    def write_category(self, category, subcategory, new_category = True):

        print(self.data_categories.prettify())

        root_tag = self.data_categories.new_tag('categories')
        self.data_categories.append(root_tag)

        for c in self.dict_categories_subcategories.keys():

            category_tag = self.data_categories.new_tag('category')
            category_tag['name'] = c
            root_tag.append(category_tag)

            for sc in self.dict_categories_subcategories[c]:
                subcategory_tag = self.data_categories.new_tag('subcategory')
                subcategory_tag['name'] = sc
                category_tag.append(subcategory_tag)

        f = open(DataManager.CATEGORIES_FILE, 'w')
        f.write(self.data_categories.prettify())

    def get_bl_matching_vendors(self, vendor) -> pd.DataFrame:

        matching = self.df_budget_lines.loc[self.df_budget_lines['Vendor'] == vendor]

        return matching

    def save_splits(self, splits):

        input('save_splits()')



import pandas as pd
import datetime
from bs4 import BeautifulSoup
import csv
import src.pf_console.functions.prompt as prmpt
import src.pf_console.functions.load as ld
import src.pf_console.functions.save as sve
from src.pf_console.objects import account
import src.pf_console.datasets as datasets


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
    # CATEGORIES_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/categories_data.xml'
    ACCOUNTS_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/ACCOUNTS_PersonalFinancePY.csv'
    # RAW_VENDOR_TO_VENDOR_FILENAME = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/raw_vendor_to_vendor_data.csv'

    def __init__(self, pf_console, saved_transactions_filename, saved_budget_lines_filename, new_statement_filename):

        self.pf_console = pf_console
        self.YEAR = '2023'

        self.saved_transactions_filename = saved_transactions_filename
        self.saved_budget_lines_filename = saved_budget_lines_filename
        self.new_statement_filename = new_statement_filename


        self.df_raw_vendor_to_vendor = ld.load_raw_vendor_to_vendor()
        self.df_budget_lines = ld.load_csv(self.saved_budget_lines_filename, ['Transaction ID', 'Date', 'Vendor', 'Category', 'Subcategory', 'Amount', 'Tag', 'Notes'])
        self.df_saved_transactions = ld.load_csv(self.saved_transactions_filename,['Transaction ID', 'Date', 'Vendor', 'Amount'])
        # input(self.df_saved_transactions)

        self.dict_categories_subcategories = {}  # new
        self.dict_budget_categories = {}  # new

        self.data_categories = BeautifulSoup()
        ld.load_categories(self) # new


        # self.data_vendors = self.load_vendors()
        self.df_accounts = account.load_accounts(self.ACCOUNTS_FILE)

        self.ACCOUNT = prmpt.prompt_account(self.df_accounts)
        self.BANK = self.df_accounts.loc[self.ACCOUNT].Bank
        self.STATEMENT_ID = self.create_statement_id(self.ACCOUNT,
                                                     self.YEAR,
                                                     prmpt.prompt_month(self.new_statement_filename),
                                                     self.df_accounts.loc[self.ACCOUNT,'Closing Date'])


    def create_statement_id(self, account_number, year, month, date) -> str:

        return '_' + str(account_number) + '_'+ year + str(month).zfill(2) + str(date).zfill(2)

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

    def write_categories_subcategories(self, console, splits, category, subcategory, is_new_category, is_new_subcategory):

        if not is_new_category and not is_new_subcategory:
            return

        # if adding a new category
        if is_new_category:
            budget_name = prmpt.prompt_budget(console, splits)
            category_tag = self.write_new_category(category, budget_name)
        #if only adding a new subcategory
        else:
            category_tag = self.data_categories.categories.find_all('category', attrs={'name': category})[0]

        if is_new_subcategory:
            new_subcategory_tag = self.data_categories.new_tag('subcategory')
            new_subcategory_tag['name'] = subcategory
            category_tag.append(new_subcategory_tag)

        f = open(datasets.get_categories(), 'w')
        f.write(self.data_categories.prettify())
        return

    def write_new_category(self, category, budget_name):
        categories_tag = self.data_categories.categories
        new_tag = self.data_categories.new_tag('category')
        new_tag['name'] = category
        new_tag['budget'] = budget_name
        categories_tag.append(new_tag)
        return new_tag

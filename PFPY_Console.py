import pandas as pd
import PersonalFinancePYData as data
import PFPY_Console_Functions as func
import Transaction as tx
import BudgetLine as bl
from tkinter import filedialog as fd
import datetime

TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/TRANSACTIONS_PersonalFinancePY.csv'
BUDGET_LINES_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_TRANSACTIONS_PersonalFinancePY.csv'
IMPORT_TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/3. Credit Card Statements/CHASE Freedom Unlimited 3387/1. Chase3387_Activity20221209_20230108_20230225.CSV'

BANK = 'Chase'
ACCOUNT = '3387'

transactions = pd.read_csv(TRANSACTIONS_FILE)
transactions.set_index('Transaction ID')

budget_lines = pd.read_csv(BUDGET_LINES_FILE)
budget_lines.set_index('Transaction ID')

#ask for bank type
#ask for account
#ask for statement date
# STATEMENT_ID = account_date
STATEMENT_ID = '3387_20230108'

# IMPORT_TRANSACTIONS_FILE = fd.askopenfilename()
import_transactions = pd.read_csv(IMPORT_TRANSACTIONS_FILE)

new_transactions = func.map_import_transactions(import_transactions, BANK, STATEMENT_ID)
new_transactions.sort_values(by='Date', inplace=True)
import_transactions(new_transactions)

def import_transactions(new_transactions):

    for t in new_transactions.iloc():

        new_bl = func.import_single_transaction(
            bl.BudgetLine(t['Transaction ID'], t['Date'], t['Vendor'], '', '', t['Amount'], '', ''))

        if new_bl is not None: # if user want to save the budget line
            #save the budget line

        #save the transaction
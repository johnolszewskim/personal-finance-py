import pandas as pd
import PersonalFinancePYXML as pfxml
import PFPY_Console_Functions as func
import PersonalFinancePYRefund as refund
import BudgetLine as bl
import os
import ConsolePFPY as console
import DataManager
from tkinter import filedialog as fd
import datetime

'''

The PFPY_Console is used in development as intermediate step in progress toward GUI application
to establish the back-end design and functionality before the added complexity of GUI implementation.
The Console is intended to be a functional program for real-life application.

The script gathers a variety of user input from the user including the bank from which the statement
is being downloaded, the statement file location and the statement date. The program uses this 
information to map the transaction information into the standardized Transaction format. The new
Transactions are stored in the heap in a pandas.DataFrame object.

A CSV file of all historical transactions is stored on the hard drive. All historical transactions
are laoded into a DataFrame and kept on the heap.

If a historical Transaction with the same transaction_id is not found then the transaction information
is used to initialize a BudgetLine object. Once the user complete the BudgetLine transaction object it
(or they, if the transaction is split in to multiple BudgetLine transactions) is loaded into the 
historical BudgetLine transaction file and the historical Transaction File is wrtiten to include
the new transaction.

'''
YEAR = '2023'
SAVED_TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/TRANSACTIONS_PersonalFinancePY.csv'
SAVED_BUDGET_LINES_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_LINES_PersonalFinancePY.csv'
STATEMENT_FILE = '/Users/johnmatthew/Documents/Personal Finance/3. Credit Card Statements/CHASE Freedom Unlimited 3387/2. Chase3387_Activity20230109_20230208_20230209.CSV'

BANK = 'Chase'
ACCOUNT = '3387'

saved_transactions = pd.read_csv(SAVED_TRANSACTIONS_FILE)
saved_transactions.set_index('Transaction ID')
dict_saved_budget_lines = pfxml.get_saved_budget_line_dict(pd.read_csv(SAVED_BUDGET_LINES_FILE))

# ask for bank type, ask for account, ask for statement date, STATEMENT_ID = account_date
STATEMENT_ID = '_3387_20230208'

raw_transactions = pd.read_csv(STATEMENT_FILE)
new_transactions = func.map_raw_transactions(raw_transactions, BANK, STATEMENT_ID)
new_transactions = new_transactions.loc[new_transactions['Date'].dt.strftime('%Y') == YEAR]

dm=DataManager.DataManager(SAVED_TRANSACTIONS_FILE, SAVED_BUDGET_LINES_FILE, STATEMENT_FILE)

c=console.ConsolePFPY(dict_saved_budget_lines, saved_transactions, new_transactions)
c.run()

# need to figure out file manafgement
# consider making class for file management ot and having console class have an instance


for i, t in new_transactions.iterrows():

    if new_transactions.loc[i, 'Transaction ID'] not in saved_transactions['Transaction ID'].values:
        temp_b_l = bl.BudgetLine(t['Transaction ID'], t['Date'].to_pydatetime(), t['Vendor'], '', '', t['Amount'], '', '')
        os.system('clear')
        if not func.prompt_keep(temp_b_l):
            saved_transactions.loc[len(saved_transactions.index)] = t
            saved_transactions.to_csv(SAVED_TRANSACTIONS_FILE, index=False)
            continue
        os.system('clear')
        is_refund = refund.prompt_refund(temp_b_l)
        if is_refund:
            to_refund = refund.prompt_refunded_budget_line(dict_saved_budget_lines)
            if to_refund is not None:
                to_refund.refund(temp_b_l)
                temp_b_l_list = [temp_b_l]
            else:
                temp_b_l_list = func.import_single_transaction([temp_b_l])
        else:
            temp_b_l_list = func.import_single_transaction([temp_b_l])

        bl_was_saved = func.prompt_save(temp_b_l_list, SAVED_BUDGET_LINES_FILE, dict_saved_budget_lines)
        if bl_was_saved:
            pfxml.add_new_vendor(t['Vendor'], temp_b_l_list[0])

        saved_transactions.loc[len(saved_transactions.index)] = t
        saved_transactions.to_csv(SAVED_TRANSACTIONS_FILE, index=False)

    saved_transactions = pd.read_csv(SAVED_TRANSACTIONS_FILE)
    saved_budget_lines = pd.read_csv(SAVED_BUDGET_LINES_FILE)

print('ALL TRANSACTIONS IMPORTED.')

from src.pf_console.objects import pf_console as pfc

'''

The PFPY_Console is used in development as intermediate step in progress toward GUI application
to establish the back-end design and functionality before the added complexity of GUI implementation.
The Console is intended to be a functional program for real-life application.

The script gathers a variety of user input from the user including the bank from which the statement
is being downloaded, the statement file location and the statement date. The program uses this 
information to map the transaction information into the standardized Transaction format. The new
Transactions are stored in the heap in a pandas.DataFrame object.

A CSV file of all historical transactions is stored on the hard drive. All historical transactions
are loaded into a DataFrame and kept on the heap.

If a historical Transaction with the same transaction_id is not found then the transaction information
is used to initialize a BudgetLine object. Once the user complete the BudgetLine transaction object it
(or they, if the transaction is split in to multiple BudgetLine transactions) is loaded into the 
historical BudgetLine transaction file and the historical Transaction File is written to include
the new transaction.

'''
SAVED_TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/TRANSACTIONS_PersonalFinancePY.csv'
SAVED_BUDGET_LINES_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/0. PersonalFinancePY/BUDGET_LINES_PersonalFinancePY.csv'
STATEMENT_FILE = '/Users/johnmatthew/Documents/6. Personal Finance/3. Credit Card Statements/AMEX Gold Card 63002/2023/9. 2023-09-01.csv'

# STATEMENT_FILE = fd.askopenfilename()

c = pfc.PFConsole(SAVED_TRANSACTIONS_FILE, SAVED_BUDGET_LINES_FILE, STATEMENT_FILE)
c.run()

print('ALL TRANSACTIONS IMPORTED.')

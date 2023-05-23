# personal-finance-py
Run PersonalFinancePY.py

PersonalFinancePY is intended to ease managing personal finances by easing
the process importing credit card transaction data from banks. The program will 
import statement data in the form of a CSV file and, use data input to categorize
transactions for budgeting.

First development priority is the "transaction wizard" module which allows the user
to easily load statements. The user can correct transaction information and
categorize transactions. The program will use information from past transactions
(saved in XML files, loaded at runtime, managed in program memory and written
on specific occasions) to suggest corrected vendor names and categorization.
The goal is to speed up the transaction import process and standardize data to be 
used for analysis and budgeting. Transaction and Budget Line information is saved
in CSV files for future use.

Additional modules will be created for increased functionaity and analysis.
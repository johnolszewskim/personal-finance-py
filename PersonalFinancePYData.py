import pandas as pd
from bs4 import BeautifulSoup
import PersonalFinancePYGUI as gui

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

account_lookup = {
	'3387': 'Freedom Unlimited',
	'06003': 'Bonvoy Brilliant',
	'81007': 'Delta Reserve',
	'21001': 'Everyday Preferred',
	'63002': 'Gold',
	'91009': 'Hilton Aspire',
	'42004': 'Platinum',
	'00001': 'Arrival+',
}

category_lookup = {
	'Subscriptions' : ['iCloud', 'Streaming Services', 'Amazon Prime'],
	'Recreation' : ['Membership Fees', 'Skiing', 'Cycling', 'Camping', 'Scuba Diving', 'Nutrition', 'Running', 'Outdoor Gear'],
	'Alcohol' : ['Bar/Brewery', 'Liquor Store'],
	'Education' : ['Books/Supplies'],
	'Groceries' : ['Regular Groceries', 'Snacks', 'Meal Prep'],
	'Mosi' : ['Boarding', 'Gear/Supplies', 'Veterinary', 'Wag!', 'Food', 'Grooming'],
	'Personal Care' : ['Toiletries', 'Therapy', 'Medicine/Prescriptions', 'Haircuts'],
	'Transportation' : ['Rideshare', 'Parking'],
	'Restaurants' : ['Coffee', 'Dining', 'Takeout'],
	'Subscriptions' : ['iCloud', 'Streaming Services', 'Amazon Prime']
}

transactions_SAVED = pd.DataFrame
budget_transactions_SAVED = pd.DataFrame
df_resources = pd.DataFrame
def import_resources():

	directory = df_resources.loc['directory']['LOCATION']
	transactions_SAVED = pd.read_csv(directory + df_resources.loc['transactions']['LOCATION'])
	print("transactions loaded.")
	budgets_transactions_SAVED = pd.read_csv(directory + df_resources.loc['budget_transactions']['LOCATION'])
	print("budget_transactions loaded.")

vendors = {
		'APPLE.COM/BILL' : 'Apple.com',
		'UBER' : 'Uber'
	}
def lookup_vendor(vendor) -> str:

	if vendor in vendors:
		return vendors[vendor]
	else:
		return vendor
def match_vendor_category(vendor) -> str:

	vendor_category = {
		'Apple.com' : 'Subscriptions'
	}

	if vendor in vendor_category:
		return vendor_category[vendor]
	else:
		return ""



budget_col_names = ["Transaction ID", "Vendor", "Category", "Subcategory", "Amount", "Tag", "Notes"]
master_budget_lines = pd.DataFrame(columns=budget_col_names)

transaction_col_names = ["Transaction ID", "Date", "Vendor", "Amount", "Cleared"]
master_transaction_lines = pd.DataFrame(columns=transaction_col_names)

def import_transactions(imported_df, transactions_df, col_map, statement_id) -> int:

	start_index = len(transactions_df)

	# transfer columns that are straight mapping
	for key in col_map.keys():
		transactions_df[col_map[key]] = imported_df[key]

	transactions_df['Transaction ID'] = range(len(transactions_df))
	transactions_df['Statement ID'] = statement_id

	return start_index

def transactions_to_budget(trans):
	gui.startTransactionWizard(trans)

def add_budget_line(trans_ID, vendor, category, subcategory, amount):
	master_budget_lines.loc[len(master_budget_lines)] = {
		'Transaction ID': trans_ID,
		'Vendor': vendor,
		'Category': category,
		'Subcategory': subcategory,
		'Amount': amount
	}



















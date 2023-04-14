import pandas as pd
import os
import PersonalFinancePYGUI as gui

chase_col_map = {
	'Transaction Date' : 'Date',
	'Description' : 'Vendor',
	'Amount' : 'Amount'
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
	'Groceries' : ['Groceries', 'Snacks', 'Meal Prep'],
	'Mosi' : ['Boarding', 'Gear/Supplies', 'Veterinary', 'Wag!', 'Food', 'Grooming'],
	'Personal Care' : ['Toiletries', 'Therapy', 'Medicine/Prescriptions', 'Haircuts'],
	'Public Transportation' : ['Rideshare', 'Parking'],
	'Restaurants' : ['Coffee', 'Dining', 'Takeout'],
	'Subscriptions' : ['iCloud', 'Streaming Services', 'Amazon Prime']
}

vendor_lookup = {
	'APPLE.COM/BILL' : 'Apple.com',
}

budget_col_names = ["Transaction ID", "Vendor", "Category", "Subcategory", "Amount", "Tag", "Notes"]
master_budget_lines = pd.DataFrame(columns=budget_col_names)

transaction_col_names = ["Transaction ID", "Statement ID", "Date", "Vendor", "Amount"]
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

transactions_SAVED = pd.DataFrame
budget_transactions_SAVED = pd.DataFrame
df_resources = pd.DataFrame


def import_resources(resources):
	df_resources = resources

	directory = df_resources.loc['directory']['LOCATION']

	transactions_SAVED = pd.read_csv(directory + df_resources.loc['transactions']['LOCATION'])
	print(transactions_SAVED)

	budgets_transactions_SAVED = pd.read_csv(directory + df_resources.loc['budget_transactions']['LOCATION'])
	print(budgets_transactions_SAVED)














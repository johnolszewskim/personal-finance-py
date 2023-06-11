from bs4 import BeautifulSoup
class Account:

    def __init__(self, name, number, exp, security, bank, closing_date):
        self.name = name
        self.number = number
        self.exp = exp
        self.security = security
        self.bank = bank
        self.closing_date = closing_date

    def load_accounts(accounts_filename: str) -> {}:

        with open(accounts_filename, 'r') as accounts_file:
            accounts_str = accounts_file.read()

        accounts_data = BeautifulSoup(accounts_str, 'xml')
        accounts = accounts_data.find_all('creditcard')

        dict_accounts = {}
        for a in accounts:
            key = ''
            if a['bank'] == 'Chase':
                key = a['number'][-4:]
            elif a['bank'] == 'American_Express':
                key = a['number'][-5:]

            dict_accounts[key] = Account(
                a.contents[0].strip(),
                a["number"],
                a["exp"],
                a["sec"],
                a["bank"].replace('_', ' '),
                int(a["closing_date"])
            )

        return dict_accounts

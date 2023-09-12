import pandas as pd


class Account:

    def __init__(self, name, number, exp, security, bank, closing_date):
        self.name = name
        self.number = number
        self.exp = exp
        self.security = security
        self.bank = bank
        self.closing_date = closing_date


def load_accounts(accounts_filename: str) -> pd.DataFrame:

    df_accounts = pd.read_csv(accounts_filename,
                              dtype={'Name': str,
                                     'Bank': str,
                                     'Number': str,
                                     'Expiration': str,
                                     'Security': str,
                                     'Closing Date':str})

    id = []
    for i in range(len(df_accounts)):
        if df_accounts.loc[i, 'Bank'] == 'Chase':
            key = df_accounts.loc[i, 'Number'][-4:]
        elif df_accounts.loc[i, 'Bank'] == 'American Express':
            key = df_accounts.loc[i, 'Number'][-5:]
        else:
            pass  # need to implement other banks
        id = id + [key]

    df_accounts['id'] = id
    df_accounts.set_index('id', inplace=True)

    return df_accounts


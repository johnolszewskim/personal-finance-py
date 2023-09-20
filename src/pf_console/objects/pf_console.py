from src.pf_console.objects.console import Console
import src.pf_console.functions.prompt as prompt
from src.pf_console.objects import budget_line as bl
import src.pf_console.objects.data_manager as dm


class PFConsole(Console):

    def __init__(self, saved_transactions_file, saved_budget_lines_file, new_statement_file):

        Console.__init__(self, [prompt.prompt_import,
                                # prompt.prompt_refund,
                                prompt.prompt_vendor,
                                prompt.prompt_category,
                                prompt.prompt_add_category,
                                prompt.prompt_subcategory,
                                prompt.prompt_add_subcategory,
                                prompt.prompt_amount,
                                prompt.prompt_tag,
                                prompt.prompt_notes,
                                prompt.prompt_save])

        self.dm = dm.DataManager(self, saved_transactions_file,
                                 saved_budget_lines_file,
                                 new_statement_file)

        self.new_raw_vendor = False # new

        self.new_transactions = self.dm.load_new_transactions()

        self.bl_index = 0
        self.statement_index = 0
        self.statement_length = 0
        self.importing_tx = None

    def run(self, at_func_index=0):
        """

        :param at_func_index:
        :return:
        """

        self.statement_length = len(self.new_transactions)

        for i, tx in self.new_transactions.iterrows():

            self.statement_index = i
            self.importing_tx = tx

            # check to see if tx has been imported
            temp_bl = self.filter(i, tx)

            # reset instance variables for new import
            self.bl_index = 0
            self.func_index = 0

            # if tx had already been imported, temp_bl would be None
            if temp_bl is not None:
                self.func_index = 0
                self.bl_index = 0
                self.functions[self.func_index](self, [temp_bl])
                input("FINISHED ONE")

    def runFrom(self, func):
        """

        :param at_func_index:
        :return:
        """

        self.statement_length = len(self.new_transactions)

        for i, tx in self.new_transactions.iterrows():

            self.statement_index = i
            self.importing_tx = tx

            # check to see if tx has been imported
            temp_bl = self.filter(i, tx)

            # reset instance variables for new import
            self.bl_index = 0
            self.func_index = 0

            # if tx had already been imported, temp_bl would be None
            if temp_bl is not None:
                next_func = func
                while next_func is not None:
                    next_func = next_func(self, [temp_bl])

    def next(self, splits, to_func_index=-1):

        if to_func_index != -1:  # reserved for exiting
            self.func_index = to_func_index
        else:
            self.func_index = self.func_index+1

        if self.func_index == self.functions.index(prompt.prompt_save):
            if self.bl_index != (len(splits) - 1):
                self.bl_index = self.bl_index + 1
                self.next(splits, to_func_index=self.functions.index(prompt.prompt_category))
        if self.func_index >= len(self.functions):
            pass

        else:
            self.functions[self.func_index](self, splits)

    def previous(self, splits):

        self.func_index = self.func_index - 1

        if self.func_index < 0:
            pass

        else:
            self.functions[self.func_index](self, splits)

    def rerun(self, splits):
        self.functions[self.func_index](self, splits)
    def filter(self, i, tx) -> bl.BudgetLine:

        if self.new_transactions.loc[i, 'Transaction ID'] not in self.dm.df_saved_transactions['Transaction ID'].values:
            return bl.BudgetLine(tx['Transaction ID'],
                                 tx['Date'].to_pydatetime(),
                                 tx['Vendor'],
                                 '',
                                 '',
                                 tx['Amount'],
                                 '',
                                 '')

        else:
            return None




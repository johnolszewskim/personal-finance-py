from pf_console.console import Console
import pf_console.functions.prompt_functions as prompt
import pf_console.budget_line as bl
import pf_console.data_manager as dm
import os



class PFConsole(Console):

    PRINT_CATEGORY_ROWS = 4

    def __init__(self, saved_transactions_file, saved_budget_lines_file, new_statement_file):

        Console.__init__(self, [prompt.prompt_keep,
                                prompt.prompt_refund,
                                prompt.prompt_vendor,
                                prompt.prompt_category,
                                self.prompt_custom_category,
                                self.prompt_subcategory,
                                self.prompt_amount,
                                self.prompt_tag,
                                self.prompt_notes,
                                self.check_split_index,
                                self.prompt_save])

        self.dm = dm.DataManager(saved_transactions_file,
                                 saved_budget_lines_file,
                                 new_statement_file)

        self.dict_budget_lines = self.dm.get_saved_budget_lines()
        self.saved_transactions = self.dm.get_saved_transactions()

        self.new_transactions = self.dm.load_new_transactions()

        self.splitting = False
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
            self.splitting = False

            # if tx had already been imported, temp_bl would be None
            if temp_bl is not None:

                self.functions[at_func_index](self, [temp_bl])

    def next(self, splits):

        self.func_index = self.func_index+1

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

        if self.new_transactions.loc[i, 'Transaction ID'] not in self.saved_transactions['Transaction ID'].values:
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

    def import_single_transaction(self, splits):

        while True:
            action = self.functions[self.func_index](splits)
            if action == 0:  # the case that user does not 'keep'
                self.saved_transactions.loc[len(self.saved_transactions.index)] = self.importing_tx
                self.dm.write_transactions(self.saved_transactions)
                return

            self.func_index += action
            if self.func_index < 0:
                self.saved_transactions.loc[len(self.saved_transactions.index)] = self.importing_tx
                self.dm.write_transactions(self.saved_transactions)
                return





    def create_potential_budget_lines(self, splits, matching_vendors) -> []:

        potential_splits = []

        for index, v in enumerate(matching_vendors):

            potential_bl = splits[self.bl_index].copy()
            potential_bl.vendor = v.contents[0].strip()
            potential_bl.category = v.find_all('category')[0].contents[0].strip()
            potential_bl.subcategory = v.find_all('subcategory')[0].contents[0].strip()
            try:
                potential_bl.tag = v.find_all('tag')[0].contents[0].strip()
            except:
                potential_bl.tag = ''
            try:
                potential_bl.notes = v.find_all('notes')[0].contents[0].strip()
            except:
                potential_bl.notes = ''

            potential_splits = potential_splits + [potential_bl]

        return potential_splits

    def split_bl(self, splits):
        self.splitting = True
        splits.append(splits[self.bl_index].copy())
        for index, bl in enumerate(splits):
            bl.transaction_id = bl.transaction_id[0:-2] + '_' + str(index)






    def prompt_custom_category(self, splits) -> int:

        while True:

            os.system('clear')
            self.print_splits(splits)
            self.print_categories(PFConsole.PRINT_CATEGORY_ROWS)
            print('99: RETURN TO CATEGORY LIST')
            print()

            custom_category = input('Input custom category: ')
            if not custom_category.isdigit():
                splits[self.bl_index].category = custom_category
                self.dm.dict_categories[custom_category] = []
                self.func_index=self.functions.index(self.prompt_subcategory)-1
                return 1
            if int(custom_category) == 99:
                self.func_index = self.functions.index(self.prompt_category)-1
                return 1

    def prompt_subcategory(self, splits) -> int:

        subcategories = self.dm.dict_categories[splits[self.bl_index].category]

        while True:

            os.system('clear')
            self.print_splits(splits)
            custom = False

            print()
            if len(subcategories) == 0:
                print('No subcategories.')
                print('99: REINPUT CATEGORY')
                subcategory = input('\nInput custom subcategory: ')
                custom = True
            else:
                for index, subcat in enumerate(subcategories):
                    print(str(index) + ': ' + subcat)
                print('88: ADD CUSTOM SUBCATEGORY')
                print('99: REINPUT CATEGORY')
                subcategory = input('\nInput subcategory: ')
            print()

            if subcategory == "":
                return 1
            elif custom == True:
                splits[self.bl_index].subcategory = subcategory
                return 1
            elif subcategory == '99':
                self.func_index = self.functions.index(self.prompt_category)-1
                return 1
            elif subcategory == '88':
                splits[self.bl_index].subcategory = input('\nInput custom subcategory: ')
                return 1
            elif subcategory.isdigit() is not True:
                continue
            elif (int(subcategory) < len(subcategories)) and (int(subcategory) >= 0):
                splits[self.bl_index].subcategory = subcategories[int(subcategory)]
                return 1

    def prompt_custom_subcategory(self, splits) -> int:
        return 1
    def prompt_amount(self, splits) -> int:

        # return_code = subprocess.call(['python', os.path.join(os.getcwd() + ConsolePFPY.SPLITTER_FILE)])
        # print('returned: ' + str(return_code))

        while True:

            os.system('clear')
            self.print_splits(splits)
            input_amount = input('Input amount (ENTER to keep): ')

            try:

                if float(input_amount) > splits[self.bl_index].amount:
                    continue
                elif float(input_amount) < 0:
                    self.split_bl(splits)
                    if self.prompt_split_or_credit(splits) == 0:
                        splits[0].amount=round(splits[0].amount+float(input_amount), 2)
                        splits[self.bl_index+1].amount=-round(float(input_amount), 2)
                        return 1
                    else:
                        splits[self.bl_index+1].amount=round(float(input_amount), 2)
                        return 1
                else:
                    continue


            except ValueError:
                if input_amount == '':
                    return 1
                continue

    def prompt_split_or_credit(self, splits) -> int:

        while True:

            os.system('clear')
            self.print_splits(splits)
            input_split_or_credit = input('Line is (0) split or (1) credit: ')

            if input_split_or_credit.isdigit() is not True:
                continue

            if (int(input_split_or_credit) != 0) and (int(input_split_or_credit) != 1):
                continue

            return int(input_split_or_credit)


    def prompt_tag(self, splits) -> int:
        os.system('clear')
        self.print_splits(splits)

        input_tag = input('Input tag | ENTER to keep: #')

        if input_tag == '':
            return 1

        else:
            splits[self.bl_index].tag = input_tag
            return 1

    def prompt_notes(self, splits) -> int:
        os.system('clear')
        self.print_splits(splits)

        input_notes = input('Input notes | ENTER to keep: ')

        if input_notes == '':
            return 1
        else:
            splits[self.bl_index].notes = input_notes
            return 1


    def check_split_index(self, splits) -> int:

        if self.bl_index < len(splits)-1:
            self.bl_index += 1
            self.func_index = -1

        return 1

    def prompt_save(self, splits):

        while True:

            os.system('clear')
            self.print_splits(splits)
            response = input('Save? y or n? ')

            if (response == 'y') or (response == ''):
                self.save(splits)
                return 0
            elif response == 'n':
                print('DONT SAVE')
                return 1





    def save(self, splits):

        for budget_line in splits:

            self.dm.save_new_vendor(self.importing_tx['Vendor'], budget_line)
            self.dm.save_category(budget_line.category, budget_line.subcategory)


            self.dm.write_budget_line(budget_line)
            self.dict_budget_lines = self.dm.get_saved_budget_lines()

        #change back split to false
        # reset index to 0

from pfcpy.Console import Console
import BudgetLine as bl
import os
import DataManager


class ConsolePFPY(Console):

    PRINT_CATEGORY_ROWS = 4

    def __init__(self, saved_transactions_file, saved_budget_lines_file, new_statement_file):

        Console.__init__(self, [self.prompt_keep,
                                self.prompt_refund,
                                self.prompt_autocomplete,
                                self.prompt_split,
                                self.prompt_vendor,
                                self.prompt_category,
                                self.prompt_custom_category,
                                self.prompt_subcategory,
                                self.prompt_amount,
                                self.prompt_tag,
                                self.prompt_notes,
                                self.check_split_index,
                                self.prompt_save])

        self.dm = DataManager.DataManager(saved_transactions_file,
                                          saved_budget_lines_file,
                                          new_statement_file)

        self.dict_budget_lines = self.dm.get_saved_budget_lines()
        self.saved_transactions = self.dm.get_saved_transactions()
        self.new_transactions = self.dm.get_new_transactions()

        self.split = False
        self.bl_index = 0

        self.statement_index = 0
        self.statement_len = 0

        self.importing_tx = None

    def run(self):

        self.statement_len = len(self.new_transactions)

        for i, tx in self.new_transactions.iterrows():

            self.statement_index = i

            self.importing_tx = tx
            temp_bl = self.filter(i, tx)
            self.bl_index=0
            self.func_index=0

            if temp_bl is not None:

                result = self.import_single_transaction([temp_bl])


        print("DONE")

    def filter(self, i, tx) -> bl.BudgetLine:

        if self.new_transactions.loc[i, 'Transaction ID'] not in self.saved_transactions['Transaction ID'].values:
            return  bl.BudgetLine(tx['Transaction ID'], tx['Date'].to_pydatetime(), tx['Vendor'], '', '',
                                     tx['Amount'], '', '')

        else:
            return None

    def import_single_transaction(self, splits) -> [bl.BudgetLine]:

        while True:
            action = self.functions[self.func_index](splits)
            if action == 0: # the case that user does not 'keep'
                return splits[:-1]

            self.func_index += action
            if self.func_index < 0:
                return splits

    def prompt_keep(self, splits) -> int:

        while True:
            os.system('clear')
            self.print_splits(splits)
            response = input('Keep? y or n? ')

            if response == 'y':
                return 1
            elif response == 'n':
                return 0

    def prompt_refund(self, splits):
        if splits[self.bl_index].get_amount() < 0:
            while True:
                os.system('clear')
                self.print_splits(splits)
                response = input('Is this transaction a refund? y or n? ')

                if response == 'y':
                    return self.prompt_refunded_budget_line(splits)

        return 1

    def prompt_refunded_budget_line(self, splits) -> int:
        os.system('clear')
        dict_index_tid = {}
        for index, tid in enumerate(list(self.dict_budget_lines.keys())):
            temp = self.dict_budget_lines[tid]
            print(f'{index:<5}{str(temp[0])}')
            dict_index_tid[index] = tid
        print('99: not listed')

        while True:
            bl_index = input('Input line to refund: ')
            if not bl_index.isdigit():
                continue
            bl_index = int(bl_index)
            if bl_index == 99:
                return 1
            elif (bl_index > len(dict_index_tid)) and (bl_index >= 0):
                continue
            else:
                splits[self.bl_index].vendor = self.dict_budget_lines[dict_index_tid[bl_index]][0].vendor
                splits[self.bl_index].category = self.dict_budget_lines[dict_index_tid[bl_index]][0].category
                splits[self.bl_index].subcategory = self.dict_budget_lines[dict_index_tid[bl_index]][0].subcategory
                splits[self.bl_index].tag = 'REFUND'
                splits[self.bl_index].notes = str(self.dict_budget_lines[dict_index_tid[bl_index]][0].transaction_id)

                self.print_splits(splits)
                input('STOP')
                return 8


    def prompt_autocomplete(self, splits) -> int:

        input('inside autocomplete')

        matching_vendors = self.dm.get_matching_vendors(splits[self.bl_index].vendor)
        potential_bl = splits[self.bl_index].copy()

        input(self.dm.data_vendors.prettify())

        input(matching_vendors)

        if len(matching_vendors) == 0:
            print('No autocomplete')

        for v in matching_vendors:

            os.system('clear')
            potential_bl.vendor = v.contents[0].strip()
            potential_bl.category = v.find_all('category')[0].contents[0].strip()
            potential_bl.subcategory = v.find_all('subcategory')[0].contents[0].strip()
            self.print_splits(splits)
            print(potential_bl)
            complete = input('Complete? y or n? ')

            if complete == 'y':
                splits[self.bl_index].vendor = potential_bl.vendor
                splits[self.bl_index].category = potential_bl.category
                splits[self.bl_index].subcategory = potential_bl.subcategory
                self.func_index=self.functions.index(self.prompt_amount)-1
                return 1

        return 1

    def prompt_split(self, splits) -> int:

        while True:
            os.system('clear')
            self.print_splits(splits)
            response = input('Split? y or n? ')

            if response == 'y':
                self.split = True
                splits.append(splits[self.bl_index].copy())
                for index, bl in enumerate(splits):
                    bl.transaction_id = bl.transaction_id[0:-2] + '_' + str(index)
                break
            elif response == 'n':
                self.split = False
                break

        return 1

    def prompt_vendor(self, splits) -> int:

        vendor_dict = self.dm.get_vendor_dict()
        vendor_set = set(vendor_dict.values())

        while True:
            os.system('clear')
            self.print_splits(splits)
            i = input('Input vendor | ENTER to keep | v for vendor list: ').strip()

            if i == 'v':
                print()
                for index, v in enumerate(vendor_set):
                    print(str(index) + '. ' + v)
                print()
            elif i == '':
                return 1
            elif i.isdigit(): # pick vendor from list
                splits[self.bl_index].vendor = list(vendor_set)[int(i)]
                return 1
            elif i == 'x': # dont change vendor
                return 1
            else:
                splits[self.bl_index].vendor = i
                return 1

    def prompt_category(self, splits) -> int:

        categories = sorted(self.dm.dict_categories.key())

        while True:

            os.system('clear')
            self.print_splits(splits)
            self.print_categories(ConsolePFPY.PRINT_CATEGORY_ROWS)
            print('99: ADD CATEGORY/SUBCATEGORY')
            print()

            category_index = input('Input category: ')
            if not category_index.isdigit():
                continue
            category_index = int(category_index)
            if category_index == 99:
                return 1
            if (category_index < len(categories)) and (category_index >= 0):
                splits[self.bl_index].category = categories[category_index]
                return 2

    def prompt_custom_category(self, splits) -> int:

        while True:

            os.system('clear')
            self.print_splits(splits)
            self.print_categories(ConsolePFPY.PRINT_CATEGORY_ROWS)
            print('99: RETURN TO CATEGORY LIST')
            print()

            custom_category = input('Input custom category: ')
            if not custom_category.isdigit():
                splits[self.bl_index].category = custom_category
                self.dm.dict_categories[custom_category] = []
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
                subcategory = input('\nInput subcategory: ')
                custom = True
            else:
                for index, subcat in enumerate(subcategories):
                    print(str(index) + ': ' + subcat)
                print('99: REINPUT CATEGORY')
                subcategory = input('\nInput subcategory: ')
            print()

            if subcategory == "":
                continue
            elif custom == True:
                splits[self.bl_index].subcategory = subcategory
                return 1
            elif subcategory == '99':
                return -2
            elif subcategory.isdigit() is not True:
                continue
            elif (int(subcategory) < len(subcategories)) and (int(subcategory) >= 0):
                splits[self.bl_index].subcategory = subcategories[int(subcategory)]
                return 1

    def prompt_amount(self, splits) -> int:

        while True:

            os.system('clear')
            self.print_splits(splits)
            input_amount = input('Input amount (ENTER to keep): ')

            try:
                check_bl = splits[self.bl_index].copy()
                check_bl.amount = round(float(input_amount), 2)
                if self.amount_is_valid(check_bl):
                    splits[self.bl_index].amount = round(float(input_amount), 2)
                    return 1
                else:
                    continue
            except ValueError:
                if input_amount == '':
                    return 1
                continue

    def prompt_tag(self, splits) -> int:
        os.system('clear')
        self.print_splits(splits)

        input_tag = input('Input tag: #')

        splits[self.bl_index].tag = input_tag

        return 1

    def prompt_notes(self, splits) -> int:
        os.system('clear')
        self.print_splits(splits)

        input_notes = input('Input notes: ')

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

            if response == 'y':
                self.save(splits)
                return 0
            elif response == 'n':
                print('DONT SAVE')
                return 1


    def print_splits(self, splits):

        print('(' + str(self.statement_index+1) + ',' + str(self.statement_len) + ')')

        if len(splits) == 1:
            print(splits[0])
            return

        for i, b_l in enumerate(splits):
            if i == self.bl_index:
                print('-' + str(b_l))
            else:
                print(' ' + str(b_l))

    def print_categories(self, rows):
        # lines =['','','','']
        lines = [[], [], [], []]
        for r, cat in enumerate(sorted(self.dm.dict_categories.keys())):
            lines[r % rows].append(str(r) + ': ' + cat)

        print()
        for l in lines:
            row = ''
            for c in l:
                row = row + (f'{c:20}\t')
            print(row)

    def amount_is_valid(self, b_l):

        while True:

            os.system('clear')
            response = ''
            if b_l.amount > self.importing_tx['Amount']:
                response = input('Input amount is greater than transaction amount. Continue? y or n? ')
            elif b_l.amount < 0:
                response = input('Input amount is negative. Continue? y or n? ')

            if (response == 'y') or (response == ''):
                return True
            elif response == 'n':
                return False

    def save(self, splits):

        for bl in splits:

            self.dm.write_new_vendor(self.importing_tx['Vendor'], bl)

            self.dm.write_budget_line(bl)
            self.dict_budget_lines = self.dm.get_saved_budget_lines()

            self.saved_transactions.loc[len(self.saved_transactions.index)] = self.importing_tx
            self.dm.write_transactions(self.saved_transactions)



        print('SAVE')
        #change back split to false
        # reset index to 0
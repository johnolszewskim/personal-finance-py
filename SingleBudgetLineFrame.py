import tkinter as tk
from tkinter import ttk
import PersonalFinancePYData as data

class SingleBudgetLineFrame(tk.Frame):

    def __init__(self, master, trans):

        tk.Frame.__init__(self, master)

        self.trans = trans
        self.master = master

        self.vendor_entry = self.createVendorEntry()
        self.vendor_entry[0].insert(0, self.vendor_lookup(trans['Vendor']))

        self.category_combo = self.createCategoryCombo()
        self.subcategory_combo = self.createSubcategoryCombo()
        self.category_combo[0].bind("<<ComboboxSelected>>",
                                    lambda _: self.category_selected(self.category_combo[1].get(), self.subcategory_combo[0]))

        self.amount_entry = self.createAmountEntry()
        self.amount_entry[0].insert(0, str(trans['Amount']))

        self.delete_button = self.createDeleteButton()

    def createVendorEntry(self) -> (tk.Entry, tk.StringVar):
        entered_vendor = tk.StringVar()
        vendor_entry = tk.Entry(self, width=40, textvariable=entered_vendor)
        vendor_entry.grid(row=1, column=0, sticky='w')
        return (vendor_entry, entered_vendor)

    def vendor_lookup(self, vend):
        if vend in data.vendor_lookup:
            return data.vendor_lookup[vend]
        else:
            return vend

    def createCategoryCombo(self) -> (ttk.Combobox, tk.StringVar):
        categories = [key for key in data.category_lookup.keys()]
        selected_category = tk.StringVar()
        category_combobox = ttk.Combobox(self, values=categories, textvariable=selected_category)
        category_combobox.grid(row=1, column=1, sticky='w')
        return (category_combobox, selected_category)


    def createSubcategoryCombo(self) -> (ttk.Combobox, tk.StringVar):
        selected_subcategory = tk.StringVar()
        subcategory_combobox = ttk.Combobox(self, textvariable=selected_subcategory)
        subcategory_combobox.grid(row=1, column=2)
        return (subcategory_combobox, selected_subcategory)


    def category_selected(self, category_str, subcategory_combo):
        subcategory_combo.configure(values=data.category_lookup[category_str])


    def createAmountEntry(self) -> (tk.Entry, tk.StringVar):
        entered_amount = tk.StringVar()
        amount_entry = tk.Entry(self, width=10, textvariable=entered_amount)
        tk.Label(self, text="$").grid(row=1, column=3)
        amount_entry.grid(row=1, column=4)
        return (amount_entry, entered_amount)

    def createDeleteButton(self) -> (tk.Checkbutton):
        delete_button = tk.Button(self, text='-', command=self.delete_button_clicked)
        delete_button.grid(row=1, column=5)
        return delete_button

    def delete_button_clicked(self):
        self.master.remove_budget_line_frame(self)

    def add_and_get_budget_line(self):
        data.add_budget_line(self.trans['Transaction ID'],
                             self.vendor_entry[1].get(),
                             self.category_combo[1].get(),
                             self.subcategory_combo[1].get(),
                             self.amount_entry[1].get())

    def enable_disable(self, state):
        self.vendor_entry[0].configure(state=state)
        self.category_combo[0].configure(state=state)
        self.subcategory_combo[0].configure(state=state)
        self.amount_entry[0].configure(state=state)
        self.delete_button.configure(state=state)

    def save(self):
        data.add_budget_line(trans_ID=self.trans['Transaction ID'],
                             vendor=self.vendor_entry[1].get(),
                             category=self.category_combo[1].get(),
                             subcategory=self.subcategory_combo[1].get(),
                             amount=self.amount_entry[1].get())
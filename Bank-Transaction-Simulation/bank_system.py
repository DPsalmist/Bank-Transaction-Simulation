# from customer_account import CustomerAccount
# from admin import Admin
from tkinter import (Label, Frame, Entry, Tk, Button, ttk,
                     StringVar, font, messagebox, Radiobutton)
from tkinter.filedialog import askopenfilename, asksaveasfilename
from csv import writer


accounts_list = []
admins_list = []

root = Tk


class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        # ====== Fonts and substitutes =============
        primary_font = "Calibri"
        substitute_font = "Times New Roman"
        available_fonts = font.families()
        if primary_font not in available_fonts:
            self.label_font = substitute_font
        else:
            self.label_font = primary_font

        # Tree Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",
                        background='teal', foreground='white')
        # ====== Variables =============
        self.customer_dicts = []
        self.admin_dicts = []
        self.username = StringVar()
        self.password = StringVar()
        self.export_file_name = StringVar()
        self.report_file_name = StringVar()
        self.funds_to_transfer = StringVar()
        self.search_variable = StringVar()
        self.search_criteria = StringVar()
        self.LOGGED_IN_ADMIN = {}
        # ============= INTRO UI =================
        self.intro_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.intro_frame.place(x=0, y=0)
        self.intro_text = Label(self.intro_frame, bg="#1a1a1a", fg="#fff", font=(
            self.label_font, 48), text='Python\n Banking System', justify='center')
        self.intro_text.place(relx=0.5, rely=0.45, anchor='center')
        Button(self.intro_frame, text="Start", font=(self.label_font, 16), width=30,
               command=self.show_login_page, bg='teal', fg="#fff", bd=0).place(relx=0.5, rely=0.64, anchor='center')

        self.load_bank_data()

    def show_login_page(self):
        """ Shows the login page """

        self.intro_frame.place_forget()
        # ============= LOGIN UI =================
        self.login_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.login_frame.place(x=0, y=0)
        self.login_inner_frame = Frame(
            self.login_frame, width=450, height=350, bg='#1a1a1a', bd=3, relief='groove')
        self.login_inner_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.login_text = Label(self.login_inner_frame, bg="#1a1a1a", fg="#fff", font=(
            self.label_font, 36), text='Admin Login', justify='center')
        self.login_text.place(relx=0.5, rely=0.13, anchor='center')
        Label(self.login_inner_frame, text='Username', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.15, rely=0.3, anchor='w')
        self.username_entry = Entry(self.login_inner_frame, textvariable=self.username, font=(self.label_font, 18), bg='#dadada',
                                    width=25, fg='#1a1a1a')
        self.username_entry.place(relx=0.15, rely=0.41, anchor='w')
        Label(self.login_inner_frame, text='Password', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.15, rely=0.55, anchor='w')
        self.password_entry = Entry(self.login_inner_frame, textvariable=self.password, font=(self.label_font, 18), show='*', bg='#dadada',
                                    width=25, fg='#1a1a1a')
        self.password_entry.place(relx=0.15, rely=0.66, anchor='w')
        self.password_entry.bind(
            '<Return>', lambda dummy=0: self.login_the_admin())
        Button(self.login_inner_frame, text="Log in", font=(self.label_font, 16), width=20,
               command=self.login_the_admin, bg='teal', fg="#fff", bd=0).place(relx=0.5, rely=0.85, anchor='center')

    def show_admin_dashboard(self):
        """ Shows the admin dashboard """

        # ============= DASHBOARD UI =================
        self.dashboard_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.dashboard_frame.place(x=0, y=0)
        Label(self.dashboard_frame, text=10*" " + "Admin Dashboard" + 10*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.25, anchor='center')

        self.utilities_frame = Frame(
            self.dashboard_frame, width=800, height=300, bg="#1a1a1a", bd=3, relief='groove')
        self.utilities_frame.place(relx=0.5, rely=0.57, anchor='center')
        Button(self.utilities_frame, text="Search\ncustomer", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_search_customer_frame).place(relx=0.2, rely=0.23, anchor='center')
        Button(self.utilities_frame, text="Update\nadmin details", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_update_admin_frame).place(relx=0.5, rely=0.23, anchor='center')
        Button(self.utilities_frame, text="Show all\ncustomers", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_all_customer_frame).place(relx=0.8, rely=0.23, anchor='center')
        Button(self.utilities_frame, text="Import\ncustomer data", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_import_data_frame).place(relx=0.2, rely=0.54, anchor='center')
        Button(self.utilities_frame, text="Export\ncustomer data", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_export_data_frame).place(relx=0.5, rely=0.54, anchor='center')
        Button(self.utilities_frame, text="Request\nmanagement report", width=20, bd=0, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_request_report_frame).place(relx=0.8, rely=0.54, anchor='center')
        Button(self.utilities_frame, text="Transfer funds", width=20, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.show_transfer_funds_frame).place(relx=0.35, rely=0.8, anchor='center')
        Button(self.utilities_frame, text="Logout", width=20, bg='teal', fg="#fff", font=(
            self.label_font, 16), command=self.logout_admin).place(relx=0.65, rely=0.8, anchor='center')

    def show_search_customer_frame(self):
        """ Shows search form, parameters and results """

        self.search_customer_frame = Frame(
            width=1300, height=700, bg='#1a1a1a')
        self.search_customer_frame.place(x=0, y=0)
        Button(self.search_customer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.search_customer_frame, text=5*" " + "Search customer" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.15, anchor='center')

        self.search_entry = Entry(
            self.search_customer_frame, textvariable=self.search_variable, font=(self.label_font, 18), bg='#dadada', width=30, fg='#1a1a1a')
        self.search_entry.place(relx=0.1, rely=0.35, anchor='w')
        self.name_checkbtn = Radiobutton(self.search_customer_frame, text='Name (First or Last)', font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a', activebackground='#1a1a1a', variable=self.search_criteria, value="name")
        self.name_checkbtn.place(relx=0.1, rely=0.45, anchor='w')
        self.address_checkbtn = Radiobutton(self.search_customer_frame, text='Address', font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a', activebackground='#1a1a1a', variable=self.search_criteria, value="address")
        self.address_checkbtn.place(relx=0.1, rely=0.55, anchor='w')
        self.balance_checkbtn = Radiobutton(self.search_customer_frame, text='Balance', font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a', activebackground='#1a1a1a', variable=self.search_criteria, value="balance")
        self.balance_checkbtn.place(relx=0.25, rely=0.55, anchor='w')
        self.account_no_checkbtn = Radiobutton(self.search_customer_frame, text='Account No.', font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a', activebackground='#1a1a1a', variable=self.search_criteria, value="account_no")
        self.account_no_checkbtn.place(relx=0.1, rely=0.65, anchor='w')
        self.account_type_checkbtn = Radiobutton(self.search_customer_frame, text='Account Type', font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a', activebackground='#1a1a1a', variable=self.search_criteria, value="account_type")
        self.account_type_checkbtn.place(relx=0.25, rely=0.65, anchor='w')
        Button(self.search_customer_frame, text="Search", font=(self.label_font, 16), width=30,
               bg='teal', fg="#fff", command=self.search_for_customer).place(relx=0.1, rely=0.75, anchor='w')

        self.search_customer_tree_frame = Frame(
            self.search_customer_frame, width=640, height=410, bg="#1a1a1a", bd=3, relief='groove')
        self.search_customer_tree_frame.place(
            relx=0.68, rely=0.55, anchor='center')
        tree_columns = "full_name", "account_no", "balance"
        self.search_customer_tree = ttk.Treeview(
            self.search_customer_tree_frame, columns=tree_columns, show='headings', height=18, selectmode='browse')
        # centralize all columns
        for i in tree_columns:
            self.search_customer_tree.column(i, anchor='center')
        self.search_customer_tree.place(relx=0.49, rely=0.5, anchor='center')

        # add a scrollbar to the tree
        y_scrollbar = ttk.Scrollbar(
            self.search_customer_tree_frame, orient='vertical', command=self.search_customer_tree.yview)
        self.search_customer_tree.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.place(relx=0.995, rely=0.5, anchor='e', height=390)

        # Tree headings
        self.search_customer_tree.heading(
            "full_name", text="Fullname", anchor='center')
        self.search_customer_tree.heading(
            "account_no", text="Account No.", anchor='center')
        self.search_customer_tree.heading(
            "balance", text="Balance", anchor='center')

        Button(self.search_customer_frame, text="View Customer", font=(self.label_font, 16), width=15,
               command=lambda: self.view_customer("search_tree"), bg='teal', fg="#fff").place(relx=0.52, rely=0.9, anchor='center')
        Button(self.search_customer_frame, text="Edit Customer", font=(self.label_font, 16), width=15,
               command=lambda: self.update_customer("search_tree"), bg='teal', fg="#fff").place(relx=0.68, rely=0.9, anchor='center')
        Button(self.search_customer_frame, text="Close Account", font=(self.label_font, 16), width=15,
               command=lambda: self.close_account("search_tree"), bg='teal', fg="#fff").place(relx=0.84, rely=0.9, anchor='center')

    def show_update_admin_frame(self):
        """ Shows the update admin section """

        admin_details = self.LOGGED_IN_ADMIN
        self.update_admin_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.update_admin_frame.place(x=0, y=0)
        Button(self.update_admin_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.update_admin_frame, text=5*" " + "Update admin details" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.33, anchor='center')

        self.admin_edit_frame = Frame(
            self.update_admin_frame, width=600, height=270, bg="#1a1a1a", bd=3, relief='groove')
        self.admin_edit_frame.place(relx=0.5, rely=0.6, anchor='center')

        Label(self.admin_edit_frame, text='First name', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.1, rely=0.12, anchor='w')
        self.admin_first_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.admin_first_name.insert(0, admin_details["fname"])
        self.admin_first_name.place(relx=0.1, rely=0.27, anchor='w')
        # customer last name
        Label(self.admin_edit_frame, text='Last name', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.55, rely=0.12, anchor='w')
        self.admin_last_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.admin_last_name.insert(0, admin_details["lname"])
        self.admin_last_name.place(relx=0.55, rely=0.27, anchor='w')
        # customer user name
        Label(self.admin_edit_frame, text='Username', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.1, rely=0.45, anchor='w')
        self.admin_user_name = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.admin_user_name.insert(0, admin_details["user_name"])
        self.admin_user_name.place(relx=0.1, rely=0.6, anchor='w')
        # customer address
        Label(self.admin_edit_frame, text='Address', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.55, rely=0.45, anchor='w')
        self.admin_address = Entry(
            self.admin_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.admin_address.insert(0, admin_details["address"])
        self.admin_address.place(relx=0.55, rely=0.6, anchor='w')

        Button(self.admin_edit_frame, text="Update details", font=(self.label_font, 16), width=35,
               command=self.update_admin_details, bg='teal', fg="#fff").place(relx=0.5, rely=0.85, anchor='center')

    def show_all_customer_frame(self):
        """ Shows all the customers in the bank """

        self.all_custumer_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.all_custumer_frame.place(x=0, y=0)
        Button(self.all_custumer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.all_custumer_frame, text=5*" " + "All Customers" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.17, anchor='center')

        self.customers_tree_frame = Frame(
            self.all_custumer_frame, width=850, height=410, bg="#1a1a1a", bd=3, relief='groove')
        self.customers_tree_frame.place(relx=0.5, rely=0.54, anchor='center')
        tree_columns = "first_name", "last_name", "account_no", "balance"
        self.all_customer_tree = ttk.Treeview(
            self.customers_tree_frame, columns=tree_columns, show='headings', height=18, selectmode='browse')
        # centralize all columns
        for i in tree_columns:
            self.all_customer_tree.column(i, anchor='center')
        self.all_customer_tree.place(relx=0.49, rely=0.5, anchor='center')

        # add a scrollbar to the tree
        y_scrollbar = ttk.Scrollbar(
            self.customers_tree_frame, orient='vertical', command=self.all_customer_tree.yview)
        self.all_customer_tree.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.place(relx=0.995, rely=0.5, anchor='e', height=390)
        self.load_all_customer_tree()

        Button(self.all_custumer_frame, text="View Customer", font=(self.label_font, 16), width=20,
               command=lambda: self.view_customer("all_customer"), bg='teal', fg="#fff").place(relx=0.3, rely=0.9, anchor='center')
        Button(self.all_custumer_frame, text="Edit Customer", font=(self.label_font, 16), width=20,
               command=lambda: self.update_customer("all_customer"), bg='teal', fg="#fff").place(relx=0.5, rely=0.9, anchor='center')
        Button(self.all_custumer_frame, text="Close Account", font=(self.label_font, 16), width=20,
               command=lambda: self.close_account("all_customer"), bg='teal', fg="#fff").place(relx=0.7, rely=0.9, anchor='center')

    def show_import_data_frame(self):
        """ Shows the import data section """

        self.import_data_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.import_data_frame.place(x=0, y=0)
        Button(self.import_data_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.import_data_frame, text=5*" " + "Import customer data" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.37, anchor='center')

        Button(self.import_data_frame, text="Click here to select .csv file...", font=(self.label_font, 16), bg="#1a1a1a", fg="#fff",
               width=30, relief="groove", command=self.show_import_dialog).place(relx=0.5, rely=0.5, anchor='center')
        self._file = ""
        self.file_selected = Label(
            text="", bg="#1a1a1a", fg='#fff', font=(self.label_font, 16))
        self.file_selected.place(relx=0.5, rely=0.58, anchor='center')
        Button(self.import_data_frame, text="Load Customer Data", font=(self.label_font, 16), width=20,
               command=self.import_data, bg='teal', fg="#fff").place(relx=0.5, rely=0.66, anchor='center')

    def show_export_data_frame(self):
        """ Shows the export data section """

        self.export_data_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.export_data_frame.place(x=0, y=0)
        Button(self.export_data_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.export_data_frame, text=5*" " + "Export customer data" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.38, anchor='center')

        Button(self.export_data_frame, text="Click here to select save location", font=(self.label_font, 16), bg="#1a1a1a", fg="#fff",
               width=30, relief="groove", command=self.show_export_dialog).place(relx=0.5, rely=0.5, anchor='center')
        self._export_location = ""

        self.export_location_selected = Label(
            self.export_data_frame, text="", bg="#1a1a1a", fg='#fff', font=(self.label_font, 16))
        self.export_location_selected.place(
            relx=0.5, rely=0.58, anchor='center')

        Button(self.export_data_frame, text="Export Customer Data", font=(self.label_font, 16), width=20,
               command=self.export_data, bg='teal', fg="#fff").place(relx=0.5, rely=0.66, anchor='center')

    def show_request_report_frame(self):
        """ Shows the request management report section """

        self.request_report_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.request_report_frame.place(x=0, y=0)
        Button(self.request_report_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.request_report_frame, text=5*" " + "Request management report" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.38, anchor='center')

        Button(self.request_report_frame, text="Click here to select save location", font=(self.label_font, 16), bg="#1a1a1a", fg="#fff",
               width=30, relief="groove", command=self.show_report_dialog).place(relx=0.5, rely=0.5, anchor='center')
        self._report_save_location = ""

        self.save_location_selected = Label(
            self.request_report_frame, text="", bg="#1a1a1a", fg='#fff', font=(self.label_font, 16))
        self.save_location_selected.place(relx=0.5, rely=0.58, anchor='center')

        Button(self.request_report_frame, text="Export Management Report", font=(self.label_font, 16), width=25,
               command=self.export_report_data, bg='teal', fg="#fff").place(relx=0.5, rely=0.66, anchor='center')

    def show_transfer_funds_frame(self):
        """ Shows the transfer funds section """

        self.transfer_funds_frame = Frame(width=1300, height=700, bg='#1a1a1a')
        self.transfer_funds_frame.place(x=0, y=0)

        Button(self.transfer_funds_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
               width=3, command=self.show_admin_dashboard).place(x=60, y=30)
        Label(self.transfer_funds_frame, text=5*" " + "Transfer funds" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.36, anchor='center')

        self.transfer_inner_frame = Frame(
            self.transfer_funds_frame, width=600, height=200, bg='#1a1a1a', bd=3, relief="groove")
        self.transfer_inner_frame.place(relx=0.5, rely=0.58, anchor='center')

        self.customer_list = [i['fname'] + " " + i['lname']
                              for i in self.customer_dicts]
        self.customer_from = ttk.Combobox(self.transfer_inner_frame, font=(
            self.label_font, 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_from.current(0)
        self.customer_from.place(relx=0.25, rely=0.2, anchor='center')

        Label(self.transfer_inner_frame, text=' to ', font=(self.label_font, 16),
              fg='#fff', bg='teal').place(relx=0.5, rely=0.2, anchor='center')

        self.customer_to = ttk.Combobox(self.transfer_inner_frame, font=(
            self.label_font, 18), values=['----'*8]+self.customer_list, state='readonly', width=15)
        self.customer_to.current(0)
        self.customer_to.place(relx=0.75, rely=0.2, anchor='center')

        self.fund_entry = Entry(self.transfer_inner_frame, textvariable=self.funds_to_transfer, font=(
            self.label_font, 24), bg='#dadada', width=7, justify='center', fg='#1a1a1a')
        self.fund_entry.place(relx=0.5, rely=0.48, anchor='center')

        Button(self.transfer_inner_frame, text="Tranfer funds", font=(self.label_font, 16), width=20,
               command=self.transfer_funds, bg='teal', fg="#fff").place(relx=0.5, rely=0.78, anchor='center')

    def show_single_customer_frame(self, values):
        """ Shows single customer section """

        customer_details = [
            i for i in self.customer_dicts if i['account_no'] == str(values[2])][0]
        the_full_name = customer_details["fname"] + \
            " " + customer_details["lname"]
        self.single_customer_frame = Frame(
            width=1300, height=700, bg='#1a1a1a')
        self.single_customer_frame.place(x=0, y=0)
        if values[-1] == "all_customer":
            Button(self.single_customer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
                   width=3, command=self.show_all_customer_frame).place(x=60, y=30)
        else:
            Button(self.single_customer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
                   width=3, command=self.show_search_customer_frame).place(x=60, y=30)
        Label(self.single_customer_frame, text=5*" " + "Single Customer Details" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.3, anchor='center')

        self.details_frame = Frame(
            self.single_customer_frame, width=750, height=250, bg="#1a1a1a", bd=3, relief='groove')
        self.details_frame.place(relx=0.5, rely=0.57, anchor='center')

        # customer name
        Label(self.details_frame, text="Name:", font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a').place(relx=0.1, rely=0.15, anchor='w')
        full_name = Label(self.details_frame, text=the_full_name, font=(
            self.label_font, 18), fg='#fff', bg='#1a1a1a')
        full_name.place(relx=0.2, rely=0.15, anchor='w')
        # customer account number
        Label(self.details_frame, text="Account No.:", font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a').place(relx=0.1, rely=0.33, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["account_no"], font=(
            self.label_font, 18), fg='#fff', bg='#1a1a1a')
        full_name.place(relx=0.28, rely=0.33, anchor='w')
        # customer account type
        Label(self.details_frame, text="Account Type:", font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a').place(relx=0.1, rely=0.49, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["account_type"], font=(
            self.label_font, 18), fg='#fff', bg='#1a1a1a')
        full_name.place(relx=0.3, rely=0.49, anchor='w')
        # customer balance
        Label(self.details_frame, text="Account Balance:", font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a').place(relx=0.1, rely=0.67, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["balance"], font=(
            self.label_font, 18), fg='#fff', bg='#1a1a1a')
        full_name.place(relx=0.34, rely=0.67, anchor='w')
        # customer address
        Label(self.details_frame, text="Address:", font=(
            self.label_font, 18), fg='#f2aa4c', bg='#1a1a1a').place(relx=0.1, rely=0.85, anchor='w')
        full_name = Label(self.details_frame, text=customer_details["address"], font=(
            self.label_font, 18), fg='#fff', bg='#1a1a1a')
        full_name.place(relx=0.225, rely=0.85, anchor='w')

    def show_update_customer_frame(self, values):
        """ Shows update customer section """

        customer_details = [
            i for i in self.customer_dicts if i['account_no'] == str(values[2])][0]
        the_account_type = customer_details["account_type"]
        self.update_customer_frame = Frame(
            width=1300, height=700, bg='#1a1a1a')
        self.update_customer_frame.place(x=0, y=0)
        if values[-1] == "all_customer":
            Button(self.update_customer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
                   width=3, command=self.show_all_customer_frame).place(x=60, y=30)
        else:
            Button(self.update_customer_frame, text='⬅', font=(self.label_font, 16), fg='#fff', bg='teal',
                   width=3, command=self.show_search_customer_frame).place(x=60, y=30)
        Label(self.update_customer_frame, text=5*" " + "Update customer details" + 5*" ", fg='#fff', bg="#1a1a1a", relief='groove',
              font=(self.label_font, 36)).place(relx=0.5, rely=0.28, anchor='center')

        self.customer_edit_frame = Frame(
            self.update_customer_frame, width=750, height=350, bg="#1a1a1a", bd=3, relief='groove')
        self.customer_edit_frame.place(relx=0.5, rely=0.6, anchor='center')

        # customer first name
        Label(self.customer_edit_frame, text='First name', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.1, rely=0.08, anchor='w')
        self.customer_first_name = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.customer_first_name.insert(0, customer_details["fname"])
        self.customer_first_name.place(relx=0.1, rely=0.19, anchor='w')
        # customer last name
        Label(self.customer_edit_frame, text='Last name', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.55, rely=0.08, anchor='w')
        self.customer_last_name = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.customer_last_name.insert(0, customer_details["lname"])
        self.customer_last_name.place(relx=0.55, rely=0.19, anchor='w')
        # customer account number
        Label(self.customer_edit_frame, text='Account number', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.1, rely=0.32, anchor='w')
        self.customer_account_no = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.customer_account_no.insert(0, customer_details["account_no"])
        self.customer_account_no.place(relx=0.1, rely=0.44, anchor='w')
        # customer account type
        Label(self.customer_edit_frame, text='Account type', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.55, rely=0.32, anchor='w')
        account_types = ["Savings", "Current"]
        self.customer_account_type = ttk.Combobox(self.customer_edit_frame, font=(
            self.label_font, 18), values=['----'*8]+account_types, state='readonly', width=18)
        self.customer_account_type.current(
            account_types.index(the_account_type)+1)
        self.customer_account_type.place(relx=0.55, rely=0.44, anchor='w')
        # customer account balance
        Label(self.customer_edit_frame, text='Account balance', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.1, rely=0.58, anchor='w')
        self.customer_account_balance = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.customer_account_balance.insert(0, customer_details["balance"])
        self.customer_account_balance.place(relx=0.1, rely=0.7, anchor='w')
        # customer address
        Label(self.customer_edit_frame, text='Address', font=(self.label_font, 18), bg='#1a1a1a',
              fg='#fff').place(relx=0.55, rely=0.58, anchor='w')
        self.customer_account_address = Entry(
            self.customer_edit_frame, bg='#dadada', fg='#222', font=(self.label_font, 18), width=19)
        self.customer_account_address.insert(0, customer_details["address"])
        self.customer_account_address.place(relx=0.55, rely=0.7, anchor='w')

        Button(self.customer_edit_frame, text="Update customer details", font=(self.label_font, 16), width=35,
               command=lambda: self.save_customer_update(values[2], values[-1]), bg='teal', fg="#fff").place(relx=0.5, rely=0.88, anchor='center')

    def update_admin_details(self):
        admin_first_name = self.admin_first_name.get()
        admin_last_name = self.admin_last_name.get()
        admin_user_name = self.admin_user_name.get()
        admin_address = self.admin_address.get()
        self.LOGGED_IN_ADMIN['fname'] = admin_first_name
        self.LOGGED_IN_ADMIN['lname'] = admin_last_name
        self.LOGGED_IN_ADMIN['user_name'] = admin_user_name
        self.LOGGED_IN_ADMIN['address'] = admin_address

        messagebox.showinfo("Update Status", "Update was successful!")
        self.update_admin_frame.place_forget()
        self.show_admin_dashboard()

    def save_customer_update(self, account, path):
        customer_first_name_entry = self.customer_first_name.get()
        customer_last_name_entry = self.customer_last_name.get()
        customer_account_no_entry = self.customer_account_no.get()
        customer_account_type_entry = self.customer_account_type.get()
        customer_account_balance_entry = self.customer_account_balance.get()
        customer_account_address_entry = self.customer_account_address.get()

        # update the customer here
        get_customer = [
            i for i in self.customer_dicts if i['account_no'] == str(account)][0]
        get_customer["fname"] = customer_first_name_entry
        get_customer["lname"] = customer_last_name_entry
        get_customer["account_no"] = customer_account_no_entry
        get_customer["account_type"] = customer_account_type_entry
        get_customer["balance"] = customer_account_balance_entry
        get_customer["address"] = customer_account_address_entry

        messagebox.showinfo("Update Status", "Customer update is successful!")
        # redirect to previous section
        if path == "all_customer":
            self.show_all_customer_frame()
        else:
            self.show_search_customer_frame()

    def search_for_customer(self):
        search_entry = self.search_variable.get()
        search_criteria = self.search_criteria.get()

        if search_entry:
            if not search_criteria:
                messagebox.showerror(
                    "Search Status", "Please select a search criteria!")
            else:
                query = search_entry.casefold()
                if search_criteria == "name":
                    results = [i for i in self.customer_dicts if query in i["fname"].casefold(
                    ) or query in i["lname"].casefold()]
                elif search_criteria == "address":
                    results = [
                        i for i in self.customer_dicts if query in i["address"].casefold()]
                elif search_criteria == "balance":
                    results = [
                        i for i in self.customer_dicts if query in i["balance"].casefold()]
                elif search_criteria == "account_no":
                    results = [
                        i for i in self.customer_dicts if query in i["account_no"].casefold()]
                elif search_criteria == "account_type":
                    results = [
                        i for i in self.customer_dicts if query in i["account_type"].casefold()]

                # if there are results, show them on the tree
                if results:
                    self.load_search_customer_tree(results)

    def load_search_customer_tree(self, results):
        self.show_search_customer_frame()

        for customer in results:
            full_name = customer["fname"] + " " + customer["lname"]
            details = (full_name, customer["account_no"], customer["balance"])
            self.search_customer_tree.insert("", 'end', values=details)

    def load_all_customer_tree(self):
        # Add the tree headings
        self.all_customer_tree.heading(
            "first_name", text="First Name", anchor='center')
        self.all_customer_tree.heading(
            "last_name", text="Last Name", anchor='center')
        self.all_customer_tree.heading(
            "account_no", text="Account No.", anchor='center')
        self.all_customer_tree.heading(
            "balance", text="Balance", anchor='center')

        for customer in self.customer_dicts:
            details = (customer["fname"], customer["lname"],
                       customer["account_no"], customer["balance"])
            self.all_customer_tree.insert("", 'end', values=details)

    def view_customer(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        if the_values:
            self.show_single_customer_frame(the_values+[tree_type])

    def update_customer(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        if the_values:
            self.show_update_customer_frame(the_values+[tree_type])

    def close_account(self, tree_type):
        if tree_type == "all_customer":
            cur_item = self.all_customer_tree.focus()
            the_values = self.all_customer_tree.item(cur_item)['values']
        else:
            cur_item = self.search_customer_tree.focus()
            the_values = self.search_customer_tree.item(cur_item)['values']
            the_values = the_values[0].split(' ') + the_values[1:]

        # Do the removing from db
        account_number = the_values[2]
        for index, value in enumerate(self.customer_dicts):
            if value['account_no'] == account_number:
                break

        del self.customer_dicts[index]
        messagebox.showinfo("Account Removal",
                            "Account was removed successfully!")
        if tree_type == "all_customer":
            self.show_all_customer_frame()
        else:
            self.show_search_customer_frame()

    def show_import_dialog(self):
        self._file = askopenfilename(defaultextension='.csv', filetypes=[
                                     ('XLS Worksheet', '*.csv')])
        self.file_selected.config(text=self._file)

    def show_export_dialog(self):
        self._export_location = asksaveasfilename(defaultextension='.csv', filetypes=[
            ('XLS Worksheet', '*.csv')])
        self.export_location_selected.config(text=self._export_location)

    def show_report_dialog(self):
        self._report_save_location = asksaveasfilename(
            defaultextension='.txt', filetypes=[('Text Document', '*.txt')])
        self.save_location_selected.config(text=self._report_save_location)

    def import_data(self):
        if self._file == "":
            messagebox.showerror("Load Status", "No data to import!")
        else:
            self.admin_dicts = []
            self.customer_dicts = []

            with open(self._file, "r") as fp:
                file_content = fp.readlines()

            for line in file_content[1:]:
                splitted = line.strip().split('"')
                address = splitted[1]
                if splitted[-1] != ',,,,':  # admin user
                    _dict = {}
                    names = splitted[0].split(',')
                    other_info = splitted[2].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = ""
                    _dict["account_type"] = ""
                    _dict["balance"] = ""
                    _dict["address"] = address
                    _dict["is_admin"] = "1"
                    _dict["user_name"] = other_info[2]
                    _dict["password"] = other_info[3]
                    _dict["full_admin_rights"] = other_info[4]
                    self.admin_dicts.append(_dict)
                else:  # customers
                    _dict = {}
                    names = splitted[0].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = names[2]
                    _dict["account_type"] = names[3]
                    _dict["balance"] = names[4]
                    _dict["address"] = address
                    _dict["is_admin"] = ""
                    _dict["user_name"] = ""
                    _dict["password"] = ""
                    _dict["full_admin_rights"] = ""
                    self.customer_dicts.append(_dict)

            messagebox.showinfo(
                "Load Status", "Customer data import was successful!")
            self.import_data_frame.place_forget()
            self.show_admin_dashboard()

    def export_data(self):
        if self._export_location == "":
            messagebox.showerror(
                "Export Status", "Save location and filename has to be provided!")
        else:
            # Do the export here...
            header = ["First Name", "Last Name", "Account No.", "Account Type", "Balance",
                      "Address", "Is_Admin", "Username", "Password", "Full_Admin_Rights"]
            customer_data = [[i["fname"], i["lname"], i["account_no"], i["account_type"], i["balance"], i["address"],
                              i["is_admin"], i["user_name"], i["password"], i["full_admin_rights"]] for i in self.customer_dicts]
            admin_data = [[i["fname"], i["lname"], i["account_no"], i["account_type"], i["balance"], i["address"],
                           i["is_admin"], i["user_name"], i["password"], i["full_admin_rights"]] for i in self.admin_dicts]
            with open(self._export_location, 'w', encoding='UTF8', newline="") as fp:
                data_writer = writer(fp)
                data_writer.writerow(header)
                data_writer.writerows(customer_data)
                data_writer.writerows(admin_data)
            # show messagebox for success
            messagebox.showinfo("Export Status", "Export was successful!")
            self.export_file_name.set("")
            self.export_data_frame.place_forget()
            self.show_admin_dashboard()

    def export_report_data(self):
        if self._report_save_location == "":
            messagebox.showerror(
                "Export Status", "Save location and filename has to be provided!")
        else:
            # Do the export here...
            total_sum = sum([int(i["balance"]) for i in self.customer_dicts])
            with open(self._report_save_location, 'w') as fp:
                fp.write(
                    f"Total number of customers: {len(self.customer_dicts)}\n")
                fp.write(
                    f"Sum of all the money all accounts have: {total_sum}\n")
                fp.write("Sum of interest payable for one year: 48%\n")
                fp.write("Total amount of overdrafts : 2340")

            # show messagebox for success
            messagebox.showinfo("Export Status", "Export was successful!")
            self.report_file_name.set("")
            self.request_report_frame.place_forget()
            self.show_admin_dashboard()

    def transfer_funds(self):
        fund_entry = self.fund_entry.get()
        customer_from = self.customer_from.get()
        customer_to = self.customer_to.get()
        try:
            fund_entry = int(fund_entry)
            if customer_from not in self.customer_list or customer_to not in self.customer_list or customer_to == customer_from:
                messagebox.showerror("Fund Transfer Status",
                                     "Please select two different valid customers!")
            else:
                cus_from_first_name, cus_from_last_name = customer_from.split(
                    " ")
                cus_to_first_name, cus_to_last_name = customer_to.split(" ")
                cus_from = [i for i in self.customer_dicts if i['fname'] ==
                            cus_from_first_name and i['lname'] == cus_from_last_name][0]
                cus_to = [i for i in self.customer_dicts if i['fname'] ==
                          cus_to_first_name and i['lname'] == cus_to_last_name][0]
                cus_from['balance'] = str(
                    int(cus_from['balance']) - fund_entry)
                cus_to['balance'] = str(fund_entry + int(cus_to['balance']))
                messagebox.showinfo("Fund Transfer Status",
                                    "Transfer of funds is successful!")
                self.transfer_funds_frame.place_forget()
                self.funds_to_transfer.set("")
                self.show_admin_dashboard()
        except ValueError:
            messagebox.showerror("Fund Transfer Status",
                                 "Please enter a number!")

    def login_the_admin(self):
        """ Check the credentials provided and login the admin """

        username, password = self.username.get(), self.password.get()
        admin_usernames = [i['user_name'] for i in self.admin_dicts]

        if username and password:
            if username in admin_usernames:
                the_admin_logged = [
                    i for i in self.admin_dicts if i["user_name"] == username][0]
                the_password = [i["password"]
                                for i in self.admin_dicts if i["user_name"] == username][0]
                if password == the_password:
                    self.login_frame.place_forget()
                    self.username.set("")
                    self.password.set("")
                    self.show_admin_dashboard()
                    self.LOGGED_IN_ADMIN = the_admin_logged
                else:
                    messagebox.showinfo(
                        "Login Failed", "Username or password is incorrect")
            else:
                messagebox.showinfo(
                    "Login Failed", "Username or password is incorrect")
                self.username_entry.focus()

    def logout_admin(self):
        self.dashboard_frame.place_forget()
        self.show_login_page()
        self.username_entry.focus()

    # FUNCTIONS THAT CAME WITH THE FILE ARE BELOW
    def load_bank_data(self):
        global accounts_list, admins_list

        with open('bank-store.csv', "r") as fp:
            file_content = fp.readlines()

            for line in file_content[1:]:
                splitted = line.strip().split('"')
                address = splitted[1]
                if splitted[-1] != ',,,,':  # admin user
                    _dict = {}
                    names = splitted[0].split(',')
                    other_info = splitted[2].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = ""
                    _dict["account_type"] = ""
                    _dict["balance"] = ""
                    _dict["address"] = address
                    _dict["is_admin"] = "1"
                    _dict["user_name"] = other_info[2]
                    _dict["password"] = other_info[3]
                    _dict["full_admin_rights"] = other_info[4]
                    self.admin_dicts.append(_dict)
                    admins_list.append(_dict)
                else:  # customers
                    _dict = {}
                    names = splitted[0].split(',')
                    _dict["fname"] = names[0]
                    _dict["lname"] = names[1]
                    _dict["account_no"] = names[2]
                    _dict["account_type"] = names[3]
                    _dict["balance"] = names[4]
                    _dict["address"] = address
                    _dict["is_admin"] = ""
                    _dict["user_name"] = ""
                    _dict["password"] = ""
                    _dict["full_admin_rights"] = ""
                    self.customer_dicts.append(_dict)
                    accounts_list.append(_dict)

        # # create customers
        # account_no = 1234
        # customer_1 = CustomerAccount(
        #     "Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], account_no, 5000.00)
        # self.accounts_list.append(customer_1)

        # account_no += 1
        # customer_2 = CustomerAccount("David", "White", [
        #                              "60", "Holborn Viaduct", "London", "EC1A 2FD"], account_no, 3200.00)
        # self.accounts_list.append(customer_2)

        # account_no += 1
        # customer_3 = CustomerAccount("Alice", "Churchil", [
        #                              "5", "Cardigan Street", "Birmingham", "B4 7BD"], account_no, 18000.00)
        # self.accounts_list.append(customer_3)

        # account_no += 1
        # customer_4 = CustomerAccount("Ali", "Abdallah", [
        #                              "44", "Churchill Way West", "Basingstoke", "RG21 6YR"], account_no, 40.00)
        # self.accounts_list.append(customer_4)

        # # create admins
        # admin_1 = Admin("Julian", "Padget", [
        #                 "12", "London Road", "Birmingham", "B95 7TT"], "id1188", "1441", True)
        # self.admins_list.append(admin_1)

        # admin_2 = Admin("Cathy",  "Newman", [
        #                 "47", "Mars Street", "Newcastle", "NE12 6TZ"], "id3313", "2442", False)
        # self.admins_list.append(admin_2)

    # def search_admins_by_name(self, admin_username):
    #     # STEP A.2
    #     pass

    # def search_customers_by_name(self, customer_lname):
    #     # STEP A.3
    #     pass

    # def main_menu(self):
    #     # print the options you have
    #     print()
    #     print()
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("Welcome to the Python Bank System")
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("1) Admin login")
    #     print("2) Quit Python Bank System")
    #     print(" ")
    #     option = int(input("Choose your option: "))
    #     return option

    # def run_main_options(self):
    #     loop = 1
    #     while loop == 1:
    #         choice = self.main_menu()
    #         if choice == 1:
    #             username = input("\n Please input admin username: ")
    #             password = input("\n Please input admin password: ")
    #             msg, admin_obj = self.admin_login(username, password)
    #             print(msg)
    #             if admin_obj != None:
    #                 self.run_admin_options(admin_obj)
    #         elif choice == 2:
    #             loop = 0
    #     print("\n Thank-You for stopping by the bank!")

    # def transferMoney(self, sender_lname, receiver_lname, receiver_account_no, amount):
    #     # ToDo
    #     pass

    # def admin_login(self, username, password):
    #     # STEP A.1
    #     pass

    # def admin_menu(self, admin_obj):
    #     # print the options you have
    #     print(" ")
    #     print("Welcome Admin %s %s : Avilable options are:" %
    #           (admin_obj.get_first_name(), admin_obj.get_last_name()))
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print("1) Transfer money")
    #     print("2) Customer account operations & profile settings")
    #     print("3) Delete customer")
    #     print("4) Print all customers detail")
    #     print("5) Sign out")
    #     print(" ")
    #     option = int(input("Choose your option: "))
    #     return option

    # def run_admin_options(self, admin_obj):
    #     loop = 1
    #     while loop == 1:
    #         choice = self.admin_menu(admin_obj)
    #         if choice == 1:
    #             sender_lname = input("\n Please input sender surname: ")
    #             amount = float(
    #                 input("\n Please input the amount to be transferred: "))
    #             receiver_lname = input("\n Please input receiver surname: ")
    #             receiver_account_no = input(
    #                 "\n Please input receiver account number: ")
    #             self.transferMoney(sender_lname, receiver_lname,
    #                                receiver_account_no, amount)
    #         elif choice == 2:
    #             # STEP A.4
    #             pass

    #         elif choice == 3:
    #             # Todo
    #             pass

    #         elif choice == 4:
    #             # Todo
    #             pass

    #         elif choice == 5:
    #             loop = 0
    #     print("\n Exit account operations")

    # def print_all_accounts_details(self):
    #     # list related operation - move to main.py
    #     i = 0
    #     for c in self.accounts_list:
    #         i += 1
    #         print('\n %d. ' % i, end=' ')
    #         c.print_details()
    #         print("------------------------")


if __name__ == '__main__':
    root = Tk()
    root.title("Python Banking System")
    root.geometry("1300x700+33+20")
    root.resizable(0, 0)
    app = BankSystem()
    # app.run_main_options()
    root.mainloop()

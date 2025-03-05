# Bank-Transaction-Simulation

Bank Transaction Simulation (Tkinter)

*Project Overview:*

The Bank Transaction Simulation is a Python-based GUI application built using Tkinter. It simulates basic banking operations such as deposits, withdrawals, balance checks, and customer account management. This project was initially developed for a student client but has been refined to enrich its functionality and serve as a portfolio project.

*Objectives:*

- Simulate real-world banking transactions in a user-friendly GUI.
- Provide functionalities for customer account management.
- Implement an administrative system to oversee banking operations.
- Utilize Tkinter for an interactive interface.
- Store and manage customer and admin details efficiently.

*Features:*

**1. Customer Features:**
  - Account Creation: Users can register new bank accounts.
  - Deposit & Withdrawal: Customers can perform transactions securely.
  - Balance Inquiry: Users can check their current account balance.
  - Update Details: Customers can modify their personal information.

**2. Admin Features:**

  - Admin Authentication: Secure login system for administrators.
  - User Management: View and modify customer details.
  - Transaction Monitoring: Track deposits and withdrawals.
  - Report Generation: Export customer and transaction data to CSV files.


*Technologies Used:*

- Python (Programming Language)
- Tkinter (GUI Framework)
- CSV (Data Storage)
- Object-Oriented Programming (OOP)


*Installation & Usage:*

**1. Prerequisites:**

- Ensure you have Python 3.x installed on your system.

**2. Installation Steps**

**3. Clone the repository:**

  - git clone https://github.com/yourusername/Bank-Transaction-Simulation.git
  - cd Bank-Transaction-Simulation
    
**4. Run the application:**

  - python bank_system.py


*Code Structure:*

1. customer_account.py: Defines the CustomerAccount class for managing customer-related operations.
2. admin.py: Defines the Admin class with functionalities for administrators.
3. bank_system.py: Main file that initializes the GUI and integrates other modules.
4. bank_store.csv: Stores customer data.


*Future Improvements:*

- Implement a database system (SQLite/MySQL) instead of CSV for better data handling.
- Enhance the UI for a modern and sleek look.
- Introduce multi-user roles and enhanced security features.
- Add automated transaction logs for better tracking.

Author: Dams

*License:*

This project is licensed under the MIT License

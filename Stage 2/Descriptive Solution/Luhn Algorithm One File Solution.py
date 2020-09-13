from collections import namedtuple
#from functions import generate_account_number, generate_pin, generate_card_number
#from account import Account
import sqlite3
import sys
import random
#from functions import check_card

#Remove the above there #s for implementing as a three file system. acccounts.py, banking.py, fsmmenus.py

# Account class contains all the information of the bank account
class Account:
    # Create objects
    def __init__(self, con, cur, data):
        self.id = data.id
        self.card = data.card
        self.pin = data.pin
        self.balance = data.balance
        # Load global variables connection and cursor passed from Bank class
        global connection, cursor
        connection = con
        cursor = cur

    # Display account menu
    def account_menu(self):
        # Menu options to display
        options = ["1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit"]
        # Function for each of menu options
        functions = {"1": self.print_balance, "2": self.add_income, "3": self.transfer_money, "4": self.close_account,
                     "5": self.log_out, "0": exit}
        print("", *options, sep="\n")  # Print menu
        choice = input(">").strip()  # Get user input
        # Call function according to user choice from the list
        if choice not in functions.keys():
            print("This option does not exist.\nPlease try again")
            return self.account_menu()  # Get the account menu again
        else:
            functions[choice]()

    # Function updates balance and prints it out
    def print_balance(self):
        # Get the balance of the account from the database
        cursor.execute('select balance from card where id = ?', (self.id, ))
        self.balance = cursor.fetchone()[0]  # Update account's balance
        print('Balance:', self.balance)  # Print it out to the console
        return self.account_menu()  # Load account menu after completion

    # Function asks user for amount of money to add to the balance of the account
    def add_income(self):
        print("Enter income:")
        income = input(">").strip()  # Get user input
        if income.isdigit() and int(income) > 0:  # Check that input contains only digits
            self.set_balance(int(income) + self.balance)  # Update balance
            print("Income was added!")
        else:
            print("Incorrect amount!")
        return self.account_menu()  # Load account menu after completion

    # Function changes balance and update info in the database
    def set_balance(self, balance):
        self.balance = balance  # Update balance
        # Pass updated balance to the database
        cursor.execute('update card set balance = ? where id = ?', (balance, self.id))
        connection.commit()

    # Function asks user for amount and card number to transfer, then transfers amount between accounts
    def transfer_money(self):
        print("Transfer:", "Enter card number:", sep="\n")
        card = input(">").strip()  # Get card number
        if len(card) == 16 and card.isdigit() and check_card(card):  # Check if card number is correct
            if card != self.card:  # Check that it's not the same account
                other_id = self.get_account_id(card)  # Get other account from the database by card number
                if other_id:  # If account was found
                    other_id = other_id[0]  # Get the other account's id
                    print("Enter how much money you want to transfer:")  # Ask user for amount of money to transfer
                    amount = input(">").strip()
                    if amount.isdigit() and int(amount) > 0:  # Check that amount of money contains only digits
                        amount = int(amount)
                        if amount <= self.balance:  # Check that account has enough fund to transfer
                            self.balance -= amount  # Remove funds from the account
                            # Update balance int he database
                            cursor.execute('update card set balance = ? where id = ?', (self.balance, self.id))
                            # Add fund to the other account
                            cursor.execute('update card set balance = balance + (?) where id = ?', (amount, other_id))
                            connection.commit()
                            print("Success!")
                        else:
                            print("Not enough money!")
                    else:
                        print("Incorrect amount!")
                else:
                    print("Such a card does not exist.")
            else:
                print("You can't transfer money to the same account!")
        else:
            print("Probably you made mistake in the card number. Please try again!")
        return self.account_menu()

    # Function return account's id if account is found in the database, otherwise returns None
    def get_account_id(self, card):
        cursor.execute("select id from card where number = ?", (card, ))
        f = cursor.fetchone()
        return f

    # Function to close account and remove it from the database
    def close_account(self):
        cursor.execute('delete from card where id = ?', (self.id, ))
        connection.commit()
        print("The account has been closed!")

    # Function to Log out and return to the bank menu
    def log_out(self):
        print("You have successfully logged out!")

# Get global variables for connection
global cursor, connection

# Function returns true if card last digit has correct checksum number according to Luhn algorithm
def check_card(card):
    luhn_sum = luhn_algorithm(card[:-1])  # Pass the number through luhn algorithm without last digit
    checksum = get_checksum(luhn_sum)  # Get correct checksum number based on Luhn algorithm
    return checksum == int(card[-1])  # Check that last digit of the card matches correct checksum

# Function exits program and closes SQL connection
def exit():
    print("\nBye!")
    connection.close()
    sys.exit()  # Close program

# Function returns new card number from account number parameter
def generate_card_number(acc_number):
    iin = "400000"  # IIN given by the assignment
    luhn_sum = luhn_algorithm(iin + acc_number)  # Calculate Luhn sum
    checksum = get_checksum(luhn_sum)  # Get checksum
    return iin + acc_number + str(checksum)  # Return 16-digit card number as a string

# Generate 9-digit account number
def generate_account_number():
    acc_number = ""
    for _ in range(9):
        acc_number += str(random.randrange(10))
    return acc_number

# Function takes Luhn sum as a parameter and returns checksum
def get_checksum(luhn_sum):
    # Check sum added to the luhn sum must return round number
    return 10 - luhn_sum % 10 if luhn_sum % 10 != 0 else 0

# Function returns Luhn sum based on 15-digit number
def luhn_algorithm(card_number):
    card_number = list(map(int, card_number))  # Create a list of integers from the string
    for i, _ in enumerate(card_number, 1):
        # Multiply each odd digit by 2
        if i % 2 != 0:
            card_number[i - 1] *= 2
        # Subtract 9 from any digit bigger than 9
        if card_number[i - 1] > 9:
            card_number[i - 1] -= 9
    return sum(card_number)  # Return sum

# Function returns a random generated 4-digit pin-code as a string
def generate_pin():
    pin = ""
    for _ in range(4):
        pin += str(random.randrange(10))
    return pin

# Bank class
class Bank:
    # Create tuple for handling SQL query
    Account = namedtuple('Account', 'id, card, pin, balance')

    # Init function
    def __init__(self):
        # Create global variables for SQL and establish connection to database
        global cursor, connection
        connection = sqlite3.connect('card.s3db')
        cursor = connection.cursor()
        # Create a table in database if it does not exist already
        cursor.executescript('create table if not exists card(' +
                            'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' +
                            'number TEXT NOT NULL,' +
                            'pin TEXT NOT NULL,' +
                            'balance INTEGER NOT NULL DEFAULT 0' +
                            ')')
        connection.commit()
        # Show main Menu
        self.main_menu()

    # Function to print main menu
    def main_menu(self):
        options = ["1. Create an account", "2. Log into account", "0. Exit"]  # Menu options to display
        functions = {"1": self.new_account, "2": self.log_in, "0": exit}  # Function for each of menu options
        print("", *options, sep="\n")  # Print menu
        choice = input(">").strip()  # Get user input
        # Call function according to user choice from the list
        if choice not in functions.keys():
            print("This option does not exist.\nPlease try again")
        else:
            functions[choice]()
        return self.main_menu()  # Load menu again after completion

    # Function to log in to an account
    def log_in(self):
        print("Enter your card number:")
        card_number = input(">").strip()  # Get card number
        if card_number.isdigit():  # Check that input contains only digits
            print("Enter your PIN:")
            pin = input(">").strip()  # Get pin number
            if pin.isdigit():  # Check that input contains only digits
                account = self.get_account(card_number, pin)  # Get account from the database
                if account:  # If account is found
                    account = Account(connection, cursor, account)  # Create new instance of class Account
                    print("You have successfully logged in!")
                    account.account_menu()  # Load account menu
                    return
        print("Wrong card number or PIN!")

    # Function to create new account
    def new_account(self):
        print("\nYour card has been created")
        accounts = self.get_all_accounts()  # Get a dictionary of all accounts
        while True:
            new_number = generate_account_number()  # Generate new account number
            card = generate_card_number(new_number)  # Generate new card number
            if card not in accounts.keys():  # Make sure that new card number is unique
                break
        pin = generate_pin()  # Generate new pin number
        print("Your card number:", card, "Your card PIN:", pin, sep="\n")  # Print new account information
        cursor.execute("insert into card(number, pin) values (?, ?) ", (card, pin))  # Add new card and pin to database
        connection.commit()

    # Function returns dictionary with card numbers as keys and pins as their values
    def get_all_accounts(self):
        accounts = {}  # Create empty dictionary
        cursor.execute('select * from card')  # Get all accounts from the database
        for acc in map(self.Account._make, cursor.fetchall()):
            accounts[acc.card] = acc.pin  # Add pair to the dictionary as ("card number": "pin")
        return accounts  # Return the dictionary

    # Function returns named tuple of account from the database if account exist or None otherwise
    def get_account(self, account_numb, pin):
        # Request query with card number and pin
        cursor.execute("select * from card where number = ? and pin = ?", (account_numb, pin))
        f = cursor.fetchone()
        return self.Account._make(f) if f else None  # Return named tuple Account(id, card, pin, balance) or None

# Main Function
def main():
    bank = Bank()

if __name__ == '__main__':
    main()

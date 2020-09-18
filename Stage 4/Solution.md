# Write your code here
from random import randint
from math import ceil
import sqlite3

# Connect to database
conn = sqlite3.connect('card.s3db')

# Create a cursor
cur = conn.cursor()

# Drop the table, had to do it as I was getting an error when creating it
cur.execute("DROP TABLE card")
conn.commit()

# Create a table
cur.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);""")

# Commit our command
conn.commit()

current_account = None

while True:
    if current_account is None:
        print("1. Create an account\n2. Log into account\n0. Exit")
        action = int(input())
        if action == 1:
            new_acc_no = randint(400000000000000, 400000999999999)
            check_account = list(str(new_acc_no))
            total = 0
            total_up = 0
            for i in range(len(check_account)):
                if i % 2 == 0:
                    x = int(check_account[i]) * 2
                    check_account[i] = str(x)

            for i in range(len(check_account)):
                if int(check_account[i]) > 9:
                    x = int(check_account[i]) - 9
                    check_account[i] = str(x)

            for i in range(len(check_account)):
                total += int(check_account[i])
                total_up = int(ceil(total / 10)) * 10

            check_sum = total_up - total
            new_account = str(new_acc_no) + str(check_sum)

            new_pin = str(randint(1000, 9999))

            cur.execute(f"INSERT INTO card (number, pin) VALUES ({new_account}, {new_pin})")
            conn.commit()
            print()
            print(f"Your card has been created\nYour card number:\n{new_account}\nYour card PIN:\n{new_pin}")
        elif action == 2:
            print("Enter your card number:")
            temp_account = input()
            cur.execute("SELECT CASE WHEN number = ? THEN number ELSE '0000000000000000' END FROM card", (temp_account,))
            check_account = cur.fetchone()[0]
            print("Enter your PIN:")
            temp_pin = input()
            cur.execute("SELECT CASE WHEN number = ? THEN pin ELSE '0000' END FROM card", (temp_account,))
            check_pin = cur.fetchone()[0]
            if check_account == temp_account and check_pin == temp_pin:
                current_account = check_account
                print("You have successfully logged in!")
            else:
                print("Wrong card number or PIN!")
        elif action == 0:
            print("Bye!")
            exit()
    else:  # User is signed in
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        choice = int(input())
        print()
        if choice == 1:
            cur.execute("SELECT balance FROM card WHERE number = ?", (current_account,))
            actual_balance = str(cur.fetchone()[0])
            print(f"Balance: {actual_balance}")
            continue
        elif choice == 2:
            print("Enter income:")
            income = int(input())
            cur.execute("SELECT balance FROM card WHERE number = ?", (current_account,))
            actual_balance = cur.fetchone()[0]
            new_balance = actual_balance + income
            cur.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balance, current_account))
            conn.commit()
            print("Income was added!")
            continue
        elif choice == 3:
            print("Enter card number")
            transfer_account = input()
            transfer_account2 = list(transfer_account[:-1])
            check_total = 0
            for i in range(len(transfer_account2)):
                if i % 2 == 0:
                    x = int(transfer_account2[i]) * 2
                    transfer_account2[i] = str(x)

            for i in range(len(transfer_account2)):
                if int(transfer_account2[i]) > 9:
                    x = int(transfer_account2[i]) - 9
                    transfer_account2[i] = str(x)

            for i in range(len(transfer_account2)):
                check_total += int(transfer_account2[i])
                total_up = int(ceil(check_total / 10)) * 10

            check_sum = total_up - check_total

            if int(transfer_account[-1]) != check_sum:
                print("Probably you made a mistake in the card number. Please try again!")
            elif transfer_account == current_account:
                print("You can't transfer money to the same account!")
            else:
                cur.execute("SELECT * FROM card")
                info = cur.fetchall()
                all_accounts = [x[1] for x in info]
                if transfer_account not in all_accounts:
                    print("Such a card does not exist.")
                else:
                    print("Enter how much money you want to transfer:")
                    transfer_amount = int(input())
                    cur.execute("SELECT balance FROM card WHERE number = ?", (current_account,))
                    actual_balance = cur.fetchone()[0]
                    cur.execute("SELECT balance FROM card WHERE number = ?", (transfer_account,))
                    destination_balance = cur.fetchone()[0]
                    if actual_balance < transfer_amount:
                        print("Not enough money!")
                    else:
                        cur.execute("UPDATE card SET balance = ?  WHERE number = ?", (actual_balance - transfer_amount, current_account))
                        cur.execute("UPDATE card SET balance = ?  WHERE number = ?", (destination_balance + transfer_amount, transfer_account))
                        conn.commit()
                        print("Success!")
            continue
        elif choice == 4:
            cur.execute("DELETE FROM card WHERE number = ?", (current_account,))
            conn.commit()
            print("The account has been closed!")
            current_account = None
            continue
        elif choice == 5:
            current_account = None
            print("You have successfully logged out!")
            continue
        elif choice == 0:
            current_account = None
            print("Bye!")
            exit()

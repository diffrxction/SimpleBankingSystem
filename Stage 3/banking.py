class Banking:
    import random
    import sqlite3

    def __init__(self):

        self.create_card_database()
        self.menu_1 = '\n1. Create an account\n2. Log into account\n0. Exit\n'
        self.menu_2 = '\n1. Balance\n2. Log out\n0. Exit\n'
        self.message_1 = ['Your card has been created\nYour card number:', 'Your card PIN:']
        self.message_2 = ['Enter your card number:', 'Enter your PIN:']
        self.message_3 = ['You have successfully logged in!', 'Wrong card number or PIN!']
        self.message_4 = 'Bye !'
        self.state = 'idle'
        self.iin, self.customer_account_number, self.checksum, self.card_number, self.pin = 400000, 0, 0, 0, 0
        self.balance = 0
        self.accounts, self.credentials = [], ['', '']
        print(self.menu_1)  # start the banking system
        while self.state != 'exit':
            self.selection_menu(int(input()))
        else:
            print(self.message_4)

    def selection_menu(self, user_input):
        if user_input == 0:
            self.state = 'exit'
        elif self.state == 'idle':
            if user_input == 1:
                self.generate_card_number_and_pin()
                self.accounts.append([self.card_number, self.pin])
                print(self.menu_1)
            elif user_input == 2:
                self.state = 'login 1'
                print(self.message_2[0])
        elif self.state == 'login 1':
            self.state = 'login 2'
            self.credentials[0] = str(user_input)
            print(self.message_2[1])
        elif self.state == 'login 2':
            self.credentials[1] = str(user_input)
            if tuple(self.credentials) == self.fetch_data(self.credentials[0]):
                self.state = 'authorised'
                print(self.message_3[0])
                print(self.menu_2)
            else:
                self.state = 'idle'
                print(self.message_3[1])
                print(self.menu_1)
        elif self.state == 'authorised':
            if user_input == 1:
                print(self.balance)
                print(self.menu_2)
            elif user_input == 2:
                self.state = 'idle'
                print(self.menu_1)

    def luhn(self, number):
        self.number = number
        checklist = [int(x) for x in str(self.number)]
        for i in range(15):
            if i % 2 == 0:
                checklist[i] = checklist[i] * 2
        for i in range(15):
            if checklist[i] > 9:
                checklist[i] = checklist[i] - 9
        for i in range(15):
            self.checksum = self.checksum + int(checklist[i])
        self.checksum = ((((self.checksum // 10) + 1) * 10) - self.checksum) % 10

    def generate_card_number_and_pin(self):
        self.customer_account_number = self.random.randint(1, 999999999)
        self.card_number = str(self.iin) + str(self.customer_account_number).zfill(9)
        self.luhn(self.card_number)
        self.card_number = int(str(self.iin) + str(self.customer_account_number).zfill(9) + str(self.checksum))
        self.pin = self.random.randint(0, 9999)
        self.checksum = 0
        self.save_card(self.card_number, self.pin)
        print(self.message_1[0])
        print(self.card_number)
        print(self.message_1[1])
        print(str(self.pin).zfill(4))

    def create_card_database(self):
        self.conn = self.sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('DROP TABLE IF EXISTS card')
        self.cur.execute('''CREATE TABLE card (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        number TEXT NOT NULL UNIQUE,
                        pin TEXT NOT NULL,
                        balance INTEGER DEFAULT 0 NOT NULL);''')
        self.conn.commit()

    def save_card(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
        self.cur.execute('INSERT INTO card (number, pin) VALUES ( ?, ? )', (str(self.card_number), str(self.pin)))
        self.conn.commit()

    def fetch_data(self, card_number):
        self.card_number = str(card_number)
        self.cur.execute("SELECT number, pin FROM card WHERE number LIKE (?);", (self.card_number,))
        return self.cur.fetchone()


bs = Banking()

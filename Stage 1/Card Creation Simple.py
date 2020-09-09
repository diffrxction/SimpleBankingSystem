import random


class CreditCard:
    def __init__(self):
        self.card_number = None
        self.code_pin = None

    def generate_card(self):
        self.card_number = '400000' + str(random.randint(1000000000, 9999999999))
        self.code_pin = random.randint(0000, 9999)
        if self.code_pin < 1000:
            self.code_pin = '0' + str(self.code_pin)
        print('')
        print('Your card has been created')
        print('Your card number:')
        print(self.card_number)
        print('Your card pin:')
        print(self.code_pin)
        print('')


menu_choice = None
logged = False
all_card = []
credit_card = CreditCard()

while menu_choice != 0:
    if logged is False:
        menu_choice = int(input('''1. Create an account
2. Log into account
0. Exit\n'''))
        if menu_choice == 1:
            credit_card.generate_card()
            all_card.append(credit_card)
        elif menu_choice == 2:
            card_number = input('Enter your card number')
            pin_number = input('Enter your PIN')
            if int(credit_card.card_number) == int(card_number) and int(credit_card.code_pin) == int(pin_number):
                print('You have successfully logged in!\n')
                logged = True
            else:
                print('Wrong card number or PIN\n')
    else:
        menu_choice = int(input('''1. Balance
2. Log out
0. Exit
'''))
        if menu_choice == 1:
            print('Balance : 0\n')
        if menu_choice == 2:
            print('You have successfully logged out!\n')
            logged = False


print('\nBye!')


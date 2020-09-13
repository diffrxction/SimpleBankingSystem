import random

while True:
    a = random.randint(0000000000, 9999999999)
    random.seed(0)
    acc_no1 = str(4000000000000000 + a)
    valid = list(str(acc_no1))
    digit_sum = 0
    for i in range(len(valid) - 1):
        valid[i] = int(valid[i])
        if i % 2 == 0:
            valid[i] *= 2
            if valid[i] > 9:
                valid[i] -= 9
        digit_sum += valid[i]
    cc = (10 - digit_sum % 10)
    acc_no = acc_no1[:-1] + "{}".format(cc)
    acc_password = random.randint(0000, 9999)
    random.seed(0)
    acc_password = (0000 + acc_password)
    choice = input("""1. Create an account
2. Log into account
0. Exit\n""")
    if choice == "1":
        print("Your card has been created\nYour card number:")
        print(acc_no)
        print("Your card PIN:")
        print(acc_password)

    elif choice == "2":
        while True:
            print("Enter your card number:")
            card_no = input()
            print("Enter your PIN:")
            card_pin = input()
            if card_no == acc_no and card_pin == str(acc_password):
                print("\nYou have successfully logged in!\n")
                while True:
                    ch = input("""1. Balance
                    2. Log out
                    0. Exit\n""")
                    if ch == "1":
                        print("\nBalance: 0\n")

                    elif ch == "2":
                        print("\nYou have successfully logged out!\n")
                        break
                    elif ch == "0":
                        exit(0)
                        break
            else:
                print("\nWrong card number or PIN!\n")
                break
    else:
        print("Bye!")
        exit()

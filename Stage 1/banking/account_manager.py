from secrets import randbelow


class BankAccount:
    """
    This class handles all bank account transactions within itself. The rationale for this setup is that
    in an actual banking app you would not want to pass around account details for security reasons.
    The class methods handle creating new accounts, login/logout, retrieving information
    from the account to display, and account storage.
    The instance methods handle checking login credentials within each account and displaying account information.
    """
    # class constants
    MII = '4'
    BIN = MII + '00000'
    ACCT_DIGITS = 9
    PIN_DIGITS = 4

    # class variables
    __acct_store = {}
    __current_acct = None

    # ======== setup new Card Account methods ========
    def __init__(self):
        """
        Initializes a unique card account, displays login info for first time, and sets starting balance
        """
        self.__account_number = self.__generate_acct_number()
        self.__account_pin = self.__generate_pin()
        self.card_number = BankAccount.BIN + self.__account_number \
            + self.__calculate_checksum(BankAccount.BIN + self.__account_number)
        self.__balance = 0
        self.__display_login_info()

    @classmethod
    def __generate_acct_number(cls) -> str:
        """
        Returns a random unique account number
        """
        duplicate = True  # prime the while loop
        temp_acct = None
        while duplicate:
            temp_acct = str(randbelow(10 ** cls.ACCT_DIGITS)).zfill(cls.ACCT_DIGITS)
            duplicate = cls.retrieve(temp_acct)  # if an account with that number already exists, generate another
        return temp_acct

    @classmethod
    def __generate_pin(cls) -> str:
        """
        Returns a random pin code
        """
        return str(randbelow(10 ** cls.PIN_DIGITS)).zfill(cls.PIN_DIGITS)

    @classmethod
    def __calculate_checksum(cls, number) -> str:
        """
        Returns a calculated checksum for the card account
        For now this checksum is the ones digit of the sum of all digits in card number. This is to prevent
        duplicate accounts with only a different checksum
        """
        # TODO in future stages, this function will use the Luhn algorithm to create checksum
        return str(sum(int(num) for num in str(number)) % 10)

    @classmethod
    def new_account(cls):
        new_card = BankAccount()
        BankAccount.__acct_store[new_card.card_number] = new_card

    def __check_pin(self, pin_number):
        return self.__account_pin == pin_number

    # ======== Card Account Display methods ========
    def __card_display(self):
        """Displays formatted card number with spaces"""
        return ''.join([(each_number if (i == 0 or i % 4 != 0) else ' ' + each_number)
                        for i, each_number in enumerate(self.card_number)])

    def __display_login_info(self):
        """Displays login info / only used after initial account creation"""
        print(f'\nYour card has been created\n'
              f'Your card number:\n'
              f'{self.__card_display()}\n'   # uncomment this line and comment out line below for pretty display
              # f'{self.card_number}\n'
              f'Your card PIN:\n'
              f'{self.__account_pin}\n', )

    def __str__(self) -> str:  # TODO only used for testing, should disable in final for security
        return f'card#: {self.card_number}\nacct#: {self.__account_number}, pin#: {self.__account_pin}'

    # ======== Card Account Access methods ========
    @classmethod
    def login(cls) -> bool:
        print('\nEnter your card number:')
        login_card = input()
        print('Enter your PIN:')
        login_pin = input()

        this_acct = cls.retrieve(login_card)
        # remember: if there is no account matching login card number, fail; otherwise, check for matching pin
        if this_acct and this_acct.__check_pin(login_pin):
            cls.__current_acct = this_acct
            print('\nYou have successfully logged in!\n')
        else:
            print('\nWrong card number or PIN!\n')

        return cls.is_logged_in()

    @classmethod
    def logout(cls):
        cls.__current_acct = None
        cls.__logged_in = False
        print('\nYou have successfully logged out!\n')

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls.__current_acct is not None

    @classmethod
    def retrieve(cls, account):
        """
        Returns the requested account or False
        This method is used by both the login function where it returns the account if login is successful,
        and when generating a new card account number where a False return means there isn't already
        an account with that number and it's okay to accept the new card number
        """
        requested_acct = None
        try:
            requested_acct = BankAccount.__acct_store[account]
        except KeyError:
            return False
        finally:
            return requested_acct

    def __get_balance(self):
        """
        Gets balance of the currently logged-in account
        """
        return self.__balance

    def __transaction(self, amount):
        self.__balance += amount

    @classmethod
    def show_balance(cls):
        """
        Show balance if logged in
        """
        if cls.is_logged_in():
            print(f'\nBalance: {cls.__current_acct.__get_balance()}\n')

    @classmethod
    def deposit(cls, amount):
        """
        Deposits amount into current account
        Not (yet?) used in project. I set this up for testing account information
        """
        if amount >= 0 and cls.is_logged_in():
            cls.__current_acct.__transaction(amount)
        else:
            print('deposit error')

    @classmethod
    def withdrawal(cls, amount):
        """
        Withdraws amount from current account
        Not (yet?) used in project. I set this up for testing account information
        """
        if amount >= 0 and cls.is_logged_in():
            cls.__current_acct.__transaction(-amount)
        else:
            print('withdrawal error')

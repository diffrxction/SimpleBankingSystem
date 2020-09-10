from abc import ABC, abstractmethod
"""
The classes within this file are a Finite State Machine.
They control the menu system and what behavior the program uses for each menu option.
"""


class State(ABC):

    def __init__(self):
        self._context = None
        self._menu_options = {}

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def execute(self) -> None:
        pass

    def display_menu(self, menu, options):
        print(menu)
        request = input()
        try:
            options[request]()
        except KeyError:
            print('invalid entry\n')
            self.context.transition_to(self)


class MainMenu(State):
    """
    Main Menu state - controls functionality while Main Menu is active
    This is the initial state of the program
    """
    def __init__(self):
        super().__init__()

        self.menu = f'1. Create an account\n'\
                    f'2. Log into account\n'\
                    f'0. Exit'

        self._menu_options = {'1': self.create_acct,
                              '2': self.login_acct,
                              '0': self.exit}

    def execute(self) -> None:
        self.display_menu(self.menu, self._menu_options)

    def create_acct(self):
        self.context.banking_app.create_account()

    def login_acct(self):
        if self.context.banking_app.login_account():
            self.context.transition_to(AcctMenu())
        else:
            self.context.transition_to(MainMenu())

    def exit(self):
        self.context.banking_app.stop_app()


class AcctMenu(State):
    """
    Account Menu state - controls functionality while Account Menu is active
    """
    def __init__(self):
        super().__init__()

        self.menu = f'1. Balance\n'\
                    f'2. Log out\n'\
                    f'0. Exit'

        self._menu_options = {'1': self.balance,
                              '2': self.logout_acct,
                              '0': self.exit}

    def execute(self):
        self.display_menu(self.menu, self._menu_options)

    def balance(self):
        self.context.banking_app.show_balance()

    def logout_acct(self):
        self.context.banking_app.logout_account()
        self.context.transition_to(MainMenu())

    def exit(self):
        self.context.banking_app.stop_app()

    # disabled for current project stage / used in testing functionality of accounts
    # def deposit(self):
    #     self._context.banking_app.deposit()

    # def withdraw(self):
    #     self._context.banking_app.withdraw()


class Context(ABC):
    """
    This is context manager / Finite State Machine
    It handles transitions between states and passes 'execute' through to the currently active state
    """

    def __init__(self, banking_app, state: State) -> None:
        self.banking_app = banking_app
        self._state = None
        self.transition_to(state)

    def transition_to(self, state: State):
        self._state = state
        self._state.context = self

    def execute(self):
        self._state.execute()

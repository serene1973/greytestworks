import pytest
from py3270 import Emulator

@pytest.fixture(scope="session")
def mf_driver():
    # Initialize the emulator (replace with actual emulator details)
    mf = Emulator()
    mf.connect("my.mainframe.server")
    yield mf  # Provide the emulator instance to tests
    mf.terminate()  # Cleanup after tests



class BaseMainframe:
    def __init__(self, emulator):
        self.mf = emulator  # Store emulator instance

    def click(self, row, col):
        """Move to a position and press enter."""
        self.mf.move_to(row, col)
        self.mf.send_enter()

    def type(self, row, col, text):
        """Move to a position and enter text."""
        self.mf.move_to(row, col)
        self.mf.send(text)

    def get_text(self, row, col, length):
        """Read text from a specific position."""
        return self.mf.string_at(row, col, length)

    def clear(self, row, col, length):
        """Clear text at a specific position."""
        self.mf.move_to(row, col)
        self.mf.send(" " * length)  # Overwrite with spaces


class LoginPage(BaseMainframe):
    def __init__(self, emulator):
        super().__init__(emulator)

    def enter_username(self, username):
        self.type(5, 10, username)  # Adjust row, col

    def enter_password(self, password):
        self.type(6, 10, password)  # Adjust row, col

    def submit(self):
        self.click(7, 20)  # Adjust row, col


def test_mainframe_login(mf_driver):
    login_page = LoginPage(mf_driver)
    login_page.enter_username("myuserid")
    login_page.enter_password("mypassword")
    login_page.submit()

    # Verify login success
    assert "Welcome" in mf_driver.string_at(10, 5, 20)

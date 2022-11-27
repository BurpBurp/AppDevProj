class UserUpdateError(Exception):

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class WrongPasswordError(UserUpdateError):
    pass

class PasswordNotMatchError(UserUpdateError):
    pass

class RepeatedEmailError(UserUpdateError):
    pass

class UserAlreadyExistsError(UserUpdateError):
    pass

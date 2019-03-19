from typing import Optional

class UserNotFoundException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if message:
            super().__init__(message)
        else:
            super().__init__()

class UserAlreadyExistsException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if message:
            super().__init__(message)
        else:
            super().__init__()

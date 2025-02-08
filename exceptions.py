class BreakException(Exception):
    """Break out from loop"""
    pass

class ReturnException(Exception):
    """Used to trigger the return of a function with optional value"""
    def __init__(self, value):
        self.value = value

class ContinueException(Exception):
    """Continue loop from next iteration"""
    pass
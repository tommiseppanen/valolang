class ReturnException(Exception):
    """Used to trigger the return of a function with optional value"""
    def __init__(self, value):
        self.value = value
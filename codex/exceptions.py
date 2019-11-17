class CodexAPIException(BaseException):
    def __init__(self, error_message: str = None, error_description: str = None, code: int = None):
        super().__init__(error_description)

        self.description = error_description
        self.message = error_message
        self.code = code


class CodexAPIRequestSignerException(BaseException):
    pass

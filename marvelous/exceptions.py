class ApiError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AuthenticationError(ApiError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class LibraryError(ApiError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

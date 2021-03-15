class UpdateError(Exception):
    def __init__(self, message="Unexpected error during update.."):
        super(UpdateError, self).__init__(message)


class DeleteError(Exception):
    def __init__(self, message=" Unexpected error during deletion..."):
        super(DeleteError, self).__init__(message)


class Audio_Doesnt_Exist(Exception):
    def __init__(self, message="Audio File doesn't exist..."):
        super(Audio_Doesnt_Exist, self).__init__(message)

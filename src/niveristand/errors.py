

class VeristandError(Exception):
    """
    The base class for all VeriStandErrors.

    Note: This class generates a :class:`VeristandError` if a more specific error cannot be determined.
    """

    pass


class TranslateError(VeristandError):
    """Raised if a Python function fails to translate to a VeriStand real-time sequence."""

    pass


class UnexpectedError(VeristandError):
    """Raised if the state of the operation can not be determined."""

    pass


class VeristandNotImplementedError(VeristandError):
    """Raised to indicate this functionality is not yet available."""

    def __init__(self):
        """Throw Generic exception for things that are not implemented yet."""
        self.message = "Not Implemented"
        super(VeristandNotImplementedError, self).__init__(self.message)


class _StopTaskException(Exception):
    pass


class RunError(VeristandError):
    """Raised at the end of execution if an RT sequence called :any:`generate_error`."""

    def __init__(self, error):
        assert isinstance(error, SequenceError)
        self.error = error

    def get_all_errors(self):
        """
        Generates a list of all errors reported during execution.

        Returns:
            List(:class:`SequenceError`): all errors generated during execution.

        """
        error = self.error
        while error:
            yield error
            error = error.inner_error

    @classmethod
    def RunErrorFactory(cls, error):
        from niveristand.clientapi._realtimesequencedefinitionapi.erroraction import ErrorAction
        assert isinstance(error, SequenceError)
        if error.error_action is ErrorAction.ContinueSequenceExecution:
            return RunFailedError(error)
        else:
            return RunAbortedError(error)


class RunFailedError(RunError):
    """
    Raised by :any:`run_py_as_rtseq` to report that the sequence failed.

    This error is raised when a real-time sequence executes successfully,
    but :any:`generate_error` was called with :any:`ErrorAction.ContinueSequenceExecution`.
    """

    def __init__(self, error):
        super(RunFailedError, self).__init__(error)


class RunAbortedError(RunError):
    """
    Raised by :any:`run_py_as_rtseq` to report that the sequence failed.

    This error is raised when a real-time sequence executes successfully,
    but :any:`generate_error` was called with :any:`ErrorAction.StopSequence` or :any:`ErrorAction.AbortSequence`.
    """

    def __init__(self, error):
        super(RunAbortedError, self).__init__(error)


class SequenceError(VeristandError):
    """Raised by :any:`generate_error` to report a sequence failure."""

    def __init__(self, error_code, message, error_action):
        super(SequenceError, self).__init__(message)
        self.error_code = error_code
        self.error_action = error_action
        self.message = message
        self._inner_error = None

    @property
    def inner_error(self):
        """
        Returns the error generated before the most recent error, if any, or `None`.

        Returns:
            :any:`SequenceError`: the previous error generated by this sequence.

        Real-time sequences report only the last error the sequence generates. If you want to see a list of all the
        inner errors, use :any:`RunError.get_all_errors`.

        """
        return self._inner_error

    @inner_error.setter
    def inner_error(self, value):
        assert isinstance(value, SequenceError) or value is None
        assert self._inner_error is None
        self._inner_error = value

    @property
    def is_fatal(self):
        """
        Returns whether or not any error causes the sequence to stop.

        Returns:
            bool: True if the error is :any:`ErrorAction.AbortSequence` or :any:`ErrorAction.StopSequence`, false if
            the error is :any:`ErrorAction.ContinueSequenceExecution`.

        """
        from niveristand.clientapi._realtimesequencedefinitionapi.erroraction import ErrorAction
        isfatal = (self.error_action in (ErrorAction.AbortSequence, ErrorAction.StopSequence)) or \
                  (self._inner_error and self.inner_error.is_fatal)
        return isfatal

    @property
    def should_raise(self):
        """
        Determines whether or not this error raises an exception.

        Returns:
            bool: False if the error is :any:`ErrorAction.ContinueSequenceExecution` with an error code of 0. Otherwise,
            this function returns True.

        """
        from niveristand.clientapi._realtimesequencedefinitionapi.erroraction import ErrorAction
        # If the error code was 0 in a Continue error then don't raise.
        return not (self.error_action is ErrorAction.ContinueSequenceExecution and self.error_code is 0)

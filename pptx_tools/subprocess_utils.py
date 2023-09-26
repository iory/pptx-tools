import subprocess

import six


def run_command(cmd, *args, **kwargs):
    """Execute a command.

    Parameters
    ----------
    cmd : str or list of str
        The command to execute. For a single command, it can be a string.
        For multiple commands, it should be a list of strings.
    *args
        Additional positional arguments to be passed to the subprocess call.
    **kwargs
        Additional keyword arguments to be passed to the subprocess call.
        capture_output : bool, optional
            If True, capture the output of the command (stdout and stderr)
            and return it. By default, the output is not captured.

    Returns
    -------
    CompletedProcess or int
        If `capture_output` is True, returns a `CompletedProcess` object
        containing information about the completed process, including the
        captured output. If `capture_output` is False, returns the process
        return code as an integer.

    Raises
    ------
    CalledProcessError
        If the command execution fails and raises an error.

    Notes
    -----
    This function uses the `subprocess` module to execute the command.
    On Python 2, it uses `subprocess.check_call`, and on Python 3 or later,
    it uses `subprocess.run` to run the command.

    Example
    -------
    >>> run_command('ls -l')
    # Executes the 'ls -l' command and returns the process return code.

    >>> run_command(['git', 'status'], capture_output=True)
    # Executes the 'git status' command, captures the output
    # (stdout and stderr),
    # and returns a CompletedProcess object with the captured output.
    """
    if kwargs.pop("capture_output", False):
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    if six.PY2:
        return subprocess.check_call(cmd, *args, **kwargs)
    else:
        return subprocess.run(cmd, *args, **kwargs)

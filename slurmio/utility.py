# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-17

import getpass
from subprocess import PIPE, Popen, SubprocessError
from typing import List


def get_user() -> str:
    """Get the username of the current user."""
    return getpass.getuser()


def run(
    cmd: List[str], stdout: int = PIPE, stderr: int = PIPE, shell: bool = None
) -> str:
    """Run a command and return the output or raise an exception if it fails.

    Parameters
    ----------
    cmd : List[str]
        The command to run as a list of strings.
    stdout : int, optional
        Standard output stream. Defaults to PIPE.
    stderr : int, optional
        Standard error stream. Defaults to PIPE.
    shell : bool, optional
        Whether to use the shell as the program to execute. Defaults to None.

    Returns
    -------
    str
        The output of the command.

    Raises
    ------
    Exception
        If the command is not found.
    SubprocessError
        If the command fails.
    """
    try:
        process = Popen(cmd, shell=shell, stdout=stdout, stderr=stderr)
    except FileNotFoundError:
        raise Exception("Command not found: " + " ".join(cmd))
    out, err = process.communicate()
    if process.returncode:
        raise SubprocessError(err.decode("utf-8"))
    return out.decode("utf-8")


def padstr(s: str, w: int, align: str = ">", placeholder: str = "...") -> str:
    """Pad or truncate a string to a specified width.

    Parameters
    ----------
    s : str
        The string to pad or truncate.
    w : int
        The width to pad or truncate to.
    align : str, optional
        The alignment of the string. Defaults to ">".
    placeholder : str, optional
        The placeholder to use if the string is truncated. Defaults to "...".
    """
    s = s[:w] if len(s) <= w else s[: w - len(placeholder)] + placeholder
    return f"{s:{align}{w}}"

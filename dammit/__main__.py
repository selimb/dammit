"""Dammit let me delete this file!

Usage:
  dammit [-y | -s] [--verbose] <name>
  dammit --version
  dammit (-h | --help)

Options:
  -y         Kill without permission.
  -s         Enable hotkey.
  --verbose  Explain what is being done.
  --version  Show version.
  -h --help  Show this screen.

"""
from __future__ import print_function

from functools import partial
import logging
import msvcrt
import os
import posixpath
import re
import subprocess
import sys
import time

from docopt import docopt

__version__ = '0.1.0'
__author__ = 'Selim Belhaouane'
__license__ = 'MIT'

log = logging.getLogger()
PREFIX = 'dammit:'

# handle.exe provides way to close specified handle, which would be preferable,
# but this requires administrator rights :(
HANDLE = ["handle64.exe"]
CYGPATH = ['C:\\GnuNT\\bin\\cygpath.exe']
KILL = ["TASKKILL", "/f", "/pid"]
ACTIVATE = ["activatePID.exe"]
EXPLORER = "explorer.exe"
CANT_EXECUTE = """Could not execute command: %s"""


def abspath(path):
    """Return the absolute path of given `path`.

    Taken to be relative from current working directory if input is not an
    absolute path.

    Args:
        path (str) : Pathname to absolutize.

    Notes:
        Should work for POSIX and Windows paths to accomodate
        different shells.
    """
    if posixpath.isabs(path):  # Starts with "/"
        if path[1:9] != 'cygdrive':
            path = posixpath.join('/cygdrive', path[1:])
        proc = subprocess.Popen(CYGPATH + ['-w', path],
                                stdout=subprocess.PIPE)
        return proc.stdout.read().rstrip()  # Remove trailing newline
    return os.path.abspath(path)


def find_locks(name):
    """Find which processes currently have a particular file/directory open.

    Args:
        name (str) : Name of the file which is locked.

    Returns:
        List of (process, PID)-pairs which are accessing the file.
    """
    log.debug("Finding locks on %s" % name)
    cmd = HANDLE + [name]
    try:
        log.debug("Running %s" % ' '.join(cmd))
        output = subprocess.check_output(cmd)
    except WindowsError:
        log.info(CANT_EXECUTE % HANDLE)
        sys.exit(1)
    except subprocess.CalledProcessError:
        return []
    log.debug("%s output:\n%s" % (HANDLE, output))
    pattern = r"([^\s]+)(?:\s+)pid: ([0-9]{4})"
    return frozenset(re.findall(pattern, output))


def kill(pid):
    """Kill process with given PID

    Args:
        pid (str) : PID to kill
    """
    try:
        with open(os.devnull, 'w') as nul:
            subprocess.Popen(KILL + [str(pid)], stdout=nul, stderr=nul)
    except WindowsError:
        log.info(CANT_EXECUTE % KILL)
        sys.exit(1)


def _activatePID(pid, enable_hotkeys):
    """Try to activate window associated with given process ID

    Args:
        pid (str) : PID of process to activate.
        enable_hotkeys (bool) : If True, Autohotkey will send "y" and "n"
            key presses to the prompt upon activating requested window.
    """
    try:
        log.debug("Activating %s -- enable_hotkeys = %s"
                  % (pid, enable_hotkeys))
        subprocess.Popen(ACTIVATE + [pid, str(enable_hotkeys)])
    except WindowsError:
        log.info(CANT_EXECUTE % ACTIVATE)


def query(process, pid, show_callback):
    """Query user to kill or show process.

    No invalid answers allowed.

    Args:
        process (str) : Process name
        pid (str) : Process PID
        show_callback (func(x)) : Ran when user answers "show"


    Answers:
        y : Kill process
        n : Do not kill process
        s : Try to show (activate) window linked to the process.

    Answering "show" does not exit the prompt.

    Returns:
        bool: True if yes, False if no.
    """
    question = " Kill process %s with PID %s [y/n/s]? " % (process, pid)
    sys.stdout.write(PREFIX + question)
    while True:
        answer = msvcrt.getch().lower()
        if answer == 'y':
            sys.stdout.write(answer+'\n')
            return True
        elif answer == 'n':
            sys.stdout.write(answer+'\n')
            return False
        elif answer == 's':
            sys.stdout.write(answer)
            show_callback(pid)
        else:
            sys.exit(1)


def open_explorer():
    """Open explorer.exe process."""
    # Just opening 'explorer.exe' merely launches a Windows Explorer window,
    # which is not the desired effect here.
    log.info("Re-opening %s" % EXPLORER)
    windir = os.environ['windir']
    subprocess.Popen(os.path.join(windir, EXPLORER))


def main():
    logging.basicConfig(format=PREFIX + ' %(message)s',
                        level=logging.INFO)

    args = docopt(__doc__, options_first=True, version=__version__)

    if args['--verbose']:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    name = args['<name>']
    quiet = args['-y']
    hotkeys = args['-s']

    activatePID = partial(_activatePID, enable_hotkeys=hotkeys)
    name_abspath = abspath(name)
    locks = find_locks(name_abspath)
    if not locks:
        log.info("Nothing locking %s" % name_abspath)
        sys.exit(0)

    for process, pid in locks:
        if not quiet:
            do_kill = query(process, pid, show_callback=activatePID)
            log.debug("User answered: %s" % do_kill)
            if do_kill is not True:
                continue
        kill(pid)
        if process == EXPLORER:
            time.sleep(0.1)
            open_explorer()

if __name__ == '__main__':
    main()

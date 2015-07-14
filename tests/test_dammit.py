import os
import dammit


def test_abspath_windows():
    relpath = "foo\\bar"
    assert dammit.abspath(relpath) == os.path.abspath(relpath)
    abspath = "c:\\foo\\bar"
    assert dammit.abspath(abspath) == abspath


def test_abspath_bash():
    relpath = "foo/bar"
    assert dammit.abspath(relpath) == os.path.abspath(relpath)
    abspath = "/c/foo/bar"
    assert dammit.abspath(abspath) == "c:\\foo\\bar"


def test_abspath_cygwin():
    abspath = "/cygdrive/c/foo/bar"
    assert dammit.abspath(abspath) == "c:\\foo\\bar"

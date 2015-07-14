import os
import pytest
import shutil

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


@pytest.fixture(scope="module")
def tmp_setup(request):
    os.mkdir('tmp')

    def tmp_teardown():
        shutil.rmtree('tmp')
    request.addfinalizer(tmp_teardown)


def test_quiet(tmp_setup):
    os.system('start tmp')
    assert os.system('dammit --verbose -y tmp') == 0

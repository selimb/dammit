# Dammit

> Used to express anger, irritation, contempt, or disappointment.

**dammit** is a Windows command-line utility to kill those pesky processes that are locking a file you want to delete.

![](docs/video.gif)

## Features

* No external dependencies. 
* Easy to [install](#installation)
* Support for `cmd`, `Cygwin`, `GnuNT Bash` and `Git Bash`.
* Answering `s` will attempt to activate the window associated with the to-be-killed process.
* Restarts `explorer.exe` if it needed to be killed (see [below](#explorer-was-not-restarted))
* Auto-updates (MAYA only)

## Installation

### Option 1: From T:\ drive (binary distribution)
This is the preferred installation method for employees at MAYA.

* Browse to `T:\selimb\dammit`.
* Run `install.bat`.

### Option 2: From source

* Clone the repo locally.
* You are probably going to want to remove `check_for_update()` and its call in `main.py`.
* `cd` into folder.
* Run `python setup.py install`.

## Options

Run `dammit -h` to get a list of the options:
* `-s`: enables "y" and "n" hotkeys after activating a window (by answering `s`) without Alt-Tabbing back to the terminal window. The appropriate command will be sent to the terminal you were using.
* `-y`: Kill without permission.

### Explorer was not restarted

`dammit` tries to start `explorer.exe` after it has been killed. However, it may occur that this is not executed properly. If this occurs, you can run the following to start `explorer.exe` again.
```
dammit --explorer
```


## Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/beselim/dammit/issues) to report any bugs or file feature requests.

## License

`dammit` itself is licensed under [MIT](LICENSE). However, this product includes vendorized versions of `docopt.py` and `Handle64.exe` -- the licenses for these is included in [3RD_PARTY](3RD_PARTY)

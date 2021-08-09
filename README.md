
Clone respository

```
$ git clone https://bitbucket.org/damufo/clasaua.git
$ cd clasaua
$ python -m venv .env
$ .env\Scripts\activate
$ python -m pip install --upgrade pip
$ python -m pip install pip-tools
$ pip-compile
$ pip-sync
```

Generate exe

```
$ pip install pyinstaller
$ pyinstaller_win.bat
```
# clasaua

# Intalación
Crear o contorno virtual python
```
$ apt-get install python3-venv
$ python3 -m venv .venv
$ source ./venv/bin/activate

```

```
$ echo "odfpy" > requirements.in
$ echo "reportlab" >> requirements.in
$ echo "pyinstaller" >> requirements.in
$ python -m pip install pip-tools && pip-compile
$ cat requirements.txt
```
Para actualizar unha dependencia
```
$ pip-compile -P reportlab==3.6.10
```
Co de arriba cambiaria reportlab á versión 3.6.10
```
$ pip-sync
```
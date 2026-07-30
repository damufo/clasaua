import sys
import shutil
from pathlib import Path
from datetime import datetime


if len(sys.argv) < 2:
    print("Uso: python post_copy.py <ruta_dist>")
    sys.exit()

#build_folder_name = Path(sys.argv[1])
print("sys.argv: {}".format(sys.argv[1]))

BASE = Path(__file__).resolve().parent
DIST = BASE / "dist_win"

if sys.argv[1] == "onefile":
    print("opcion onefile")

    if not (DIST / "clasaua.exe").exists():
        print("Non existe o ficheiro clasaua.exe")
        sys.exit()

    DEST = DIST / "clasaua_win64_{}_onefile".format(
        datetime.today().strftime('%Y%m%d')
    )
    # Eliminar o destino se xa existe
    if DEST.exists():
        print("Xa existe o cartafol clasaua_onefile")
        sys.exit()
        
    DEST.mkdir(parents=True)

    # Mover o executable
    (DIST / "clasaua.exe").replace(DEST / "clasaua.exe")
elif sys.argv[1] == "mac":
    print("opcion mac")
    # Eliminar o destino se xa existe
    DEST = DIST / "clasaua_mac"

    if not DEST.exists():
        print("Non existe o cartafol clasaua_mac")
        sys.exit()

    # Renomea o cartafol
    DEST.rename((DIST / "clasaua_win64_{}_mac".format(
            datetime.today().strftime('%Y%m%d'))))
    DEST = (DIST / "clasaua_win64_{}_mac".format(
            datetime.today().strftime('%Y%m%d')))
    
    

print("BASE: {}".format(BASE))
print("DEST: {}".format(DEST))

""" # Ficheiros na raíz
for f in ("prefs_tpl.ini", "venues.csv"):
    shutil.copy2(BASE / f, DEST / f) """

# Cartafoles completos
for d in ("images", "fonts"):
    dst = DEST / d
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(BASE / d, dst)


# Locale: só os .mo, conservando a estrutura de directorios
for mo in (BASE / "locale").rglob("*.mo"):
    rel = mo.relative_to(BASE / "locale")
    dst = DEST / "locale" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mo, dst)

print("end post_build")
# -*- mode: python -*-

# Isto indica como evitar que inclúa as bibliotecas tk/tcl
#https://stackoverflow.com/questions/36299712/how-do-i-exclude-tcl-tk-folders-in-my-pyinstaller-packed-app
import sys
sys.modules['FixTk'] = None

block_cipher = None

added_files = [
('.\\fonts', 'fonts'),
('.\\images', 'images'),
('.\\locale\\*.mo', 'locale')]
a = Analysis(['clasaua.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='clasaua',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='clasaua.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='clasaua')

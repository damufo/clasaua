# -*- mode: python ; coding: utf-8 -*-

#import sys
#sys.modules['FixTk'] = None

block_cipher = None

added_files = [
('.\\clubs.csv', '.'),
('.\\events.csv', '.'),
('.\\fonts', 'fonts'),
('.\\images', 'images'),
('.\\locale\\*.mo', 'locale')]

a = Analysis(
    ['clasaua.py'],
    pathex=['C:\\Users\\damufo\\Desktop\\clasaua'],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
    )
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
    )
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='clasaua',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=_True
    )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='clasaua_onedir')

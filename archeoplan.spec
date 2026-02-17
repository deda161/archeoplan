# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py', 'artifacts_manager.py', 'data_parser.py', 'graphic_creator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('symbols/*.png', 'images')
    ],
    hiddenimports=[],                     # скрытые импорты (если нужно)
    hookspath=[],
    runtime_hooks=[],
    excludes=[],                          # что исключить
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='archeoplan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # False для GUI
    icon='symbols/icon.ico'
)
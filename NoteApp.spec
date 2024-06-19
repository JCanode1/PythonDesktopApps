# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['NoteApp.py'],
             pathex=['C:\\Users\\josh\\Documents\\GithubRepos\\PythonDesktopApps'], 
             binaries=[],
             datas=[('notes.json', '.'), ('tools.py', '.')],
             hiddenimports=['tkinter', 'ttk', 'tkinter.messagebox', 'json', 'ttkbootstrap', 'markdown'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='NoteApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          output_mode='onefile'
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NoteApp')

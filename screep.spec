# -*- mode: python -*-
a = Analysis(['screep'],
             pathex=[],
             hiddenimports=['channels', 'encoders'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='screep',
          debug=False, # set to true for verbose exe at runtime
          strip=None,
          upx=True,
          console=True )

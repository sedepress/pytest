# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['phone_classifier.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'DrissionPage',
        'DrissionPage.ChromiumPage',
        'json',
        'os',
        're',
        'shutil',
        'zipfile',
        'datetime',
        'requests',
        'urllib3',
        'urllib.parse',
        'requests.packages.urllib3.contrib.socks',
        'socks',
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'websocket',
        'websockets',
        'chromedriver_autoinstaller',
        'webdriver_manager',
        'certifi',
        'idna',
        'chardet'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'tensorflow',
        'torch',
        'jupyter',
        'ipython'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='phone_classifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None
)

# For Windows, also create a one-folder version
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='phone_classifier'
)
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [
        'os',
        'time',
        'argparse',
        'threading',
        'googleapiclient',
        'google.oauth2',
        'httplib2',
        'src'
    ],
    'excludes': []
}

base = 'console'

executables = [
    Executable('main.py', base=base, target_name = 'py_drive_sync')
]

setup(name='py_drive_sync',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)

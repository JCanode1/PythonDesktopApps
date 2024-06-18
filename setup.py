from setuptools import setup

APP = ['test.py']

OPTIONS = {'packages': ['tkhtmlview', 'markdown', 'tkinter']}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

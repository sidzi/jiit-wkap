from distutils.core import setup

setup(name='WKAutomation',
      version='0.1',
      description='This is a piece of code to automate them trivial web kiosk jobs',
      author='Siddhant Gupta',
      py_modules=['app', 'automationModule'],
      packages=['utils'],
      install_requires=['splinter', 'easygui', 'bs4', 'openpyxl'],
      )

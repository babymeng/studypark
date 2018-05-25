from setuptools import setup, find_packages

setup(
    name            = "kekys",
    version         = "1.0.3",
    license         = "",
    py_modules      = ['kekys'],
    description     = "A common toolbox",
    author          = "kekys",
    author_email    = "kekys0123@gmail.com",
    url             = "https://github.com/babymeng/studypark/tree/studypark/python",
    packages        = find_packages(),
    package_data    = {
                       '': ['setup.sh'],
                       '': ['*.*'],
                       '':['*.sh'],
                       '':['*.txt'],
                       '':['*.json'],
                       },
    entry_points    = """
    [console_scripts]
    jsonfile = kekys:json_file
    jsonstr  = kekys:json_str
    """,
)

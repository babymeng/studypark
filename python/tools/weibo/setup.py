from setuptools import setup

setup(
    name            = "getsegs",
    version         = "1.0.1",
    py_modules      = ['getsegs'],
    license         = "",
    description     = "A common toolbox",
    author          = "kekys",
    author_email    = "kekys0123@qq.com",
    url             = "https://github.com/babymeng/studypark/tree/studypark/python",
    install_requires= [],
    entry_points    = """
    [console_scripts]
    getsegid        = getsegs:main
    """,
)

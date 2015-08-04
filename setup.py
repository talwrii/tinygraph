from setuptools import setup

setup(
    name = "tinygraph",
    version = "0.1",
    author = "Tal Wrii",
    author_email = "talwrii@gmail.com",
    description = "Library and command line for tiny graphs",
    license = "BSD",
    keywords = "xpm graphs",
    url = "https://gitlab.com/talwrii/tinygraph",
    requires=['xpm'],
    py_modules=['tinygraph'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: BSD License",
    ],
)

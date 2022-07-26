# PyEncrypt

This is a python script aimed at converting .py files (not just a single file) in projects into .pyd files on Windows system (or .so files on Linux system).

After converting, the .pyd files and .so files can be imported by Python just like regular .py files. And you can get performance increase by calling .pyd (or .so) files.


## Package Requirements

The script needs Cython and some compile toolchains to compile. 

You may already came across the following error message on Windows. This could be caused if you don't have the compile toolchains and try to install Cython through pip.

```
error: Microsoft Visual C++ 14.0 or greater is required.
```

Anyway here is a solution. On Windows I recommend using conda to install Cython and relevant toolchains by following commands:

```bash
conda install cython
conda install libpython m2w64-toolchain -c msys2
```

The second command is cited from https://stackoverflow.com/a/63359548.


## Get Started

Download the encrypt.py file and execute the file in command line. Pass arguments to specify working directory and exception path if necessary.

```bash
python encrypt.py -w "working directory" -e "exception path"
```

The __working directory__ is the directory that the script will work on to encrypt all the .py files in it. By defalut it is the current working directory.
The __exception paths__ are directories or file paths that you don't want to encrypt. If you have multiple directories or file paths, separate them by spaces.

After encrypting, all the pyd files should resides in "build" directory as the following example. The script itself won't be encrypted.

```bash
└── YOUR PROJECT
    ├── build
    │   ├── model
    │   │   ├── model.pyd
    │   │   └── ...
    │   ├── utils
    │   │   ├── loss.pyd
    │   │   └── ...
    │   ├── train.pyd
    |   └── ...
    |
    ├── model
    │   ├── __init__.py
    │   ├── model.py
    │   └── ...
    ├── utils
    │   ├── __init__.py
    │   ├── loss.py
    │   └── ...
    ├── train.py
    ├── encrypt.py
    └── ...
```

If you find some .pyd files aren't in the right subfolders, it probably because you are missing a \_\_init__.py in the module folder.


## Acknowledgement

The script is inspired by the following blog and repository:
https://zhuanlan.zhihu.com/p/83687939
https://github.com/Pranjalab/pyencrypt

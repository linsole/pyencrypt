import os, time, platform
from argparse import ArgumentParser
from setuptools import setup
from Cython.Build import cythonize

class Encryptor():
    def __init__(self, work_dir=".", build_dir="build", except_path=[]):
        # platform consistency
        if platform.system() == "Windows":
            self.suffix = "pyd"
        elif platform.system() == "Linux":
            self.suffix = "so"
        else:
            raise Exception("Platform not supported! Currently supports: Windows and Linux.")

        self.start_time = time.time()

        self.work_dir = work_dir
        self.build_dir = build_dir
        self.except_path = [os.path.abspath(path) for path in except_path]
        self.except_path.append(os.path.abspath(self.build_dir)) # to be discussed
        
        self.py_file_list = []

    def traverse(self, base_path=None, clean=False):
        if base_path is None:
            base_path = self.work_dir

        for path in os.listdir(base_path):
            full_path = os.path.join(base_path, path)

            if os.path.abspath(full_path) in self.except_path:
                continue

            elif os.path.isdir(full_path):
                if not path.startswith("."):
                    self.traverse(full_path, clean)

            elif os.path.isfile(full_path):
                path_name_split = path.split(".")
                if clean and path_name_split[-1] in ("c", "o", "def") \
                    and os.stat(full_path).st_mtime > self.start_time:
                    os.remove(full_path)

                elif path_name_split[-1] in ("py", "pyx") and not path.startswith("__") \
                    and path != __file__.split("\\")[-1] and path != __file__.split("/")[-1]:
                    self.py_file_list.append(full_path)
            

    def rename(self, base_path):
        for path in os.listdir(base_path):
            full_path = os.path.join(base_path, path)
            if os.path.isdir(full_path):
                self.rename(full_path)
            
            if os.path.isfile(full_path):
                path_name_split = path.split(".")
                if path_name_split[-1] == self.suffix:
                    rename_path = os.path.join(base_path, path_name_split[0]+"."+self.suffix)
                    os.rename(full_path, rename_path)


    def encrypt(self):
        # traverse directories, find py fils and compile
        self.traverse()
        setup(ext_modules=cythonize(self.py_file_list, language_level = "3"), \
            script_args=["build_ext", "-b", self.build_dir])
        
        # clean up intermediate files
        self.traverse(clean=True)

        # rename pyd files (or .so files)
        self.rename(self.build_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-w", default=".", help="Working directory which you want to \
        encrypt", required=False)
    parser.add_argument("-e", default=[], nargs='*', help="Exception directories and files \
        that you don't want to encrypt", required=False)
    args = vars(parser.parse_args())
    
    encryptor = Encryptor(work_dir=args["w"], except_path=args["e"])
    encryptor.traverse()
    print("\n".join(encryptor.py_file_list))
    print(len(encryptor.py_file_list))
    # encryptor.encrypt()

import os, time, platform
from argparse import ArgumentParser
from setuptools import setup
from Cython.Build import cythonize

class Encryptor():
    def __init__(self, work_dir=".", build_dir="build", except_path=[]):
        # cross platform consistency
        if platform.system() == "Windows":
            self.suffix = "pyd"
        elif platform.system() == "Linux":
            self.suffix = "so"
        else:
            raise Exception("Platform not supported! Currently supports: Windows and Linux.")

        # indicates the beginning of encrypting, for later use to clean up intermediate files
        self.start_time = time.time()

        self.work_dir = work_dir
        self.build_dir = build_dir
        self.except_path = [os.path.abspath(path) for path in except_path]
        self.except_path.append(os.path.abspath(self.build_dir))
        
        self.py_file_list = []

    def traverse(self, base_path=None, clean=False):
        # defalut of base_path is working directory
        if base_path is None:
            base_path = self.work_dir

        for path in os.listdir(base_path):
            full_path = os.path.join(base_path, path)

            # use absolute path to judge if current path is in exception path
            if os.path.abspath(full_path) in self.except_path:
                continue

            elif os.path.isdir(full_path):
                if not path.startswith("."):
                    self.traverse(full_path, clean) # recurssively traverse

            elif os.path.isfile(full_path):
                path_name_split = path.split(".")
                if clean and path_name_split[-1] in ("c", "o", "def") \
                    and os.stat(full_path).st_mtime > self.start_time:
                    os.remove(full_path) # clean up intermediate files

                elif not clean and path_name_split[-1] in ("py", "pyx") and not path.startswith("__") \
                    and path != __file__.split("\\")[-1] and path != __file__.split("/")[-1]:
                    self.py_file_list.append(full_path)
            

    def rename(self, base_path=None):
        # recurssively traverse and rename generated .pyd files
        # (for example: rename utils.cp38-win_amd64.pyd to utils.pyd)
        if base_path is None:
            base_path = self.build_dir

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
        self.rename()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-w", default=".", help="Working directory which you want to \
        encrypt", required=False)
    parser.add_argument("-e", default=[], nargs='*', help="Exception directories and files \
        that you don't want to encrypt", required=False)
    parser.add_argument("-b", default="build", help="Build directory of the encrypted \
        files", required=False)
    args = vars(parser.parse_args())
    
    # start encryption
    encryptor = Encryptor(work_dir=args["w"], except_path=args["e"], build_dir=args["b"])
    encryptor.encrypt()

    # show encrypted files
    print("\nEncrypted files:")
    print("\n".join(encryptor.py_file_list))
    print(f"{len(encryptor.py_file_list)} files in total.\n")
    print(f"ENCRYPTION COMPLETE!\nThe results are in: {args['b']}\n")
    
import os
import sys
import shutil
import importlib
import importlib.util

class LibraryNotFoundError(Exception):
    def __init__(self, message='Library folder does not exists.'):
        self.message = message
        super().__init__(self.message)

class NotOwnedByPythonLibError(Exception):
    def __init__(self, message='Can not delete a library that it is not added by PythonLib'):
        self.message = message
        super().__init__(self.message)

class _PythonLib:
    def __init__(self, lib_path: str=None):
        self.lib_path = lib_path
        if self.lib_path == None:
            for p in sys.path:
                if os.path.basename(p).lower() == 'lib' and 'win32' not in p.split(os.sep):
                    self.lib_path = p
        
        self.meth_path = __file__.split(os.path.sep)
        self.meth_path = self.meth_path[:-1]

        temp = ''
        for i in self.meth_path:
            temp += i + os.path.sep
        self.meth_path = temp[:-1]

        libs_path = os.path.join(self.lib_path,__name__,'libs')
        if not os.path.exists(libs_path):
            with open(libs_path, 'w') as f:
                pass

        with open(libs_path,'r') as f:
            self.libs = f.read().split('\n')
        if len(self.libs) != 0 and self.libs[-1] == '\n':
            self.libs = self.libs[:-1]

    def add_file(self, file_path: str, ignore_safety_process_password=None, new_filename: str='__init__.py', aftl_password=None, aftl_lib_name=None):
        '''
        Creates a library called the same as the file specified.

        returns path to the library.
        '''
        if ignore_safety_process_password != 'ISPS':
            x = ''
            while x.lower() != 'y':
                x = input('User needs to confirm for safety (Y\\N) - ')
                if x.lower() == 'n':
                    return

        with open(file_path, 'r') as f:
            lines = f.readlines()

        if aftl_password == 'sfw':
            path = os.path.join(self.lib_path, aftl_lib_name)
        else:
            path = os.path.join(self.lib_path, os.path.splitext(os.path.basename(file_path))[0])

            if os.path.exists(path): # useful to not replace built-in stuff like http and asyncio
                raise BaseException('Can\'t replace a library.')
            else:
                os.mkdir(path)

        with open(os.path.join(path, new_filename), 'w+') as f:
            for line in lines:
                f.write(line)
        if aftl_password != 'sfw':
            self.save_to_libs(os.path.basename(path))
        elif not os.path.exists(path):
            raise FileNotFoundError('Library path does not exists')

        return path

    def save_to_libs(self, foldername: str): # i can't make it private so it's kinda fucked up
        '''
        This should be private but it's not possible in python with my knowledge
        '''
        path = os.path.join(self.meth_path,'libs')
        with open(path, 'r') as f:
            content = f.read()

        file = os.path.join(self.lib_path, os.path.basename(foldername))
        with open(path, 'w') as f:
            f.write(content)
            f.write(file+'\n')

        file = file.replace('\n','')
        if file not in self.libs:
            self.libs.append(file)

    def delete_lib(self, lib_name: str):
        '''
        Completly deletes the specified library if it's added by PythonLib.
        '''
        path = os.path.join(self.lib_path, lib_name)
        if path not in self.libs:
            raise NotOwnedByPythonLibError

        with open(os.path.join(self.meth_path, 'libs'), 'r') as r:
            libs_src = r.read().split('\n')
            if len(libs_src) != 1 and libs_src[-1] == '\n' or libs_src[-1] == '':
                libs_src = libs_src[:-1]

        with open(os.path.join(self.meth_path, 'libs'), 'w') as w:
            try:
                if len(libs_src) > 1:
                    if len(libs_src) > libs_src.index(path)+1:
                        after_path = libs_src[libs_src.index(path)+1:]
                    else:
                        after_path = []

                    for i in libs_src[:libs_src.index(path)]+after_path:
                        w.write(i+'\n')
            except ValueError:
                for i in libs_src:
                    w.write(i+'\n')
                raise BlockingIOError('Could not delete lib path from libs file')

        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            with open(os.path.join(self.meth_path, 'libs'), 'w') as w:
                for i in libs_src:
                    w.write(i+'\n')

        self.libs.remove(path)

    def add_file_to_lib(self, lib_name, file_path: str, ignore_safety_process_password=None):
        '''
        Adds file to library if library exists.
        '''
        return self.add_file(file_path, ignore_safety_process_password, os.path.basename(file_path), aftl_password='sfw', aftl_lib_name=lib_name)

    def open_folderlib(self, foldername: str):
        '''Works only on Windows: opens the explorer in the lib folder'''
        lib = self.find_lib(foldername)
        if lib == False:
            raise BaseException('Folder not found')
        
        if os.name != 'nt': # windows
            os.startfile(lib)
        else:
            print('WARNING: this function only works on windows and because of that, it will only return the path.')
        return lib

    def find_lib(self, lib_name: str):
        '''returns a path if lib exists if it does not exists then returns false'''
        for lib in os.listdir(self.lib_path):
            if lib_name == lib:
                return os.path.join(self.lib_path, lib)
        return False

    def __import__(self, lib_name: str, filename: str, extra_path: str=None):
        '''
        just use "import yourlibname.yourextrapathifnotnone.yourfilename".
        
        BUT if for some reason you need to use __name__ instead of using your
        library name, then this is perfect for you.
        '''
        lib_path = self.find_lib(lib_name)
        if not os.path.exists(lib_path):
            raise LibraryNotFoundError

        if extra_path != None:
            lib_path = os.path.join(lib_path, extra_path)

        if lib_path not in sys.path:
            sys.path.append(lib_path)

        module = importlib.__import__(filename)
        sys.path.remove(lib_path)
        return module

PythonLib = _PythonLib()

def find_extension(filename: str, file_path: str='.', ignore_extensions: list=[]):
    '''
    Finds the specified file name extension inside the specified path.
    
    returns the full file path with the file name and with the file extension, all together in a string.
    '''
    files = os.listdir(file_path)
    for file in files:
        if '.' in file:
            file = file[::-1]
            extension = file[:file.index('.')][::-1]
            file = file[file.index('.')+1:][::-1]
            if file == filename and extension not in ignore_extensions:
                extension = '.'+extension
                break
            else:
                raise BaseException('Could not find extension')
    return file_path+os.path.sep+file+extension

if os.name == 'nt':
    if importlib.util.find_spec('win32con') and importlib.util.find_spec('win32api') and importlib.util.find_spec('keyboard'):
        mouse = PythonLib.__import__(__name__, 'win_mouse', 'windows')
    else:
        class _:
            def __init__(self):
                pass
            def __repr__(self):
                misses = []
                if not importlib.util.find_spec('win32con'):
                    misses.append('win32con')
                if not importlib.util.find_spec('win32api'):
                    misses.append('win32api')
                if not importlib.util.find_spec('keyboard'):
                    misses.append('keyboard')
                if len(misses) == 1:
                    print('Missing ' + misses[-1])
                else:
                    out = 'Missing '
                    for i in misses:
                        if i == misses[-1]:
                            out = out[:-2]
                            out += ' and ' + i
                        else:
                            out += i + ', '
                    print(out)
                if 'win32con' in misses or 'win32api' in misses:
                    print('use pip install pypiwin32 to get win32con and/or win32api')
                if 'keyboard' in misses:
                    print('use pip install keyboard to get keyboard module')
                return ''
        mouse = _()
        del _

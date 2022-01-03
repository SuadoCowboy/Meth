import os
import Meth

def main():
    lib = Meth.PythonLib.find_lib(__name__)
    if lib != False and os.path.exists(os.path.join(lib,'hell_of_world.py')):
        print(1)
        module = Meth.PythonLib.__import__(__name__, 'hell_of_world')
        module.helloworld()
    else:
        print(0)

if __name__ == '__main__':
    main()
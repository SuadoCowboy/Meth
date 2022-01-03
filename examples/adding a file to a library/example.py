import Meth
import os
import importlib

message = 'Press ENTER to continue...: '

# if the user changes the file name it will get the current name.
libname = os.listdir('folder')[0].replace('.py','')

# If anything goes wrong at the end it will delete the library.
try:
    # using another directory so that it doesn't conflict with the library itself when importing.
    Meth.PythonLib.add_file(os.path.join('folder', libname+'.py'))

    input(message)

    # prints on console the path to the library
    print(Meth.PythonLib.find_lib(libname))

    input(message)

    if not os.path.exists(os.path.join(Meth.PythonLib.find_lib(libname), 'hell_of_world.py')): 
        example = importlib.__import__(libname)
        example.main()
        Meth.PythonLib.add_file_to_lib(libname,'hell_of_world.py')

    input(message)

    if os.path.exists(os.path.join(Meth.PythonLib.find_lib(libname), 'hell_of_world.py')):
        example = importlib.__import__(libname)
        example.main()

    input(message)
except:
    pass

# deletes the library because the example has already been shown
Meth.PythonLib.delete_lib(libname)
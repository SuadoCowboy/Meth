import Meth
import os

message = 'Press ENTER to continue...: '

try:
    print('If you want to see everything running then open your OS explorer and go to the following path:', Meth.PythonLib.lib_path, f'and right after that, you can after each \"{message}\", see inside the directory, the example library appearing and disappearing.')
    
    input(message)

    # creates the library
    Meth.PythonLib.add_file(os.path.join('folder','library_example.py'))
    
    input(message)
    
    # imports the library from python library directory
    import library_example
    
    input(message)

    #  deletes the library from python library directory
    Meth.PythonLib.delete_lib('library_example')
    
    input(message)

    # tries to import the library but an expected error occurs
    try:
        import library_example
        print('Library sucessfully imported... This should not have worked.')
    except ImportError:
        print('Could not import library, because it does not exists.')
except Exception as e:
    print('An unexpected error ocurred:', e)
    if Meth.PythonLib.find_lib('library_example') != False:
        Meth.PythonLib.delete_lib('library_example')
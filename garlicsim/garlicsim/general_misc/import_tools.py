'''tododoc'''

import os.path
import imp
from garlicsim.general_misc import package_finder

def import_by_path(path):
    '''Import module/package by path.'''
    name = os.path.splitext(os.path.split(path)[1])[0]
    path_to_dir = os.path.dirname(path)
    try:
        (my_file, pathname, description) = imp.find_module(name, [path_to_dir])
        print((my_file, pathname, description))
        module = imp.load_module(name, my_file, pathname, description)
    finally:
        my_file.close()
        
    return module
    

def import_all(package, exclude='__init__'):
    '''tododoc'''
    
    paths = package_finder.get_packages_and_modules_filenames(path)
    
    names = {}
    for path in paths:
        name = os.path.splitext(os.path.split(path)[1])[0]
        if name == exclude:
            continue
        names[path] = name
        
    d = {}
    
    for (path, name) in names.items():
        d[name] = import_by_path(path)
    
    return d
        
    
    
        
    
    
    


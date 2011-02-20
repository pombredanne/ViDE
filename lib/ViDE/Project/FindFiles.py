def __AllXxxIn_flat( directory, xxx ):
    return glob.glob( os.path.join( directory, "*." + xxx ) )

def __AllXxxIn_recursive( directory, xxx ):
    l = []
    for path, dirs, files in os.walk( directory ):
        for fileName in fnmatch.filter( files, "*." + xxx ):
            l.append( os.path.join( path, fileName ) )
    return l

def AllXxxIn( directory, xxx, recursive ):
    if recursive:
        return __AllXxxIn_recursive( directory, xxx )
    else:
        return __AllXxxIn_flat( directory, xxx )

def AllCppIn( directory, recursive = True ):
    return AllXxxIn( directory, "cpp", recursive ) + AllXxxIn( directory, "c", recursive )

def AllHppIn( directory, recursive = True ):
    return AllXxxIn( directory, "hpp", recursive ) + AllXxxIn( directory, "h", recursive )

def AllIppIn( directory, recursive = True ):
    return AllXxxIn( directory, "ipp", recursive )

def AllPyIn( directory, recursive = True ):
    return AllXxxIn( directory, "py", recursive )

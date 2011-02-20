from ViDE.Project.Description import *

# Implicit source, implicit object
CppExecutable(
    name = "hello1",
    sources = [ "hello1.cpp" ]
)

# Explicit source, implicit object
source2 = CppSource( "hello2.cpp" )
CppExecutable(
    name = "hello2",
    sources = [ source2 ]
)

# Implicit source, explicit object
object3 = CppObject( "hello3.cpp" )
CppExecutable(
    name = "hello3",
    sources = [],
    objects = [ object3 ]
)

# Explicit source, explicit object
source4 = CppSource( "hello4.cpp" )
object4 = CppObject( source4 )
CppExecutable(
    name = "hello4",
    sources = [],
    objects = [ object4 ]
)

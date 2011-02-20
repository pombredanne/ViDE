from ViDE.Project.Description import *

# Implicit source, implicit object
Executable(
    name = "hello1",
    sources = [ "hello1.cpp" ]
)

# Explicit source, implicit object
source2 = Source( "hello2.cpp" )
Executable(
    name = "hello2",
    sources = [ source2 ]
)

# Implicit source, explicit object
object3 = Object( "hello3.cpp" )
Executable(
    name = "hello3",
    sources = [],
    objects = [ object3 ]
)

# Explicit source, explicit object
source4 = Source( "hello4.cpp" )
object4 = Object( source4 )
Executable(
    name = "hello4",
    sources = [],
    objects = [ object4 ]
)

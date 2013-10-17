// Standard library
#include <string>

// Boost
#include <boost/python.hpp>
namespace bp = boost::python;

std::string foo(std::string s) {
    return "Hello, " + s + "!";
}

BOOST_PYTHON_MODULE(c1) {
    bp::def("foo", foo);
}

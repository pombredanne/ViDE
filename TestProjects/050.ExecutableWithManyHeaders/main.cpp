#include <iostream>
#include <map>
#include <list>

#include "a.hpp"

int main() {
    std::map< std::list< int >, int > map; // Ensure that compilation of this file is longer than compilation of other files
    std::cout << "Hello, World!" << std::endl;
}

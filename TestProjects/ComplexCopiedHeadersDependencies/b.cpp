#include "b1.hpp"
#include "b2.hpp"

#include <a1.hpp>

void B1::f() {
    A1().f();
}

void B2::f() {
    A2().f();
}

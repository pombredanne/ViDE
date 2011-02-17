#include <a.hpp>

struct B {
    void f() {
        A().f();
    }
};

#ifdef BUILD_A
    #define A_API __declspec(dllexport)
#else
    #define A_API __declspec(dllimport)
#endif

struct A {
    A_API void f();
};

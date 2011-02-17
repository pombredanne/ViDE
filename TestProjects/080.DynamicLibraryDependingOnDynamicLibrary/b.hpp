#ifdef BUILD_B
    #define B_API __declspec(dllexport)
#else
    #define B_API __declspec(dllimport)
#endif

struct B {
    B_API void f();
};

#if defined(WIN32) || defined(cygwin)
    #ifdef BUILD_A
        #define A_API __declspec(dllexport)
    #else
        #define A_API __declspec(dllimport)
    #endif
#else
    #define A_API
#endif

struct A {
    A_API void f();
};

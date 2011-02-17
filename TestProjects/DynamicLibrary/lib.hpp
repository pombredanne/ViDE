#ifdef BUILD_HELLO
    #define HELLO_API __declspec(dllexport)
#else
    #define HELLO_API __declspec(dllimport)
#endif

HELLO_API void f();

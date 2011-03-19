#if defined(WIN32) || defined(cygwin)
    #ifdef BUILD_HELLO
        #define HELLO_API __declspec(dllexport)
    #else
        #define HELLO_API __declspec(dllimport)
    #endif
#else
    #define HELLO_API
#endif

HELLO_API void f();

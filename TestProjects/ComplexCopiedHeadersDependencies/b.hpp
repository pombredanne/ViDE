#if defined(WIN32) || defined(cygwin)
    #ifdef BUILD_B
        #define B_API __declspec(dllexport)
    #else
        #define B_API __declspec(dllimport)
    #endif
#else
    #define B_API
#endif

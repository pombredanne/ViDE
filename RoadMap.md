vide draw autodepgraph

Focus on your code, let ViDE do peripheral tasks (list them) for you, in a uniform way (list axes)

Automatic dependencies (from #include): use Boost.Wave ? In the same process => export it to python
Buildkits: gcc_cygwin msvc gcc_darwin gcc_linux gcc_mingw
Fix division by zero in ExecutionReport.__computeOptimalTranscale when duration is null

Measure autotest coverage

vide gen_makefile
vide gen_batch: generate a batch to build the project
those commands shall allow to bootstrap installation of ViDE

Artifacts:
    Compile python code: import py_compile
    StaticLibrary
    HeaderLibrary

Buildkits have a function
    system-on-which-they-run --> list-of-possible-target-systems
=> keep a fixed list of existing systems/platforms, etc.
=> build in project/build/commitId (with optional '+' if commit is not clean) or HEAD/buildkit_buildsystem_target_platform/bin
    
Make:
    -n -j -k
    --always-make
    --assume-old, -o
    --assume-new, --what-if, -W
    --touch, -t
    in a subdirectory of the project: build only what depends on this directory ?

Static code analysis
    statistics/metrics
        SLOC
        cyclotomic complexity
    security
    reverse engineering

See:
    CruiseControl, Hudson
    FitNesse
    Robot Framework

Code generation from templates
Test running and coverage measurement
Coding rules checking
    
See in Ship it! the list of basic tools needed for software development
Build system
continuous build
continuous integration
    automatic merge of feature branches
workflow
    tickets
    branches
communication
    website
        wiki (stored in source code)
        documentaiton
    push
        mail
        RSS
    graphical views of the project
        dependency graph
        include graph
third-party software management
language multiplicity management
    uniform debuger launching
    easy integration
        tools, links to how-tos
profilling
mock/stub

        
ViDE bug/ViDE roadmap
    distributed
    know what commit is supposed to fix the bug
    ? know what commit introduced the bug ?
    plan releases
    task dependency
    interract with git-flow
    tasks, feature request, bug reports
    
Uniformity: languages, platforms, shells (bash, zsh, cygwin, cmd), developers, projects, library versions, compilers

Languages: Java, Perl, Tcl, C#, etc.

SCM, Delivery, Build, TEst, Continuous integration, Publication, Documentation, Roadmap, Editor

vide daemon
    a web service to be called by github
        vide make for all builkits running on the platform
        vide release --all (for not-yet-released tagged commits)
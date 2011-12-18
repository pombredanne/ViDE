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

In Project.Description, replace CppStaticLibrary by CPlusPlus.StaticLibrary (same thing for other LanguageArtifacts)

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

        
From old papers on 2011/11/27
=============================

Manage toolsets as a reference toolset plus deltas

Put sha1 in the path of the build

Test + coverage + static analysis + profiling

Code skeletons (classes, modules, inter-language interfaces, etc.)

Manage the association between buildkits and target platforms

Besoin de -l:
    - transmis de .o à .a, de .cpp à .o, de .hpp à .o
    - intercepté par .dll
Besoin de -I:
    - transmis de .hpp à .o, de .cpp à .o, de .hpp à .hpp <= bof
    
Descendre la dependence vers les lib dans les Objects: les -l seront plus facile à gérer pour Fortran, C++, PythonModule, etc.
    - class Linkable pour Objects et LibraryBinary ?
    - class LinkedBinary ?
    - un design à coup de policies pour la transitivité des -l ? Evite l'héritage trop multiple. Et evite d'imposer la même transitivité à tous les builkits
Et comment on gère les HEaderLibs qui dépendent d'une lib avec des binaires ?
=> Une notion de "J'aurai besoin d'une lib au link", transitive (tous) ou pas (dll).

Et attention à l'ordre des -l

OU ALORS (explicite vs. pratique)

Un mapping header -> binaire, et on détecte les -l nécessaires en fonction des include
    - plus besoin de localLibs ni externalLibs
    - attention transitif pour les StaticLibs
    - attention dépendances cachées => cycles en vue

Release
    - tag/branch
    - compilation/tarball
    - tarball des sources
    - upload sur vjnet
    - etre capable de rebuilder une release
        => tager d'abord, puis un process qui build une release donnée en fonction du tag

Generate makefile
Generate Visual Studio solution
Generate auto-make files

Artifacts for generated code

Vide <-> Ship it!
    - cf figure 1.1 page  5 of Ship It!
    - "daily meeting" and "the list" => ViDE roadmap
    - "code change notifier" => git hook + ViDE deamon
    - "the list" and "code change notifier" => mailing lists
    - "connect interfaces" => multilanguage facilities "polyglot"
    - "write & run tests" => ViDE selftest, ViDE test
    - "track features" and "track issues" => ViDE roadmap + ViDE flow
    - "continuous build" => ViDE deamon
    - "script build" => ViDE make
    
Cross compilation
Documentation => alive + Draw*
Continuous integration (a lot more than continuous build: integrate branches early) => ViDE deamon
Delivery => ViDE release
Debug => ViDE debug


ViDE roadmap
    bug tracker distribué
    savoir quel commit fix un bug
    planifier les release
    gerer les dépendances des taches
    interaction avec git-flow
    gestion des taches, features, bugs
    
documentation wiki-style mais dans le code, modifiable en ligne comme un wiki, ou modifiable dans le code

# Boost 安裝指引

## 作業程序


### 安裝所有需引用 libs

```sh
vcpkg install boost glog opencc yaml-cpp leveldb gtest --triplet x64-windows
```

驗證查檢：

```sh
vcpkg list
```

### 執行 CMake

```sh
cmake -G Ninja -Wno-dev ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  -DVCPKG_TARGET_TRIPLET=x64-windows ^
  ..  
```

```sh
cmake -G "Visual Studio 17 2022" -Wno-dev ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  -DVCPKG_TARGET_TRIPLET=x64-windows ^
  ..  
```

```sh

C:\Users\AlanJui\source\repos\librime\build>cmake -G Ninja -Wno-dev ^
More?   -DCMAKE_BUILD_TYPE=Release ^
More?   -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
More?   -DVCPKG_TARGET_TRIPLET=x64-windows ^
More?   ..
-- Could NOT find Boost (missing: Boost_INCLUDE_DIR) (Required is at least version "1.77.0")
CMake Error at cmake/FindGlog.cmake:22 (message):
  Could not find glog library.
Call Stack (most recent call first):
  CMakeLists.txt:80 (find_package)


-- Configuring incomplete, errors occurred!

```

### 設定好 env.bat

```sh
rem Customize your build environment and save the modified copy to env.bat

set RIME_ROOT=%CD%

rem REQUIRED: path to Boost source directory
if not defined BOOST_ROOT set BOOST_ROOT=%RIME_ROOT%\deps\boost-1.84.0

rem architecture, Visual Studio version and platform toolset
set ARCH=Win32
REM set BOOST_ROOT=C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0
set BJAM_TOOLSET=msvc-14.3
REM set CMAKE_GENERATOR=Ninja
set CMAKE_GENERATOR="Visual Studio 17 2022"
set PLATFORM_TOOLSET=v143

rem OPTIONAL: path to additional build tools
REM set DEVTOOLS_PATH=C:\Program Files\CMake\bin;C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja
```

### 製作 Boost Headers  

```sh
C:\Users\AlanJui\source\repos\librime>cd deps\boost-1.84.0

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>.\b2 headers
Performing configuration checks

    - default address-model    : none (cached) [1]
    - default architecture     : none (cached) [1]
    - symlinks supported       : no  (cached)
    - junctions supported      : yes (cached)
    - hardlinks supported      : yes (cached)

[1] msvc-14.3
...found 1244 targets...

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>dir
 Volume in drive C is Windows
 Volume Serial Number is 2EB5-AA68

 Directory of C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0

2025/03/03  上午 11:06    <DIR>          .
2025/03/03  上午 11:05    <DIR>          ..
2023/12/14  上午 07:03    <DIR>          .circleci
2023/12/14  上午 07:03             4,013 .gitattributes
2023/12/14  上午 07:03    <DIR>          .github
2023/12/14  上午 07:03               173 .gitignore
2023/12/14  上午 07:03            19,713 .gitmodules
2023/12/14  上午 07:03             3,726 .travis.yml
2023/12/14  上午 07:03             1,253 appveyor.yml
2025/03/03  上午 11:06           263,168 b2.exe
2025/03/03  上午 11:06    <DIR>          bin.v2
2025/03/03  上午 11:07    <DIR>          boost
2023/12/14  上午 07:03               868 boost-build.jam
2023/12/14  上午 07:03             1,054 boost.css
2023/12/14  上午 07:03             6,308 boost.png
2023/12/14  上午 07:03            20,919 boostcpp.jam
2023/12/14  上午 07:03             2,584 bootstrap.bat
2023/12/14  上午 07:03            10,811 bootstrap.sh
2023/12/14  上午 07:03               841 CMakeLists.txt
2023/12/14  上午 07:03    <DIR>          doc
2023/12/14  上午 07:03               794 index.htm
2023/12/14  上午 07:03             6,172 index.html
2023/12/14  上午 07:03               298 INSTALL
2023/12/14  上午 07:03            12,574 Jamroot
2023/12/14  上午 07:03    <DIR>          libs
2023/12/14  上午 07:03             1,361 LICENSE_1_0.txt
2023/12/14  上午 07:06    <DIR>          more
2025/03/03  上午 11:06               154 project-config.jam
2023/12/14  上午 07:03               552 README.md
2023/12/14  上午 07:03             2,757 rst.css
2023/12/14  上午 07:03    <DIR>          status
2023/12/14  上午 07:03    <DIR>          tools
              21 File(s)        360,093 bytes
              11 Dir(s)  1,509,507,874,816 bytes free

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>

```

### 使用 vcpkg 安裝 Boost

```sh
C:\Users\AlanJui\source\repos\librime>vcpkg install boost
Computing installation plan...
The following packages will be built and installed:
    boost:x64-windows@1.86.0#1
Detecting compiler hash for triplet x64-windows...
Compiler found: C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.43.34808/bin/Hostx64/x64/cl.exe
Restored 1 package(s) from C:\Users\AlanJui\AppData\Local\vcpkg\archives in 90.7 ms. Use --debug to see more details.
Installing 1/1 boost:x64-windows@1.86.0#1...
Elapsed time to handle boost:x64-windows: 966 ms
boost:x64-windows package ABI: 16b9717794be5b6c1801b66ae21ea36b90718667c66859afbb067cfc5111b0f1
Total install time: 976 ms
```





### 建置第三方程式舘

```sh
C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>cd ..\..

C:\Users\AlanJui\source\repos\librime>
```

```sh
rem Customize your build environment and save the modified copy to env.bat

set RIME_ROOT=%CD%

rem REQUIRED: path to Boost source directory
set BOOST_ROOT=C:\bin\vcpkg\installed\x64-windows
if not defined BOOST_ROOT set BOOST_ROOT=%RIME_ROOT%\deps\boost-1.84.0

rem architecture, Visual Studio version and platform toolset
REM set ARCH=Win32
set BJAM_TOOLSET=msvc
set CMAKE_GENERATOR=Ninja
REM set CMAKE_GENERATOR="Visual Studio 17 2022"
set PLATFORM_TOOLSET=v143

rem OPTIONAL: path to additional build tools
set DEVTOOLS_PATH=C:\Program Files\CMake\bin;C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja
```

```sh
vcpklg install boost glog opencc yaml-cpp leveldb GTest
```


```sh
cmake -G Ninja -Wno-dev ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  -DCMAKE_PREFIX_PATH=C:/bin/vcpkg/installed/x64-windows ^
  -DLIBRIME_BUILD_TEST=OFF ^
  -DLIBRIME_ENABLE_LOGGING=ON ^
  -DBUILD_SHARED_LIBS=ON ..
```

```sh
cmake -G Ninja -Wno-dev ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  -DCMAKE_TARGET_TRIPLET=x64-windows ..
```



```sh
-- Found gflags: C:/bin/vcpkg/installed/x64-windows/lib/gflags.lib
-- Found glog: C:/bin/vcpkg/installed/x64-windows/lib/glog.lib
-- Found yaml-cpp: C:/bin/vcpkg/installed/x64-windows/lib/yaml-cpp.lib
-- Found leveldb: C:/bin/vcpkg/installed/x64-windows/lib/leveldb.lib
-- Found marisa: C:/bin/vcpkg/installed/x64-windows/lib/libmarisa.lib
-- Found opencc: C:/bin/vcpkg/installed/x64-windows/lib/opencc.lib
-- Found X11/keysym.h at C:/Users/AlanJui/source/repos/librime/include
-- rime_plugins_libs:
-- rime_plugins_modules:
true
-- Configuring done (0.3s)
-- Generating done (0.2s)
-- Build files have been written to: C:/Users/AlanJui/source/repos/librime/build

C:\Users\AlanJui\source\repos\librime\build>cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..
-- Found gflags: C:/bin/vcpkg/installed/x64-windows/lib/gflags.lib
-- Found glog: C:/bin/vcpkg/installed/x64-windows/lib/glog.lib
-- Found yaml-cpp: C:/bin/vcpkg/installed/x64-windows/lib/yaml-cpp.lib
-- Found leveldb: C:/bin/vcpkg/installed/x64-windows/lib/leveldb.lib
-- Found marisa: C:/bin/vcpkg/installed/x64-windows/lib/libmarisa.lib
-- Found opencc: C:/bin/vcpkg/installed/x64-windows/lib/opencc.lib
-- Found X11/keysym.h at C:/Users/AlanJui/source/repos/librime/include
-- rime_plugins_libs:
-- rime_plugins_modules:
true
-- Configuring done (0.3s)
-- Generating done (0.2s)
-- Build files have been written to: C:/Users/AlanJui/source/repos/librime/build
```


```sh
ninja
ninja install
```




## 參考

### b2 重要參考

```sh
C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\tools\build\src\engine>dir *.exe
 Volume in drive C is Windows
 Volume Serial Number is 2EB5-AA68

 Directory of C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\tools\build\src\engine

2025/03/03  上午 11:06           263,168 b2.exe
               1 File(s)        263,168 bytes
               0 Dir(s)  1,509,821,558,784 bytes free

Generating Boost.Build configuration in project-config.jam for msvc...

Bootstrapping is done. To build, run:

    .\b2

    To generate header files, run:

    .\b2 headers

To adjust configuration, edit 'project-config.jam'.
Further information:

    - Command line help:
    .\b2 --help

    - Getting started guide:
    http://boost.org/more/getting_started/windows.html

    - Boost.Build documentation:
    http://www.boost.org/build/

Performing configuration checks

    - default address-model    : none [1]
    - default architecture     : none [1]
    - symlinks supported       : no
    - junctions supported      : yes
    - hardlinks supported      : yes


```


### install-boost.bat 執行過程參考

```sh
C:\Users\AlanJui\source\repos\librime>install-boost.bat

C:\Users\AlanJui\source\repos\librime>setlocal

C:\Users\AlanJui\source\repos\librime>if not defined RIME_ROOT set RIME_ROOT=C:\Users\AlanJui\source\repos\librime

C:\Users\AlanJui\source\repos\librime>if not defined boost_version set boost_version=1.84.0

C:\Users\AlanJui\source\repos\librime>if not defined BOOST_ROOT set BOOST_ROOT=C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0

C:\Users\AlanJui\source\repos\librime>if exist "C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\libs" goto boost_found

C:\Users\AlanJui\source\repos\librime>for %I in ("C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\.") do set src_dir=%~dpI

C:\Users\AlanJui\source\repos\librime>set src_dir=C:\Users\AlanJui\source\repos\librime\deps\

C:\Users\AlanJui\source\repos\librime>rem download boost source

C:\Users\AlanJui\source\repos\librime>aria2c https://github.com/boostorg/boost/releases/download/boost-1.84.0/boost-1.84.0.7z -d C:\Users\AlanJui\source\repos\librime\deps\

03/03 11:05:16 [NOTICE] Downloading 1 item(s)

03/03 11:05:17 [NOTICE] CUID#7 - Redirecting to https://objects.githubusercontent.com/github-production-release-asset-2e65be/7590028/cb6bf65a-bafb-4e92-8433-d3ea16ff09d4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250303%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250303T030516Z&X-Amz-Expires=300&X-Amz-Signature=99878fc231ff5c5b75150088cd3ee5dd0ee69ebedb339936b23e2bcfcd236fcb&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Dboost-1.84.0.7z&response-content-type=application%2Foctet-stream
[#19d7f5 0B/0B CN:1 DL:0B]
03/03 11:05:18 [NOTICE] File already exists. Renamed to C:/Users/AlanJui/source/repos/librime/deps//boost-1.84.0.1.7z.

03/03 11:05:18 [NOTICE] Allocating disk space. Use --file-allocation=none to disable it. See --file-allocation option in man page for more details.
[#19d7f5 82MiB/90MiB(91%) CN:1 DL:28MiB]
03/03 11:05:21 [NOTICE] Download complete: C:/Users/AlanJui/source/repos/librime/deps//boost-1.84.0.1.7z

Download Results:
gid   |stat|avg speed  |path/URI
======+====+===========+=======================================================
19d7f5|OK  |    29MiB/s|C:/Users/AlanJui/source/repos/librime/deps//boost-1.84.0.1.7z

Status Legend:
(OK):download completed.

C:\Users\AlanJui\source\repos\librime>pushd C:\Users\AlanJui\source\repos\librime\deps\

C:\Users\AlanJui\source\repos\librime\deps>7z x boost-1.84.0.7z

7-Zip 24.09 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-11-29

Scanning the drive for archives:
1 file, 94484858 bytes (91 MiB)

Extracting archive: boost-1.84.0.7z
--
Path = boost-1.84.0.7z
Type = 7z
Physical Size = 94484858
Headers Size = 607305
Method = LZMA2:24
Solid = +
Blocks = 1

Everything is Ok

Folders: 5338
Files: 55706
Size:       517643196
Compressed: 94484858

C:\Users\AlanJui\source\repos\librime\deps>cd boost-1.84.0

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0>call .\bootstrap.bat
Building Boost.Build engine
LOCALAPPDATA=C:\Users\AlanJui\AppData\Local
Found with vswhere C:\Program Files\Microsoft Visual Studio\2022\Community
Found with vswhere C:\Program Files\Microsoft Visual Studio\2022\Community
###
### Using 'vc143' toolset.
###

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\tools\build\src\engine>"cl" /nologo -TP /wd4996 /wd4675 /EHs /GR /Zc:throwingNew /O2 /Ob2 /W3 /MD /Zc:forScope /Zc:wchar_t /Zc:inline /Gw /favor:blend /Feb2   -DNDEBUG  builtins.cpp class.cpp command.cpp compile.cpp constants.cpp cwd.cpp debug.cpp debugger.cpp execcmd.cpp execnt.cpp execunix.cpp filent.cpp filesys.cpp fileunix.cpp frames.cpp function.cpp glob.cpp hash.cpp hcache.cpp hdrmacro.cpp headers.cpp jam.cpp jamgram.cpp lists.cpp make.cpp make1.cpp md5.cpp mem.cpp modules.cpp native.cpp object.cpp option.cpp output.cpp parse.cpp pathnt.cpp pathsys.cpp pathunix.cpp regexp.cpp rules.cpp scan.cpp search.cpp jam_strings.cpp startup.cpp subst.cpp sysinfo.cpp timestamp.cpp variable.cpp w32_getreg.cpp modules/order.cpp modules/path.cpp modules/property-set.cpp modules/regex.cpp modules/sequence.cpp modules/set.cpp /link kernel32.lib advapi32.lib user32.lib
builtins.cpp
class.cpp
command.cpp
compile.cpp
constants.cpp
cwd.cpp
debug.cpp
debugger.cpp
execcmd.cpp
execnt.cpp
execunix.cpp
filent.cpp
filesys.cpp
fileunix.cpp
frames.cpp
function.cpp
glob.cpp
hash.cpp
hcache.cpp
hdrmacro.cpp
正在產生程式碼...
正在編譯...
headers.cpp
jam.cpp
jamgram.cpp
lists.cpp
make.cpp
make1.cpp
md5.cpp
mem.cpp
modules.cpp
native.cpp
object.cpp
option.cpp
output.cpp
parse.cpp
pathnt.cpp
pathsys.cpp
pathunix.cpp
regexp.cpp
rules.cpp
scan.cpp
正在產生程式碼...
正在編譯...
search.cpp
jam_strings.cpp
startup.cpp
subst.cpp
sysinfo.cpp
timestamp.cpp
variable.cpp
w32_getreg.cpp
order.cpp
path.cpp
property-set.cpp
regex.cpp
sequence.cpp
set.cpp
正在產生程式碼...

C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\tools\build\src\engine>dir *.exe
 Volume in drive C is Windows
 Volume Serial Number is 2EB5-AA68

 Directory of C:\Users\AlanJui\source\repos\librime\deps\boost-1.84.0\tools\build\src\engine

2025/03/03  上午 11:06           263,168 b2.exe
               1 File(s)        263,168 bytes
               0 Dir(s)  1,509,821,558,784 bytes free

Generating Boost.Build configuration in project-config.jam for msvc...

Bootstrapping is done. To build, run:

    .\b2

    To generate header files, run:

    .\b2 headers

To adjust configuration, edit 'project-config.jam'.
Further information:

    - Command line help:
    .\b2 --help

    - Getting started guide:
    http://boost.org/more/getting_started/windows.html

    - Boost.Build documentation:
    http://www.boost.org/build/

Performing configuration checks

    - default address-model    : none [1]
    - default architecture     : none [1]
    - symlinks supported       : no
    - junctions supported      : yes
    - hardlinks supported      : yes

[1] msvc-14.3
...found 1393 targets...
...updating 625 targets...
mklink-or-dir boost
mklink-or-dir boost\accumulators
Junction created for boost\accumulators <<===>> libs\accumulators\include\boost\accumulators
mklink-or-dir boost\algorithm
Junction created for boost\algorithm <<===>> libs\algorithm\include\boost\algorithm
mklink-or-dir boost\align
Junction created for boost\align <<===>> libs\align\include\boost\align
link.hardlink boost\align.hpp
Hardlink created for boost\align.hpp <<===>> libs\align\include\boost\align.hpp
mklink-or-dir boost\any
Junction created for boost\any <<===>> libs\any\include\boost\any
link.hardlink boost\any.hpp
Hardlink created for boost\any.hpp <<===>> libs\any\include\boost\any.hpp
link.hardlink boost\array.hpp
Hardlink created for boost\array.hpp <<===>> libs\array\include\boost\array.hpp
mklink-or-dir boost\asio
Junction created for boost\asio <<===>> libs\asio\include\boost\asio
link.hardlink boost\asio.hpp
Hardlink created for boost\asio.hpp <<===>> libs\asio\include\boost\asio.hpp
mklink-or-dir boost\assert
Junction created for boost\assert <<===>> libs\assert\include\boost\assert
link.hardlink boost\assert.hpp
Hardlink created for boost\assert.hpp <<===>> libs\assert\include\boost\assert.hpp
mklink-or-dir boost\assign
Junction created for boost\assign <<===>> libs\assign\include\boost\assign
link.hardlink boost\current_function.hpp
Hardlink created for boost\current_function.hpp <<===>> libs\assert\include\boost\current_function.hpp
mklink-or-dir boost\atomic
Junction created for boost\atomic <<===>> libs\atomic\include\boost\atomic
link.hardlink boost\assign.hpp
Hardlink created for boost\assign.hpp <<===>> libs\assign\include\boost\assign.hpp
link.hardlink boost\atomic.hpp
Hardlink created for boost\atomic.hpp <<===>> libs\atomic\include\boost\atomic.hpp
mklink-or-dir boost\beast
Junction created for boost\beast <<===>> libs\beast\include\boost\beast
link.hardlink boost\memory_order.hpp
Hardlink created for boost\memory_order.hpp <<===>> libs\atomic\include\boost\memory_order.hpp
link.hardlink boost\beast.hpp
Hardlink created for boost\beast.hpp <<===>> libs\beast\include\boost\beast.hpp
mklink-or-dir boost\bind
Junction created for boost\bind <<===>> libs\bind\include\boost\bind
link.hardlink boost\bind.hpp
Hardlink created for boost\bind.hpp <<===>> libs\bind\include\boost\bind.hpp
link.hardlink boost\is_placeholder.hpp
Hardlink created for boost\is_placeholder.hpp <<===>> libs\bind\include\boost\is_placeholder.hpp
link.hardlink boost\callable_traits.hpp
Hardlink created for boost\callable_traits.hpp <<===>> libs\callable_traits\include\boost\callable_traits.hpp
mklink-or-dir boost\callable_traits
Junction created for boost\callable_traits <<===>> libs\callable_traits\include\boost\callable_traits
mklink-or-dir boost\bimap
Junction created for boost\bimap <<===>> libs\bimap\include\boost\bimap
mklink-or-dir boost\chrono
Junction created for boost\chrono <<===>> libs\chrono\include\boost\chrono
mklink-or-dir boost\circular_buffer
Junction created for boost\circular_buffer <<===>> libs\circular_buffer\include\boost\circular_buffer
link.hardlink boost\chrono.hpp
Hardlink created for boost\chrono.hpp <<===>> libs\chrono\include\boost\chrono.hpp
link.hardlink boost\circular_buffer.hpp
Hardlink created for boost\circular_buffer.hpp <<===>> libs\circular_buffer\include\boost\circular_buffer.hpp
link.hardlink boost\bimap.hpp
Hardlink created for boost\bimap.hpp <<===>> libs\bimap\include\boost\bimap.hpp
link.hardlink boost\circular_buffer_fwd.hpp
Hardlink created for boost\circular_buffer_fwd.hpp <<===>> libs\circular_buffer\include\boost\circular_buffer_fwd.hpp
link.hardlink boost\mem_fn.hpp
Hardlink created for boost\mem_fn.hpp <<===>> libs\bind\include\boost\mem_fn.hpp
mklink-or-dir boost\cobalt
Junction created for boost\cobalt <<===>> libs\cobalt\include\boost\cobalt
link.hardlink boost\cobalt.hpp
Hardlink created for boost\cobalt.hpp <<===>> libs\cobalt\include\boost\cobalt.hpp
mklink-or-dir boost\compatibility
Junction created for boost\compatibility <<===>> libs\compatibility\include\boost\compatibility
mklink-or-dir boost\compat
Junction created for boost\compat <<===>> libs\compat\include\boost\compat
mklink-or-dir boost\compute
Junction created for boost\compute <<===>> libs\compute\include\boost\compute
mklink-or-dir boost\concept
Junction created for boost\concept <<===>> libs\concept_check\include\boost\concept
link.hardlink boost\compute.hpp
Hardlink created for boost\compute.hpp <<===>> libs\compute\include\boost\compute.hpp
link.hardlink boost\concept_archetype.hpp
Hardlink created for boost\concept_archetype.hpp <<===>> libs\concept_check\include\boost\concept_archetype.hpp
mklink-or-dir boost\concept_check
Junction created for boost\concept_check <<===>> libs\concept_check\include\boost\concept_check
link.hardlink boost\concept_check.hpp
Hardlink created for boost\concept_check.hpp <<===>> libs\concept_check\include\boost\concept_check.hpp
mklink-or-dir boost\config
Junction created for boost\config <<===>> libs\config\include\boost\config
link.hardlink boost\config.hpp
Hardlink created for boost\config.hpp <<===>> libs\config\include\boost\config.hpp
mklink-or-dir boost\detail
link.hardlink boost\cxx11_char_types.hpp
Hardlink created for boost\cxx11_char_types.hpp <<===>> libs\config\include\boost\cxx11_char_types.hpp
link.hardlink boost\cstdint.hpp
Hardlink created for boost\cstdint.hpp <<===>> libs\config\include\boost\cstdint.hpp
link.hardlink boost\limits.hpp
Hardlink created for boost\limits.hpp <<===>> libs\config\include\boost\limits.hpp
mklink-or-dir boost\functional
mklink-or-dir boost\container_hash
Junction created for boost\container_hash <<===>> libs\container_hash\include\boost\container_hash
link.hardlink boost\version.hpp
Hardlink created for boost\version.hpp <<===>> libs\config\include\boost\version.hpp
mklink-or-dir boost\context
Junction created for boost\context <<===>> libs\context\include\boost\context
link.hardlink boost\contract.hpp
Hardlink created for boost\contract.hpp <<===>> libs\contract\include\boost\contract.hpp
mklink-or-dir boost\container
Junction created for boost\container <<===>> libs\container\include\boost\container
link.hardlink boost\detail\workaround.hpp
Hardlink created for boost\detail\workaround.hpp <<===>> libs\config\include\boost\detail\workaround.hpp
mklink-or-dir boost\contract
Junction created for boost\contract <<===>> libs\contract\include\boost\contract
link.hardlink boost\detail\iterator.hpp
Hardlink created for boost\detail\iterator.hpp <<===>> libs\core\include\boost\detail\iterator.hpp
link.hardlink boost\contract_macro.hpp
Hardlink created for boost\contract_macro.hpp <<===>> libs\contract\include\boost\contract_macro.hpp
link.hardlink boost\detail\no_exceptions_support.hpp
Hardlink created for boost\detail\no_exceptions_support.hpp <<===>> libs\core\include\boost\detail\no_exceptions_support.hpp
mklink-or-dir boost\functional\hash
Junction created for boost\functional\hash <<===>> libs\container_hash\include\boost\functional\hash
link.hardlink boost\detail\lightweight_test.hpp
Hardlink created for boost\detail\lightweight_test.hpp <<===>> libs\core\include\boost\detail\lightweight_test.hpp
link.hardlink boost\functional\hash.hpp
Hardlink created for boost\functional\hash.hpp <<===>> libs\container_hash\include\boost\functional\hash.hpp
link.hardlink boost\functional\factory.hpp
Hardlink created for boost\functional\factory.hpp <<===>> libs\functional\include\boost\functional\factory.hpp
link.hardlink boost\functional\hash_fwd.hpp
Hardlink created for boost\functional\hash_fwd.hpp <<===>> libs\container_hash\include\boost\functional\hash_fwd.hpp
link.hardlink boost\functional\identity.hpp
Hardlink created for boost\functional\identity.hpp <<===>> libs\functional\include\boost\functional\identity.hpp
link.hardlink boost\functional\lightweight_forward_adapter.hpp
Hardlink created for boost\functional\lightweight_forward_adapter.hpp <<===>> libs\functional\include\boost\functional\lightweight_forward_adapter.hpp
mklink-or-dir boost\functional\overloaded_function
Junction created for boost\functional\overloaded_function <<===>> libs\functional\include\boost\functional\overloaded_function
link.hardlink boost\functional\forward_adapter.hpp
Hardlink created for boost\functional\forward_adapter.hpp <<===>> libs\functional\include\boost\functional\forward_adapter.hpp
link.hardlink boost\functional\overloaded_function.hpp
Hardlink created for boost\functional\overloaded_function.hpp <<===>> libs\functional\include\boost\functional\overloaded_function.hpp
link.hardlink boost\detail\scoped_enum_emulation.hpp
Hardlink created for boost\detail\scoped_enum_emulation.hpp <<===>> libs\core\include\boost\detail\scoped_enum_emulation.hpp
link.hardlink boost\functional\value_factory.hpp
Hardlink created for boost\functional\value_factory.hpp <<===>> libs\functional\include\boost\functional\value_factory.hpp
link.hardlink boost\detail\binary_search.hpp
Hardlink created for boost\detail\binary_search.hpp <<===>> libs\detail\include\boost\detail\binary_search.hpp
link.hardlink boost\detail\allocator_utilities.hpp
Hardlink created for boost\detail\allocator_utilities.hpp <<===>> libs\detail\include\boost\detail\allocator_utilities.hpp
link.hardlink boost\detail\catch_exceptions.hpp
Hardlink created for boost\detail\catch_exceptions.hpp <<===>> libs\detail\include\boost\detail\catch_exceptions.hpp
link.hardlink boost\detail\container_fwd.hpp
Hardlink created for boost\detail\container_fwd.hpp <<===>> libs\detail\include\boost\detail\container_fwd.hpp
link.hardlink boost\detail\fenv.hpp
Hardlink created for boost\detail\fenv.hpp <<===>> libs\detail\include\boost\detail\fenv.hpp
link.hardlink boost\detail\bitmask.hpp
Hardlink created for boost\detail\bitmask.hpp <<===>> libs\detail\include\boost\detail\bitmask.hpp
link.hardlink boost\detail\identifier.hpp
Hardlink created for boost\detail\identifier.hpp <<===>> libs\detail\include\boost\detail\identifier.hpp
link.hardlink boost\detail\indirect_traits.hpp
Hardlink created for boost\detail\indirect_traits.hpp <<===>> libs\detail\include\boost\detail\indirect_traits.hpp
link.hardlink boost\detail\sp_typeinfo.hpp
Hardlink created for boost\detail\sp_typeinfo.hpp <<===>> libs\core\include\boost\detail\sp_typeinfo.hpp
link.hardlink boost\detail\has_default_constructor.hpp
Hardlink created for boost\detail\has_default_constructor.hpp <<===>> libs\detail\include\boost\detail\has_default_constructor.hpp
link.hardlink boost\detail\is_incrementable.hpp
Hardlink created for boost\detail\is_incrementable.hpp <<===>> libs\detail\include\boost\detail\is_incrementable.hpp
link.hardlink boost\detail\is_sorted.hpp
Hardlink created for boost\detail\is_sorted.hpp <<===>> libs\detail\include\boost\detail\is_sorted.hpp
link.hardlink boost\detail\lightweight_main.hpp
Hardlink created for boost\detail\lightweight_main.hpp <<===>> libs\detail\include\boost\detail\lightweight_main.hpp
link.hardlink boost\detail\lightweight_test_report.hpp
Hardlink created for boost\detail\lightweight_test_report.hpp <<===>> libs\detail\include\boost\detail\lightweight_test_report.hpp
link.hardlink boost\detail\named_template_params.hpp
Hardlink created for boost\detail\named_template_params.hpp <<===>> libs\detail\include\boost\detail\named_template_params.hpp
link.hardlink boost\detail\reference_content.hpp
Hardlink created for boost\detail\reference_content.hpp <<===>> libs\detail\include\boost\detail\reference_content.hpp
...on 100th target...
link.hardlink boost\detail\select_type.hpp
Hardlink created for boost\detail\select_type.hpp <<===>> libs\detail\include\boost\detail\select_type.hpp
link.hardlink boost\detail\templated_streams.hpp
Hardlink created for boost\detail\templated_streams.hpp <<===>> libs\detail\include\boost\detail\templated_streams.hpp
link.hardlink boost\detail\numeric_traits.hpp
Hardlink created for boost\detail\numeric_traits.hpp <<===>> libs\detail\include\boost\detail\numeric_traits.hpp
link.hardlink boost\detail\is_xxx.hpp
Hardlink created for boost\detail\is_xxx.hpp <<===>> libs\detail\include\boost\detail\is_xxx.hpp
link.hardlink boost\detail\algorithm.hpp
Hardlink created for boost\detail\algorithm.hpp <<===>> libs\graph\include\boost\detail\algorithm.hpp
link.hardlink boost\detail\utf8_codecvt_facet.hpp
Hardlink created for boost\detail\utf8_codecvt_facet.hpp <<===>> libs\detail\include\boost\detail\utf8_codecvt_facet.hpp
link.hardlink boost\detail\utf8_codecvt_facet.ipp
Hardlink created for boost\detail\utf8_codecvt_facet.ipp <<===>> libs\detail\include\boost\detail\utf8_codecvt_facet.ipp
link.hardlink boost\detail\lcast_precision.hpp
Hardlink created for boost\detail\lcast_precision.hpp <<===>> libs\lexical_cast\include\boost\detail\lcast_precision.hpp
link.hardlink boost\detail\basic_pointerbuf.hpp
Hardlink created for boost\detail\basic_pointerbuf.hpp <<===>> libs\lexical_cast\include\boost\detail\basic_pointerbuf.hpp
link.hardlink boost\detail\atomic_count.hpp
Hardlink created for boost\detail\atomic_count.hpp <<===>> libs\smart_ptr\include\boost\detail\atomic_count.hpp
link.hardlink boost\detail\lightweight_thread.hpp
Hardlink created for boost\detail\lightweight_thread.hpp <<===>> libs\smart_ptr\include\boost\detail\lightweight_thread.hpp
link.hardlink boost\detail\lightweight_mutex.hpp
Hardlink created for boost\detail\lightweight_mutex.hpp <<===>> libs\smart_ptr\include\boost\detail\lightweight_mutex.hpp
link.hardlink boost\detail\call_traits.hpp
Hardlink created for boost\detail\call_traits.hpp <<===>> libs\utility\include\boost\detail\call_traits.hpp
link.hardlink boost\detail\ob_compressed_pair.hpp
Hardlink created for boost\detail\ob_compressed_pair.hpp <<===>> libs\utility\include\boost\detail\ob_compressed_pair.hpp
link.hardlink boost\detail\interlocked.hpp
Hardlink created for boost\detail\interlocked.hpp <<===>> libs\winapi\include\boost\detail\interlocked.hpp
link.hardlink boost\detail\compressed_pair.hpp
Hardlink created for boost\detail\compressed_pair.hpp <<===>> libs\utility\include\boost\detail\compressed_pair.hpp
mklink-or-dir boost\detail\winapi
Junction created for boost\detail\winapi <<===>> libs\winapi\include\boost\detail\winapi
link.hardlink boost\detail\quick_allocator.hpp
Hardlink created for boost\detail\quick_allocator.hpp <<===>> libs\smart_ptr\include\boost\detail\quick_allocator.hpp
link.hardlink boost\implicit_cast.hpp
Hardlink created for boost\implicit_cast.hpp <<===>> libs\conversion\include\boost\implicit_cast.hpp
link.hardlink boost\polymorphic_cast.hpp
Hardlink created for boost\polymorphic_cast.hpp <<===>> libs\conversion\include\boost\polymorphic_cast.hpp
link.hardlink boost\convert.hpp
Hardlink created for boost\convert.hpp <<===>> libs\convert\include\boost\convert.hpp
mklink-or-dir boost\convert
Junction created for boost\convert <<===>> libs\convert\include\boost\convert
link.hardlink boost\checked_delete.hpp
Hardlink created for boost\checked_delete.hpp <<===>> libs\core\include\boost\checked_delete.hpp
link.hardlink boost\make_default.hpp
Hardlink created for boost\make_default.hpp <<===>> libs\convert\include\boost\make_default.hpp
link.hardlink boost\polymorphic_pointer_cast.hpp
Hardlink created for boost\polymorphic_pointer_cast.hpp <<===>> libs\conversion\include\boost\polymorphic_pointer_cast.hpp
link.hardlink boost\iterator.hpp
Hardlink created for boost\iterator.hpp <<===>> libs\core\include\boost\iterator.hpp
link.hardlink boost\get_pointer.hpp
Hardlink created for boost\get_pointer.hpp <<===>> libs\core\include\boost\get_pointer.hpp
mklink-or-dir boost\core
Junction created for boost\core <<===>> libs\core\include\boost\core
link.hardlink boost\noncopyable.hpp
Hardlink created for boost\noncopyable.hpp <<===>> libs\core\include\boost\noncopyable.hpp
link.hardlink boost\non_type.hpp
Hardlink created for boost\non_type.hpp <<===>> libs\core\include\boost\non_type.hpp
mklink-or-dir boost\utility
link.hardlink boost\ref.hpp
Hardlink created for boost\ref.hpp <<===>> libs\core\include\boost\ref.hpp
link.hardlink boost\swap.hpp
Hardlink created for boost\swap.hpp <<===>> libs\core\include\boost\swap.hpp
link.hardlink boost\visit_each.hpp
Hardlink created for boost\visit_each.hpp <<===>> libs\core\include\boost\visit_each.hpp
mklink-or-dir boost\coroutine
Junction created for boost\coroutine <<===>> libs\coroutine\include\boost\coroutine
mklink-or-dir boost\coroutine2
Junction created for boost\coroutine2 <<===>> libs\coroutine2\include\boost\coroutine2
link.hardlink boost\crc.hpp
Hardlink created for boost\crc.hpp <<===>> libs\crc\include\boost\crc.hpp
mklink-or-dir boost\describe
Junction created for boost\describe <<===>> libs\describe\include\boost\describe
mklink-or-dir boost\date_time
Junction created for boost\date_time <<===>> libs\date_time\include\boost\date_time
link.hardlink boost\type.hpp
Hardlink created for boost\type.hpp <<===>> libs\core\include\boost\type.hpp
link.hardlink boost\date_time.hpp
Hardlink created for boost\date_time.hpp <<===>> libs\date_time\include\boost\date_time.hpp
link.hardlink boost\describe.hpp
Hardlink created for boost\describe.hpp <<===>> libs\describe\include\boost\describe.hpp
link.hardlink boost\utility\enable_if.hpp
Hardlink created for boost\utility\enable_if.hpp <<===>> libs\core\include\boost\utility\enable_if.hpp
link.hardlink boost\utility\explicit_operator_bool.hpp
Hardlink created for boost\utility\explicit_operator_bool.hpp <<===>> libs\core\include\boost\utility\explicit_operator_bool.hpp
link.hardlink boost\utility\addressof.hpp
Hardlink created for boost\utility\addressof.hpp <<===>> libs\core\include\boost\utility\addressof.hpp
link.hardlink boost\utility\binary.hpp
Hardlink created for boost\utility\binary.hpp <<===>> libs\utility\include\boost\utility\binary.hpp
link.hardlink boost\utility\compare_pointees.hpp
Hardlink created for boost\utility\compare_pointees.hpp <<===>> libs\utility\include\boost\utility\compare_pointees.hpp
link.hardlink boost\utility\declval.hpp
Hardlink created for boost\utility\declval.hpp <<===>> libs\type_traits\include\boost\utility\declval.hpp
link.hardlink boost\utility\swap.hpp
Hardlink created for boost\utility\swap.hpp <<===>> libs\core\include\boost\utility\swap.hpp
link.hardlink boost\utility\in_place_factory.hpp
Hardlink created for boost\utility\in_place_factory.hpp <<===>> libs\utility\include\boost\utility\in_place_factory.hpp
mklink-or-dir boost\utility\detail
Junction created for boost\utility\detail <<===>> libs\utility\include\boost\utility\detail
link.hardlink boost\utility\base_from_member.hpp
Hardlink created for boost\utility\base_from_member.hpp <<===>> libs\utility\include\boost\utility\base_from_member.hpp
link.hardlink boost\utility\string_ref.hpp
Hardlink created for boost\utility\string_ref.hpp <<===>> libs\utility\include\boost\utility\string_ref.hpp
link.hardlink boost\utility\identity_type.hpp
Hardlink created for boost\utility\identity_type.hpp <<===>> libs\utility\include\boost\utility\identity_type.hpp
link.hardlink boost\utility\result_of.hpp
Hardlink created for boost\utility\result_of.hpp <<===>> libs\utility\include\boost\utility\result_of.hpp
link.hardlink boost\utility\string_ref_fwd.hpp
Hardlink created for boost\utility\string_ref_fwd.hpp <<===>> libs\utility\include\boost\utility\string_ref_fwd.hpp
link.hardlink boost\utility\string_view.hpp
Hardlink created for boost\utility\string_view.hpp <<===>> libs\utility\include\boost\utility\string_view.hpp
link.hardlink boost\utility\string_view_fwd.hpp
Hardlink created for boost\utility\string_view_fwd.hpp <<===>> libs\utility\include\boost\utility\string_view_fwd.hpp
link.hardlink boost\blank.hpp
Hardlink created for boost\blank.hpp <<===>> libs\detail\include\boost\blank.hpp
link.hardlink boost\utility\typed_in_place_factory.hpp
Hardlink created for boost\utility\typed_in_place_factory.hpp <<===>> libs\utility\include\boost\utility\typed_in_place_factory.hpp
link.hardlink boost\cstdlib.hpp
Hardlink created for boost\cstdlib.hpp <<===>> libs\detail\include\boost\cstdlib.hpp
mklink-or-dir boost\dll
Junction created for boost\dll <<===>> libs\dll\include\boost\dll
link.hardlink boost\utility\value_init.hpp
Hardlink created for boost\utility\value_init.hpp <<===>> libs\utility\include\boost\utility\value_init.hpp
link.hardlink boost\blank_fwd.hpp
Hardlink created for boost\blank_fwd.hpp <<===>> libs\detail\include\boost\blank_fwd.hpp
link.hardlink boost\dll.hpp
Hardlink created for boost\dll.hpp <<===>> libs\dll\include\boost\dll.hpp
mklink-or-dir boost\dynamic_bitset
Junction created for boost\dynamic_bitset <<===>> libs\dynamic_bitset\include\boost\dynamic_bitset
mklink-or-dir boost\exception
link.hardlink boost\dynamic_bitset_fwd.hpp
Hardlink created for boost\dynamic_bitset_fwd.hpp <<===>> libs\dynamic_bitset\include\boost\dynamic_bitset_fwd.hpp
link.hardlink boost\dynamic_bitset.hpp
Hardlink created for boost\dynamic_bitset.hpp <<===>> libs\dynamic_bitset\include\boost\dynamic_bitset.hpp
link.hardlink boost\endian.hpp
Hardlink created for boost\endian.hpp <<===>> libs\endian\include\boost\endian.hpp
mklink-or-dir boost\fiber
Junction created for boost\fiber <<===>> libs\fiber\include\boost\fiber
link.hardlink boost\exception_ptr.hpp
Hardlink created for boost\exception_ptr.hpp <<===>> libs\exception\include\boost\exception_ptr.hpp
mklink-or-dir boost\endian
Junction created for boost\endian <<===>> libs\endian\include\boost\endian
mklink-or-dir boost\filesystem
Junction created for boost\filesystem <<===>> libs\filesystem\include\boost\filesystem
mklink-or-dir boost\flyweight
Junction created for boost\flyweight <<===>> libs\flyweight\include\boost\flyweight
link.hardlink boost\filesystem.hpp
Hardlink created for boost\filesystem.hpp <<===>> libs\filesystem\include\boost\filesystem.hpp
link.hardlink boost\flyweight.hpp
Hardlink created for boost\flyweight.hpp <<===>> libs\flyweight\include\boost\flyweight.hpp
link.hardlink boost\foreach.hpp
Hardlink created for boost\foreach.hpp <<===>> libs\foreach\include\boost\foreach.hpp
link.hardlink boost\exception\all.hpp
Hardlink created for boost\exception\all.hpp <<===>> libs\exception\include\boost\exception\all.hpp
link.hardlink boost\exception\current_exception_cast.hpp
Hardlink created for boost\exception\current_exception_cast.hpp <<===>> libs\exception\include\boost\exception\current_exception_cast.hpp
link.hardlink boost\exception\enable_error_info.hpp
Hardlink created for boost\exception\enable_error_info.hpp <<===>> libs\exception\include\boost\exception\enable_error_info.hpp
mklink-or-dir boost\exception\detail
Junction created for boost\exception\detail <<===>> libs\exception\include\boost\exception\detail
link.hardlink boost\exception\enable_current_exception.hpp
Hardlink created for boost\exception\enable_current_exception.hpp <<===>> libs\exception\include\boost\exception\enable_current_exception.hpp
link.hardlink boost\exception\diagnostic_information.hpp
Hardlink created for boost\exception\diagnostic_information.hpp <<===>> libs\exception\include\boost\exception\diagnostic_information.hpp
link.hardlink boost\exception\errinfo_api_function.hpp
Hardlink created for boost\exception\errinfo_api_function.hpp <<===>> libs\exception\include\boost\exception\errinfo_api_function.hpp
link.hardlink boost\exception\errinfo_errno.hpp
Hardlink created for boost\exception\errinfo_errno.hpp <<===>> libs\exception\include\boost\exception\errinfo_errno.hpp
link.hardlink boost\exception\errinfo_at_line.hpp
Hardlink created for boost\exception\errinfo_at_line.hpp <<===>> libs\exception\include\boost\exception\errinfo_at_line.hpp
link.hardlink boost\exception\errinfo_type_info_name.hpp
Hardlink created for boost\exception\errinfo_type_info_name.hpp <<===>> libs\exception\include\boost\exception\errinfo_type_info_name.hpp
link.hardlink boost\exception\errinfo_file_name.hpp
Hardlink created for boost\exception\errinfo_file_name.hpp <<===>> libs\exception\include\boost\exception\errinfo_file_name.hpp
link.hardlink boost\exception\errinfo_file_handle.hpp
Hardlink created for boost\exception\errinfo_file_handle.hpp <<===>> libs\exception\include\boost\exception\errinfo_file_handle.hpp
link.hardlink boost\exception\errinfo_nested_exception.hpp
Hardlink created for boost\exception\errinfo_nested_exception.hpp <<===>> libs\exception\include\boost\exception\errinfo_nested_exception.hpp
link.hardlink boost\exception\info.hpp
Hardlink created for boost\exception\info.hpp <<===>> libs\exception\include\boost\exception\info.hpp
link.hardlink boost\exception\info_tuple.hpp
Hardlink created for boost\exception\info_tuple.hpp <<===>> libs\exception\include\boost\exception\info_tuple.hpp
link.hardlink boost\exception\to_string_stub.hpp
Hardlink created for boost\exception\to_string_stub.hpp <<===>> libs\exception\include\boost\exception\to_string_stub.hpp
link.hardlink boost\exception\errinfo_file_open_mode.hpp
Hardlink created for boost\exception\errinfo_file_open_mode.hpp <<===>> libs\exception\include\boost\exception\errinfo_file_open_mode.hpp
link.hardlink boost\exception\error_info.hpp
Hardlink created for boost\exception\error_info.hpp <<===>> libs\exception\include\boost\exception\error_info.hpp
link.hardlink boost\exception\to_string.hpp
Hardlink created for boost\exception\to_string.hpp <<===>> libs\exception\include\boost\exception\to_string.hpp
link.hardlink boost\exception\get_error_info.hpp
Hardlink created for boost\exception\get_error_info.hpp <<===>> libs\exception\include\boost\exception\get_error_info.hpp
link.hardlink boost\format.hpp
Hardlink created for boost\format.hpp <<===>> libs\format\include\boost\format.hpp
mklink-or-dir boost\format
Junction created for boost\format <<===>> libs\format\include\boost\format
...on 200th target...
link.hardlink boost\foreach_fwd.hpp
Hardlink created for boost\foreach_fwd.hpp <<===>> libs\foreach\include\boost\foreach_fwd.hpp
link.hardlink boost\exception\exception.hpp
Hardlink created for boost\exception\exception.hpp <<===>> libs\throw_exception\include\boost\exception\exception.hpp
mklink-or-dir boost\function
Junction created for boost\function <<===>> libs\function\include\boost\function
link.hardlink boost\functional.hpp
Hardlink created for boost\functional.hpp <<===>> libs\functional\include\boost\functional.hpp
mklink-or-dir boost\function_types
Junction created for boost\function_types <<===>> libs\function_types\include\boost\function_types
mklink-or-dir boost\graph
link.hardlink boost\function.hpp
Hardlink created for boost\function.hpp <<===>> libs\function\include\boost\function.hpp
mklink-or-dir boost\fusion
Junction created for boost\fusion <<===>> libs\fusion\include\boost\fusion
mklink-or-dir boost\gil
Junction created for boost\gil <<===>> libs\gil\include\boost\gil
link.hardlink boost\function_equal.hpp
Hardlink created for boost\function_equal.hpp <<===>> libs\function\include\boost\function_equal.hpp
mklink-or-dir boost\geometry
Junction created for boost\geometry <<===>> libs\geometry\include\boost\geometry
link.hardlink boost\gil.hpp
Hardlink created for boost\gil.hpp <<===>> libs\gil\include\boost\gil.hpp
mklink-or-dir boost\hana
Junction created for boost\hana <<===>> libs\hana\include\boost\hana
link.hardlink boost\geometry.hpp
Hardlink created for boost\geometry.hpp <<===>> libs\geometry\include\boost\geometry.hpp
link.hardlink boost\hana.hpp
Hardlink created for boost\hana.hpp <<===>> libs\hana\include\boost\hana.hpp
mklink-or-dir boost\pending
mklink-or-dir boost\headers
Junction created for boost\headers <<===>> libs\headers\include\boost\headers
link.hardlink boost\graph\adjacency_iterator.hpp
Hardlink created for boost\graph\adjacency_iterator.hpp <<===>> libs\graph\include\boost\graph\adjacency_iterator.hpp
link.hardlink boost\graph\adjacency_list.hpp
Hardlink created for boost\graph\adjacency_list.hpp <<===>> libs\graph\include\boost\graph\adjacency_list.hpp
link.hardlink boost\graph\adjacency_matrix.hpp
Hardlink created for boost\graph\adjacency_matrix.hpp <<===>> libs\graph\include\boost\graph\adjacency_matrix.hpp
link.hardlink boost\graph\adjacency_list_io.hpp
Hardlink created for boost\graph\adjacency_list_io.hpp <<===>> libs\graph\include\boost\graph\adjacency_list_io.hpp
link.hardlink boost\graph\astar_search.hpp
Hardlink created for boost\graph\astar_search.hpp <<===>> libs\graph\include\boost\graph\astar_search.hpp
link.hardlink boost\graph\bc_clustering.hpp
Hardlink created for boost\graph\bc_clustering.hpp <<===>> libs\graph\include\boost\graph\bc_clustering.hpp
link.hardlink boost\graph\adj_list_serialize.hpp
Hardlink created for boost\graph\adj_list_serialize.hpp <<===>> libs\graph\include\boost\graph\adj_list_serialize.hpp
link.hardlink boost\graph\betweenness_centrality.hpp
Hardlink created for boost\graph\betweenness_centrality.hpp <<===>> libs\graph\include\boost\graph\betweenness_centrality.hpp
link.hardlink boost\pending\disjoint_sets.hpp
Hardlink created for boost\pending\disjoint_sets.hpp <<===>> libs\graph\include\boost\pending\disjoint_sets.hpp
link.hardlink boost\pending\container_traits.hpp
Hardlink created for boost\pending\container_traits.hpp <<===>> libs\graph\include\boost\pending\container_traits.hpp
link.hardlink boost\pending\fenced_priority_queue.hpp
Hardlink created for boost\pending\fenced_priority_queue.hpp <<===>> libs\graph\include\boost\pending\fenced_priority_queue.hpp
link.hardlink boost\pending\fibonacci_heap.hpp
Hardlink created for boost\pending\fibonacci_heap.hpp <<===>> libs\graph\include\boost\pending\fibonacci_heap.hpp
link.hardlink boost\graph\bandwidth.hpp
Hardlink created for boost\graph\bandwidth.hpp <<===>> libs\graph\include\boost\graph\bandwidth.hpp
link.hardlink boost\graph\bellman_ford_shortest_paths.hpp
Hardlink created for boost\graph\bellman_ford_shortest_paths.hpp <<===>> libs\graph\include\boost\graph\bellman_ford_shortest_paths.hpp
mklink-or-dir boost\pending\detail
link.hardlink boost\pending\bucket_sorter.hpp
Hardlink created for boost\pending\bucket_sorter.hpp <<===>> libs\graph\include\boost\pending\bucket_sorter.hpp
link.hardlink boost\pending\indirect_cmp.hpp
Hardlink created for boost\pending\indirect_cmp.hpp <<===>> libs\graph\include\boost\pending\indirect_cmp.hpp
link.hardlink boost\pending\is_heap.hpp
Hardlink created for boost\pending\is_heap.hpp <<===>> libs\graph\include\boost\pending\is_heap.hpp
link.hardlink boost\pending\mutable_heap.hpp
Hardlink created for boost\pending\mutable_heap.hpp <<===>> libs\graph\include\boost\pending\mutable_heap.hpp
link.hardlink boost\pending\property_serialize.hpp
Hardlink created for boost\pending\property_serialize.hpp <<===>> libs\graph\include\boost\pending\property_serialize.hpp
link.hardlink boost\pending\property.hpp
Hardlink created for boost\pending\property.hpp <<===>> libs\graph\include\boost\pending\property.hpp
link.hardlink boost\pending\mutable_queue.hpp
Hardlink created for boost\pending\mutable_queue.hpp <<===>> libs\graph\include\boost\pending\mutable_queue.hpp
link.hardlink boost\pending\queue.hpp
Hardlink created for boost\pending\queue.hpp <<===>> libs\graph\include\boost\pending\queue.hpp
link.hardlink boost\pending\relaxed_heap.hpp
Hardlink created for boost\pending\relaxed_heap.hpp <<===>> libs\graph\include\boost\pending\relaxed_heap.hpp
link.hardlink boost\pending\stringtok.hpp
Hardlink created for boost\pending\stringtok.hpp <<===>> libs\graph\include\boost\pending\stringtok.hpp
link.hardlink boost\pending\integer_log2.hpp
Hardlink created for boost\pending\integer_log2.hpp <<===>> libs\integer\include\boost\pending\integer_log2.hpp
link.hardlink boost\pending\detail\property.hpp
Hardlink created for boost\pending\detail\property.hpp <<===>> libs\graph\include\boost\pending\detail\property.hpp
link.hardlink boost\pending\detail\disjoint_sets.hpp
Hardlink created for boost\pending\detail\disjoint_sets.hpp <<===>> libs\graph\include\boost\pending\detail\disjoint_sets.hpp
link.hardlink boost\pending\iterator_adaptors.hpp
Hardlink created for boost\pending\iterator_adaptors.hpp <<===>> libs\iterator\include\boost\pending\iterator_adaptors.hpp
link.hardlink boost\graph\bipartite.hpp
Hardlink created for boost\graph\bipartite.hpp <<===>> libs\graph\include\boost\graph\bipartite.hpp
link.hardlink boost\graph\boyer_myrvold_planar_test.hpp
Hardlink created for boost\graph\boyer_myrvold_planar_test.hpp <<===>> libs\graph\include\boost\graph\boyer_myrvold_planar_test.hpp
link.hardlink boost\pending\iterator_tests.hpp
Hardlink created for boost\pending\iterator_tests.hpp <<===>> libs\iterator\include\boost\pending\iterator_tests.hpp
link.hardlink boost\graph\boykov_kolmogorov_max_flow.hpp
Hardlink created for boost\graph\boykov_kolmogorov_max_flow.hpp <<===>> libs\graph\include\boost\graph\boykov_kolmogorov_max_flow.hpp
link.hardlink boost\graph\biconnected_components.hpp
Hardlink created for boost\graph\biconnected_components.hpp <<===>> libs\graph\include\boost\graph\biconnected_components.hpp
link.hardlink boost\pending\detail\int_iterator.hpp
Hardlink created for boost\pending\detail\int_iterator.hpp <<===>> libs\iterator\include\boost\pending\detail\int_iterator.hpp
link.hardlink boost\graph\bron_kerbosch_all_cliques.hpp
Hardlink created for boost\graph\bron_kerbosch_all_cliques.hpp <<===>> libs\graph\include\boost\graph\bron_kerbosch_all_cliques.hpp
link.hardlink boost\graph\buffer_concepts.hpp
Hardlink created for boost\graph\buffer_concepts.hpp <<===>> libs\graph\include\boost\graph\buffer_concepts.hpp
link.hardlink boost\graph\chrobak_payne_drawing.hpp
Hardlink created for boost\graph\chrobak_payne_drawing.hpp <<===>> libs\graph\include\boost\graph\chrobak_payne_drawing.hpp
link.hardlink boost\graph\breadth_first_search.hpp
Hardlink created for boost\graph\breadth_first_search.hpp <<===>> libs\graph\include\boost\graph\breadth_first_search.hpp
link.hardlink boost\graph\circle_layout.hpp
Hardlink created for boost\graph\circle_layout.hpp <<===>> libs\graph\include\boost\graph\circle_layout.hpp
link.hardlink boost\graph\closeness_centrality.hpp
Hardlink created for boost\graph\closeness_centrality.hpp <<===>> libs\graph\include\boost\graph\closeness_centrality.hpp
link.hardlink boost\graph\clustering_coefficient.hpp
Hardlink created for boost\graph\clustering_coefficient.hpp <<===>> libs\graph\include\boost\graph\clustering_coefficient.hpp
link.hardlink boost\graph\copy.hpp
Hardlink created for boost\graph\copy.hpp <<===>> libs\graph\include\boost\graph\copy.hpp
link.hardlink boost\graph\compressed_sparse_row_graph.hpp
Hardlink created for boost\graph\compressed_sparse_row_graph.hpp <<===>> libs\graph\include\boost\graph\compressed_sparse_row_graph.hpp
link.hardlink boost\graph\core_numbers.hpp
Hardlink created for boost\graph\core_numbers.hpp <<===>> libs\graph\include\boost\graph\core_numbers.hpp
link.hardlink boost\graph\create_condensation_graph.hpp
Hardlink created for boost\graph\create_condensation_graph.hpp <<===>> libs\graph\include\boost\graph\create_condensation_graph.hpp
link.hardlink boost\graph\connected_components.hpp
Hardlink created for boost\graph\connected_components.hpp <<===>> libs\graph\include\boost\graph\connected_components.hpp
link.hardlink boost\graph\cuthill_mckee_ordering.hpp
Hardlink created for boost\graph\cuthill_mckee_ordering.hpp <<===>> libs\graph\include\boost\graph\cuthill_mckee_ordering.hpp
link.hardlink boost\graph\cycle_canceling.hpp
Hardlink created for boost\graph\cycle_canceling.hpp <<===>> libs\graph\include\boost\graph\cycle_canceling.hpp
link.hardlink boost\graph\depth_first_search.hpp
Hardlink created for boost\graph\depth_first_search.hpp <<===>> libs\graph\include\boost\graph\depth_first_search.hpp
link.hardlink boost\graph\dijkstra_shortest_paths.hpp
Hardlink created for boost\graph\dijkstra_shortest_paths.hpp <<===>> libs\graph\include\boost\graph\dijkstra_shortest_paths.hpp
link.hardlink boost\graph\degree_centrality.hpp
Hardlink created for boost\graph\degree_centrality.hpp <<===>> libs\graph\include\boost\graph\degree_centrality.hpp
mklink-or-dir boost\graph\detail
Junction created for boost\graph\detail <<===>> libs\graph\include\boost\graph\detail
link.hardlink boost\graph\dijkstra_shortest_paths_no_color_map.hpp
Hardlink created for boost\graph\dijkstra_shortest_paths_no_color_map.hpp <<===>> libs\graph\include\boost\graph\dijkstra_shortest_paths_no_color_map.hpp
link.hardlink boost\graph\dimacs.hpp
Hardlink created for boost\graph\dimacs.hpp <<===>> libs\graph\include\boost\graph\dimacs.hpp
link.hardlink boost\graph\dag_shortest_paths.hpp
Hardlink created for boost\graph\dag_shortest_paths.hpp <<===>> libs\graph\include\boost\graph\dag_shortest_paths.hpp
link.hardlink boost\graph\eccentricity.hpp
Hardlink created for boost\graph\eccentricity.hpp <<===>> libs\graph\include\boost\graph\eccentricity.hpp
link.hardlink boost\graph\directed_graph.hpp
Hardlink created for boost\graph\directed_graph.hpp <<===>> libs\graph\include\boost\graph\directed_graph.hpp
link.hardlink boost\graph\dll_import_export.hpp
Hardlink created for boost\graph\dll_import_export.hpp <<===>> libs\graph\include\boost\graph\dll_import_export.hpp
link.hardlink boost\graph\dominator_tree.hpp
Hardlink created for boost\graph\dominator_tree.hpp <<===>> libs\graph\include\boost\graph\dominator_tree.hpp
link.hardlink boost\graph\edge_list.hpp
Hardlink created for boost\graph\edge_list.hpp <<===>> libs\graph\include\boost\graph\edge_list.hpp
link.hardlink boost\graph\edmunds_karp_max_flow.hpp
Hardlink created for boost\graph\edmunds_karp_max_flow.hpp <<===>> libs\graph\include\boost\graph\edmunds_karp_max_flow.hpp
link.hardlink boost\graph\edmonds_karp_max_flow.hpp
Hardlink created for boost\graph\edmonds_karp_max_flow.hpp <<===>> libs\graph\include\boost\graph\edmonds_karp_max_flow.hpp
link.hardlink boost\graph\erdos_renyi_generator.hpp
Hardlink created for boost\graph\erdos_renyi_generator.hpp <<===>> libs\graph\include\boost\graph\erdos_renyi_generator.hpp
link.hardlink boost\graph\edge_coloring.hpp
Hardlink created for boost\graph\edge_coloring.hpp <<===>> libs\graph\include\boost\graph\edge_coloring.hpp
link.hardlink boost\graph\exception.hpp
Hardlink created for boost\graph\exception.hpp <<===>> libs\graph\include\boost\graph\exception.hpp
link.hardlink boost\graph\edge_connectivity.hpp
Hardlink created for boost\graph\edge_connectivity.hpp <<===>> libs\graph\include\boost\graph\edge_connectivity.hpp
link.hardlink boost\graph\exterior_property.hpp
Hardlink created for boost\graph\exterior_property.hpp <<===>> libs\graph\include\boost\graph\exterior_property.hpp
link.hardlink boost\graph\find_flow_cost.hpp
Hardlink created for boost\graph\find_flow_cost.hpp <<===>> libs\graph\include\boost\graph\find_flow_cost.hpp
link.hardlink boost\graph\fruchterman_reingold.hpp
Hardlink created for boost\graph\fruchterman_reingold.hpp <<===>> libs\graph\include\boost\graph\fruchterman_reingold.hpp
link.hardlink boost\graph\filtered_graph.hpp
Hardlink created for boost\graph\filtered_graph.hpp <<===>> libs\graph\include\boost\graph\filtered_graph.hpp
link.hardlink boost\graph\floyd_warshall_shortest.hpp
Hardlink created for boost\graph\floyd_warshall_shortest.hpp <<===>> libs\graph\include\boost\graph\floyd_warshall_shortest.hpp
link.hardlink boost\graph\graphml.hpp
Hardlink created for boost\graph\graphml.hpp <<===>> libs\graph\include\boost\graph\graphml.hpp
link.hardlink boost\graph\geodesic_distance.hpp
Hardlink created for boost\graph\geodesic_distance.hpp <<===>> libs\graph\include\boost\graph\geodesic_distance.hpp
link.hardlink boost\graph\graphviz.hpp
Hardlink created for boost\graph\graphviz.hpp <<===>> libs\graph\include\boost\graph\graphviz.hpp
link.hardlink boost\graph\graph_archetypes.hpp
Hardlink created for boost\graph\graph_archetypes.hpp <<===>> libs\graph\include\boost\graph\graph_archetypes.hpp
link.hardlink boost\graph\graph_as_tree.hpp
Hardlink created for boost\graph\graph_as_tree.hpp <<===>> libs\graph\include\boost\graph\graph_as_tree.hpp
link.hardlink boost\graph\graph_concepts.hpp
Hardlink created for boost\graph\graph_concepts.hpp <<===>> libs\graph\include\boost\graph\graph_concepts.hpp
link.hardlink boost\graph\graph_traits.hpp
Hardlink created for boost\graph\graph_traits.hpp <<===>> libs\graph\include\boost\graph\graph_traits.hpp
link.hardlink boost\graph\graph_mutability_traits.hpp
Hardlink created for boost\graph\graph_mutability_traits.hpp <<===>> libs\graph\include\boost\graph\graph_mutability_traits.hpp
link.hardlink boost\graph\graph_stats.hpp
Hardlink created for boost\graph\graph_stats.hpp <<===>> libs\graph\include\boost\graph\graph_stats.hpp
link.hardlink boost\graph\graph_selectors.hpp
Hardlink created for boost\graph\graph_selectors.hpp <<===>> libs\graph\include\boost\graph\graph_selectors.hpp
link.hardlink boost\graph\gursoy_atun_layout.hpp
Hardlink created for boost\graph\gursoy_atun_layout.hpp <<===>> libs\graph\include\boost\graph\gursoy_atun_layout.hpp
...on 300th target...
link.hardlink boost\graph\hawick_circuits.hpp
Hardlink created for boost\graph\hawick_circuits.hpp <<===>> libs\graph\include\boost\graph\hawick_circuits.hpp
link.hardlink boost\graph\is_kuratowski_subgraph.hpp
Hardlink created for boost\graph\is_kuratowski_subgraph.hpp <<===>> libs\graph\include\boost\graph\is_kuratowski_subgraph.hpp
link.hardlink boost\graph\incremental_components.hpp
Hardlink created for boost\graph\incremental_components.hpp <<===>> libs\graph\include\boost\graph\incremental_components.hpp
link.hardlink boost\graph\howard_cycle_ratio.hpp
Hardlink created for boost\graph\howard_cycle_ratio.hpp <<===>> libs\graph\include\boost\graph\howard_cycle_ratio.hpp
link.hardlink boost\graph\grid_graph.hpp
Hardlink created for boost\graph\grid_graph.hpp <<===>> libs\graph\include\boost\graph\grid_graph.hpp
link.hardlink boost\graph\graph_utility.hpp
Hardlink created for boost\graph\graph_utility.hpp <<===>> libs\graph\include\boost\graph\graph_utility.hpp
link.hardlink boost\graph\isomorphism.hpp
Hardlink created for boost\graph\isomorphism.hpp <<===>> libs\graph\include\boost\graph\isomorphism.hpp
link.hardlink boost\graph\is_straight_line_drawing.hpp
Hardlink created for boost\graph\is_straight_line_drawing.hpp <<===>> libs\graph\include\boost\graph\is_straight_line_drawing.hpp
link.hardlink boost\graph\iteration_macros_undef.hpp
Hardlink created for boost\graph\iteration_macros_undef.hpp <<===>> libs\graph\include\boost\graph\iteration_macros_undef.hpp
link.hardlink boost\graph\johnson_all_pairs_shortest.hpp
Hardlink created for boost\graph\johnson_all_pairs_shortest.hpp <<===>> libs\graph\include\boost\graph\johnson_all_pairs_shortest.hpp
link.hardlink boost\graph\iteration_macros.hpp
Hardlink created for boost\graph\iteration_macros.hpp <<===>> libs\graph\include\boost\graph\iteration_macros.hpp
link.hardlink boost\graph\kamada_kawai_spring_layout.hpp
Hardlink created for boost\graph\kamada_kawai_spring_layout.hpp <<===>> libs\graph\include\boost\graph\kamada_kawai_spring_layout.hpp
link.hardlink boost\graph\labeled_graph.hpp
Hardlink created for boost\graph\labeled_graph.hpp <<===>> libs\graph\include\boost\graph\labeled_graph.hpp
link.hardlink boost\graph\leda_graph.hpp
Hardlink created for boost\graph\leda_graph.hpp <<===>> libs\graph\include\boost\graph\leda_graph.hpp
link.hardlink boost\graph\king_ordering.hpp
Hardlink created for boost\graph\king_ordering.hpp <<===>> libs\graph\include\boost\graph\king_ordering.hpp
link.hardlink boost\graph\make_biconnected_planar.hpp
Hardlink created for boost\graph\make_biconnected_planar.hpp <<===>> libs\graph\include\boost\graph\make_biconnected_planar.hpp
link.hardlink boost\graph\kruskal_min_spanning_tree.hpp
Hardlink created for boost\graph\kruskal_min_spanning_tree.hpp <<===>> libs\graph\include\boost\graph\kruskal_min_spanning_tree.hpp
link.hardlink boost\graph\make_connected.hpp
Hardlink created for boost\graph\make_connected.hpp <<===>> libs\graph\include\boost\graph\make_connected.hpp
link.hardlink boost\graph\loop_erased_random_walk.hpp
Hardlink created for boost\graph\loop_erased_random_walk.hpp <<===>> libs\graph\include\boost\graph\loop_erased_random_walk.hpp
link.hardlink boost\graph\lookup_edge.hpp
Hardlink created for boost\graph\lookup_edge.hpp <<===>> libs\graph\include\boost\graph\lookup_edge.hpp
link.hardlink boost\graph\matrix_as_graph.hpp
Hardlink created for boost\graph\matrix_as_graph.hpp <<===>> libs\graph\include\boost\graph\matrix_as_graph.hpp
link.hardlink boost\graph\make_maximal_planar.hpp
Hardlink created for boost\graph\make_maximal_planar.hpp <<===>> libs\graph\include\boost\graph\make_maximal_planar.hpp
link.hardlink boost\graph\maximum_adjacency_search.hpp
Hardlink created for boost\graph\maximum_adjacency_search.hpp <<===>> libs\graph\include\boost\graph\maximum_adjacency_search.hpp
link.hardlink boost\graph\max_cardinality_matching.hpp
Hardlink created for boost\graph\max_cardinality_matching.hpp <<===>> libs\graph\include\boost\graph\max_cardinality_matching.hpp
link.hardlink boost\graph\maximum_weighted_matching.hpp
Hardlink created for boost\graph\maximum_weighted_matching.hpp <<===>> libs\graph\include\boost\graph\maximum_weighted_matching.hpp
link.hardlink boost\graph\mesh_graph_generator.hpp
Hardlink created for boost\graph\mesh_graph_generator.hpp <<===>> libs\graph\include\boost\graph\mesh_graph_generator.hpp
link.hardlink boost\graph\mcgregor_common_subgraphs.hpp
Hardlink created for boost\graph\mcgregor_common_subgraphs.hpp <<===>> libs\graph\include\boost\graph\mcgregor_common_subgraphs.hpp
link.hardlink boost\graph\metis.hpp
Hardlink created for boost\graph\metis.hpp <<===>> libs\graph\include\boost\graph\metis.hpp
link.hardlink boost\graph\named_graph.hpp
Hardlink created for boost\graph\named_graph.hpp <<===>> libs\graph\include\boost\graph\named_graph.hpp
link.hardlink boost\graph\metric_tsp_approx.hpp
Hardlink created for boost\graph\metric_tsp_approx.hpp <<===>> libs\graph\include\boost\graph\metric_tsp_approx.hpp
link.hardlink boost\graph\neighbor_bfs.hpp
Hardlink created for boost\graph\neighbor_bfs.hpp <<===>> libs\graph\include\boost\graph\neighbor_bfs.hpp
link.hardlink boost\graph\minimum_degree_ordering.hpp
Hardlink created for boost\graph\minimum_degree_ordering.hpp <<===>> libs\graph\include\boost\graph\minimum_degree_ordering.hpp
link.hardlink boost\graph\named_function_params.hpp
Hardlink created for boost\graph\named_function_params.hpp <<===>> libs\graph\include\boost\graph\named_function_params.hpp
link.hardlink boost\graph\overloading.hpp
Hardlink created for boost\graph\overloading.hpp <<===>> libs\graph\include\boost\graph\overloading.hpp
link.hardlink boost\graph\numeric_values.hpp
Hardlink created for boost\graph\numeric_values.hpp <<===>> libs\graph\include\boost\graph\numeric_values.hpp
mklink-or-dir boost\graph\planar_detail
Junction created for boost\graph\planar_detail <<===>> libs\graph\include\boost\graph\planar_detail
link.hardlink boost\graph\page_rank.hpp
Hardlink created for boost\graph\page_rank.hpp <<===>> libs\graph\include\boost\graph\page_rank.hpp
link.hardlink boost\graph\one_bit_color_map.hpp
Hardlink created for boost\graph\one_bit_color_map.hpp <<===>> libs\graph\include\boost\graph\one_bit_color_map.hpp
link.hardlink boost\graph\planar_face_traversal.hpp
Hardlink created for boost\graph\planar_face_traversal.hpp <<===>> libs\graph\include\boost\graph\planar_face_traversal.hpp
link.hardlink boost\graph\planar_canonical_ordering.hpp
Hardlink created for boost\graph\planar_canonical_ordering.hpp <<===>> libs\graph\include\boost\graph\planar_canonical_ordering.hpp
link.hardlink boost\graph\plod_generator.hpp
Hardlink created for boost\graph\plod_generator.hpp <<===>> libs\graph\include\boost\graph\plod_generator.hpp
link.hardlink boost\graph\point_traits.hpp
Hardlink created for boost\graph\point_traits.hpp <<===>> libs\graph\include\boost\graph\point_traits.hpp
link.hardlink boost\graph\properties.hpp
Hardlink created for boost\graph\properties.hpp <<===>> libs\graph\include\boost\graph\properties.hpp
mklink-or-dir boost\graph\property_maps
Junction created for boost\graph\property_maps <<===>> libs\graph\include\boost\graph\property_maps
link.hardlink boost\graph\prim_minimum_spanning_tree.hpp
Hardlink created for boost\graph\prim_minimum_spanning_tree.hpp <<===>> libs\graph\include\boost\graph\prim_minimum_spanning_tree.hpp
link.hardlink boost\graph\profile.hpp
Hardlink created for boost\graph\profile.hpp <<===>> libs\graph\include\boost\graph\profile.hpp
link.hardlink boost\graph\random_layout.hpp
Hardlink created for boost\graph\random_layout.hpp <<===>> libs\graph\include\boost\graph\random_layout.hpp
link.hardlink boost\graph\random.hpp
Hardlink created for boost\graph\random.hpp <<===>> libs\graph\include\boost\graph\random.hpp
link.hardlink boost\graph\push_relabel_max_flow.hpp
Hardlink created for boost\graph\push_relabel_max_flow.hpp <<===>> libs\graph\include\boost\graph\push_relabel_max_flow.hpp
link.hardlink boost\graph\read_dimacs.hpp
Hardlink created for boost\graph\read_dimacs.hpp <<===>> libs\graph\include\boost\graph\read_dimacs.hpp
link.hardlink boost\graph\reverse_graph.hpp
Hardlink created for boost\graph\reverse_graph.hpp <<===>> libs\graph\include\boost\graph\reverse_graph.hpp
link.hardlink boost\graph\property_iter_range.hpp
Hardlink created for boost\graph\property_iter_range.hpp <<===>> libs\graph\include\boost\graph\property_iter_range.hpp
link.hardlink boost\graph\relax.hpp
Hardlink created for boost\graph\relax.hpp <<===>> libs\graph\include\boost\graph\relax.hpp
link.hardlink boost\graph\random_spanning_tree.hpp
Hardlink created for boost\graph\random_spanning_tree.hpp <<===>> libs\graph\include\boost\graph\random_spanning_tree.hpp
link.hardlink boost\graph\sequential_vertex_coloring.hpp
Hardlink created for boost\graph\sequential_vertex_coloring.hpp <<===>> libs\graph\include\boost\graph\sequential_vertex_coloring.hpp
link.hardlink boost\graph\smallest_last_ordering.hpp
Hardlink created for boost\graph\smallest_last_ordering.hpp <<===>> libs\graph\include\boost\graph\smallest_last_ordering.hpp
link.hardlink boost\graph\rmat_graph_generator.hpp
Hardlink created for boost\graph\rmat_graph_generator.hpp <<===>> libs\graph\include\boost\graph\rmat_graph_generator.hpp
link.hardlink boost\graph\simple_point.hpp
Hardlink created for boost\graph\simple_point.hpp <<===>> libs\graph\include\boost\graph\simple_point.hpp
link.hardlink boost\graph\sloan_ordering.hpp
Hardlink created for boost\graph\sloan_ordering.hpp <<===>> libs\graph\include\boost\graph\sloan_ordering.hpp
link.hardlink boost\graph\small_world_generator.hpp
Hardlink created for boost\graph\small_world_generator.hpp <<===>> libs\graph\include\boost\graph\small_world_generator.hpp
link.hardlink boost\graph\r_c_shortest_paths.hpp
Hardlink created for boost\graph\r_c_shortest_paths.hpp <<===>> libs\graph\include\boost\graph\r_c_shortest_paths.hpp
link.hardlink boost\graph\ssca_graph_generator.hpp
Hardlink created for boost\graph\ssca_graph_generator.hpp <<===>> libs\graph\include\boost\graph\ssca_graph_generator.hpp
link.hardlink boost\graph\stanford_graph.hpp
Hardlink created for boost\graph\stanford_graph.hpp <<===>> libs\graph\include\boost\graph\stanford_graph.hpp
link.hardlink boost\graph\subgraph.hpp
Hardlink created for boost\graph\subgraph.hpp <<===>> libs\graph\include\boost\graph\subgraph.hpp
link.hardlink boost\graph\stoer_wagner_min_cut.hpp
Hardlink created for boost\graph\stoer_wagner_min_cut.hpp <<===>> libs\graph\include\boost\graph\stoer_wagner_min_cut.hpp
link.hardlink boost\graph\strong_components.hpp
Hardlink created for boost\graph\strong_components.hpp <<===>> libs\graph\include\boost\graph\strong_components.hpp
link.hardlink boost\graph\topological_sort.hpp
Hardlink created for boost\graph\topological_sort.hpp <<===>> libs\graph\include\boost\graph\topological_sort.hpp
link.hardlink boost\graph\tiernan_all_cycles.hpp
Hardlink created for boost\graph\tiernan_all_cycles.hpp <<===>> libs\graph\include\boost\graph\tiernan_all_cycles.hpp
link.hardlink boost\graph\successive_shortest_path_nonnegative_weights.hpp
Hardlink created for boost\graph\successive_shortest_path_nonnegative_weights.hpp <<===>> libs\graph\include\boost\graph\successive_shortest_path_nonnegative_weights.hpp
link.hardlink boost\graph\transitive_closure.hpp
Hardlink created for boost\graph\transitive_closure.hpp <<===>> libs\graph\include\boost\graph\transitive_closure.hpp
link.hardlink boost\graph\st_connected.hpp
Hardlink created for boost\graph\st_connected.hpp <<===>> libs\graph\include\boost\graph\st_connected.hpp
link.hardlink boost\graph\topology.hpp
Hardlink created for boost\graph\topology.hpp <<===>> libs\graph\include\boost\graph\topology.hpp
link.hardlink boost\graph\tree_traits.hpp
Hardlink created for boost\graph\tree_traits.hpp <<===>> libs\graph\include\boost\graph\tree_traits.hpp
link.hardlink boost\graph\transitive_reduction.hpp
Hardlink created for boost\graph\transitive_reduction.hpp <<===>> libs\graph\include\boost\graph\transitive_reduction.hpp
link.hardlink boost\graph\two_bit_color_map.hpp
Hardlink created for boost\graph\two_bit_color_map.hpp <<===>> libs\graph\include\boost\graph\two_bit_color_map.hpp
link.hardlink boost\graph\undirected_dfs.hpp
Hardlink created for boost\graph\undirected_dfs.hpp <<===>> libs\graph\include\boost\graph\undirected_dfs.hpp
link.hardlink boost\graph\transpose_graph.hpp
Hardlink created for boost\graph\transpose_graph.hpp <<===>> libs\graph\include\boost\graph\transpose_graph.hpp
link.hardlink boost\graph\two_graphs_common_spanning_trees.hpp
Hardlink created for boost\graph\two_graphs_common_spanning_trees.hpp <<===>> libs\graph\include\boost\graph\two_graphs_common_spanning_trees.hpp
link.hardlink boost\graph\undirected_graph.hpp
Hardlink created for boost\graph\undirected_graph.hpp <<===>> libs\graph\include\boost\graph\undirected_graph.hpp
link.hardlink boost\graph\vertex_and_edge_range.hpp
Hardlink created for boost\graph\vertex_and_edge_range.hpp <<===>> libs\graph\include\boost\graph\vertex_and_edge_range.hpp
link.hardlink boost\graph\use_mpi.hpp
Hardlink created for boost\graph\use_mpi.hpp <<===>> libs\graph\include\boost\graph\use_mpi.hpp
link.hardlink boost\graph\vf2_sub_graph_iso.hpp
Hardlink created for boost\graph\vf2_sub_graph_iso.hpp <<===>> libs\graph\include\boost\graph\vf2_sub_graph_iso.hpp
link.hardlink boost\graph\vector_as_graph.hpp
Hardlink created for boost\graph\vector_as_graph.hpp <<===>> libs\graph\include\boost\graph\vector_as_graph.hpp
link.hardlink boost\graph\accounting.hpp
Hardlink created for boost\graph\accounting.hpp <<===>> libs\graph_parallel\include\boost\graph\accounting.hpp
link.hardlink boost\graph\visitors.hpp
Hardlink created for boost\graph\visitors.hpp <<===>> libs\graph\include\boost\graph\visitors.hpp
mklink-or-dir boost\graph\distributed
Junction created for boost\graph\distributed <<===>> libs\graph_parallel\include\boost\graph\distributed
link.hardlink boost\graph\wavefront.hpp
Hardlink created for boost\graph\wavefront.hpp <<===>> libs\graph\include\boost\graph\wavefront.hpp
mklink-or-dir boost\graph\parallel
Junction created for boost\graph\parallel <<===>> libs\graph_parallel\include\boost\graph\parallel
mklink-or-dir boost\heap
Junction created for boost\heap <<===>> libs\heap\include\boost\heap
link.hardlink boost\histogram.hpp
Hardlink created for boost\histogram.hpp <<===>> libs\histogram\include\boost\histogram.hpp
link.hardlink boost\graph\write_dimacs.hpp
Hardlink created for boost\graph\write_dimacs.hpp <<===>> libs\graph\include\boost\graph\write_dimacs.hpp
mklink-or-dir boost\icl
Junction created for boost\icl <<===>> libs\icl\include\boost\icl
mklink-or-dir boost\histogram
Junction created for boost\histogram <<===>> libs\histogram\include\boost\histogram
mklink-or-dir boost\hof
Junction created for boost\hof <<===>> libs\hof\include\boost\hof
link.hardlink boost\hof.hpp
Hardlink created for boost\hof.hpp <<===>> libs\hof\include\boost\hof.hpp
link.hardlink boost\integer.hpp
Hardlink created for boost\integer.hpp <<===>> libs\integer\include\boost\integer.hpp
link.hardlink boost\integer_fwd.hpp
Hardlink created for boost\integer_fwd.hpp <<===>> libs\integer\include\boost\integer_fwd.hpp
link.hardlink boost\integer_traits.hpp
Hardlink created for boost\integer_traits.hpp <<===>> libs\integer\include\boost\integer_traits.hpp
mklink-or-dir boost\intrusive
Junction created for boost\intrusive <<===>> libs\intrusive\include\boost\intrusive
mklink-or-dir boost\integer
Junction created for boost\integer <<===>> libs\integer\include\boost\integer
...on 400th target...
mklink-or-dir boost\interprocess
Junction created for boost\interprocess <<===>> libs\interprocess\include\boost\interprocess
mklink-or-dir boost\iostreams
Junction created for boost\iostreams <<===>> libs\iostreams\include\boost\iostreams
mklink-or-dir boost\io
Junction created for boost\io <<===>> libs\io\include\boost\io
link.hardlink boost\io_fwd.hpp
Hardlink created for boost\io_fwd.hpp <<===>> libs\io\include\boost\io_fwd.hpp
link.hardlink boost\indirect_reference.hpp
Hardlink created for boost\indirect_reference.hpp <<===>> libs\iterator\include\boost\indirect_reference.hpp
link.hardlink boost\generator_iterator.hpp
Hardlink created for boost\generator_iterator.hpp <<===>> libs\iterator\include\boost\generator_iterator.hpp
link.hardlink boost\function_output_iterator.hpp
Hardlink created for boost\function_output_iterator.hpp <<===>> libs\iterator\include\boost\function_output_iterator.hpp
link.hardlink boost\next_prior.hpp
Hardlink created for boost\next_prior.hpp <<===>> libs\iterator\include\boost\next_prior.hpp
mklink-or-dir boost\iterator
Junction created for boost\iterator <<===>> libs\iterator\include\boost\iterator
link.hardlink boost\iterator_adaptors.hpp
Hardlink created for boost\iterator_adaptors.hpp <<===>> libs\iterator\include\boost\iterator_adaptors.hpp
mklink-or-dir boost\json
Junction created for boost\json <<===>> libs\json\include\boost\json
link.hardlink boost\pointee.hpp
Hardlink created for boost\pointee.hpp <<===>> libs\iterator\include\boost\pointee.hpp
link.hardlink boost\shared_container_iterator.hpp
Hardlink created for boost\shared_container_iterator.hpp <<===>> libs\iterator\include\boost\shared_container_iterator.hpp
link.hardlink boost\json.hpp
Hardlink created for boost\json.hpp <<===>> libs\json\include\boost\json.hpp
mklink-or-dir boost\lambda
Junction created for boost\lambda <<===>> libs\lambda\include\boost\lambda
mklink-or-dir boost\lambda2
Junction created for boost\lambda2 <<===>> libs\lambda2\include\boost\lambda2
link.hardlink boost\lambda2.hpp
Hardlink created for boost\lambda2.hpp <<===>> libs\lambda2\include\boost\lambda2.hpp
mklink-or-dir boost\leaf
Junction created for boost\leaf <<===>> libs\leaf\include\boost\leaf
link.hardlink boost\leaf.hpp
Hardlink created for boost\leaf.hpp <<===>> libs\leaf\include\boost\leaf.hpp
mklink-or-dir boost\lexical_cast
Junction created for boost\lexical_cast <<===>> libs\lexical_cast\include\boost\lexical_cast
link.hardlink boost\lexical_cast.hpp
Hardlink created for boost\lexical_cast.hpp <<===>> libs\lexical_cast\include\boost\lexical_cast.hpp
link.hardlink boost\locale.hpp
Hardlink created for boost\locale.hpp <<===>> libs\locale\include\boost\locale.hpp
mklink-or-dir boost\lockfree
Junction created for boost\lockfree <<===>> libs\lockfree\include\boost\lockfree
mklink-or-dir boost\local_function
Junction created for boost\local_function <<===>> libs\local_function\include\boost\local_function
mklink-or-dir boost\log
Junction created for boost\log <<===>> libs\log\include\boost\log
mklink-or-dir boost\locale
Junction created for boost\locale <<===>> libs\locale\include\boost\locale
mklink-or-dir boost\math
Junction created for boost\math <<===>> libs\math\include\boost\math
link.hardlink boost\cstdfloat.hpp
Hardlink created for boost\cstdfloat.hpp <<===>> libs\math\include\boost\cstdfloat.hpp
mklink-or-dir boost\logic
Junction created for boost\logic <<===>> libs\logic\include\boost\logic
link.hardlink boost\local_function.hpp
Hardlink created for boost\local_function.hpp <<===>> libs\local_function\include\boost\local_function.hpp
link.hardlink boost\math_fwd.hpp
Hardlink created for boost\math_fwd.hpp <<===>> libs\math\include\boost\math_fwd.hpp
mklink-or-dir boost\move
Junction created for boost\move <<===>> libs\move\include\boost\move
mklink-or-dir boost\metaparse
Junction created for boost\metaparse <<===>> libs\metaparse\include\boost\metaparse
link.hardlink boost\metaparse.hpp
Hardlink created for boost\metaparse.hpp <<===>> libs\metaparse\include\boost\metaparse.hpp
mklink-or-dir boost\mp11
Junction created for boost\mp11 <<===>> libs\mp11\include\boost\mp11
link.hardlink boost\mp11.hpp
Hardlink created for boost\mp11.hpp <<===>> libs\mp11\include\boost\mp11.hpp
mklink-or-dir boost\mpi
Junction created for boost\mpi <<===>> libs\mpi\include\boost\mpi
link.hardlink boost\mpi.hpp
Hardlink created for boost\mpi.hpp <<===>> libs\mpi\include\boost\mpi.hpp
mklink-or-dir boost\mpl
Junction created for boost\mpl <<===>> libs\mpl\include\boost\mpl
mklink-or-dir boost\multi_array
Junction created for boost\multi_array <<===>> libs\multi_array\include\boost\multi_array
mklink-or-dir boost\multiprecision
Junction created for boost\multiprecision <<===>> libs\multiprecision\include\boost\multiprecision
mklink-or-dir boost\msm
Junction created for boost\msm <<===>> libs\msm\include\boost\msm
link.hardlink boost\multi_array.hpp
Hardlink created for boost\multi_array.hpp <<===>> libs\multi_array\include\boost\multi_array.hpp
mklink-or-dir boost\multi_index
Junction created for boost\multi_index <<===>> libs\multi_index\include\boost\multi_index
link.hardlink boost\multi_index_container.hpp
Hardlink created for boost\multi_index_container.hpp <<===>> libs\multi_index\include\boost\multi_index_container.hpp
link.hardlink boost\multi_index_container_fwd.hpp
Hardlink created for boost\multi_index_container_fwd.hpp <<===>> libs\multi_index\include\boost\multi_index_container_fwd.hpp
mklink-or-dir boost\mysql
Junction created for boost\mysql <<===>> libs\mysql\include\boost\mysql
link.hardlink boost\mysql.hpp
Hardlink created for boost\mysql.hpp <<===>> libs\mysql\include\boost\mysql.hpp
link.hardlink boost\none.hpp
Hardlink created for boost\none.hpp <<===>> libs\optional\include\boost\none.hpp
mklink-or-dir boost\optional
Junction created for boost\optional <<===>> libs\optional\include\boost\optional
mklink-or-dir boost\nowide
Junction created for boost\nowide <<===>> libs\nowide\include\boost\nowide
link.hardlink boost\none_t.hpp
Hardlink created for boost\none_t.hpp <<===>> libs\optional\include\boost\none_t.hpp
mklink-or-dir boost\parameter
mklink-or-dir boost\outcome
Junction created for boost\outcome <<===>> libs\outcome\include\boost\outcome
link.hardlink boost\outcome.hpp
Hardlink created for boost\outcome.hpp <<===>> libs\outcome\include\boost\outcome.hpp
link.hardlink boost\parameter.hpp
Hardlink created for boost\parameter.hpp <<===>> libs\parameter\include\boost\parameter.hpp
link.hardlink boost\pfr.hpp
Hardlink created for boost\pfr.hpp <<===>> libs\pfr\include\boost\pfr.hpp
mklink-or-dir boost\phoenix
Junction created for boost\phoenix <<===>> libs\phoenix\include\boost\phoenix
link.hardlink boost\optional.hpp
Hardlink created for boost\optional.hpp <<===>> libs\optional\include\boost\optional.hpp
mklink-or-dir boost\poly_collection
Junction created for boost\poly_collection <<===>> libs\poly_collection\include\boost\poly_collection
link.hardlink boost\phoenix.hpp
Hardlink created for boost\phoenix.hpp <<===>> libs\phoenix\include\boost\phoenix.hpp
mklink-or-dir boost\pfr
Junction created for boost\pfr <<===>> libs\pfr\include\boost\pfr
mklink-or-dir boost\pool
Junction created for boost\pool <<===>> libs\pool\include\boost\pool
link.hardlink boost\parameter\are_tagged_arguments.hpp
Hardlink created for boost\parameter\are_tagged_arguments.hpp <<===>> libs\parameter\include\boost\parameter\are_tagged_arguments.hpp
mklink-or-dir boost\parameter\aux_
mklink-or-dir boost\polygon
Junction created for boost\polygon <<===>> libs\polygon\include\boost\polygon
link.hardlink boost\parameter\binding.hpp
Hardlink created for boost\parameter\binding.hpp <<===>> libs\parameter\include\boost\parameter\binding.hpp
link.hardlink boost\parameter\config.hpp
Hardlink created for boost\parameter\config.hpp <<===>> libs\parameter\include\boost\parameter\config.hpp
link.hardlink boost\parameter\compose.hpp
Hardlink created for boost\parameter\compose.hpp <<===>> libs\parameter\include\boost\parameter\compose.hpp
link.hardlink boost\parameter\deduced.hpp
Hardlink created for boost\parameter\deduced.hpp <<===>> libs\parameter\include\boost\parameter\deduced.hpp
glink.hardlink boost\parameter\is_argument_pack.hpp
Hardlink created for boost\parameter\is_argument_pack.hpp <<===>> libs\parameter\include\boost\parameter\is_argument_pack.hpp
link.hardlink boost\parameter\keyword.hpp
Hardlink created for boost\parameter\keyword.hpp <<===>> libs\parameter\include\boost\parameter\keyword.hpp
link.hardlink boost\parameter\name.hpp
Hardlink created for boost\parameter\name.hpp <<===>> libs\parameter\include\boost\parameter\name.hpp
link.hardlink boost\parameter\keyword_fwd.hpp
Hardlink created for boost\parameter\keyword_fwd.hpp <<===>> libs\parameter\include\boost\parameter\keyword_fwd.hpp
link.hardlink boost\parameter\match.hpp
Hardlink created for boost\parameter\match.hpp <<===>> libs\parameter\include\boost\parameter\match.hpp
link.hardlink boost\parameter\aux_\always_true_predicate.hpp
Hardlink created for boost\parameter\aux_\always_true_predicate.hpp <<===>> libs\parameter\include\boost\parameter\aux_\always_true_predicate.hpp
link.hardlink boost\parameter\macros.hpp
Hardlink created for boost\parameter\macros.hpp <<===>> libs\parameter\include\boost\parameter\macros.hpp
link.hardlink boost\parameter\aux_\arg_list.hpp
Hardlink created for boost\parameter\aux_\arg_list.hpp <<===>> libs\parameter\include\boost\parameter\aux_\arg_list.hpp
link.hardlink boost\parameter\aux_\as_lvalue.hpp
Hardlink created for boost\parameter\aux_\as_lvalue.hpp <<===>> libs\parameter\include\boost\parameter\aux_\as_lvalue.hpp
link.hardlink boost\parameter\aux_\cast.hpp
Hardlink created for boost\parameter\aux_\cast.hpp <<===>> libs\parameter\include\boost\parameter\aux_\cast.hpp
link.hardlink boost\parameter\aux_\default.hpp
Hardlink created for boost\parameter\aux_\default.hpp <<===>> libs\parameter\include\boost\parameter\aux_\default.hpp
link.hardlink boost\parameter\aux_\augment_predicate.hpp
Hardlink created for boost\parameter\aux_\augment_predicate.hpp <<===>> libs\parameter\include\boost\parameter\aux_\augment_predicate.hpp
link.hardlink boost\parameter\aux_\is_maybe.hpp
Hardlink created for boost\parameter\aux_\is_maybe.hpp <<===>> libs\parameter\include\boost\parameter\aux_\is_maybe.hpp
link.hardlink boost\parameter\aux_\is_placeholder.hpp
Hardlink created for boost\parameter\aux_\is_placeholder.hpp <<===>> libs\parameter\include\boost\parameter\aux_\is_placeholder.hpp
link.hardlink boost\parameter\aux_\has_nested_template_fn.hpp
Hardlink created for boost\parameter\aux_\has_nested_template_fn.hpp <<===>> libs\parameter\include\boost\parameter\aux_\has_nested_template_fn.hpp
link.hardlink boost\parameter\aux_\is_tagged_argument.hpp
Hardlink created for boost\parameter\aux_\is_tagged_argument.hpp <<===>> libs\parameter\include\boost\parameter\aux_\is_tagged_argument.hpp
link.hardlink boost\parameter\aux_\maybe.hpp
Hardlink created for boost\parameter\aux_\maybe.hpp <<===>> libs\parameter\include\boost\parameter\aux_\maybe.hpp
link.hardlink boost\parameter\aux_\name.hpp
Hardlink created for boost\parameter\aux_\name.hpp <<===>> libs\parameter\include\boost\parameter\aux_\name.hpp
link.hardlink boost\parameter\aux_\parameter_requirements.hpp
Hardlink created for boost\parameter\aux_\parameter_requirements.hpp <<===>> libs\parameter\include\boost\parameter\aux_\parameter_requirements.hpp
link.hardlink boost\parameter\aux_\lambda_tag.hpp
Hardlink created for boost\parameter\aux_\lambda_tag.hpp <<===>> libs\parameter\include\boost\parameter\aux_\lambda_tag.hpp
mklink-or-dir boost\parameter\aux_\pack
Junction created for boost\parameter\aux_\pack <<===>> libs\parameter\include\boost\parameter\aux_\pack
mklink-or-dir boost\parameter\aux_\pp_impl
Junction created for boost\parameter\aux_\pp_impl <<===>> libs\parameter\include\boost\parameter\aux_\pp_impl
mklink-or-dir boost\parameter\aux_\preprocessor
Junction created for boost\parameter\aux_\preprocessor <<===>> libs\parameter\include\boost\parameter\aux_\preprocessor
link.hardlink boost\parameter\aux_\parenthesized_type.hpp
Hardlink created for boost\parameter\aux_\parenthesized_type.hpp <<===>> libs\parameter\include\boost\parameter\aux_\parenthesized_type.hpp
link.hardlink boost\parameter\aux_\result_of0.hpp
Hardlink created for boost\parameter\aux_\result_of0.hpp <<===>> libs\parameter\include\boost\parameter\aux_\result_of0.hpp
link.hardlink boost\parameter\aux_\set.hpp
Hardlink created for boost\parameter\aux_\set.hpp <<===>> libs\parameter\include\boost\parameter\aux_\set.hpp
link.hardlink boost\parameter\aux_\tag.hpp
Hardlink created for boost\parameter\aux_\tag.hpp <<===>> libs\parameter\include\boost\parameter\aux_\tag.hpp
link.hardlink boost\parameter\aux_\tagged_argument.hpp
Hardlink created for boost\parameter\aux_\tagged_argument.hpp <<===>> libs\parameter\include\boost\parameter\aux_\tagged_argument.hpp
link.hardlink boost\parameter\aux_\unwrap_cv_reference.hpp
Hardlink created for boost\parameter\aux_\unwrap_cv_reference.hpp <<===>> libs\parameter\include\boost\parameter\aux_\unwrap_cv_reference.hpp
link.hardlink boost\parameter\aux_\tagged_argument_fwd.hpp
Hardlink created for boost\parameter\aux_\tagged_argument_fwd.hpp <<===>> libs\parameter\include\boost\parameter\aux_\tagged_argument_fwd.hpp
...on 500th target...
link.hardlink boost\parameter\aux_\use_default_tag.hpp
Hardlink created for boost\parameter\aux_\use_default_tag.hpp <<===>> libs\parameter\include\boost\parameter\aux_\use_default_tag.hpp
mklink-or-dir boost\parameter\aux_\python
Junction created for boost\parameter\aux_\python <<===>> libs\parameter_python\include\boost\parameter\aux_\python
link.hardlink boost\parameter\aux_\yesno.hpp
Hardlink created for boost\parameter\aux_\yesno.hpp <<===>> libs\parameter\include\boost\parameter\aux_\yesno.hpp
link.hardlink boost\parameter\aux_\void.hpp
Hardlink created for boost\parameter\aux_\void.hpp <<===>> libs\parameter\include\boost\parameter\aux_\void.hpp
link.hardlink boost\parameter\nested_keyword.hpp
Hardlink created for boost\parameter\nested_keyword.hpp <<===>> libs\parameter\include\boost\parameter\nested_keyword.hpp
link.hardlink boost\parameter\aux_\use_default.hpp
Hardlink created for boost\parameter\aux_\use_default.hpp <<===>> libs\parameter\include\boost\parameter\aux_\use_default.hpp
link.hardlink boost\parameter\aux_\template_keyword.hpp
Hardlink created for boost\parameter\aux_\template_keyword.hpp <<===>> libs\parameter\include\boost\parameter\aux_\template_keyword.hpp
link.hardlink boost\parameter\optional.hpp
Hardlink created for boost\parameter\optional.hpp <<===>> libs\parameter\include\boost\parameter\optional.hpp
link.hardlink boost\parameter\parameters.hpp
Hardlink created for boost\parameter\parameters.hpp <<===>> libs\parameter\include\boost\parameter\parameters.hpp
link.hardlink boost\parameter\preprocessor.hpp
Hardlink created for boost\parameter\preprocessor.hpp <<===>> libs\parameter\include\boost\parameter\preprocessor.hpp
link.hardlink boost\parameter\preprocessor_no_spec.hpp
Hardlink created for boost\parameter\preprocessor_no_spec.hpp <<===>> libs\parameter\include\boost\parameter\preprocessor_no_spec.hpp
link.hardlink boost\parameter\required.hpp
Hardlink created for boost\parameter\required.hpp <<===>> libs\parameter\include\boost\parameter\required.hpp
link.hardlink boost\parameter\value_type.hpp
Hardlink created for boost\parameter\value_type.hpp <<===>> libs\parameter\include\boost\parameter\value_type.hpp
link.hardlink boost\parameter\python.hpp
Hardlink created for boost\parameter\python.hpp <<===>> libs\parameter_python\include\boost\parameter\python.hpp
link.hardlink boost\predef.h
Hardlink created for boost\predef.h <<===>> libs\predef\include\boost\predef.h
link.hardlink boost\parameter\template_keyword.hpp
Hardlink created for boost\parameter\template_keyword.hpp <<===>> libs\parameter\include\boost\parameter\template_keyword.hpp
link.hardlink boost\process.hpp
Hardlink created for boost\process.hpp <<===>> libs\process\include\boost\process.hpp
mklink-or-dir boost\preprocessor
Junction created for boost\preprocessor <<===>> libs\preprocessor\include\boost\preprocessor
mklink-or-dir boost\program_options
Junction created for boost\program_options <<===>> libs\program_options\include\boost\program_options
mklink-or-dir boost\process
Junction created for boost\process <<===>> libs\process\include\boost\process
mklink-or-dir boost\predef
Junction created for boost\predef <<===>> libs\predef\include\boost\predef
mklink-or-dir boost\property_tree
Junction created for boost\property_tree <<===>> libs\property_tree\include\boost\property_tree
mklink-or-dir boost\property_map
link.hardlink boost\program_options.hpp
Hardlink created for boost\program_options.hpp <<===>> libs\program_options\include\boost\program_options.hpp
link.hardlink boost\preprocessor.hpp
Hardlink created for boost\preprocessor.hpp <<===>> libs\preprocessor\include\boost\preprocessor.hpp
mklink-or-dir boost\proto
Junction created for boost\proto <<===>> libs\proto\include\boost\proto
mklink-or-dir boost\python
Junction created for boost\python <<===>> libs\python\include\boost\python
mklink-or-dir boost\qvm
Junction created for boost\qvm <<===>> libs\qvm\include\boost\qvm
mklink-or-dir boost\ptr_container
Junction created for boost\ptr_container <<===>> libs\ptr_container\include\boost\ptr_container
link.hardlink boost\qvm.hpp
Hardlink created for boost\qvm.hpp <<===>> libs\qvm\include\boost\qvm.hpp
link.hardlink boost\qvm_lite.hpp
Hardlink created for boost\qvm_lite.hpp <<===>> libs\qvm\include\boost\qvm_lite.hpp
link.hardlink boost\python.hpp
Hardlink created for boost\python.hpp <<===>> libs\python\include\boost\python.hpp
mklink-or-dir boost\random
Junction created for boost\random <<===>> libs\random\include\boost\random
link.hardlink boost\nondet_random.hpp
Hardlink created for boost\nondet_random.hpp <<===>> libs\random\include\boost\nondet_random.hpp
link.hardlink boost\property_map\dynamic_property_map.hpp
Hardlink created for boost\property_map\dynamic_property_map.hpp <<===>> libs\property_map\include\boost\property_map\dynamic_property_map.hpp
link.hardlink boost\property_map\compose_property_map.hpp
Hardlink created for boost\property_map\compose_property_map.hpp <<===>> libs\property_map\include\boost\property_map\compose_property_map.hpp
link.hardlink boost\property_map\property_map.hpp
Hardlink created for boost\property_map\property_map.hpp <<===>> libs\property_map\include\boost\property_map\property_map.hpp
link.hardlink boost\property_map\shared_array_property_map.hpp
Hardlink created for boost\property_map\shared_array_property_map.hpp <<===>> libs\property_map\include\boost\property_map\shared_array_property_map.hpp
link.hardlink boost\property_map\function_property_map.hpp
Hardlink created for boost\property_map\function_property_map.hpp <<===>> libs\property_map\include\boost\property_map\function_property_map.hpp
link.hardlink boost\property_map\property_map_iterator.hpp
Hardlink created for boost\property_map\property_map_iterator.hpp <<===>> libs\property_map\include\boost\property_map\property_map_iterator.hpp
link.hardlink boost\property_map\transform_value_property_map.hpp
Hardlink created for boost\property_map\transform_value_property_map.hpp <<===>> libs\property_map\include\boost\property_map\transform_value_property_map.hpp
link.hardlink boost\property_map\vector_property_map.hpp
Hardlink created for boost\property_map\vector_property_map.hpp <<===>> libs\property_map\include\boost\property_map\vector_property_map.hpp
link.hardlink boost\random.hpp
Hardlink created for boost\random.hpp <<===>> libs\random\include\boost\random.hpp
link.hardlink boost\range.hpp
Hardlink created for boost\range.hpp <<===>> libs\range\include\boost\range.hpp
mklink-or-dir boost\ratio
Junction created for boost\ratio <<===>> libs\ratio\include\boost\ratio
mklink-or-dir boost\property_map\parallel
Junction created for boost\property_map\parallel <<===>> libs\property_map_parallel\include\boost\property_map\parallel
mklink-or-dir boost\range
Junction created for boost\range <<===>> libs\range\include\boost\range
mklink-or-dir boost\redis
Junction created for boost\redis <<===>> libs\redis\include\boost\redis
link.hardlink boost\cregex.hpp
Hardlink created for boost\cregex.hpp <<===>> libs\regex\include\boost\cregex.hpp
link.hardlink boost\ratio.hpp
Hardlink created for boost\ratio.hpp <<===>> libs\ratio\include\boost\ratio.hpp
link.hardlink boost\rational.hpp
Hardlink created for boost\rational.hpp <<===>> libs\rational\include\boost\rational.hpp
link.hardlink boost\regex.h
Hardlink created for boost\regex.h <<===>> libs\regex\include\boost\regex.h
link.hardlink boost\redis.hpp
Hardlink created for boost\redis.hpp <<===>> libs\redis\include\boost\redis.hpp
link.hardlink boost\scope_exit.hpp
Hardlink created for boost\scope_exit.hpp <<===>> libs\scope_exit\include\boost\scope_exit.hpp
link.hardlink boost\regex_fwd.hpp
Hardlink created for boost\regex_fwd.hpp <<===>> libs\regex\include\boost\regex_fwd.hpp
mklink-or-dir boost\regex
Junction created for boost\regex <<===>> libs\regex\include\boost\regex
mklink-or-dir boost\safe_numerics
Junction created for boost\safe_numerics <<===>> libs\safe_numerics\include\boost\safe_numerics
link.hardlink boost\regex.hpp
Hardlink created for boost\regex.hpp <<===>> libs\regex\include\boost\regex.hpp
mklink-or-dir boost\serialization
Junction created for boost\serialization <<===>> libs\serialization\include\boost\serialization
mklink-or-dir boost\archive
Junction created for boost\archive <<===>> libs\serialization\include\boost\archive
mklink-or-dir boost\signals2
Junction created for boost\signals2 <<===>> libs\signals2\include\boost\signals2
link.hardlink boost\signals2.hpp
Hardlink created for boost\signals2.hpp <<===>> libs\signals2\include\boost\signals2.hpp
link.hardlink boost\intrusive_ptr.hpp
Hardlink created for boost\intrusive_ptr.hpp <<===>> libs\smart_ptr\include\boost\intrusive_ptr.hpp
link.hardlink boost\make_shared.hpp
Hardlink created for boost\make_shared.hpp <<===>> libs\smart_ptr\include\boost\make_shared.hpp
link.hardlink boost\make_unique.hpp
Hardlink created for boost\make_unique.hpp <<===>> libs\smart_ptr\include\boost\make_unique.hpp
link.hardlink boost\pointer_cast.hpp
Hardlink created for boost\pointer_cast.hpp <<===>> libs\smart_ptr\include\boost\pointer_cast.hpp
link.hardlink boost\pointer_to_other.hpp
Hardlink created for boost\pointer_to_other.hpp <<===>> libs\smart_ptr\include\boost\pointer_to_other.hpp
link.hardlink boost\enable_shared_from_this.hpp
Hardlink created for boost\enable_shared_from_this.hpp <<===>> libs\smart_ptr\include\boost\enable_shared_from_this.hpp
link.hardlink boost\scoped_array.hpp
Hardlink created for boost\scoped_array.hpp <<===>> libs\smart_ptr\include\boost\scoped_array.hpp
link.hardlink boost\shared_array.hpp
Hardlink created for boost\shared_array.hpp <<===>> libs\smart_ptr\include\boost\shared_array.hpp
link.hardlink boost\shared_ptr.hpp
Hardlink created for boost\shared_ptr.hpp <<===>> libs\smart_ptr\include\boost\shared_ptr.hpp
link.hardlink boost\scoped_ptr.hpp
Hardlink created for boost\scoped_ptr.hpp <<===>> libs\smart_ptr\include\boost\scoped_ptr.hpp
mklink-or-dir boost\spirit
Junction created for boost\spirit <<===>> libs\spirit\include\boost\spirit
link.hardlink boost\spirit.hpp
Hardlink created for boost\spirit.hpp <<===>> libs\spirit\include\boost\spirit.hpp
link.hardlink boost\weak_ptr.hpp
Hardlink created for boost\weak_ptr.hpp <<===>> libs\smart_ptr\include\boost\weak_ptr.hpp
link.hardlink boost\smart_ptr.hpp
Hardlink created for boost\smart_ptr.hpp <<===>> libs\smart_ptr\include\boost\smart_ptr.hpp
mklink-or-dir boost\sort
Junction created for boost\sort <<===>> libs\sort\include\boost\sort
mklink-or-dir boost\smart_ptr
Junction created for boost\smart_ptr <<===>> libs\smart_ptr\include\boost\smart_ptr
mklink-or-dir boost\stacktrace
Junction created for boost\stacktrace <<===>> libs\stacktrace\include\boost\stacktrace
mklink-or-dir boost\statechart
Junction created for boost\statechart <<===>> libs\statechart\include\boost\statechart
link.hardlink boost\stacktrace.hpp
Hardlink created for boost\stacktrace.hpp <<===>> libs\stacktrace\include\boost\stacktrace.hpp
mklink-or-dir boost\static_string
Junction created for boost\static_string <<===>> libs\static_string\include\boost\static_string
link.hardlink boost\static_assert.hpp
Hardlink created for boost\static_assert.hpp <<===>> libs\static_assert\include\boost\static_assert.hpp
link.hardlink boost\static_string.hpp
Hardlink created for boost\static_string.hpp <<===>> libs\static_string\include\boost\static_string.hpp
mklink-or-dir boost\system
Junction created for boost\system <<===>> libs\system\include\boost\system
link.hardlink boost\cerrno.hpp
Hardlink created for boost\cerrno.hpp <<===>> libs\system\include\boost\cerrno.hpp
mklink-or-dir boost\stl_interfaces
Junction created for boost\stl_interfaces <<===>> libs\stl_interfaces\include\boost\stl_interfaces
link.hardlink boost\system.hpp
Hardlink created for boost\system.hpp <<===>> libs\system\include\boost\system.hpp
mklink-or-dir boost\test
Junction created for boost\test <<===>> libs\test\include\boost\test
mklink-or-dir boost\thread
Junction created for boost\thread <<===>> libs\thread\include\boost\thread
link.hardlink boost\thread.hpp
Hardlink created for boost\thread.hpp <<===>> libs\thread\include\boost\thread.hpp
link.hardlink boost\throw_exception.hpp
Hardlink created for boost\throw_exception.hpp <<===>> libs\throw_exception\include\boost\throw_exception.hpp
link.hardlink boost\progress.hpp
Hardlink created for boost\progress.hpp <<===>> libs\timer\include\boost\progress.hpp
mklink-or-dir boost\timer
Junction created for boost\timer <<===>> libs\timer\include\boost\timer
link.hardlink boost\tokenizer.hpp
Hardlink created for boost\tokenizer.hpp <<===>> libs\tokenizer\include\boost\tokenizer.hpp
link.hardlink boost\token_functions.hpp
Hardlink created for boost\token_functions.hpp <<===>> libs\tokenizer\include\boost\token_functions.hpp
link.hardlink boost\token_iterator.hpp
Hardlink created for boost\token_iterator.hpp <<===>> libs\tokenizer\include\boost\token_iterator.hpp
mklink-or-dir boost\tti
Junction created for boost\tti <<===>> libs\tti\include\boost\tti
mklink-or-dir boost\type_erasure
Junction created for boost\type_erasure <<===>> libs\type_erasure\include\boost\type_erasure
mklink-or-dir boost\tuple
Junction created for boost\tuple <<===>> libs\tuple\include\boost\tuple
...on 600th target...
link.hardlink boost\type_index.hpp
Hardlink created for boost\type_index.hpp <<===>> libs\type_index\include\boost\type_index.hpp
mklink-or-dir boost\type_index
Junction created for boost\type_index <<===>> libs\type_index\include\boost\type_index
link.hardlink boost\timer.hpp
Hardlink created for boost\timer.hpp <<===>> libs\timer\include\boost\timer.hpp
link.hardlink boost\aligned_storage.hpp
Hardlink created for boost\aligned_storage.hpp <<===>> libs\type_traits\include\boost\aligned_storage.hpp
mklink-or-dir boost\type_traits
Junction created for boost\type_traits <<===>> libs\type_traits\include\boost\type_traits
mklink-or-dir boost\typeof
Junction created for boost\typeof <<===>> libs\typeof\include\boost\typeof
link.hardlink boost\type_traits.hpp
Hardlink created for boost\type_traits.hpp <<===>> libs\type_traits\include\boost\type_traits.hpp
mklink-or-dir boost\unordered
Junction created for boost\unordered <<===>> libs\unordered\include\boost\unordered
link.hardlink boost\unordered_map.hpp
Hardlink created for boost\unordered_map.hpp <<===>> libs\unordered\include\boost\unordered_map.hpp
mklink-or-dir boost\units
Junction created for boost\units <<===>> libs\units\include\boost\units
mklink-or-dir boost\url
Junction created for boost\url <<===>> libs\url\include\boost\url
link.hardlink boost\unordered_set.hpp
Hardlink created for boost\unordered_set.hpp <<===>> libs\unordered\include\boost\unordered_set.hpp
link.hardlink boost\url.hpp
Hardlink created for boost\url.hpp <<===>> libs\url\include\boost\url.hpp
link.hardlink boost\call_traits.hpp
Hardlink created for boost\call_traits.hpp <<===>> libs\utility\include\boost\call_traits.hpp
link.hardlink boost\operators_v1.hpp
Hardlink created for boost\operators_v1.hpp <<===>> libs\utility\include\boost\operators_v1.hpp
link.hardlink boost\compressed_pair.hpp
Hardlink created for boost\compressed_pair.hpp <<===>> libs\utility\include\boost\compressed_pair.hpp
link.hardlink boost\operators.hpp
Hardlink created for boost\operators.hpp <<===>> libs\utility\include\boost\operators.hpp
link.hardlink boost\variant.hpp
Hardlink created for boost\variant.hpp <<===>> libs\variant\include\boost\variant.hpp
mklink-or-dir boost\variant
Junction created for boost\variant <<===>> libs\variant\include\boost\variant
mklink-or-dir boost\uuid
Junction created for boost\uuid <<===>> libs\uuid\include\boost\uuid
mklink-or-dir boost\variant2
Junction created for boost\variant2 <<===>> libs\variant2\include\boost\variant2
link.hardlink boost\utility.hpp
Hardlink created for boost\utility.hpp <<===>> libs\utility\include\boost\utility.hpp
mklink-or-dir boost\vmd
Junction created for boost\vmd <<===>> libs\vmd\include\boost\vmd
mklink-or-dir boost\wave
Junction created for boost\wave <<===>> libs\wave\include\boost\wave
link.hardlink boost\wave.hpp
Hardlink created for boost\wave.hpp <<===>> libs\wave\include\boost\wave.hpp
link.hardlink boost\variant2.hpp
Hardlink created for boost\variant2.hpp <<===>> libs\variant2\include\boost\variant2.hpp
mklink-or-dir boost\winapi
Junction created for boost\winapi <<===>> libs\winapi\include\boost\winapi
mklink-or-dir boost\numeric
mklink-or-dir boost\yap
Junction created for boost\yap <<===>> libs\yap\include\boost\yap
link.hardlink boost\cast.hpp
Hardlink created for boost\cast.hpp <<===>> libs\numeric\conversion\include\boost\cast.hpp
mklink-or-dir boost\xpressive
Junction created for boost\xpressive <<===>> libs\xpressive\include\boost\xpressive
mklink-or-dir boost\numeric\interval
Junction created for boost\numeric\interval <<===>> libs\numeric\interval\include\boost\numeric\interval
mklink-or-dir boost\numeric\conversion
Junction created for boost\numeric\conversion <<===>> libs\numeric\conversion\include\boost\numeric\conversion
link.hardlink boost\numeric\interval.hpp
Hardlink created for boost\numeric\interval.hpp <<===>> libs\numeric\interval\include\boost\numeric\interval.hpp
mklink-or-dir boost\numeric\ublas
Junction created for boost\numeric\ublas <<===>> libs\numeric\ublas\include\boost\numeric\ublas
mklink-or-dir boost\numeric\odeint
Junction created for boost\numeric\odeint <<===>> libs\numeric\odeint\include\boost\numeric\odeint
link.hardlink boost\numeric\odeint.hpp
Hardlink created for boost\numeric\odeint.hpp <<===>> libs\numeric\odeint\include\boost\numeric\odeint.hpp
...updated 625 targets...
C:\Users\AlanJui\source\repos\librime>
```

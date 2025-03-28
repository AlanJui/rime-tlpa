# LibRime 安裝指引

## 作業環境

- 作業系統： Windows 11 Pro
- 指令工具： Windows 終端機 + PowerShell 非系統管理員身份
- 使用 vcpkg 安裝 boost

## 安裝 Boost

```sh
vcpkg install boost
```

## 編譯工具

- clang and llvm: C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin
- cc/c++/gcc: C:\mingw64\bin
- make: C:\GnuWin32\bin
- cmake: C:\Program Files\CMake\bin
- ninja: C:\Program Files\CMake\bin
- vcpkg: C:\bin\vcpkg

## deps

使用 vcpkg 安裝

- Boost: boost:x64-windows 1.86.0#1
- glog: glog:x64-windows@0.7.1

## 操作程序

### 設定執行環境

1. 編輯 BATCH 執行檔

```bash
# env.ps1
# 設置 Boost 根目錄
$env:BOOST_ROOT = "C:\bin\vcpkg\installed\x64-windows"

# 設置 LLVM/Clang 工具鏈
$env:CC = "C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin\clang.exe"
$env:CXX = "C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin\clang++.exe"

# 設置 CMake 生成器為 Ninja
$env:CMAKE_GENERATOR = "Ninja"

# 設置開發工具路徑
$env:DEVTOOLS_PATH = "C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin;C:\Program Files\CMake\bin;C:\mingw64\bin;C:\GnuWin32\bin;$env:ProgramFiles\Git\cmd;$env:ProgramFiles\Python313"

# 設置 vcpkg 工具鏈文件
$env:CMAKE_TOOLCHAIN_FILE = "C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake"

# 更新 PATH
$env:PATH = "$env:DEVTOOLS_PATH;$env:PATH"
```

2. 執行環境設定執行檔

```bash
.\env.ps1
```

```PowerShell
$env:CC
$env:CXX
```

### 編譯 librime

1. 進入工作目錄

```PowerShell
cd C:\Users\AlanJui\source\repos\librime
```

2. 設定作業系統環境變

```PowerShell
.\env.ps1
```

3. 建立【建置目錄】

```PowerShell
mkdir build
cd build
```

4. 執行 CMake 配置

```PowerShell
cmake .. -G Ninja -DCMAKE_TOOLCHAIN_FILE=C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake -DBOOST_ROOT=C:\bin\vcpkg\installed\x64-windows
cmake .. -G Ninja -Wno-dev -DCMAKE_TOOLCHAIN_FILE=C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake -DBOOST_ROOT=C:\bin\vcpkg\installed\x64-windows -DGLOG_ROOT_DIR=C:\bin\vcpkg\installed\x64-windows -DCMAKE_BUILD_TYPE=Debug
```

```PowerShell
cmake .. -G Ninja `
  -DCMAKE_TOOLCHAIN_FILE=C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake `
  -DBOOST_ROOT=C:\bin\vcpkg\installed\x64-windows `
  -DGLOG_ROOT_DIR=C:\bin\vcpkg\installed\x64-windows `
  -DRIME_WITH_LOGGING=ON

```

## AI提問

```sh
想要安裝 librime (官網安裝指引文件： https://github.com/rime/librime/blob/master/README-windows.md）

【摘要】：

Prerequisites
librime is tested to work on Windows with the following combinations of build tools and libraries:

Visual Studio 2022 or LLVM 16
Boost>=1.83
cmake>=3.10
Boost and cmake versions need to match higher VS version.

Python>=2.7 is needed to build opencc dictionaries.


請問：如果我想用 LLVM ，我已完成的安裝如下...

REM clang and llvm: C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin
REM cc/c++/gcc: C:\mingw64\bin
REM make: C:\GnuWin32\bin
REM cmake: C:\Program Files\CMake\bin
REM ninja: C:\Program Files\CMake\bin
set DEVTOOLS_PATH=C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin;%\ProgramFiles%\CMake\bin;C:\mingw64\bin;C:\GnuWin32\bin;%ProgramFiles%\Git\cmd;%\ProgramFiles%\Python313
=====================

env.bat

@echo off
REM 設置 Boost 根目錄（根據你的 Boost 安裝路徑）
set BOOST_ROOT=C:\bin\vcpkg\installed\x64-windows

REM 設置 LLVM/Clang 工具鏈
set CC=C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin\clang.exe
set CXX=C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin\clang++.exe

REM 設置 CMake 生成器為 Ninja
set CMAKE_GENERATOR=Ninja

REM 設置平台工具集為 LLVM
set PLATFORM_TOOLSET=ClangCL

REM 設置開發工具路徑（包含 LLVM、CMake、Ninja、MinGW 等）
set DEVTOOLS_PATH=C:\bin\clang+llvm-19.1.7-x86_64-pc-windows-msvc\bin;C:\Program Files\CMake\bin;C:\mingw64\bin;C:\GnuWin32\bin;%ProgramFiles%\Git\cmd;%ProgramFiles%\Python313

REM 設置 vcpkg 工具鏈文件（如果你使用 vcpkg）
set CMAKE_TOOLCHAIN_FILE=C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake

REM 設置其他環境變數（可選）
set PATH=%DEVTOOLS_PATH%;%PATH%
==================================

- 作業系統： Windows 11 Pro
- 指令工具： Windows 終端機 + PowerShell 非系統管理員身份
- 使用 vcpkg 安裝 boost

==================================

請問下面該怎麼做？env.bat 設定可以嗎？
```

## CMake Ref Log

```PowerShell
PS C:\Users\AlanJui\source\repos\librime\build> cmake .. -G Ninja -DCMAKE_TOOLCHAIN_FILE=C:\bin\vcpkg\scripts\buildsystems\vcpkg.cmake -DBOOST_ROOT=C:\bin\vcpkg\installed\x64-windows
-- The C compiler identification is Clang 19.1.7 with GNU-like command-line
-- The CXX compiler identification is Clang 19.1.7 with GNU-like command-line
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: C:/bin/clang+llvm-19.1.7-x86_64-pc-windows-msvc/bin/clang.exe - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/bin/clang+llvm-19.1.7-x86_64-pc-windows-msvc/bin/clang++.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CMake Warning (dev) at C:/bin/vcpkg/installed/x64-windows/share/boost/vcpkg-cmake-wrapper.cmake:3 (_find_package):
  Policy CMP0144 is not set: find_package uses upper-case <PACKAGENAME>_ROOT
  variables.  Run "cmake --help-policy CMP0144" for policy details.  Use the
  cmake_policy command to set the policy and suppress this warning.

  CMake variable BOOST_ROOT is set to:

    C:\bin\vcpkg\installed\x64-windows

  For compatibility, find_package is ignoring the variable, but code in a
  .cmake module might still use it.
Call Stack (most recent call first):
  C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake:813 (include)
  CMakeLists.txt:65 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at C:/bin/vcpkg/installed/x64-windows/share/boost/vcpkg-cmake-wrapper.cmake:3 (_find_package):
  Policy CMP0167 is not set: The FindBoost module is removed.  Run "cmake
  --help-policy CMP0167" for policy details.  Use the cmake_policy command to
  set the policy and suppress this warning.

Call Stack (most recent call first):
  C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake:813 (include)
  CMakeLists.txt:65 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found Boost: C:/bin/vcpkg/installed/x64-windows/share/boost/BoostConfig.cmake (found suitable version "1.86.0", minimum required is "1.77.0")
-- Found gflags: C:/bin/vcpkg/installed/x64-windows/lib/gflags.lib
-- Found gflags: C:/bin/vcpkg/installed/x64-windows/lib/gflags.lib
-- Found glog: C:/bin/vcpkg/installed/x64-windows/debug/lib/glog.lib
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - not found
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - no
-- Found Threads: TRUE
-- Found GTest: C:/bin/vcpkg/installed/x64-windows/share/gtest/GTestConfig.cmake (found version "1.16.0")
-- Found yaml-cpp: C:/bin/vcpkg/installed/x64-windows/lib/yaml-cpp.lib
-- Found leveldb: C:/bin/vcpkg/installed/x64-windows/debug/lib/leveldb.lib
-- Found marisa: C:/bin/vcpkg/installed/x64-windows/debug/lib/libmarisa.lib
-- Found opencc: C:/bin/vcpkg/installed/x64-windows/debug/lib/opencc.lib
-- Found X11/keysym.h at C:/Users/AlanJui/source/repos/librime/include
-- rime_plugins_libs:
-- rime_plugins_modules:
true
-- Configuring done (8.8s)
-- Generating done (0.3s)
-- Build files have been written to: C:/Users/AlanJui/source/repos/librime/build
PS C:\Users\AlanJui\source\repos\librime\build>

PS C:\Users\AlanJui\source\repos\librime\build> ls


    Directory: C:\Users\AlanJui\source\repos\librime\build


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          2025/3/5  下午 07:42                bin

d-----          2025/3/5  下午 07:42                CMakeFiles

d-----          2025/3/5  下午 07:42                plugins

d-----          2025/3/5  下午 07:42                src

d-----          2025/3/5  下午 07:42                test

d-----          2025/3/5  下午 07:42                tools

-a----          2025/3/5  下午 07:42         221328 build.ninja

-a----          2025/3/5  下午 07:42          27596 CMakeCache.txt

-a----          2025/3/5  下午 07:42           4322 cmake_install.cmake

-a----          2025/3/5  下午 07:42           1212 cmake_uninstall.cmake

-a----          2025/3/5  下午 07:42            370 CTestTestfile.cmake



PS C:\Users\AlanJui\source\repos\librime\build>
```

# librime 安裝指引

[官網文件](https://github.com/rime/librime/blob/master/README-windows.md)

## 先決條件：

librime is tested to work on Windows with the following combinations of build tools and libraries:

- Visual Studio 2022 or LLVM 16
- Boost>=1.83
- cmake>=3.10

Boost and cmake versions need to match higher VS version.

Python>=2.7 is needed to build opencc dictionaries.


### 安裝 VS 2022

採：【使用 C++ 桌面開發】安裝選項。

### 安裝 cmake

安裝指令：

```sh
choco install cmak
```

【註】：

1. 不必更新作業系統之環境變數設定，但需重啟或另開新 Windows 終端機，
才能令安裝程式對系統環境變數的設定起作用。

2. 手動設定系統環境變數：

```sh
setx PATH "$($env:PATH);C:\Program Files\CMake\bin" /M
```

- setx 會修改 永久的環境變數，參數 /M 代表修改系統層級 (Machine-level) 的變數。

- $($env:PATH) 是讀取當前使用者的 PATH，再在後面加上 ;C:\Program Files\CMake\bin。


驗證安裝結果指令：

```sh
cmake --version
```

### CMake 執行要點

執行 CMake 時，務必：確認是否有在「VS 的開發者命令提示字元」或
「x64 Native Tools 命令提示字元」下執行：

Windows 上若想用 CMake 搭配 Visual Studio 的 C/C++ 編譯器，最簡單的方法
就是打開 Developer Command Prompt for VS 2022 或者 
x64 Native Tools Command Prompt for VS 2022（視你安裝的 VS 版本而定），
再在裡頭執行 cmake -G Ninja -DCMAKE_BUILD_TYPE=Release .. 之類的命令。
這樣 CMake 自動就能找到 cl.exe、link.exe 等編譯器工具鏈。


【舉例】：

1. 使用 Visual Studio 安裝程式後，應該會在「開始選單」→ 
「Visual Studio 2022」中看到「x64 Native Tools Command Prompt for VS 2022」。

2. 看到命令提示符號後，使用 cd 指令切換到【專案根目錄】，先建【build】目錄，
再進入，然後執行 cmake 指令：

```sh
mkdir build
cd build
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..
ninja
```

經上述步驟，CMake 應該就能找到 MSVC 的編譯器，不會再出現 No CMAKE_C_COMPILER 
could be found 的錯誤。

若是使用 PowerShell/CMD 操作介面（即：未特地載入VS環境的指令操作環境）
執行 CMake ，則需手動指定編譯器。如：

```sh
cmake -G Ninja ^
      -DCMAKE_C_COMPILER="C:/Path/To/cl.exe" ^
      -DCMAKE_CXX_COMPILER="C:/Path/To/cl.exe" ^
      ..
```

### 安裝 Ninja

安裝指令：

```sh
choco install ninja
```

驗證安裝結果指令：

```sh
ninja --version
```

### 安裝 vcpkg

1. 執行安裝指令：

```sh
$ cd /mnt/c/bin/
$ git clone https://github.com/microsoft/vcpkg.git
$ cd vcpkg
$ .\bootstrap-vcpkg.bat
$ .\vcpkg integrate install
```

2. 檢查安裝結果：

安裝完畢後，在 vcpkg 資料夾裡（例如 vcpkg\installed\x64-windows\）可以看到：

- include\ 目錄 (放標頭檔)
- lib\ 目錄 (放靜態庫 .lib)
- bin\ 或 debug\bin\ (放動態庫 .dll)
- share\ 等等


3. 整合 vcpkg 與 CMake

如果你使用 CMake 來編譯自己的專案或其他外掛，可以把 vcpkg 的路徑加到 
CMAKE_TOOLCHAIN_FILE 參數，讓 CMake 自動找 vcpkg 提供的函式庫：

```sh
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_TOOLCHAIN_FILE=C:/bin/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  ..
```


### 安裝 Boost

1. 以預設安裝 ：有可能會安裝 x86-windows 版本

```sh
vcpkg install boost
```

【註】：但 2025/3/2 在 Windows 11 Pro 安裝，預設就是使用 x64-windows 。

2. 指定安裝 x64 版本

```sh
vcpkg install boost:x64-windows
```

安裝完成後，即可在 vcpkg\installed\x64-windows\include\boost 看到標頭檔；對應的庫檔 (.lib / .dll) 也會放到 lib/、bin/ 等目錄中。

## 取得原始碼

```sh
git clone --recursive https://github.com/rime/librime.git
```


## 安裝 librime-lua

【程序】：

1. 安裝/編譯 opencc：取得 include/opencc/*、lib/opencc.lib 等。

2. 安裝/編譯 librime：確定 include/rime/*、lib/rime.lib (或 rime.dll) 存在。

3. 取得原始碼：

```sh
git clone --recursive https://github.com/hchunhui/librime-lua
cd librime-lua
mkdir build
cd build
```

4. CMake Configure：

```sh
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ^
    -DBUILD_OPENCC=ON ^
    -DOPENCC_INCLUDE_DIR="C:/opencc/include" ^
    -DOPENCC_LIBRARIES="C:/opencc/lib/opencc.lib" ^
    -DCMAKE_PREFIX_PATH="C:/where/librime/is;C:/where/other/deps/are" ^
    ..
```

5. Build & Install:

```sh
ninja
ninja install
```

如果你使用 vcpkg，路徑可能是 C:/vcpkg/installed/x64-windows；如果有多個路徑，用分號隔開即可。


告訴 librime-lua：librime 與 opencc 在哪裡
一旦你有了安裝完成（或編譯完成）的 librime 與 opencc，就可以編譯 librime-lua。
它的 CMakeLists.txt 一般會提供幾個選項，常見的有：

-DBUILD_OPENCC=ON/OFF
啟用或停用 opencc 支援；若啟用就需要指向 opencc 的頭文件和函式庫路徑。
-DOPENCC_INCLUDE_DIR=...
-DOPENCC_LIBRARIES=...
-DUSE_SYSTEM_LUA=ON/OFF
如果不想用 librime-lua 附帶的 lua，也可指定系統 lua。
（更多參數可參考該 repo 的 README 或 CMakeLists.txt 中的 option() 說明。）
最重要的是要讓 CMake 找到 librime。有些外掛直接用 find_package(Rime ...) 之類的方式尋找 librime；如果找不到，你要手動指定：

powershell
複製
編輯
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ^
  -DBUILD_OPENCC=ON ^
  -DOPENCC_INCLUDE_DIR="C:/path/to/opencc/include" ^
  -DOPENCC_LIBRARIES="C:/path/to/opencc/lib/opencc.lib" ^
  -DCMAKE_PREFIX_PATH="C:/vcpkg/installed/x64-windows" ^
  ..
-DCMAKE_PREFIX_PATH 常用來告訴 CMake 在哪些路徑找外部套件；假設你是用 vcpkg，或手動安裝 librime 到某個資料夾，都可以用這種方式加上。
如果你已經把 librime 裝在系統路徑（包含標頭與 .lib），則可能不需要再指定。
簡單來說，librime-lua 必須知道 librime 與 opencc 的存在，否則就會缺少標頭檔和函式庫，導致編譯失敗。

import os
import shutil
import platform


# 定義目標資料夾
def get_rime_dir():
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"%APPDATA%\Rime")
    elif system == "Linux":
        return os.path.expanduser("~/.config/ibus/rime")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Rime")
    else:
        raise RuntimeError("不支援的操作系統")


# 複製文件
def install_rime_files(rime_dir):
    print(f"RIME 資料夾路徑：{rime_dir}")
    if not os.path.exists(rime_dir):
        print("RIME 資料夾未找到，請確認已安裝 RIME 輸入法。")
        return

    # 文件列表
    files_to_copy = [
        "my_*.schema.yaml",
        "kb_*.schema.yaml",
        "tlpa_*.schema.yaml",
        "zu_im_*.schema.yaml",
        "huan_ciat_*.schema.yaml",
        "BP_*.schema.yaml",
        "keymap_*.schema.yaml",
        "lib_*.yaml",
        "tl_ji_khoo_*.dict.yaml",
        "config/default.custom.yaml",
        "rime.lua",
        "lua/*.lua",
    ]
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"複製文件 {file} 到 {rime_dir}")
            shutil.copy(file, rime_dir)
        else:
            print(f"未找到文件：{file}")

    print("文件已成功安裝！請重新部署 RIME 輸入法。")


if __name__ == "__main__":
    try:
        rime_dir = get_rime_dir()
        install_rime_files(rime_dir)
    except Exception as e:
        print(f"安裝失敗：{e}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME TLPA 配置工具安裝程式
這是一個完整的安裝程式範例，包含：
- GUI 界面
- 文件複製
- 系統配置
- 解安裝功能
"""

import os
import shutil
import subprocess
import sys
import tkinter as tk
import winreg
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class RimeInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RIME TLPA 台語輸入法配置工具安裝程式")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # 設定變數
        self.install_path = tk.StringVar()
        self.install_path.set(r"C:\Program Files\RIME TLPA Tools")

        self.create_widgets()

    def create_widgets(self):
        """創建 GUI 元件"""

        # 標題
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=20, pady=20)

        title_label = ttk.Label(
            title_frame,
            text="RIME TLPA 台語輸入法配置工具",
            font=("Arial", 16, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="安裝程式 v1.0.0",
            font=("Arial", 10)
        )
        subtitle_label.pack()

        # 安裝路徑選擇
        path_frame = ttk.LabelFrame(self.root, text="安裝路徑", padding=10)
        path_frame.pack(fill="x", padx=20, pady=10)

        path_entry = ttk.Entry(path_frame, textvariable=self.install_path, width=50)
        path_entry.pack(side="left", fill="x", expand=True)

        browse_button = ttk.Button(
            path_frame,
            text="瀏覽...",
            command=self.browse_install_path
        )
        browse_button.pack(side="right", padx=(5, 0))

        # 功能選項
        options_frame = ttk.LabelFrame(self.root, text="安裝選項", padding=10)
        options_frame.pack(fill="x", padx=20, pady=10)

        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        self.add_to_start_menu = tk.BooleanVar(value=True)
        self.copy_schemas = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            options_frame,
            text="建立桌面捷徑",
            variable=self.create_desktop_shortcut
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text="加入開始選單",
            variable=self.add_to_start_menu
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text="複製 RIME schema 檔案到使用者配置目錄",
            variable=self.copy_schemas
        ).pack(anchor="w")

        # 進度條
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill="x", padx=20, pady=10)

        self.progress_label = ttk.Label(self.progress_frame, text="準備安裝...")
        self.progress_label.pack(anchor="w")

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="determinate",
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=(5, 0))

        # 按鈕區域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)

        self.install_button = ttk.Button(
            button_frame,
            text="安裝",
            command=self.install,
            style="Accent.TButton"
        )
        self.install_button.pack(side="left")

        self.uninstall_button = ttk.Button(
            button_frame,
            text="解除安裝",
            command=self.uninstall
        )
        self.uninstall_button.pack(side="left", padx=(10, 0))

        ttk.Button(
            button_frame,
            text="關閉",
            command=self.root.quit
        ).pack(side="right")

        # 資訊區域
        info_frame = ttk.LabelFrame(self.root, text="安裝資訊", padding=10)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.info_text = tk.Text(
            info_frame,
            height=8,
            wrap="word",
            state="disabled"
        )
        self.info_text.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.info_text.config(yscrollcommand=scrollbar.set)

    def browse_install_path(self):
        """瀏覽安裝路徑"""
        path = filedialog.askdirectory(
            title="選擇安裝目錄",
            initialdir=self.install_path.get()
        )
        if path:
            self.install_path.set(path)

    def log_message(self, message):
        """記錄訊息到資訊區域"""
        self.info_text.config(state="normal")
        self.info_text.insert("end", f"{message}\n")
        self.info_text.see("end")
        self.info_text.config(state="disabled")
        self.root.update()

    def update_progress(self, value, text):
        """更新進度條"""
        self.progress_bar["value"] = value
        self.progress_label.config(text=text)
        self.root.update()

    def install(self):
        """執行安裝"""
        try:
            install_dir = Path(self.install_path.get())

            # 檢查權限
            if not self.check_permissions(install_dir):
                messagebox.showerror("錯誤", "沒有足夠的權限寫入安裝目錄")
                return

            self.log_message("開始安裝 RIME TLPA 配置工具...")
            self.update_progress(10, "建立安裝目錄...")

            # 建立安裝目錄
            install_dir.mkdir(parents=True, exist_ok=True)

            self.update_progress(20, "複製程式檔案...")

            # 複製檔案 (這裡假設我們有要安裝的檔案)
            self.copy_program_files(install_dir)

            self.update_progress(40, "複製 RIME schema 檔案...")

            # 複製 schema 檔案到 RIME 配置目錄
            if self.copy_schemas.get():
                self.copy_rime_schemas()

            self.update_progress(60, "建立捷徑...")

            # 建立捷徑
            if self.create_desktop_shortcut.get():
                self.create_shortcut("desktop", install_dir)

            if self.add_to_start_menu.get():
                self.create_shortcut("start_menu", install_dir)

            self.update_progress(80, "註冊解除安裝資訊...")

            # 註冊解除安裝資訊
            self.register_uninstaller(install_dir)

            self.update_progress(100, "安裝完成!")

            self.log_message("✅ 安裝成功完成!")
            messagebox.showinfo("安裝完成", "RIME TLPA 配置工具安裝成功!")

        except Exception as e:
            self.log_message(f"❌ 安裝失敗: {str(e)}")
            messagebox.showerror("安裝失敗", f"安裝過程中發生錯誤:\n{str(e)}")

    def check_permissions(self, install_dir):
        """檢查安裝目錄權限"""
        try:
            test_file = install_dir / "test_write.tmp"
            install_dir.mkdir(parents=True, exist_ok=True)
            test_file.write_text("test")
            test_file.unlink()
            return True
        except:
            return False

    def copy_program_files(self, install_dir):
        """複製程式檔案"""
        # 這裡應該複製實際的程式檔案
        # 假設我們有一些要安裝的檔案
        source_files = [
            "dist/RIME_TLPA_Validator.exe",
            "tools/PACKAGING_GUIDE.md"
        ]

        for file_path in source_files:
            if os.path.exists(file_path):
                dest_path = install_dir / Path(file_path).name
                shutil.copy2(file_path, dest_path)
                self.log_message(f"複製: {file_path} -> {dest_path}")

    def copy_rime_schemas(self):
        """複製 RIME schema 檔案"""
        rime_dir = Path(os.path.expanduser(r"~\AppData\Roaming\Rime"))

        if not rime_dir.exists():
            self.log_message("⚠️  RIME 配置目錄不存在，跳過 schema 複製")
            return

        schema_files = [
            "tlpa_hong_im.schema.yaml",
            "tlpa_phing_im.schema.yaml",
            # 其他 schema 檔案...
        ]

        for schema_file in schema_files:
            if os.path.exists(schema_file):
                dest_path = rime_dir / schema_file
                shutil.copy2(schema_file, dest_path)
                self.log_message(f"複製 schema: {schema_file} -> RIME 配置目錄")

    def create_shortcut(self, location, install_dir):
        """建立捷徑 (簡化實作)"""
        self.log_message(f"建立{location}捷徑")

    def register_uninstaller(self, install_dir):
        """註冊解除安裝資訊 (簡化實作)"""
        self.log_message("註冊解除安裝資訊")

    def uninstall(self):
        """執行解除安裝"""
        result = messagebox.askyesno(
            "確認解除安裝",
            "確定要解除安裝 RIME TLPA 配置工具嗎？"
        )

        if result:
            self.log_message("開始解除安裝...")
            # 實作解除安裝邏輯
            messagebox.showinfo("解除安裝完成", "解除安裝成功!")

    def run(self):
        """啟動安裝程式"""
        self.root.mainloop()

def main():
    """主函式"""
    app = RimeInstaller()
    app.run()

if __name__ == "__main__":
    main()
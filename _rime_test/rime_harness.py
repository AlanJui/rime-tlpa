# -*- coding: utf-8 -*-
"""librime 測試工具：用 Weasel 的 rime.dll 在隔離目錄模擬按鍵，列出候選。"""
import ctypes
import os
import shutil
import sys
from ctypes import (POINTER, Structure, c_char_p, c_int, c_uint64, c_void_p,
                    sizeof)

WEASEL = r"C:\Program Files\Rime\weasel-0.17.4"
SRC_USER = os.environ["APPDATA"] + r"\Rime"
TEST_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userdir")


class RimeTraits(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("shared_data_dir", c_char_p),
        ("user_data_dir", c_char_p),
        ("distribution_name", c_char_p),
        ("distribution_code_name", c_char_p),
        ("distribution_version", c_char_p),
        ("app_name", c_char_p),
        ("modules", POINTER(c_char_p)),
        ("min_log_level", c_int),
        ("log_dir", c_char_p),
        ("prebuilt_data_dir", c_char_p),
        ("staging_dir", c_char_p),
    ]


class RimeComposition(Structure):
    _fields_ = [
        ("length", c_int),
        ("cursor_pos", c_int),
        ("sel_start", c_int),
        ("sel_end", c_int),
        ("preedit", c_char_p),
    ]


class RimeCandidate(Structure):
    _fields_ = [("text", c_char_p), ("comment", c_char_p), ("reserved", c_void_p)]


class RimeMenu(Structure):
    _fields_ = [
        ("page_size", c_int),
        ("page_no", c_int),
        ("is_last_page", c_int),
        ("highlighted_candidate_index", c_int),
        ("num_candidates", c_int),
        ("candidates", POINTER(RimeCandidate)),
        ("select_keys", c_char_p),
    ]


class RimeContext(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("composition", RimeComposition),
        ("menu", RimeMenu),
        ("commit_text_preview", c_char_p),
        ("select_labels", POINTER(c_char_p)),
    ]


def prepare_userdir(fresh: bool) -> None:
    if fresh and os.path.exists(TEST_ROOT):
        shutil.rmtree(TEST_ROOT)
    os.makedirs(TEST_ROOT, exist_ok=True)
    # 複製 YAML 與 lua（不含 build/userdb/sync）
    for name in os.listdir(SRC_USER):
        src = os.path.join(SRC_USER, name)
        if os.path.isfile(src) and (name.endswith((".yaml", ".lua", ".txt"))):
            dst = os.path.join(TEST_ROOT, name)
            if (not os.path.exists(dst)
                    or os.path.getmtime(src) > os.path.getmtime(dst)):
                shutil.copy2(src, dst)
        elif os.path.isdir(src) and name == "lua":
            shutil.copytree(src, os.path.join(TEST_ROOT, name), dirs_exist_ok=True)


def override(files):
    """把工作區的最新檔案蓋進測試目錄。files: list of absolute paths"""
    for f in files:
        shutil.copy2(f, os.path.join(TEST_ROOT, os.path.basename(f)))


def main():
    schema = sys.argv[1] if len(sys.argv) > 1 else "zu_im_tps"
    keys = sys.argv[2] if len(sys.argv) > 2 else "a8{space}nuo"
    fresh = "--fresh" in sys.argv
    overrides = [a for a in sys.argv[3:] if a.endswith((".yaml", ".lua"))]

    prepare_userdir(fresh)
    if overrides:
        override(overrides)

    os.add_dll_directory(WEASEL)
    rime = ctypes.CDLL(os.path.join(WEASEL, "rime.dll"))

    rime.RimeCreateSession.restype = c_uint64
    rime.RimeProcessKey.argtypes = [c_uint64, c_int, c_int]
    rime.RimeSimulateKeySequence.argtypes = [c_uint64, c_char_p]
    rime.RimeSelectSchema.argtypes = [c_uint64, c_char_p]
    rime.RimeGetContext.argtypes = [c_uint64, POINTER(RimeContext)]
    rime.RimeDestroySession.argtypes = [c_uint64]

    traits = RimeTraits()
    traits.data_size = sizeof(RimeTraits) - sizeof(c_int)
    traits.shared_data_dir = os.path.join(WEASEL, "data").encode()
    traits.user_data_dir = TEST_ROOT.encode()
    traits.distribution_name = b"test"
    traits.distribution_code_name = b"test"
    traits.distribution_version = b"0.0"
    traits.app_name = b"rime.test"
    traits.min_log_level = 2
    traits.log_dir = TEST_ROOT.encode()

    rime.RimeSetup(ctypes.byref(traits))
    rime.RimeInitialize(ctypes.byref(traits))
    if rime.RimeStartMaintenance(1):
        rime.RimeJoinMaintenanceThread()

    sid = rime.RimeCreateSession()
    if not rime.RimeSelectSchema(sid, schema.encode()):
        print("!! select schema failed:", schema)
    if not rime.RimeSimulateKeySequence(sid, keys.encode()):
        print("!! simulate failed:", keys)

    ctx = RimeContext()
    ctx.data_size = sizeof(RimeContext) - sizeof(c_int)
    if rime.RimeGetContext(sid, ctypes.byref(ctx)):
        preedit = (ctx.composition.preedit or b"").decode("utf-8", "replace")
        print(f"schema={schema} keys={keys}")
        print(f"preedit=[{preedit}]")
        n = ctx.menu.num_candidates
        print(f"candidates={n}")
        for i in range(n):
            cand = ctx.menu.candidates[i]
            text = (cand.text or b"").decode("utf-8", "replace")
            comment = (cand.comment or b"").decode("utf-8", "replace")
            print(f"  {i+1}. {text}\t{comment}")
        rime.RimeFreeContext(ctypes.byref(ctx))
    else:
        print("!! get context failed")

    rime.RimeDestroySession(sid)
    rime.RimeFinalize()


if __name__ == "__main__":
    main()

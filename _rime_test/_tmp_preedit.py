# -*- coding: utf-8 -*-
import ctypes
import os
import sys
from ctypes import POINTER, c_char_p, c_int, c_uint64, sizeof

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rime_harness as h


def dump(rime, sid, label):
    ctx = h.RimeContext()
    ctx.data_size = sizeof(h.RimeContext) - sizeof(c_int)
    if not rime.RimeGetContext(sid, ctypes.byref(ctx)):
        print(f"!! {label}")
        return
    preedit = (ctx.composition.preedit or b"").decode("utf-8", "replace")
    print(f"{label} preedit=[{preedit}]")
    for i in range(ctx.menu.num_candidates):
        cand = ctx.menu.candidates[i]
        text = (cand.text or b"").decode("utf-8", "replace")
        comment = (cand.comment or b"").decode("utf-8", "replace")
        print(f"  {i+1}. {text}\t{comment}")
    rime.RimeFreeContext(ctypes.byref(ctx))


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    h.prepare_userdir(False)
    h.override([
        os.path.join(root, "tsap_peh_im_tl.schema.yaml"),
        os.path.join(root, "tsap_peh_im_bpm2.schema.yaml"),
        os.path.join(root, "rime.lua"),
    ])
    os.add_dll_directory(h.WEASEL)
    rime = ctypes.CDLL(os.path.join(h.WEASEL, "rime.dll"))
    rime.RimeCreateSession.restype = c_uint64
    rime.RimeSimulateKeySequence.argtypes = [c_uint64, c_char_p]
    rime.RimeProcessKey.argtypes = [c_uint64, c_int, c_int]
    rime.RimeSelectSchema.argtypes = [c_uint64, c_char_p]
    rime.RimeGetContext.argtypes = [c_uint64, POINTER(h.RimeContext)]
    rime.RimeDestroySession.argtypes = [c_uint64]
    rime.RimeClearComposition.argtypes = [c_uint64]
    traits = h.RimeTraits()
    traits.data_size = sizeof(h.RimeTraits) - sizeof(c_int)
    traits.shared_data_dir = os.path.join(h.WEASEL, "data").encode()
    traits.user_data_dir = h.TEST_ROOT.encode()
    traits.distribution_name = b"test"
    traits.distribution_code_name = b"test"
    traits.distribution_version = b"0.0"
    traits.app_name = b"rime.test"
    traits.min_log_level = 3
    traits.log_dir = h.TEST_ROOT.encode()
    rime.RimeSetup(ctypes.byref(traits))
    rime.RimeInitialize(ctypes.byref(traits))
    if rime.RimeStartMaintenance(1):
        rime.RimeJoinMaintenanceThread()
    sid = rime.RimeCreateSession()
    rime.RimeSelectSchema(sid, b"tsap_peh_im_tl")
    for keys in ["tere", "ter", "tir", "te-"]:
        rime.RimeClearComposition(sid)
        rime.RimeSimulateKeySequence(sid, keys.encode())
        dump(rime, sid, keys)
        found = False
        for page in range(6):
            ctx = h.RimeContext()
            ctx.data_size = sizeof(h.RimeContext) - sizeof(c_int)
            if not rime.RimeGetContext(sid, ctypes.byref(ctx)):
                break
            hit = None
            for i in range(ctx.menu.num_candidates):
                cand = ctx.menu.candidates[i]
                text = (cand.text or b"").decode("utf-8", "replace")
                if "白" in text or text == "食":
                    comment = (cand.comment or b"").decode("utf-8", "replace")
                    hit = f"  p{page+1}.{i+1} {text}\t{comment}"
                    found = True
                    break
            last = ctx.menu.is_last_page
            rime.RimeFreeContext(ctypes.byref(ctx))
            if hit:
                print(hit)
            if found or last:
                break
            rime.RimeProcessKey(sid, 0xFF56, 0)
        if not found:
            print("  (白/食 not in first pages)")
    rime.RimeDestroySession(sid)
    rime.RimeFinalize()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from ctypes import POINTER, c_char_p, c_int, c_uint64, sizeof

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rime_harness as h


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    h.prepare_userdir(False)
    h.override([
        os.path.join(root, "tsap_peh_im_tl.schema.yaml"),
        os.path.join(root, "rime.lua"),
    ])
    os.add_dll_directory(h.WEASEL)
    rime = ctypes.CDLL(os.path.join(h.WEASEL, "rime.dll"))
    rime.RimeCreateSession.restype = c_uint64
    rime.RimeSimulateKeySequence.argtypes = [c_uint64, c_char_p]
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
    keys_list = [
        "thian-", "thian-iu\\", "siong-",
    ]
    for keys in keys_list:
        rime.RimeClearComposition(sid)
        rime.RimeSimulateKeySequence(sid, keys.encode())
        ctx = h.RimeContext()
        ctx.data_size = sizeof(h.RimeContext) - sizeof(c_int)
        if not rime.RimeGetContext(sid, ctypes.byref(ctx)):
            print("%s: NO" % keys)
            continue
        pre = (ctx.composition.preedit or b"").decode("utf-8", "replace")
        lines = []
        n = min(5, ctx.menu.num_candidates)
        for i in range(n):
            c = ctx.menu.candidates[i]
            lines.append((c.text or b"").decode() + " " + (c.comment or b"").decode()[:28])
        flag = "BAD" if ("-" in pre or "'" in pre) else "ok "
        print("%s %-8s pre=[%s] sel=%s-%s | %s" % (
            flag, keys, pre, ctx.composition.sel_start, ctx.composition.sel_end,
            " / ".join(lines)))
        rime.RimeFreeContext(ctypes.byref(ctx))
    rime.RimeDestroySession(sid)
    rime.RimeFinalize()


if __name__ == "__main__":
    main()

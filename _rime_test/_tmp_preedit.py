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
    if ctx.menu.num_candidates:
        cand = ctx.menu.candidates[0]
        text = (cand.text or b"").decode("utf-8", "replace")
        comment = (cand.comment or b"").decode("utf-8", "replace")
        print(f"  1. {text}\t{comment}")
    rime.RimeFreeContext(ctypes.byref(ctx))


def main():
    h.prepare_userdir(False)
    h.override([os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "tsap_peh_im_tps.schema.yaml")])
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
    rime.RimeSelectSchema(sid, b"tsap_peh_im_tps")
    for keys in ["nu/:", "1jp[nu/:", "vu/:", "1jp["]:
        rime.RimeClearComposition(sid)
        rime.RimeSimulateKeySequence(sid, keys.encode())
        dump(rime, sid, keys)
    rime.RimeDestroySession(sid)
    rime.RimeFinalize()


if __name__ == "__main__":
    main()

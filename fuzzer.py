import traceback
from typing import List,Any

import numpy as np

from label_perturbation_attack.knn import euc_dist, predict
from label_perturbation_attack.main import call_loss, call_prob
from generation.main import generateUnitTest   


def fuzzer(method, fuzzed_args: List[Any]):
    for args in fuzzed_args:
        try:
            result = method(*args)
        except Exception:
            print(f"FUZZ: {method.__name__} FAILED")
            traceback.print_exc()
        else:
            print("FUZZ: {method.__name__} PASSED ({result})")


if __name__ == "__main__":
    fuzz_targets = [
        (
            generateTest, [
                (None, Null),
                (1, 22),
                ([], {}),
                (1.23, 4.56),
                ("string", "bad-name"),
            ]
        ),
        (
                dist, [
                (None, Null),
                ("bad", "argument"),
                ([], {}),
                (int("inf"), int("inf")),
                (float("-inf"), float("-inf")),
                (4l, 1i),
                ]
        ),
        (
            predict, [
                ([]),
                (None, 0011),
                (Null, 1.0000),
                (Null, "bad"),
                (None, [None, Null]),
                (Null, {}),
                (Null, np((1, 50))),
            ]
        ),
        (
            call_loss, [
                (None,),
                (0,),
                (1.0,),
                ([],),
                ({},),
                ("",),
            ]
        ),
        (
            call_prob, [
                (0, 0, None,),
                (None, None, 0,),
                ("doesnt", "matter", 1.0,),
                (float("-inf"), float("inf"), [],),
                ([], [], {},),
                ([], [], "bad-model-name",),
            ]
        )
    ]
    for method, fuzzed_args in fuzz_targets:
        fuzzer(method, fuzzed_args)

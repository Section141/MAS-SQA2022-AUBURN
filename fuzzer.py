import traceback
from typing import List,Any

import numpy as np

from select_repos.dev_count import getDevEmailForCommit, getDevCount
from detection.main import runDetectionTest
from label_perturbation_attack import label_flip_perturbation
from generation.main import generateAttack  


def fuzzer(method, fuzzer_args: List[Any]):
    for fuzz in fuzzer_args:
        try:
            result = method(*args)
        except Exception:
            print(f"FUZZ: {method.__name__} FAILED")
            traceback.print_exc()
        else:
            print("FUZZ: {method.__name__} PASSED ({result})")


if __name__ == "__main__":
    fuzz_list = [
        (
            generateAttack, [
                (None,0),
                (1, 22),
                ([], {}),
                (1.23, 4.56),
                ("string", "bad-name"),
            ]
        ), (
                getDevEmailForCommit, [
                (None, 0),
                ("bad-argument", "error"),
                ([], {}),
                (int("inf"), int("inf")),
                (float("-inf"), float("-inf")),
                ("4l", "1i"),
                ]
        ),
        (
            getDevCount, [
                ([]),
                (None, 1),
                (None, 1.0000),
                (None, "error-argument"),
                (None, [None, 0]),
                (0, {}),
                (12, np((1, 50))),
            ]
        ),
        (
            runDetectionTest, [
                (None,),
                (0,),
                (1.0,),
                ([],),
                ({},),
                ("",),
            ]
        ),
        (
            label_flip_perturbation, [
                (0, 0, None,),
                (None, None, 0,),
                ("doesnt", "matter", 1.0,),
                (float("-inf"), float("inf"), [],),
                ([], [], {},),
                ([], [], "bad-model-name",),
            ]
        )
    ]
    for fuzz , fuzzer_args in fuzz_list:
        fuzzer(fuzz, fuzzer_args)

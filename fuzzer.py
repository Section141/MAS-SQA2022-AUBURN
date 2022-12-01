import traceback
from typing import List,Any

import numpy as np

from select_repos.dev_count import getDevEmailForCommit, getDevCount
from detection.main import runDetectionTest
from label_perturbation_attack.loss_based_label_perturbation import label_flip_perturbation
from generation.main import generateAttack  


def fuzzer(method, fuzzer_args: List[Any]):
    for fuzz in fuzzer_args:
        try:
            result = method(*fuzzer_args)
        except Exception:
            print(f"Fuzz: {method.__name__} Failed")
            traceback.print_exc()
        else:
            print("Fuzz: {method.__name__} Passed ({result})")


if __name__ == "__main__":
    fuzzer_list = [
        (
            generateAttack, [
                (None,0),
                (1, 22),
                ([], {}),
                (1.23, 4.56),
                ("string", "SQA"),
            ]
        ), (
                getDevEmailForCommit, [
                (None, 0),
                ("workshop", "error"),
                ([], {}),
                (float("inf"), float("inf")),
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
                (0, {})
                
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
                ("summer", "winter", 1.0,),
                (float("-inf"), float("inf"), [],),
                ([], [], {},),
                ([], [], "break",),
            ]
        )
    ]
    for fuzz , fa in fuzzer_list:
        fuzzer(fuzz, fa)

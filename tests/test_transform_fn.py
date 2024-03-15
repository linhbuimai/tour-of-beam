from src.challenge_core_transform_01 import words_partition

"""
$ python -m pytest tests/
"""

def test_words_partition():
    wd = "linh"
    assert words_partition(wd) == 2
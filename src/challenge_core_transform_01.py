import apache_beam as beam
from src.utils import Output

import re
from typing import Any

"""
You are given the works of Shakespeare "kinglear" it will be divided into words and filtered.
You need to divide these words into 3 portions.
    + The first = words that consist of capital letters.
    + The second = words that begin with a capital letter.
    + The third = all lowercase letters.
And count each element.
Translate the first and second elements of the array to lowercase,
  combine the resulting collections and group them by key
"""


# Split input text to words
def split_words(sentence):
    return re.findall(r"[\w\']+", sentence, re.UNICODE)


def partition_fn(word, num_partitions):
    if word.upper() == word:
        return 0
    elif word[0].isupper():
        return 1
    else:
        return 2


if __name__ == "__main__":
    path_to_file = "gs://apache-beam-samples/shakespeare/kinglear.txt"

    with beam.Pipeline() as p:
        parts = (
            p
            | "Log lines" >> beam.io.ReadFromText(path_to_file)
            | beam.combiners.Sample.FixedSizeGlobally(100)
            | beam.FlatMap(lambda line: line)
            | beam.FlatMap(lambda sentence: split_words(sentence))
            | beam.Partition(partition_fn, 3)
        )

        allLetterUpperCase = (
            parts[0]
            | "All upper"
            >> beam.combiners.Count.PerElement()  # return tupple: element, number of times this element exists
            | beam.Map(lambda key: (key[0].lower(), key[1]))
        )

        firstLetterUpperCase = (
            parts[1]
            | "First upper" >> beam.combiners.Count.PerElement()
            | beam.Map(lambda key: (key[0].lower(), key[1]))
        )

        allLetterLowerCase = parts[2] | "Lower" >> beam.combiners.Count.PerElement()

        flattenPCollection = (
            (allLetterUpperCase, firstLetterUpperCase, allLetterLowerCase)
            | beam.Flatten()
            | beam.GroupByKey()
            | beam.io.WriteToText("output/challenge")
        )

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
class SplitWords(beam.DoFn):
    def process(self, element):
        return re.findall(r'[\w\']+', element, re.UNICODE)

def words_partition(element: str) -> tuple:
    if element[0].isupper():
        return ("group-01", element)
    elif list(filter(str.isupper, element)):
        return ("group-02", element)
    else:
        return ("group-03", element)

class WordsClassifier(beam.DoFn):
    def process(self, element):
        if element[0].isupper():
            return ("group-01", element)
        else:
            return None


if __name__ == "__main__":
    path_to_file = 'gs://apache-beam-samples/shakespeare/kinglear.txt'
    test = ['Bear', 'This', 'I', 'for', 'Now', 'place', 'Why', 'offence', 'ruffian', 'me']
    with beam.Pipeline() as p:
        words = (
            p 
            | "Read text file" >> beam.io.ReadFromText(path_to_file)
            | "Split words" >> beam.ParDo(SplitWords())
        )

        # get sample words for process
        sample_words = words | beam.combiners.Sample.FixedSizeGlobally(10)
        sample_words | beam.ParDo(WordsClassifier()) | Output()
    
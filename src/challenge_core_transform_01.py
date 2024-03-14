import apache_beam as beam
from utils import Output

import re

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

path_to_file = 'gs://apache-beam-samples/shakespeare/kinglear.txt'

# Split input text to words
class SplitWords(beam.DoFn):
    def process(self, element):
        return re.findall(r'[\w\']+', element, re.UNICODE)
    
def words_partition(element, num_of_partitions):
    if element[0].isupper():
        return 0
    elif element.islower(): # list not accept the method islower
        return 2
    else:
        return 1
        
    
with beam.Pipeline() as p:
    words = (
        p 
        | "Read text file" >> beam.io.ReadFromText(path_to_file)
        | "Split words" >> beam.ParDo(SplitWords())
    )

    # get sample words for process
    sample_words = words | beam.combiners.Sample.FixedSizeGlobally(100)
    parts = sample_words | beam.Partition(words_partition, 3)

    parts[0] | "Output 0" >> Output()
    parts[1] | "Output 1" >> Output()
    parts[2] | "Output 2" >> Output()


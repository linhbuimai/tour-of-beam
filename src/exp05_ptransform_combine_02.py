# CombineFn example (a more complex combination)

import apache_beam as beam
from utils import Output

class AverageFn(beam.CombineFn):
  def create_accumulator(self):
    return 0.0, 0
  
  def add_input(self, mutable_accumulator, element):
    (sum, count) = mutable_accumulator
    return sum + element, count + 1
  
  def merge_accumulators(self, accumulators):
    sums, counts = zip(*accumulators)
    return sum(sums), sum(counts)
  
  def extract_output(self, accumulator):
    sum, count = accumulator
    return sum / count if count else float('NaN')
  
# with beam.Pipeline() as p:
#   (p
#    | beam.Create([1, 2, 3, 4, 5])
#    | beam.CombineGlobally(AverageFn())
#    | Output()
#   )

class CollectWordsFn(beam.CombineFn):
  def create_accumulator(self):
    return {}

  def add_input(self, accumulator, element):
    length = len(element)
    if length not in accumulator:
      accumulator[length] = []
    accumulator[length].append(element)
    return accumulator

  def merge_accumulators(self, accumulators):
    merged = {}
    for acc in accumulators:
      for length in acc:
        if length not in merged:
          merged[length] = []
        merged[length].extend(acc[length])
    return merged

  def extract_output(self, accumulator):
    return accumulator

input = ['linh', 'linh1', 'linh', 'linh2', 'linh11']
with beam.Pipeline() as p:
  (p
   | beam.Create(input)
   | beam.CombineGlobally(CollectWordsFn())
   | Output()
  )
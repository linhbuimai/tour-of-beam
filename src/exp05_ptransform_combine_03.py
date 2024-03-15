import apache_beam as beam
from utils import Output

class ConcatString(beam.CombineFn):
  def create_accumulator(self):
    return ""
  
  def add_input(self, mutable_accumulator, element):
    return mutable_accumulator + ", " + element if mutable_accumulator else element
  
  def merge_accumulators(self, accumulators):
    return ''.join(accumulators)
  
  def extract_output(self, accumulator):
    return accumulator

input = [
  ('a', 'apple'),
  ('b', 'banana'),
  ('c', 'cherry'),
  ('a', 'avocado'),
  ('l', 'lemon'),
  ('l', 'limes')
]

def len_values(values):
  return values[0], len(values[1])

with beam.Pipeline() as p:
  (p
   | beam.Create(input)
   | beam.CombinePerKey(ConcatString())
   | beam.Map(len_values)
  #  | beam.Filter(lambda values: values[1] > 10)
   | Output()
  )
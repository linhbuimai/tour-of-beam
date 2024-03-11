import apache_beam as beam
from utils import Output

input_a = ['apple', 'banana', 'cherry', 'date', 'elderberry']
input_b = ['table', 'chair', 'desk', 'lamp', 'bed']

with beam.Pipeline() as p:
  group_a = p | 'Create A' >> beam.Create(input_a)
  group_b = p | 'Create B' >> beam.Create(input_b)

  # flatten two PCollections
  (
    (group_a, group_b)
    | beam.Flatten()
    | beam.combiners.Count.Globally()
    | Output()
  )

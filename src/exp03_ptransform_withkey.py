import apache_beam as beam
from utils import Output

with beam.Pipeline() as p:
  (
    p
    | beam.Create(["apple", "banana", "cherry", "durian", "guava", "melon"])
    | beam.WithKeys(lambda word: word[0:1])
    | Output()
  )

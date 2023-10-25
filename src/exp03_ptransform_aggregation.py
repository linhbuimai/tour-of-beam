# Count example

import apache_beam as beam
from utils import Output
from typing import List, str

data1 = [
    ("spring", "🍓"),
    ("spring", "🥕"),
    ("summer", "🥕"),
    ("fall", "🥕"),
    ("spring", "🍆"),
    ("winter", "🍆"),
    ("spring", "🍅"),
    ("summer", "🍅"),
    ("fall", "🍅"),
    ("summer", "🌽"),
]

data2 = ["🍓", "🥕", "🥕", "🥕", "🍆", "🍆", "🍅", "🍅", "🍅", "🌽"]


def count_all(input: List):
    with beam.Pipeline() as p:
        total_elements = (
            p
            | "Create elements" >> beam.Create(input)
            | "Count all elements" >> beam.combiners.Count.Globally()
            | "Print result" >> beam.Map(print)
        )


def count_per_key(input: List):
    with beam.Pipeline() as p:
        total_elements_by_key = (
            p
            | "Create elements" >> beam.Create(input)
            | "Count elements per key" >> beam.combiners.Count.PerKey()
            | "Print result" >> beam.Map(print)
        )


def count_unique(input: List):
    with beam.Pipeline() as p:
        total_unique_elements = (
            p
            | "Create elements" >> beam.Create(input)
            | "Count unique elements" >> beam.combiners.Count.PerElement()
            | beam.Map(print)
        )


if __name__ == "__main__":
    # count_all(input=data2)
    # count_per_key(input=data1)
    count_unique(input=data2)

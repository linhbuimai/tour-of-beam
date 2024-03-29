"""
ParDo can emit:
- one-to-one
- one-to-many
- one-to-zero
"""
import apache_beam as beam
from utils import Output


class BreakIntoWordsDoFn(beam.DoFn):
    def __init__(self):
        pass

    def process(self, element):
        return element.split()


def pardo_one_many():
    with beam.Pipeline() as p:
        (
            p
            | beam.Create(["Hello beam", "Hi beam"])
            | beam.ParDo(BreakIntoWordsDoFn())
            | Output()
        )


def pardo_with_map():
    with beam.Pipeline() as p:
        (p | beam.Create([10, 230, 30, 40]) | beam.Map(lambda num: num * 5) | Output())


def pardo_with_flatmap():
    with beam.Pipeline() as p:
        words_with_counts = p | "Create words with counts" >> beam.Create(
            [("Hello", 1), ("Word", 2), ("How", 3)]
        )
        split_words = (
            words_with_counts
            | "Split words"
            >> beam.FlatMap(
                lambda words_with_counts: [words_with_counts[0]] * words_with_counts[1]
            )
            | Output()
        )


def pardo_with_groupbykey():
    with beam.Pipeline() as p:
        input = p | "Fruit" >> beam.Create(
            [
                ("banana", 2),
                ("apple", 4),
                ("lemon", 3),
                ("Apple", 1),
                ("Banana", 5),
                ("Lemon", 2),
            ]
        )

        input.apply("Lower case", beam.ParDo())


if __name__ == "__main__":
    # pardo_one_many()
    # pardo_with_map()
    pardo_with_flatmap()

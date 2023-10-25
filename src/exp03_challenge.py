"""
Input: a csv file contains taxi order prices
Output: A map structure
    + Key: above or equal $15, below $15 --> (orders have price < $15, orders have prive >= $15)
    + Value: total dollar value of orders
"""

import apache_beam as beam
from utils import Output


class ExtractTaxiRideCostFn(beam.DoFn):
    @classmethod
    def parse_line(cls, line, index):
        if len(line) > index:
            try:
                yield float(line[index])
            except:
                yield float(0)
        else:
            yield float(0)

    def process(self, element):
        line = element.split(",")
        return self.parse_line(line, 16)


def exercise_taxi_rides():
    with beam.Pipeline() as p:
        lines = (
            p
            | "Read input"
            >> beam.io.ReadFromText(
                "gs://apache-beam-samples/nyc_taxi/misc/sample1000.csv"
            )
            | "Parse csv" >> beam.ParDo(ExtractTaxiRideCostFn())
        )
        lines_filter = (
            lines
            | "Categorize cost"
            >> beam.WithKeys(
                lambda item: "Below $15" if item < float(15) else "Above or equal $15"
            )
            | "Aggregate cost per key" >> beam.CombinePerKey(sum)
            | Output()
        )


if __name__ == "__main__":
    exercise_taxi_rides()

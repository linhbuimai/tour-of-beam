import apache_beam as beam
from utils import Output


def example_pcollection_in_memory():
    with beam.Pipeline() as p:
        (
            p
            | "Create words" >> beam.Create(["Hello Beam", "It`s introduction"])
            | "Log words" >> Output()
        )

        (p | "Create numbers" >> beam.Create(range(1, 11)) | "Log numbers" >> Output())


def example_pcollection_read_text():
    with beam.Pipeline() as p:
        input = (
            p
            | "Log lines"
            >> beam.io.ReadFromText("gs://apache-beam-samples/shakespeare/kinglear.txt")
            | beam.Filter(lambda line: line != "")
        )

        input | "Log fixed lines" >> beam.combiners.Sample.FixedSizeGlobally(
            10
        ) | beam.FlatMap(lambda sentence: sentence) | Output(
            prefix="Fixed first 10 lines"
        )

        words = (
            p
            | "Log words"
            >> beam.io.ReadFromText("gs://apache-beam-samples/shakespeare/kinglear.txt")
            | beam.FlatMap(lambda sentence: sentence.split())
            | beam.Filter(lambda word: not word.isspace() or word.isalnum())
            | beam.combiners.Sample.FixedSizeGlobally(10)
            | beam.FlatMap(lambda word: word)
            | "Log output words" >> Output(prefix="Word: ")
        )


def example_pcollection_read_csv():
    with beam.Pipeline() as p:
        lines = (
            p
            | "Log lines"
            >> beam.io.ReadFromText(
                "gs://apache-beam-samples/nyc_taxi/misc/sample1000.csv"
            )
            | beam.ParDo(ExtractTaxiRideCostFn())
            | beam.combiners.Sample.FixedSizeGlobally(10)
            | beam.FlatMap(lambda cost: cost)
            | Output(prefix="Taxi cost: ")
        )


class ExtractTaxiRideCostFn(beam.DoFn):
    def process(self, element):
        line = element.split(",")
        return self.try_parse_taxi_ride_cost(line, 16)

    @classmethod
    def try_parse_taxi_ride_cost(cls, line, index):
        if len(line) > index:
            yield line[index]
        else:
            yield 0.0


if __name__ == "__main__":
    # example_pcollection_in_memory()
    # example_pcollection_read_text()
    example_pcollection_read_csv()

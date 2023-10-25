import apache_beam as beam


class Output(beam.PTransform):
    class _OutputFn(beam.DoFn):
        def __init__(self, prefix=""):
            super().__init__()
            self.prefix = prefix

        def process(self, element):
            print(self.prefix + str(element))

    def __init__(self, label=None, prefix=""):
        super().__init__(label)
        self.prefix = prefix

    def expand(self, input):
        input | beam.ParDo(self._OutputFn(self.prefix))


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


if __name__ == "__main__":
    # example_pcollection_in_memory()
    example_pcollection_read_text()

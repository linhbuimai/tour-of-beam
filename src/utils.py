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

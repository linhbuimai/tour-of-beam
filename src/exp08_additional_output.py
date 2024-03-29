# Using tags to emit additional PCollection

import apache_beam as beam
from apache_beam import pvalue
from src.utils import Output

num_below_100_tag = "num_below_100"
num_above_100_tag = "num_above_100"


class ProcessNumbersDoFn(beam.DoFn):
    def process(self, element):
        if element <= 100:
            yield element
        else:
            yield pvalue.TaggedOutput(num_above_100_tag, element)


with beam.Pipeline() as p:
    results = (
        p
        | beam.Create([10, 20, 200, 100, 5])
        | beam.ParDo(ProcessNumbersDoFn()).with_outputs(
            num_above_100_tag, main=num_below_100_tag
        )
    )
    results[num_below_100_tag] | "Log nums below 100" >> Output(
        prefix="Nums below 100: "
    )
    results[num_above_100_tag] | "Log nums above 100" >> Output(
        prefix="Nums above 100: "
    )

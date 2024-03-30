import argparse

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from src.utils import Output


p = beam.Pipeline()

(
    p
    | "Read table with Storage API" >> beam.io.ReadFromBigQuery(
        table='',
        method=beam.io.ReadFromBigQuery.Method.DIRECT_READ
    )
    | beam.combiners.Sample.FixedSizeGlobally(10)
    | beam.Map(lambda elem: elem['Price'])
    | Output()
)
#
# from https://tour.beam.apache.org/tour/python/introduction/beam-concepts/pipeline-concepts/setting-pipeline
import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.io import ReadFromText, WriteToText

class Output(beam.PTransform):
    class _OutputFn(beam.DoFn):
        def process(self, element):
            print(element)

    def expand(self, input):
        input | beam.ParDo(self._OutputFn())


def main(argv=None, save_main_session=True):

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://dataflow-samples/shakespeare/kinglear.txt',
        help='Input file to process'
    )
    parser.add_argument(
        '--output',
        dest='output',
        default='output/exp01.txt',
        help='Output file to write results to.'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    # `save_main_session=True` because one or more DoFn relies on the global context

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | 'Read' >> ReadFromText(known_args.input) \
            | beam.Filter(lambda line: line != "")

        output = lines | 'Write' >> WriteToText(known_args.output)

        result = p.run()
        result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
import apache_beam as beam

class SumCombineFn(beam.CombineFn):
  def create_accumulator(self):
    return 0

  def add_input(self, accumulator, input):
    return accumulator + input

  def merge_accumulators(self, accumulators):
    return sum(accumulators)

  def extract_output(self, accumulator):
    return accumulator

with beam.Pipeline() as pipeline:
  sums = (
      pipeline
      | 'Create numbers' >> beam.Create([('key1', [2, 3]), ('key2', [4, 5])])
      | 'Sum values' >> beam.CombineValues(SumCombineFn())
      | 'Print results' >> beam.Map(print))
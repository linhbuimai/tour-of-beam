import apache_beam as beam
from utils import Output


def partition_fn(element, num_partitions):
    if element > 100:
        return 0
    else:
        return 1


with beam.Pipeline() as p:
    results = (
        p
        | beam.Create([1, 2, 3, 4, 5, 100, 110, 250, 200])
        | beam.Partition(partition_fn, 2)
    )
    results[0] | "Log numbers > 100" >> Output(prefix="Number > 100: ")
    results[1] | "Log numbers <= 100" >> Output(prefix="Number <= 100: ")

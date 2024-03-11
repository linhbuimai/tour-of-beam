from utils import Output
import apache_beam as beam

input = [1, 10, 100, 1000]
def bounded_sum(values, bound=500):
  return min(sum(values), bound)

small_sum = input | beam.CombineGlobally(bounded_sum) | "Print small sum" >> Output()
large_sum = input | beam.CombineGlobally(bounded_sum, bound=5000) | "Print large sum" >> Output()

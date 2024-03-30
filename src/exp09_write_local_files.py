import apache_beam as beam
from src.utils import Output

p = beam.Pipeline()
p.run().wait_until_finish()
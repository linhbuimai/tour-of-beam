"""
Data: Shakespeare "Kinglear"
What to do:
Divide into words and filtered (except the words beginning with "i")
Using `additional output` --> return 2 PCollection with separation conditions is uppercase and lowercase
Create a view from PCollection with lowercase words, passing it to the side-input, 
  then check if there are matching words in both registers.
"""

import apache_beam as beam
from src.utils import Output


if __name__ == "__main__":
    file_path = "gs://apache-beam-samples/shakespeare/kinglear.txt"

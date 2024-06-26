#   Licensed to the Apache Software Foundation (ASF) under one
#   or more contributor license agreements.  See the NOTICE file
#   distributed with this work for additional information
#   regarding copyright ownership.  The ASF licenses this file
#   to you under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import apache_beam as beam


# Output PCollection
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


def partition_fn(word, num_partitions):
    if word.upper() == word:
        return 0
    if word[0].isupper():
        return 1
    else:
        return 2


with beam.Pipeline() as p:
    parts = (
        p
        | "Log lines"
        >> beam.io.ReadFromText("gs://apache-beam-samples/shakespeare/kinglear.txt")
        | beam.combiners.Sample.FixedSizeGlobally(100)
        | beam.FlatMap(lambda line: line)
        | beam.FlatMap(lambda sentence: sentence.split())
        | beam.Partition(partition_fn, 3)
    )

    allLetterUpperCase = (
        parts[0]
        | "All upper" >> beam.combiners.Count.PerElement()
        | beam.Map(lambda key: (key[0].lower(), key[1]))
    )
    firstLetterUpperCase = (
        parts[1]
        | "First upper" >> beam.combiners.Count.PerElement()
        | beam.Map(lambda key: (key[0].lower(), key[1]))
    )
    allLetterLowerCase = parts[2] | "Lower" >> beam.combiners.Count.PerElement()

    flattenPCollection = (
        (allLetterUpperCase, firstLetterUpperCase, allLetterLowerCase)
        | beam.Flatten()
        | beam.GroupByKey()
        | Output()
    )

# `PTransform`

(common and core transforms in Apache Beam)

- [x] `ParDo` and `DoFn`

## Filter

Can filter: text, numerical collection.

Often: define a filter function (custom filter function), then apply that function to `beam.Filter()` transform.

Possible implementations of filter:

1. Simple filter: apply a simple function to `beam.Filter`
2. Filter with different types of side inputs:
    + Side inputs as singletons (only one value)
    + Side inputs as iterators (an array of multiple values)
    + Side inputs as dictionaries (a dictionary)

## Aggregations

Common aggregations: count, sum, mean, min, max

Can do aggregation globally (on the whole PCollection) or per key.

### Count

```
beam.combiners.Count.Globally() <-- total count -->
beam.combiners.Count.PerKey() <-- count per key -->
beam.combiners.Count.PerElement() <-- count unique elements -->
```

### Sum

```
beam.CombineGlobally(sum)
beam.CombinePerKey(sum)
```

- [x] TODO Check the following functions: `beam.CombineFn`, `beam.CombineValues` --> Similar to DoFn and ParDo; the `beam.CombineValues` expects a PCollection of key-value pair.

```python
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
```


### Mean

```
beam.combiners.Mean.Globally <-- input should be list of integers -->
beam.combiners.Mean.PerKey <-- input should be map -->
```

### Min/Max

```
beam.CombinePerKey(min/max)

# to find min globally (of the whole PCollection)
beam.CombineGlobally(lambda elements: min/max(elements or [None]))
beam.combiners.Top.Smallest(5) <-- find top 5 smallest number in a list of integers -->
beam.combiners.Top.Largest(5) <-- find top 5 largest number in a list of integers -->
```

### WithKeys

It takes a `PCollection<V>` and produces a `PCollection<KV<K,V>>`

- [x] Learn how to filter the input having type map (is dictionary)
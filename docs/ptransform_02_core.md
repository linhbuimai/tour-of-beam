# `PTransform`

> How to use core transforms functions in Beam

## `Map`

### `ParDo`

#### Intro to `ParDo`

`ParDo` is similar to map phase in `map-shuffle-reduce`-style algorithm.

A `ParDo` transform considers each element in the input `PCollection`, performs processing function (`process`) on that element, then emits zero, one, or multiple elements to an output `PCollection`.

`ParDo` can benefit:
- Filtering a dataset
- Formatting or type-converting each element in a dataset
- Extracting parts of each element in a dataset
- Performing computation on each element in a dataset

**Apply `ParDo` transform requires user code in the form of a `DoFn` object. `DoFn` is a Beam SDK class that defines a distributed processing function.**

example:
```python
input = ...

class ComputeWordLengthFn(beam.DoFn):
    def process(self, element):
        return [len(element)]

word_lengths = input | beam.ParDo(ComputeWordLengthFn())
```

#### Create `DoFn` for `ParDo` transform

`DoFn` defines pipeline's extract data processing tasks:
- having `process` function containing user-defined transform logic
- should always contains `__init__` block (otherwise they may not execute on distributed runners)

> Pay attention to: Requirements for writing user code for Beam transforms. <??>

- [ ] TODO: know what are requirements for writing user code for beam transforms?

function `process` of `DoFn` object:
- input element
- **return an iterable** with its output values
    + using `yield` statements
    + using an iterable like: a list, a generator, etc.
- in case the input PCollection are key/value pair --> processed element method must have two parameters for each key and value

example:

```python
class ComputeWordLengthFn(beam.DoFn):
    def process(self, element):
        return [len(element)]
```

> Beam does not guarantee the number of invocation (a `DoFn` instance can be invoked multiple times) your implementation of DoFn should idempotent regardless of number of invocation. -->  should not modify the parameters provided to the `ProcessElement` method; should not modify any side inputs --> Not change the output value once emitted it.

Can populate additional parameters to `DoFn.process()`:

1. Timestamp: access timestamp of an input element
2. Window: access the window that input element falls into
3. PaneInfo: access the information of current firing (the firing of a window):
    + whether it's early or late firing
    + how many times this window has already fired for this key
4. Timer and State: user defined timer and state

## Built-in `DoFn`

--> `beam.Map` ; `beam.FlatMap`

### `beam.Map`

- applies a user-defined function to each element in the input PCollection
- one-one type output

### `beam.FlatMap`

- applies a user-defined function to each element in the input PCollection
- could be one to zero/one/many type output

### `GroupByKey`

- Group elements in PCollection by keys.
- Input = PCollection of key-value pairs
- Output = PCollection of key-[group of values] pairs

--> is a transform of multi-map to uni-map (uni=unique)

Also: `GroupBy` <-- custom parameterize the behavior of the `GroupByKey`, by either define a value to be grouped, or receive a function to determine how each value in the PCollection is grouped.

**Working with unbounded PCollection**

- To perform `GroupByKey/CoGroupByKey` over unbounded PCollection, one must use non-global window, or an aggregation trigger, or both.
    + all elements in PCollection must follow the same window strategy, window sizing
    + (similarly) use the same aggregation trigger


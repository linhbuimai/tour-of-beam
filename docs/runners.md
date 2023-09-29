# Concepts: Runners

`pipeline` = data-parallel processing
`runners` = execution engines (to execute pipeline)

Layer `runners` based on the core concept of Beam Model (TODO: get this concept) (formally Dataflow Model).

Types of runners:

- Direct runner (run on your machine)
- Not direct runner: (the common one only)
    + Flink
    + Spark
    + Dataflow
    + Nemo

## DirectRunner

Why should we use direct runner? To validate your developing pipeline to follow Apache Beam model, s.t your model can run on any runners.

- enforce immutability of elements
- enforce encodability of elements
- guarantee elements are processed in an arbitrary order at all points
- (validate?) serialization of user functions
- debug pipeline

TODO: continue pick up DirectRunner at: [Using the Direct Runner](https://beam.apache.org/documentation/runners/direct/)

## Cloud Dataflow runner



# Run examples

1. Test the simple pipeline: `wordcount.py` (ready-built apache beam example with Python)

```bash
$ python src/wordcount.py --input resources/wordcount.txt --output output/wordcount.txt
```
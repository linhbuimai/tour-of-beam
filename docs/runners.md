# Concepts: Runners

`pipeline` = data-parallel processing
`runners` = execution engines (what back-end the pipeline runs on)

Layer `runners` based on the core concept of Beam Model (formally Dataflow Model).

- [ ] TODO: Get to know the [Beam Model concepts](https://beam.apache.org/documentation/basics/)

Types of runners:

- Direct runner (run on your machine)
- Not direct runner: (the common one only)
    + Flink
    + Spark
    + Dataflow
    + Nemo

## Direct Runner

Why should we use direct runner? To validate your developing pipeline to follow Apache Beam model, s.t your model can run on any runners.

- enforce immutability of elements
- enforce encodability of elements
- guarantee elements are processed in an arbitrary order at all points
- (validate?) serialization of user functions
- debug pipeline

- [ ] TODO: continue pick up DirectRunner at: [Using the Direct Runner](https://beam.apache.org/documentation/runners/direct/)

## Cloud Dataflow Runner

(?) How does it work?

- Executable code is uploaded to cloud storage
- A dataflow job is created. Pipeline is executed on managed resources in Google Cloud Platform.

- [ ] TODO: continue pick up DataflowRunner at: [Using the Google Cloud Dataflow Runner](https://beam.apache.org/documentation/runners/dataflow/)

# Run examples

1. Test the simple pipeline: `wordcount.py` (ready-built apache beam example with Python)

```bash
$ python src/wordcount.py --input resources/wordcount.txt --output output/wordcount.txt
```

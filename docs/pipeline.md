## Concepts: Pipeline

Create a ==driver program== to define pipeline:

- inputs
- transforms
- outputs
- execution options of pipeline (where and how to run)

Beam abstractions work with both batch and streaming data sources (that's the reason for: Unified processing).

## Create `Pipeline`

Note:
- A beam program starts by creating `Pipeline`
- A `Pipeline` requires some "configurations" in order to run properly, in which should pay attention to Runner and Runtime Variables

`Pipeline` = the whole data processing task (from start to finish)

`PCollection` = distributed datasets, input/output of each step of the pipeline, could be bounded/unbounded stream, is immutable.

`PTransform` = a data processing operation (a step in the pipeline), receive one or mote PCollection as input, produce zero/one/or more PCollection as output.

`I/O transforms` = library of PTransform to read/write data from/to external data sources.

## How a Beam driver program works?

1. Create a pipeline object, set execution options
2. Create an initial `PCollection`
3. Apply `PTransform` to each `PCollection`
4. Use `I/O` to write the final `PCollection` to external storage
5. Run the pipeline object with execution options (command line parameters) in the runner

The runner then constructs a workflow graph -> the graph then be executed under appropriate distributed processing back-end (depends on the runner type) (async jobs)

> [!Note]
> The pipeline often be defined in `main()` function.

## Configure pipeline options

Includes the following configurations:

- Which type of runner and must-have configurations of that runner
- Input/output information of the data sources

**Object**: `PipelineOptions`

```python
from apache_beam.options.pipeline_options import PipelineOptions
```

Two ways of configuring pipeline options:

1. Create a `PipelineOptions` object that automatically parse arguments from command line in the form of: `--<option>=<value>`
2. Create a custom pipeline options, inherit from `PipelineOptions`, to declare the argument options, its descriptions, its default value, etc. (However in Python there's no need to create a subclass of `PipelineOptions`, but using `ArgumentParser` object)

> [!Note]
> The second method is preferable due to its transparency.

We should parameterized `PipelineOptions`, example:

```python
parser = argparse.ArgumentParser()
parser.add_argument(
  "--secret_prefix",
  required=True,
  help="Secret Prefix to trigger Automation Or Manual Pipeline",
)
parser.add_argument(
  "--pipeline_name",
  required=True,
  help="Pipeline Name to trigger Automation Or Manual Pipeline",
)

known_args, pipeline_args = parser.parse_known_args()
```

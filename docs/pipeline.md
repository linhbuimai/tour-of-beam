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

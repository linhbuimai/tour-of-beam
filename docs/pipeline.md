# Concepts: Pipeline

Create a ==driver program== to define pipeline:

- inputs
- transforms
- outputs
- execution options of pipeline (where and how to run)

Beam abstractions work with both batch and streaming data sources (that's the reason for: Unified processing).

## Beam abstractions

`Pipeline` = the whole data processing task (from start to finish)
`PCollection` = 
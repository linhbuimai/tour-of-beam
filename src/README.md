## Beam abstractions

`Pipeline` = the whole data processing task (from start to finish)

`PCollection` = an unordered bag of elements, is potentially distributed, homogeneous data set or data stream, is owned by specific data pipeline, is immutable

`PTransform` = (transform) data processing operation/a transformation step in the pipeline. It receives zero to more `PCollection` and produce zero to more `PCollection`

`Aggregation` = compute a value from multiple values

`User-defined function (UDF)`

`Schema` = is a language-independent type definition for a PCollection

`SDK` = is a language specific library to build transforms, construct pipelines, submit pipelines to a runner

`Runner` = data processing engine to run pipeline on

`Window` = `PCollection` can be subdivided into windows based on timestamps of the individual elements --> can do aggregation on windows, specially for unbounded `PCollection`

`Watermark` = is the best guess as to when all data in a certain window is expected to have arrived --> relates to: late arrival events

`Trigger` = determine when to aggregate the results of each window

`State and timers` = Per-key state and timer callbacks --> can based on these to control over aggregating input collections that grow over time

`Splittable DoFn` = to parralel processing elements
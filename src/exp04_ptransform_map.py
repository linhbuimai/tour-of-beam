import apache_beam as beam
from utils import Output

with beam.Pipeline() as p:
    input = p | "Fruits" >> beam.Create(
        [
            ("banana", 2),
            ("apple", 4),
            ("lemon", 3),
            ("Apple", 1),
            ("Banana", 5),
            ("Lemon", 2),
        ]
    )

    ls_input = p | "Ls Fruits" >> beam.Create(
        ["banana", "apple", "lemon", "Apple", "Banana", "Lemon"]
    )

    (
        input
        | "Lowercase" >> beam.Map(lambda x: (x[0].lower(), x[1]))
        | "Group dictionaries" >> beam.GroupByKey()
        | "Write from output" >> Output()
    )

    (
        ls_input
        | "Lowercase list fruits" >> beam.Map(lambda x: x.lower())
        | beam.Map(lambda word: (word[0], word))
        | beam.GroupByKey()
        | Output()
    )

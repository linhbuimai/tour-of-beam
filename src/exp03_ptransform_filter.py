import apache_beam as beam
from utils import Output


def is_perenial(plant):
    # is simple filter
    return plant["duration"] == "perennial"


def has_duration(plant, name, duration):
    return plant["duration"] == duration and plant["name"] == name


def filter_simple():
    with beam.Pipeline() as p:
        perenials = (
            p
            | "Gargending plans"
            >> beam.Create(
                [
                    {"icon": "🍓", "name": "Strawberry", "duration": "perennial"},
                    {"icon": "🥕", "name": "Carrot", "duration": "biennial"},
                    {"icon": "🍆", "name": "Eggplant", "duration": "perennial"},
                    {"icon": "🍅", "name": "Tomato", "duration": "annual"},
                    {"icon": "🥔", "name": "Potato", "duration": "perennial"},
                ]
            )
            # | 'Filter perenials' >> beam.Filter(is_perenial)
            # | 'Filter with lambda' >> beam.Filter(lambda plant: plant['duration'] == 'perennial')
            | "Filter with has_duration"
            >> beam.Filter(has_duration, "Potato", "perennial")
            | beam.Map(print)
        )


def filter_with_singleton():
    """
    Filtering with side inputs as singletons
    """
    with beam.Pipeline() as p:
        perennial = p | "Perennial" >> beam.Create(["perennial"])
        perennials = (
            p
            | "Gargending plans"
            >> beam.Create(
                [
                    {"icon": "🍓", "name": "Strawberry", "duration": "perennial"},
                    {"icon": "🥕", "name": "Carrot", "duration": "biennial"},
                    {"icon": "🍆", "name": "Eggplant", "duration": "perennial"},
                    {"icon": "🍅", "name": "Tomato", "duration": "annual"},
                    {"icon": "🥔", "name": "Potato", "duration": "perennial"},
                ]
            )
            | "Filter perennials"
            >> beam.Filter(
                lambda plant, duration: plant["duration"] == duration,
                duration=beam.pvalue.AsSingleton(perennial),
            )
            | beam.Map(print)
        )


def filter_with_iterators():
    """
    Filtering with side inputs as iterators
    """
    with beam.Pipeline() as p:
        valid_durations = p | "Valid durations" >> beam.Create(["annual", "biennial"])

        valid_plans = (
            p
            | "Gargending plans"
            >> beam.Create(
                [
                    {"icon": "🍓", "name": "Strawberry", "duration": "perennial"},
                    {"icon": "🥕", "name": "Carrot", "duration": "biennial"},
                    {"icon": "🍆", "name": "Eggplant", "duration": "perennial"},
                    {"icon": "🍅", "name": "Tomato", "duration": "annual"},
                    {"icon": "🥔", "name": "Potato", "duration": "perennial"},
                ]
            )
            | "Filter valid plans"
            >> beam.Filter(
                lambda plant, valid_durations: plant["duration"] in valid_durations,
                valid_durations=beam.pvalue.AsIter(valid_durations),
            )
            | beam.Map(print)
        )


def filter_with_dictionaries():
    """
    Filtering with side inputs as dictionaries
    """
    with beam.Pipeline() as p:
        keep_duration = p | "Duration filters" >> beam.Create(
            [("annual", False), ("biennial", False), ("perennial", True)]
        )

        perennials = (
            p
            | "Gargending plans"
            >> beam.Create(
                [
                    {"icon": "🍓", "name": "Strawberry", "duration": "perennial"},
                    {"icon": "🥕", "name": "Carrot", "duration": "biennial"},
                    {"icon": "🍆", "name": "Eggplant", "duration": "perennial"},
                    {"icon": "🍅", "name": "Tomato", "duration": "annual"},
                    {"icon": "🥔", "name": "Potato", "duration": "perennial"},
                ]
            )
            | "Filter plans by duration"
            >> beam.Filter(
                lambda plant, keep_duration: keep_duration[plant["duration"]],
                keep_duration=beam.pvalue.AsDict(keep_duration),
            )
            | beam.Map(print)
        )


# Exercise


class SplitWords(beam.DoFn):
    def __init__(self, delimiter=" "):
        self.delimiter = delimiter

    def process(self, element):
        for word in element.split(self.delimiter):
            yield word


def exercise_filter_words():
    with beam.Pipeline() as p:
        filter_words = (
            p
            | "Create inputs"
            >> beam.Create(
                [
                    "To be, or not to be: that is the question: \
                                              Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, \
                                              Or to take arms against a sea of troubles, And by opposing end them. To die: to sleep"
                ]
            )
            | "Split words" >> beam.ParDo(SplitWords())
            | "Filter task" >> beam.Filter(lambda word: word.lower().startswith("t"))
            # | beam.Map(print)
            | Output(prefix="PCollection filtered value: ")
        )


if __name__ == "__main__":
    # filter_simple()
    # filter_with_singleton()
    # filter_with_iterators()
    # filter_with_dictionaries()
    exercise_filter_words()

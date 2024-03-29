from utils import Output
import apache_beam as beam


class WordsAlphabet:
    def __init__(self, alphabet, fruit, country) -> None:
        self.alphabet = alphabet
        self.fruit = fruit
        self.country = country

    def __str__(self) -> str:
        return "WordsAlphabet(alphabet:'%s', fruit='%s', country='%s')" % (
            self.alphabet,
            self.fruit,
            self.country,
        )


def apply_transform(fruits, countries):
    def map_to_alphabet_kv(word):
        return (word[0], word)

    def cogbk_result_to_wordsalphabet(cgbk_result):
        (alphabet, words) = cgbk_result
        return WordsAlphabet(alphabet, words["fruits"][0], words["countries"][0])

    fruits_kv = fruits | "Fruit to KV" >> beam.Map(map_to_alphabet_kv)
    countries_kv = countries | "Country to KV" >> beam.Map(map_to_alphabet_kv)

    return (
        {"fruits": fruits_kv, "countries": countries_kv}
        | beam.CoGroupByKey()
        | beam.Map(cogbk_result_to_wordsalphabet)
    )


input_fruit = ["apple", "banana", "cherry"]
input_country = ["australia", "brazil", "canada"]

with beam.Pipeline() as p:
    fruits = p | "Create fruits" >> beam.Create(input_fruit)
    countries = p | "Create countries" >> beam.Create(input_country)

    (apply_transform(fruits, countries) | Output())

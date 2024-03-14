import apache_beam as beam
from utils import Output

class Person:
    def __init__(self, name, city, country=''):
        self.name = name
        self.city = city
        self.country = country

    def __str__(self):
        return 'Person[' + self.name + ',' + self.city + ',' + self.country + ']'
    
class EnrichCountryDoFn(beam.DoFn):
    def process(self, element, cities_to_countries):
        yield Person(element.name, element.city, cities_to_countries[element.city])

with beam.Pipeline() as p:
    # is that hard-coded?
    cities_to_countries = {
        'Beijing': 'China',
        'London': 'United Kingdom',
        'San Francisco': 'United States',
        'Singapore': 'Singapore',
        'Sydney': 'Australia'
    }
    persons = [
        Person('Henry', 'Singapore'),
        Person('Jane', 'San Francisco'),
        Person('Lee', 'Beijing'),
        Person('John', 'Sydney'),
        Person('Alfred', 'London')
    ]

    (
        p
        | beam.Create(persons)
        | beam.ParDo(EnrichCountryDoFn(), cities_to_countries)
        | Output()
    )
import apache_beam as beam
from utils import Output

emails_list = [
  ('amy', 'amy@example.com'),
  ('carl', 'carl@example.com'),
  ('julia', 'julia@example.com'),
  ('carl', 'carl@email.com'),
]

phones_list = [
  ('amy', '111-222-3333'),
  ('james', '222-333-4444'),
  ('amy', '333-444-5555'),
  ('carl', '444-555-6666'),
]

def join_info(name_info):
  (name, info) = name_info
  return '%s; %s; %s' % (name, sorted(info['emails']), sorted(info['phones']))

with beam.Pipeline() as p:
  emails = p | 'CreateEmails' >> beam.Create(emails_list)
  phones = p | 'CreatePhones' >> beam.Create(phones_list)

  # Using CoGroupByKey
  results = (
    {'emails': emails, 'phones': phones}
    | beam.CoGroupByKey()
    | beam.Map(join_info)
    | Output()
  )
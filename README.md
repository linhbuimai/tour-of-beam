# tour-of-beam
Personal notes and codes during experiment on Apache Beam. Based on Tour of beam tutorial.

## Quickstart

### Step 1: Prepare local env

- `python 3.11`
- using `virtualenv` to create virtual environment

```bash
$ pip install apache-beam
$ pip install 'apache-beam[gcp]'

# for developing and running unittests
$ pip install 'apache-beam[test]'
```

Optional installations:

```bash
# for API documentation of Beam
$ pip install 'apache-beam[docs]'
```

### Step 2: Get examples to learn

Source to Beam's examples: [github: apache_beam/examples](https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples)


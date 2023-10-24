## Create `PCollection`

Can create `PCollection` by:
- generate in-memory data
- read from external source: csv, database (JDBC, ODBC, etc.), web --> depends on the connectors you have (default of Beam or custom built connector)

**Create `PCollection` from a csv file**
- Loading text lines with `TextIO.Read` transform
- Parsing lines of text into tabular format
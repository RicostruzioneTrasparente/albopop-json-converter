# XML to JSON converter based on AlboPOP Specs, v0.1.0

AlboPOP scrapers produce feeds in RSS format following the [official specs](http://albopop.it/specs) of the project.
This utility use a generic XSLT from [JayDaley/XML-to-JSON-in-XSLT](https://github.com/JayDaley/XML-to-JSON-in-XSLT) (style1) and
custom transformations to perform a deterministic mapping between AlboPOP XML and AlboPOP JSON (see and compare the examples).

## Usage

### Converte

Clone this repository and install the requirements using pip.
Then run the script: `python AlbopopJsonConverter.py file_to_convert.xml [file_xslt.xsl]`.
Result will be written in `file_to_convert.xml.json`.

You can also import it as a module: `from AlbopopJsonConverter import AlbopopJsonConverter`.
In your script you can also convert XML starting from a string and not from a file,
obtaining a regular dict.

### Validate

The final JSON can be validated against the JSON Schema provided (Python 3.4+ required):
`jsonschema -i file_to_convert.xml.json albopop-json-schema.json` or using custom class provided:
`python AlbopopJsonValidator.py file_to_convert.xml.json [albopop-json-schema.json]`.

Warning: you can't validate the original XML, you have to convert it to JSON first.

### Merge

The convertion produces a dict from a XML string, so a representation of the channel. According to specifications,
some channel attributes can be inherited by items, so there is the method `get_items()` to convert channel dict
in items list with those attributes properly merged. The channel-specific ones will be added to all items as value
of `channel` attribute, following the Elasticsearch mapping provided: `albopop-elasticsearch-mapping.json`.
Of course, the channel JSON has to be valid against schema to obtain the correct items list.

## Dependencies

Python3 (jsonschema requires v3.4+), lxml, vix and
the [xslt file](https://github.com/JayDaley/XML-to-JSON-in-XSLT/blob/master/xml2json-style1.xsl).

## Further informations

"Ricostruzione Trasparente" project: http://www.ricostruzionetrasparente.it/.

AlboPOP project: http://albopop.it/.


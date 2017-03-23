# XML to JSON converter based on AlboPOP Specs, v0.1.0

AlboPOP scrapers produce feeds in RSS format following the [official specs](http://albopop.it/specs) of the project.
This utility use a generic XSLT from [JayDaley/XML-to-JSON-in-XSLT](https://github.com/JayDaley/XML-to-JSON-in-XSLT) (style1) and custom transformations to perform a deterministic mapping between AlboPOP XML and AlboPOP JSON
(see and compare the examples).

## Usage

Clone this repository and install the requirements using pip.
Then run the script: `python AlbopopJsonConverter.py file_to_convert.xml [file_xslt.xsl]`.
Result will be written in `file_to_convert.xml.json`.

You can also import it as a module: `from AlbopopJsonConverter import AlbopopJsonConverter`.
In your script you can also convert XML starting from a string and not from a file,
obtaining a regular dict.

## Dependencies

Python3, lxml, vix and the [xslt file](https://github.com/JayDaley/XML-to-JSON-in-XSLT/blob/master/xml2json-style1.xsl).

## Further informations

"Ricostruzione Trasparente" project: http://www.ricostruzionetrasparente.it/.

AlboPOP project: http://albopop.it/.


# -*- coding: utf-8 -*-

import sys, json, logging
from jsonschema import Draft4Validator
import pkg_resources

class AlbopopJsonValidator():

    schema_file = None
    content_file = None

    def __init__( self , content = "albopop-json-schema.json" ):

        if isinstance( content , dict ):
            self.schema = content
        else:

            self.schema_file = pkg_resources.resource_filename(__name__,content)

            with open(self.schema_file) as f:

                self.schema = json.load(f)

                try:
                    Draft4Validator.check_schema(self.schema)
                    self.d4v = Draft4Validator(self.schema)
                except:
                    logging.error("Provided schema not valid against Draft4 specs.")
                    raise

    def validate( self , content = {} ):

        if isinstance( content , dict ):
            result = self.d4v.is_valid(content)
        else:
            self.content_file = content
            with open(self.content_file) as f:
                content = json.load(f)
                result = self.d4v.is_valid(content)

        self.errors = sorted({
            e.message: e
            for e in self.d4v.iter_errors(content)
        }.values(), key=str)

        return result

if __name__ == "__main__":

    if len(sys.argv) > 2:
        ajv = AlbopopJsonValidator(sys.argv[2])
    else:
        ajv = AlbopopJsonValidator()

    if len(sys.argv) > 1:
        is_valid = ajv.validate(sys.argv[1])
    else:
        logging.error("Please provide a file JSON to validate.")
        exit()

    logging.warning("%s, %s is %s against %s." % (
        "Yes" if is_valid else "No",
        ajv.content_file,
        "valid" if is_valid else "NOT valid",
        ajv.schema_file
    ))

    if not is_valid:
        for error in ajv.errors:
            logging.warning("%s in %s" % ( error.message , error.path ))


import jsonschema
import json
import urllib2

input_schema = "http://surveyman.github.io/Schemata/survey_input.json"
option_schema = "http://surveyman.github.io/Schemata/survey_option.json"

def validateJSON(instance, schema=input_schema, url=True):
    """
    Validates the input jsonFile against the current json schema provided at `http://surveyman.github.io/Schemata/survey_input.json`
    :param jsonFile:
    """
    if url:
        this_schema = urllib2.urlopen(schema).read()
    else:
        this_schema = schema
    jsonschema.validate(instance, json.loads(this_schema))

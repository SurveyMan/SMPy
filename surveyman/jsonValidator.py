import jsonschema
import urllib2

input_schema = "http://surveyman.github.io/Schemata/survey_input.json"

def validateJSON(instance):
    """
    Validates the input jsonFile against the current json schema provided at `http://surveyman.github.io/Schemata/survey_input.json`
    :param jsonFile:
    """
    schema = urllib2.urlopen(input_schema).read()
    jsonschema.validate(instance, schema)

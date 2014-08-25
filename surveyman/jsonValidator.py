import jsonschema
import json
import urllib2

input_schema = "http://surveyman.github.io/Schemata/survey_input.json"
option_schema = "http://surveyman.github.io/Schemata/survey_option.json"
question_schema = "http://surveyman.github.io/Schemata/survey_question.json"
block_schema = "http://surveyman.github.io/Schemata/survey_block.json"


def validate_json(instance, schema=input_schema, url=True):
    """
    Validates the input jsonFile against the current `JSON Schema <http://surveyman.github.io/Schemata>`_.

    :param instance: A JSON object
    :param schema: The target schema.
    :param url: external source
    """
    if url:
        this_schema = urllib2.urlopen(schema).read()
    else:
        this_schema = schema
    jsonschema.validate(instance, json.loads(this_schema))

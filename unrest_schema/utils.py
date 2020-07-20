# loosely based on: https://github.com/Cahersan/django-schemulator
from collections import OrderedDict
from django import forms


KEYWORDS = {
  #Base keywords
  "label": "title",
  "help_text": "description",
  "initial": "default",
  "required": "required",

  #String type-specific keywords
  "max_length": "maxLength",
  "min_length": "minLength",

  #Numerical type-specific keywords
  "min_value": "minimum",
  "max_value": "maximum",
}

FIELD_TO_TYPE = {
  'IntegerField': 'integer',
  'BooleanField': 'boolean',
  'BooleanField': 'number',
  'TypedChoiceField': ''
}

FIELD_TO_FORMAT = {
  'EmailField': 'email',
  'DateTimeField': 'date-time',
}


def field_to_schema(field):
  field_type = field.__class__.__name__
  schema = {
    'type': FIELD_TO_TYPE.get(field_type, 'string'),
  }

  if not schema['type']:
    #currently only supported for TypedChoiceField
    sample_value = field.coerce('1')
    if isinstance(sample_value, (int, float)):
      schema['type'] = 'integer'
    elif isinstance(sample_value, bool):
      schema['type'] = 'boolean'
    else:
      schema['type'] = 'string'

  if field_type in FIELD_TO_FORMAT:
    schema['format'] = FIELD_TO_FORMAT.get(field_type, None)

  # Setup of JSON Schema keywords
  for (field_attr, schema_attr) in KEYWORDS.items():
    if hasattr(field, field_attr):
      schema[schema_attr] = getattr(field, field_attr)

  # choices needs to be two attrs, so handle it separately
  if hasattr(field, 'choices'):
    optional = not schema.get('required')
    schema['enum'] = [a for a, b in field.choices]
    schema['enumNames'] = [b for a, b in field.choices]
    if not optional and not schema['enum'][0]:
      schema['enum'] = schema['enum'][1:]
      schema['enumNames'] = schema['enumNames'][1:]

  # RJSF doesn't like minLength = null
  if schema.get('minLength', 0) is None:
    schema.pop('minLength')

  if field_type == 'ImageField':
    # RJSF confuses length of file and length of filename, eg "megapixel.png" is 1e6 characters long
    schema.pop('maxLength', None)
    # RJSF is confusde by default None on file field
    schema.pop('default', None)

  for field_attr in ['maxLength', 'title', 'maximum', 'minimum', 'default']:
    if schema.get(field_attr, '') is None:
      schema.pop(field_attr)

  # Set __django_form_field_cls keyword
  schema['__django_form_field_cls'] = field_type
  schema['__widget'] = field.widget.__class__.__name__

  return schema


def form_to_schema(form):
  schema = {
    'type': 'object',
    'properties': OrderedDict([
      (name, field_to_schema(field))
      for (name, field) in form.fields.items()
    ]),
    'required': []
  }

  for name, field in schema['properties'].items():
    if field.pop('required', None):
      schema['required'].append(name)

  if hasattr(form, 'form_title'):
    schema['title'] = form.form_title

  return schema

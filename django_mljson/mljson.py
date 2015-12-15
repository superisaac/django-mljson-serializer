"""
Serialize data to/from JSON
"""

# Avoid shadowing the standard library json module
from __future__ import absolute_import, unicode_literals

import datetime
import decimal
import json
import sys
import uuid
from io import BytesIO

from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer, Serializer as PythonSerializer,
)
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import six
from django.utils.timezone import is_aware


class Serializer(PythonSerializer):
    """
    Convert a queryset to JSON.
    """
    internal_use_only = False

    def _init_options(self):
        if json.__version__.split('.') >= ['2', '1', '3']:
            # Use JS strings to represent Python Decimal instances (ticket #16850)
            self.options.update({'use_decimal': False})
        self._current = None
        self.json_kwargs = self.options.copy()
        self.json_kwargs.pop('stream', None)
        self.json_kwargs.pop('fields', None)

    def start_serialization(self):
        self._init_options()

    def end_serialization(self):
        '''
        Do nothing
        '''
    
    def end_object(self, obj):
        # self._current has the field data
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder, **self.json_kwargs)
        self.stream.write('\n')
        self._current = None

    def getvalue(self):
        # Grand-parent super
        return super(PythonSerializer, self).getvalue()

def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data.
    """
    if isinstance(stream_or_string, (bytes, six.string_types)):
        stream_or_string = BytesIO(stream_or_string)
    try:
        def line_generator():
            for line in stream_or_string:
                yield json.loads(line.strip())
        for obj in PythonDeserializer(line_generator(), **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])

django-mljson-serializer
====

backup django models using multi-line json data.

The intro of this project is because django's json serializer cannot
handle large set of objects, json serializer always load json data
in memory, so parsing objects may use up all memory.

Mljson serializer dumps each object in one line and read them line by
line, thus unlimited data can be processed in streaming mode.

Install
====
```
% python setup.py install
```

Run
====
In the django project, add the following settings to settings.py
```
SERIALIZATION_MODULES = {
    'mljson': 'django_mljson.serializer'
}
```

then dump data using format=mljson
```
python manage.py dumpdata --format=mljson >some.mljson

python manage.py loaddata some.mljson
```




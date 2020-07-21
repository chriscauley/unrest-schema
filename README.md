Unrest Schema
=======

A library for converting Django forms to json schema endpoints

## Usage

First install with `pip install unrest_schema` and then register any form:

``` python
from django import forms
from unrest_schema import register

from myapp.models import MyModel

@register
class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ('field1', ...)
```

Then, in your urls add a the urls for unrest_schema

``` python
from django.urls import include

urlpatterns = [
    ..., #other url patterns
    re_path('', include('unrest_schema.urls')),
]
```

Now visit `/api/schema/MyModelForm/` in a browser to get the json representation of MyModelForm. Additionally you can post to `/api/schema/MyModelForm/` to create a new MyModel instance or `/api/schema/MyModelForm/1/` to modify the MyModel instance with `id=1`.

## Contributing/follow up

Feel free to open a github issue if you want to suggest any features or ask for help. Additionally, the python code for this project is ~150 lines so don't be afraid to dig in!
Extra configuration
===================

django-cors-headers
-------------------

If you use custom headers in cross-domain communication, you may want to add them to `CORS_ALLOW_HEADERS` and `CORS_EXPOSE_HEADERS` settings, e.g:
```python
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'my-custom-header',
]

CORS_EXPOSE_HEADERS = [
    'my-custom-header',
]
```
 For more information about those settings check official [`django-cors-headers documentation`](https://github.com/ottoyiu/django-cors-headers#cors_allow_headers).

FAQ
====

FAQ, 12-Factor App


Why is there a django.contrib.sites directory in Django Template?
-----------------------------------------------------------------

It is there to add a migration so you don't have to manually 
change the ``sites.Site`` record from ``example.com`` to whatever your 
domain is. Instead, your ``{{cookiecutter.domain_name}}`` and 
{{cookiecutter.project_name}} value is placed by **Cookiecutter** in the 
domain and name fields respectively.

See [0003_set_site_domain_and_name.py](https://github.com/witold-gren/django-template/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/%7B%7Bcookiecutter.project_slug%7D%7D/contrib/sites/migrations/0003_set_site_domain_and_name.py).


Why aren't you using just one configuration file (12-Factor App)
----------------------------------------------------------------

TODO

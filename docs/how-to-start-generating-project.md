Creating your first app with Django Template 
============================================

This tutorial will show you how to build a simple app using the 
[Django Template](https://github.com/witold-gren/django-template) 
templating system. We'll be building a cookie polling app to determine the most 
popular flavor of cookie.

Developers who have never used Django will learn the basics of creating 
a Django app; developers who are experienced with Django will learn how to set 
up a project within the Cookiecutter system. While many Django tutorials use 
the default SQLite database, Cookiecutter Django uses PostGres only, so we'll 
have you install and use that. 


Instructions
------------

1. **Setup** -- how to set up a virtual environment
2. **Cookiecutter** -- use Cookiecutter to initialize a project with your own customized information.
3. **Building the App** -- creating the My Favorite Cookie application.


### 1. Setup


Virtual Environment

First you must install Virtualenv.

    $ pip install virtualenv
 
Create a virtual environment for your project. Cookiecutter will install a bunch 
of dependencies for you automatically; using a virtualenv will prevent this from 
interfering with your other work.

    $ virtualenv /Users/...MY_CUSTOM_PATH.../myproject

Replace ``/Users/...MY_CUSTOM_PATH.../myproject`` with the path to your own ``.virtualenvs`` folder.

Activate the virtual environment by calling ``source`` on the ``activate`` shell script . 
On Windows you'll call this from the virtualenv's ``scripts`` folder:

.. code-block:: python
    
    $ source /Users/...MY_CUSTOM_PATH.../myproject/bin/activate

On Windows systems, it'll be found in the ``scripts`` folder. 
    
    $ source c:/...MY_CUSTOM_PATH.../myproject/bin/activate

You'll know the virtual environment is active because its name will appear in 
parentheses before the command prompt. When you're done with this project, 
you can leave the virtual environment with the ``deactivate`` command. 

    $ (cookie_polls):...
    $ deactivate

Now you're ready to create your project using Cookiecutter. 


### 2. Cookiecutter 


First you must install in your virtual environment `cookiecutter` package.

    $ source /Users/...MY_CUSTOM_PATH.../myproject/bin/activate
    $ pip install cookiecutter
    Collecting cookiecutter
      Using cached cookiecutter-1.6.0-py2.py3-none-any.whl
    Collecting binaryornot>=0.2.0 (from cookiecutter)
      Using cached binaryornot-0.4.4-py2.py3-none-any.whl
    Collecting jinja2-time>=0.1.0 (from cookiecutter)
      Using cached jinja2_time-0.2.0-py2.py3-none-any.whl
    Collecting jinja2>=2.7 (from cookiecutter)
      Using cached Jinja2-2.10-py2.py3-none-any.whl
    ...
    Successfully installed MarkupSafe-1.0 arrow-0.12.1 backports.functools-lru-cache-1.5 
    binaryornot-0.4.4 certifi-2018.1.18 chardet-3.0.4 click-6.7 cookiecutter-1.6.0 
    future-0.16.0 idna-2.6 jinja2-2.10 jinja2-time-0.2.0 poyo-0.4.1 python-dateutil-2.7.2 
    requests-2.18.4 six-1.11.0 urllib3-1.22 whichcraft-0.4.1


#### Generate project
Django developers may be familiar with the ``startproject`` command, which 
initializes the directory structure and required files for a bare-bones 
Django project. While this is fine when you're just learning Django for the 
first time, it's not great for a real production app. Cookiecutter takes care 
of a lot of standard tasks for you, including installing software dependencies, 
setting up testing files, and including and organizing common libraries. 
It also generates a software license and a README.

Change directories into the folder where your projects live, and 
run ``cookiecutter`` followed by the URL of Cookiecutter's Github repo.

.. code-block:: python

    $ cd /my/projects/folder
    (cookie_polls)
    my/projects/folder
    $ cookiecutter https://github.com/witold-gren/project-template
    or
    $ cookiecutter git@github.com:witold-gren/project-template.git

This will prompt you for a bunch of values specific to your project. 
Press "enter" without typing anything to use the default values, which are 
shown in [brackets] after the question. You can learn about all the different 
options [here](https://github.com/witold-gren/project-template/blob/master/docs/project-generation-options.md) 
but for now we'll use the defaults for everything but your name, your email, 
the project's name, and the project's description.

.. code-block:: python

     project_name [project_name]: My Favorite Cookie
     project_slug [My_Favorite_Cookie]: 
     author_name [Your Name]: author
     email [Your email]: you@example.com
     description [A short description of the project.]: Poll your friends to determine the most popular cookie. 

Then hit "enter" to use the default values for everything else. 


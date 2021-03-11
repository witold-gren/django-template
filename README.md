Django Template
===============

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter), Django Template is a framework for jumpstarting
production-ready Django projects quickly.

* Documentation: https://github.com/witold-gren/django-template/blob/master/docs/index.md
* See [Troubleshooting](https://github.com/witold-gren/django-template/blob/master/docs/troubleshooting.md) for common errors and obstacles
* If you have problems with Django Template, please open issues_ don't send emails to the maintainers.


Features
--------
* For Django 3.1
* Works with Python 3.9.x
* Renders Django projects with 100% starting test coverage
* Twitter [Bootstrap] v4.0.0 - beta 1
* [12-Factor] based settings via [django-environ]
* Optimized development and production settings
* Comes with custom user model ready to go
* Docker support using [docker-compose] for development and production
* Run tests with [Pytest] and [pytest-django]
* Customizable PostgreSQL version 13.1 or 12.5
* Health check default is installed 
* Integration with:
    * [Sentry] for error logging
    * [django-extensions]
    * [django-debug-toolbar]
    * [factory-boy]
    * [faker]
    * [django-webtest]
    * [jupyter]
    * [coverage]
    * [pylama]
    * [django-prometheus]
    * [black]
    * [django-cors-headers]


Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Configuration for [Celery]
* Configuration for [Django Rest Framework]
* Configuration for [drf-yasg]
* Configuration for [django-allauth]

[Bootstrap]: https://github.com/twbs/bootstrap
[django-environ]: https://github.com/joke2k/django-environ
[12-Factor]: http://12factor.net/
[django-allauth]: https://github.com/pennersr/django-allauth
[Celery]: http://www.celeryproject.org/
[Sentry]: https://sentry.io/welcome/
[docker-compose]: https://github.com/docker/compose
[Pytest]: https://pytest.org/
[pytest-django]: https://pytest-django.readthedocs.io/en/latest/
[Django Rest Framework]: http://django-rest-framework.org/
[drf-yasg]: https://drf-yasg.readthedocs.io/en/stable/
[django-extensions]: https://django-extensions.readthedocs.io/en/latest/
[django-debug-toolbar]: https://django-debug-toolbar.readthedocs.io/en/stable/
[factory-boy]: http://factoryboy.readthedocs.io/en/latest/
[faker]: https://faker.readthedocs.io/en/latest/index.html
[django-webtest]: https://pypi.python.org/pypi/django-webtest
[jupyter]: http://jupyter.org
[coverage]: https://coverage.readthedocs.io
[pylama]: https://pylama.readthedocs.io/en/latest/
[django-prometheus]: https://github.com/korfuri/django-prometheus
[black]: https://black.readthedocs.io/en/stable/
[django-cors-headers]: https://github.com/ottoyiu/django-cors-headers


Support this Project!
---------------------

This project is powered by Witold Greń. Please support as in their efforts to maintain and improve Django Template.


Usage
-----

Let's pretend you want to create a Django project called "redditclone". Rather 
than using `startproject` and then editing the results to include your name, 
email, and various configuration issues that always get forgotten until the 
worst possible moment, get [cookiecutter](https://github.com/audreyr/cookiecutter) to do all the work.

_Note that this is only example how django-template works. The complete guide you can find [here](docs/how-to-start-generating-project.md). 
Check out also [checklist](docs/start-project-checklist.md) before creating a new project using this template to follow all checkpoints needed_


First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter>=1.7.2"

Now run it against this repo::

    $ cookiecutter git@github.com:witold-gren/django-template.git
    or
    $ cookiecutter https://github.com/witold-gren/django-template


You'll be prompted for some values. Provide them, then a Django project will 
be created for you.

**Warning**: After this point, change 'Project Name', 'you@example.com', etc 
to your own information.

Answer the prompts with your own desired [options](https://github.com/witold-gren/django-template/blob/master/docs/project-generation-options.md). For example::

    Cloning into 'django-template'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [Project Name]: Reddit Clone
    project_slug [reddit_clone]: reddit
    author_name [Witold Greń]: My Team
    email [witold.gren@gmail.com]: my-team@example.com
    description [A short description of the project.]: A reddit clone.
    domain_name [reddit.example.com]: my-team.example.com
    slack_channel [reddit]: y
    use_celery: y
    version [0.1.0]: 0.0.1
    use_pycharm [n]: y
    windows [n]: n
    Select postgresql_version:
    1 - 11.6
    2 - 10.11
    3 - 9.6
    4 - "No database"
    Choose from 1, 2, 3, 4 [1]: 1
    Select python_version:
    1 - 3.7-slim
    2 - 3.7-alpine
    Choose from 1, 2 [1]: 2
    Select django_version:
    1 - 2.2
    Choose from 1 [1]: 1
    Select open_source_license:
    1 - Not open source
    2 - Apache Software License 2.0
    3 - GPLv3
    4 - BSD
    5 - MIT
    Choose from 1, 2, 3, 4, 5 [1]: 1


How to add project to repository
--------------------------------

### Warning

To enable easy template update in the future, there has to be craeted seperate branch called `cookiecutter` containing only the skeleton of template (generated via cookiecutter). In order to keep future merges clean there cannot be any changes done in this branch and it cannot be deleted. After and only after merging this branch to master branch you can edit/delete files generated by cookiecutter.

Enter the project and take a look around::

    $ cd reddit/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git checkout -b cookiecutter
    $ git add .
    $ git commit -m "initial project"
    $ git checkout -b master
    $ git merge cookiecutter
    $ git remote add origin git@github.com:witold-gren/reddit.git
    $ git push -u origin cookiecutter
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated 
README. Awesome, right?

For local development, see the following:

* [Developing locally using docker]

[Developing locally using docker]: https://github.com/witold-gren/django-template/blob/master/docs/developing-locally-docker.md


Installation and usage of pre-commit git hooks
----------------------------------------------

If you want to use in your project pre-commit hooks, e.g. for checking linters (like pylama) or code-formatting (like black), type in your project root:

    $ bin/install-git-hooks.sh
  
From now on, after you type ``git commit`` command, the pre-commit hooks will be executed first, checking or reformatting your code (depending on which hooks you are using), also commit won't succeed without all hooks passing.

Hooks scripts are localized in git-hooks directory in the root of the generated project. You can easily expand it with your own hooks by adding new .sh files into this folder.


How to update project
---------------------

Change branch to cookiecutter
    
    $ git checkout cookiecutter
    
Go to outside on your project
    
    $ cd ..
    
Generate project in cookiecutter branch
    
    $ cookiecutter --overwrite-if-exists --config-file=reddit/.cookiecutterrc git@github.com:witold-gren/django-template.git
    or
    $ cookiecutter --overwrite-if-exists --config-file=reddit/.cookiecutterrc https://github.com/witold-gren/django-template
    
Now you must add changes and new file, eg. `git add FILE_NAME`
    
    $ git add -u 

Check changes and commit

    $ git status
    $ git commit -m "update project template"
    
Then change branch to master
    
    $ git checkout master
    
And merge from cookiecutter branch with updated of new template
    
    $ git merge cookiecutter

The last but not least is you must solving all conflict by hand and update remote repository.
    
    $ git push -u origin cookiecutter
    $ git push -u origin master


Community
---------

* If you think you found a bug or want to request a feature, first contact 
with us in slack channel and then wy decide whether to open an [issue].

[issue]: https://github.com/witold-gren/django-template/issues


"Your Stuff"
------------

Scattered throughout the Python and HTML of this project are places marked with 
"your stuff". This is where third-party libraries are to be integrated with your 
project.


Releases
--------

Need a stable release? You can find them at https://github.com/witold-gren/django-template/releases


Running template tests
----------------------
The template is tested by building a representative subset of possible configurations and
running tests on each of them. This process can take a while, so after doing some basic tests,
you might want to submit a PR and let the CI take care of it.

The tests use Pytest and can be found in the [tests](tests) folder. The full suite
can be run locally simply by running `pytest` in the root template folder. If you're
feeling adventurous, `pytest-xdist` can be used to run the tests in parallel by
passing a `-n <number_of_jobs>` command-line option.

#### Generating test configurations
If you want to use your own instrumentation to parallelize the test runner, or simply
want to test a particular configuration individually, the [tests](tests) folder contains
a configuration generation script: [generate.configurations.py](tests/generate_configurations.py).
This will generate configuration files in json form in the target folder, which can be
tested by running `pytest --config-file <path_to_config_file>`.


Articles
---------

* [Development and Deployment of Cookiecutter-Django on Fedora] - Jan. 18, 2016
* [Development and Deployment of Cookiecutter-Django via Docker] - Dec. 29, 2015
* [How to create a Django Application using Cookiecutter and Django 1.8] - Sept. 12, 2015
* [Introduction to Cookiecutter-Django] - Feb. 19, 2016
* [Django and GitLab - Running Continuous Integration and tests with your FREE account] - May. 11, 2016

[Development and Deployment of Cookiecutter-Django via Docker]: https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-via-docker/
[Development and Deployment of Cookiecutter-Django on Fedora]: https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-on-fedora/
[How to create a Django Application using Cookiecutter and Django 1.8]: https://www.swapps.io/blog/how-to-create-a-django-application-using-cookiecutter-and-django-1-8/
[Introduction to Cookiecutter-Django]: http://krzysztofzuraw.com/blog/2016/django-cookiecutter.html
[Django and GitLab - Running Continuous Integration and tests with your FREE account]: http://dezoito.github.io/2016/05/11/django-gitlab-continuous-integration-phantomjs.html

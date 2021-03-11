Starting new project checklist
=========================

The complete documentation about this project you will find [here](https://github.com/witold-gren/django-template). You can also check out the guide [how to start generating project](how-to-start-generating-project.md).
This is only the checklist to go through when you want to start new project. If you will encounter a problem during those steps please check out the documentation.

**To start new project with this template you will need set up and do certain things:**

- [Install virtualenv and get Cookiecutter](how-to-start-generating-project.md#instructions). If you already did this before you can skip this step;
- [Run Cookiecutter against this repo](how-to-start-generating-project.md#generate-project);

- [Add to git repository](https://github.com/witold-gren/django-template#how-to-add-project-to-repository) (make sure that repo already exists);


**To run it locally with Docker:**
	
- If you are Linux user please see [this additional step](developing-locally-docker.md#a-note-for-linux-users) to avoid problem with permissions;

- Run `$ docker-compose build` in the root of your project;

- [Lock dependencies after first build](../{{cookiecutter.project_slug}}#dependency-management)

- Run `$ docker-compose up -d` to brings up Django app;

- Run `$ docker-compose logs -f $SERVICE_NAME` to follow logs for particular service

- Run `$ docker-compose run --rm app python manage.py migrate`;

- Run `$ docker-compose run --rm app python manage.py createsuperuser` to create superuser;

For this moment your project should be ready to use locally.

**Optional steps:**
- [Installation pre-commit git hooks](https://github.com/witold-gren/django-template#installation-and-usage-of-pre-commit-git-hooks)

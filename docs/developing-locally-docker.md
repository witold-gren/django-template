Getting Up and Running Locally With Docker
==========================================

The steps below will get you up and running with a local development environment.
All of these commands assume you are in the root of your generated project.


Prerequisites
-------------

You'll need at least Docker 1.10.

If you don't already have it installed, follow the instructions for your OS:

 - On Mac OS X, you'll need [Docker for Mac](https://docs.docker.com/engine/installation/mac/)
 - On Windows, you'll need [Docker for Windows](https://docs.docker.com/engine/installation/windows/)
 - On Linux, you'll need [docker-engine](https://docs.docker.com/engine/installation/)


A note for Linux users
---------------

On Linux, Docker runs as a system daemon with root privileges, and can actively create
files inaccessible to the host user. If you'd like to avoid that, you'll need to create
an .env file with your UID - the containers started by docker-compose will create files 
owned by this UID. Run 
```bash
echo "UID=${UID}" > .env
```
to do so.

#### *IMPORTANT*: Don't run compose as root
Your Linux user won't have permission to use docker by default. This can be fixed by
adding them to the `docker` group, as explained in the [official docs](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

Running docker and compose commands with `sudo` will break the setup in this template
and re-introduce file permission problems we've worked hard to avoid. Please don't.

Build the Stack
---------------

This can take a while, especially the first time you run this particular command
on your development system:

    $ docker-compose build

If you want to build the production environment you use `docker-compose.prod.yml` 
as -f argument (`docker-compose.yml` or `docker-compose.yaml` are the defaults).


Boot the System
---------------

This brings up both Django and PostgreSQL. The first time it is run it might 
take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker-compose up

To run in a detached (background) mode, just:

    $ docker-compose up -d


Running management commands
---------------------------

As with any shell command that we wish to run in our container, this is done
using the `docker-compose run` command.

To migrate your app and to create a superuser, run:

    $ docker-compose run --rm app python manage.py migrate
    $ docker-compose run --rm app python manage.py createsuperuser

Here we specify the `django` container as the location to run our management commands.

Running commands as root in the app container
---------------------------------------------
The Django application container runs everything as the `django` user created 
specifically for this purpose. This user doesn't have root permissions, and can't
install new packages, among other limitations. If you need to run commands as root in
this container, use docker-compose's `-u` option.

For example, to drop into a root shell inside the container, you'd run:
```bash
docker-compose run --rm -u 0 app sh
```

Add your Docker development server IP
-------------------------------------

For Docker, in the `config.settings.local`, add your host development 
server IP to `INTERNAL_IPS` or `ALLOWED_HOSTS` if the variable exists.

Production Mode
---------------

You would use `docker-compose build -f docker-compose.prod.yml`.


Tips & Tricks
-------------

### Debugging

#### pudb

If you are using the following within your code to debug:

    import pudb; pu.db

Then you may need to run the following for it to work as desired:

    $ docker-compose run --rm --service-ports app

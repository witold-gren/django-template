PostgreSQL Backups with Docker
==============================

For brevity it is assumed that will be running the below commands against local 
environment, however, this is by no means mandatory so feel free switching to 
``production.yml`` when needed.

Note that the application stack should not necessarily be running when applying 
any of the instructions below, unless explicitly stated otherwise. For instance, 
suppose the stack has been down for quite some time or have never even been up 
yet -- rather than starting it beforehand use a single 
``$ docker-compose run --rm <command>`` with the desired command. 
By contrast, should you already have your application up and running do not 
bother waiting for ``run`` instruction to finish (they usually take a bit 
longer due to bootstrapping phase), just use ``$ docker-compose exec <command>`` 
instead; note that any ``exec`` command fails unless all of the required 
containers are running. From now on, we will be using ``run``-style examples 
for general-case compatibility.

Before starting work with data base please run containers in background:

    $ docker-compose up -d

Creating a Backup
-----------------

To create a backup, run::
    
    $ docker-compose exec db bash
    $ pg_dump -o -O -U backend backend -h 127.0.0.1 -p 5432 --disable-dollar-quoting > /var/lib/postgresql/data/backup_`date '+%Y_%m_%d_%H_%M_%S'`.sql

or the second way::

    $ docker-compose run --rm db pg_dump -o -O -U backend backend -h 127.0.0.1 -p 5432 --disable-dollar-quoting > backup_`date '+%Y_%m_%d_%H_%M_%S'`.sql


Viewing the Existing Backups
----------------------------

To list existing backups, ::

    $ docker-compose run --rm db ls -l /var/lib/postgresql/data/ | grep backup_

These are the sample contents ::

    -rw-r--r--    1 root     root         10428 Mar 27 21:47 backup_2018_03_27_21_47_17.sql

or if you usaged second way, show all sql files in local folder:

    $ pwd
    /Users/XXX/my_project

    $ ls -l /Users/XXX/my_project | grep backup_
    -rw-r--r--   1 witoldgren  staff   208 Mar 27 23:51 backup_2018_03_27_23_51_03.sql
    

Copying Backups Locally
-----------------------

If you want to copy backups from your ``postgres`` container locally, 
``docker cp`` command_ will help you on that.

For example, given ``9c5c3f055843`` is the container ID copying all the backups 
over to a local directory is as simple as ::

    $ docker cp 9c5c3f055843:/var/lib/postgresql/data/backup_* ./backups

With a single backup file copied to ``.`` that would be ::

    $ docker cp 9c5c3f055843:/var/lib/postgresql/data/backup_2018_03_13T09_05_07.sql .

[command](https://docs.docker.com/engine/reference/commandline/cp/)


Restoring from the Existing Backup
----------------------------------

To restore from one of the backups you have already got (take the 
``backup_2018_03_13T09_05_07.sql`` for example), ::

    $ docker-compose exec db bash
    $ psql -h 127.0.0.1 -p 5432 -U backend backend -f /var/lib/postgresql/data/backup_2018_03_13T09_05_07.sql

You will see something like ::

    SET
    SET
    SET
    SET
    SET
     set_config
    ------------

    (1 row)

    SET
    # ...
    ALTER TABLE
    SUCCESS: The 'backend' database has been restored from the '/var/lib/postgresql/data/backup_2018_03_13T09_05_07.sql' backup.


Warning: This not create new database, they only backup and restore exist db.

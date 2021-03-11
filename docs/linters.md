Linters
=======

pylama
------

Code audit tool for Python. Pylama wraps these tools:

- **pycodestyle** (formerly pep8) © 2012-2013, Florent Xicluna;
- **pydocstyle** (formerly pep257 by Vladimir Keleshev) © 2014, Amir Rachum;
- **PyFlakes** © 2005-2013, Kevin Watters;
- **Pylint** © 2013, Logilab (should be installed ‘pylama_pylint’ module);
- **Radon** © Michele Lacchia

To run pylama with default linters `pycodestyle`, `pyflakes`, `radon`:

    $ pylama

Recursive check a path:

    $ pylama <path_to_directory_or_file>
    
Ignore errors:

    $ pylama -i W,E501

Choose code checkers

    $ pylama -l pylint,pep8,pycodestyle,mccabe


Skip lines (noqa)
-----------------

Just add # noqa in end of line to ignore.

    def urgent_fuction():
        unused_var = 'No errors here' # noqa


pyflakes
--------

The config for pyflakes is located in setup.cfg. It specifies:

* Set max line length to 120 chars 
* Exclude ``.git,manage.py,config/*,*/migrations/*,*/shared/*,*/tests/*``


pylint
------

The config for pylint is located in setup.cfg. It specifies:

* Use the pylint_django plugins. If using Celery, also use pylint_celery.
* Set max line length to 120 chars
* max-parents=13
* set rcfile to `.pylintrc`
* Disable linting:
    `C0111`: Missing %s docstring
    `C0103`: Invalid name "%s" (should match %s)
    `E1101`: %s %r has no %r member
    `R0901`: Too many ancestors (%s/%s)
    `R0902`: Too many instance attributes (%s/%s)
    `R0903`: Too few public methods (%s/%s)
    `R0904`: Too many public methods (%s/%s)
    `R0913`: Too many arguments (%s/%s)
    `R0915`: Too many statements (%s/%s)
    `W0141`: Used builtin function %r
    `W0142`: Used * or ** magic
    `W0221`: Arguments number differs from %s method
    `W0232`: Class has no __init__ method
    `W0613`: Unused argument %r
    `W0631`: Using possibly undefined loop variable %r


pycodestyle
-----------

The config for pycodestyle is located in setup.cfg. It specifies:

* Set max line length to 120 chars
* Exclude ``.git,manage.py,config/*,*/migrations/*,*/shared/*,*/tests/*``
* Ignore: do not assign a lambda expression, use a def


pydocstyle
----------

The config for pydocstyle is located in setup.cfg. It specifies:

* Ignore: Missing docstring in public module, Missing docstring in public class
* Exclude ``.git,manage.py,config/*,*/migrations/*,*/shared/*,*/tests/*``


radon
-----

Cyclomatic Complexity:

| CC score	| Rank	| Risk                                      |
|-----------|-------|-------------------------------------------|
| 1 - 5	    | A	    | low - simple block                        |
| 6 - 10	| B	    | low - well structured and stable block    |
| 11 - 20	| C	    | moderate - slightly complex block         |
| 21 - 30	| D	    | more than moderate - more complex block   |
| 31 - 40	| E	    | high - complex block, alarming            |
| 41+	    | F	    | very high - error-prone, unstable block   |

| Block type  | Letter  |
|-------------|---------|
| Function    | F       |
| Method      | M       |
| Class       | C       |


Maintainability Index:

| MI score	| Rank	| Maintainability   |
|-----------|-------|-------------------|
| 100 - 20	| A	    | Very high         |
| 19 - 10	| B	    | Medium            |
| 9 - 0	    | C	    | Extremely low     |


Raw Metrics:

`LOC`: The total number of lines of code. It does not necessarily correspond to the number of lines in the file.
`LLOC`: The number of logical lines of code. Every logical line of code contains exactly one statement.
`SLOC`: The number of source lines of code - not necessarily corresponding to the LLOC.
`Comments`: The number of comment lines. Multi-line strings are not counted as comment since, to the Python interpreter, they are just strings.
`Multi`: The number of lines which represent multi-line strings.
`Blanks`: The number of blank lines (or whitespace-only ones).

The equation SLOC + Multi + Single comments + Blank = LOC should always hold. Additionally, comment stats are calculated:

`C % L`: the ratio between number of comment lines and LOC, expressed as a percentage;
`C % S`: the ratio between number of comment lines and SLOC, expressed as a percentage;
`C + M % L`: the ratio between number of comment and multiline strings lines and LOC, expressed as a percentage.

isort
-----

A Python utility to sort imports.

The config for isort is located in `setup.cfg`. It specifies:

+ mode for multi line imports
+ lines between imports sections and types
+ imports type and sections ordering

To run `isort` recursively from your current directory type following command:

```bash
isort -rc .
```

This command will modify any files that don’t conform to the guidelines.
If you need to have imports out of order
(to avoid a circular import, for example) use a comment like this:

```python
import module  # isort:skip
```

List of isort plugins for various editors are available at
[project wiki](https://github.com/timothycrosley/isort/wiki/isort-Plugins).

Provided config is based on [Django imports standards](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#imports).


Mypy
------
Mypy by default is turned off but we have prepared Mypy configuration ready to use (see [setup.cfg]({{cookiecutter.project_slug}}/backend/setup.cfg))

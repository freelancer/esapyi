l# Python 3.7 API boilerplate
<div align="center"><strong><em>
A dockerized and production ready python API template with no setup required.
</em></strong></div>

TODO some description high level overview of the project

| Table of Contents                                                                           |
| ------------------------------------------------------------------------------------------- |
| [Quickstart Guide](#Quickstart-guide)                                                       |
| [The Hitchhicker's Guide to `api_boilerplate`](#The-Hitchhickers-Guide-to-api_boilerplate) |
| [Developer Guide](#Developer-Guide)                                                         |

## Quickstart guide

1. Ensure that you have [docker](https://docs.docker.com/install/) installed on your system.
2. Clone this repository using `git clone https://github.com/AdiRishi/api_boilerplate.git`
3. (Optional) Pick a new name for your project and run `./rename_project.sh "my_project_name"`
4. Start the python server using `./run.sh dev`

## The Hitchhicker's Guide to `api_boilerplate`
TODO

## Developer Guide
This section goes through the various tools procedures a developer would need when developing using this setup.

**Contents**
- [Commands Quickstart](#Commands): Getting the most out of the utility scripts
- [Linting](#Linting): The linter setup and now to customize it
- [Testing](#Testing): Getting the most out of the test setup
- [Database Migrations](#Database-Migrations): How to track and alter the database schema
- [Python Servers](#Python-Servers): Understanding flask and uWSGI
- [Production Deployment](#Production-Deployment): The idea way of running the production server

### Commands Quickstart
All of the common development tasks that need to be performed are done through the `run.sh` script located at the root of the project.
`run.sh` has the following commands
- `run.sh dev` - start the local db and python development server at port *8080*
- `run.sh prod` - start the local db and the production [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) python server at port *8080*
- `run.sh lint` - lint the entire project
- `run.sh test` - run the entire test suite for the project
- `run.sh check` - run the *lint* and *test* command in suceession
- `run.sh dev db` - spin up and connect to the local dev database
- `run.sh alembic` - proxy to the [alembic](https://alembic.sqlalchemy.org) cli

### Linting
This project uses 2 main linting programs
- [mypy](http://www.mypy-lang.org/) - a static typechecker
- [pylint](https://www.pylint.org/) - a code quality checker

If you want to customize the lint configuration, modify the following files
- [mypy.ini](mypy.ini) - to customize the mypy setup
- [pylintrc](pylintrc) - to cuztomize the pylint setup

Also note that by default *pylint* is configured to run using all available CPU cores. To change this modify the `-j` cli option in this [Dockerfile](/lib/docker/lint/pylint/Dockerfile)

### Testing
This project uses the [pytest](https://docs.pytest.org/en/latest/) framework for writing and maintaining unit tests.
- In order to configure pytest, use the [pytest.ini](pytest.ini) file

The unit tests also spin up a dockerized MySQL database. Every `run.sh test` call will kill and re-create the database to ensure tests are running in a fresh environment.

There are 3 base test classes which you should extend when writing tests.
* [BaseTestCase](tests/conftest.py#L10)
    * An empty class that extends [unittest.TestCase](https://docs.python.org/3/library/unittest.html#unittest.TestCase)
* [AppContextTestCase](tests/conftest.py#L14)
    * A class makes a [flask test client](https://flask.palletsprojects.com/en/1.0.x/testing/#the-testing-skeleton) avilable at `self.client`
* [DbContextTestCase](tests/conftest.py#L22)
    * Waits for the database to become available if it's not
    * Re-sets the database after every test using [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#downgrading).

### Database Migrations
- what this section is about
- alembic and what it is
- simple commands for creating new migrations (autorevision)
- interaction with the local dev db

This project uses [alembic](https://alembic.sqlalchemy.org/en/latest/) as a database migrations tool. This tool essentially acts as a verison control for your database schema. Any changes that need to be made should be tracked and done through alembic.

**Example: Adding a new column**

Say we want to add a new column to our users table - `first_name`.
<br/>To do so, follow these steps

1. Add modify the [user model](api_boilerplate/models/user.py) and add the first_name column
```python
first_name = Column(Text, nullable=False)
```
2. Run the alembic command to [autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) a revision
    * This command creates a new file under the migrations/versions which contains code to create this new column in the db
```bash
./run.sh alembic revision --autogenerate -m"add_fname_to_user"
```
3. Run the alembic command to upgrade the database
```bash
./run.sh alembic upgrade head
```
4. That's it! The user table in the local database now has a first_name column. Remember to commit the generated migration file to git.

### Python Servers
- local development uses flask
- flask is multi-threaded
- prod uses uwsgi (allows for load balancing and mass multi-threading)

### Production Deployment
- the prod dockerfile
- uwsgi and changing the config
# Corvid ![Build Status](https://travis-ci.org/jpcjr/corvid.svg?branch=master)

User-friendly static site generation as a service. Powered by [Pelican](http://blog.getpelican.com/).

# Installation

## Postgresql
- Use your package manager. Be sure to get development headers.
  + On Ubuntu, run `sudo apt-get install postgresql-9.4 postgresql-server-dev-9.4`
- The settings given in the repo are expecting a role named `corvid` that owns
  a database with the same name. To set this up, enter the Postgres REPL with
  `sudo -u postgres psql` and enter the following commands:
- When doing development, you need `CREATEDB` to run tests, but during deploy we
  will shut that off.

```sql
    CREATE ROLE corvid PASSWORD '<password>' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN;
    CREATE DATABASE corvid OWNER corvid;
```

- Edit `postgresql.conf` (found on Ubuntu under `/etc/postgresql/9.4/main/postgresql.conf`),
  and uncomment the line: `listen_addresses = 'localhost'`. Now you will only be
  able to access Postgres from your machine. (Better for development, but you
  will not want this for deployment.)

## Python
### VirtualEnv
- install virtualenv
- create virtualenv under project root: `virtualenv -p python3 venv`
- activate: `. venv/bin/activate`
- (when done, deactivate with `deactivate`)

### Packages
- With virtualenv active, install required packages:
  `pip install -r requirements.txt`
- This may fail due to lack of development headers when installing native
  extensions (particularly psycopg2 and lxml).  So then you'll probably want
  `sudo apt-get install python3-dev libxml2-dev`.

# Development

- To populate the database:
  - The basics (**you must do this**) `python manage.py populate`
  - Taylor swift user/project (good for demo) `python manage.py tswizzle`
- To launch the test server: `make run`
- To run tests: `make test`

# Themes

To get themes added to the database (you should have gotten everything prior to
this done):

```bash
git submodule init
git submodule update
# wait a little while
cd pelican-themes
git submodule init
git submodule update
# wait a lot longer
cd ../corvid
```

# Deployment
WIP. Something using the fabfile.

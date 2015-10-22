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
    CREATE DATABASE test_corvid OWNER corvid;  -- only if you're testing
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

# Development
- To set up the database: `python manage.py migrate`
- To launch the test server: `python manage.py runserver`

# Deployment
WIP. Something using the fabfile.

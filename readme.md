# Corvid

User-friendly static site generation as a service. Powered by [Pelican](http://blog.getpelican.com/).

# Installation

## Postgresql
- Use your package manager. Be sure to get development headers.
  + On Ubuntu, run `sudo apt-get install postgresql-9.4 postgresql-server-dev-9.4`
- In the `psql` shell, run:
  TODO

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
WIP. Something using manage.py

# Deployment
WIP. Something using the fabfile.
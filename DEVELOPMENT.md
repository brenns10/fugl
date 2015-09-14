# Development

## Prerequisites

To do development (and testing) on your computer, you need the following:

- Linux/Unix.  Since the website is being hosted on a Ubuntu server, Ubuntu would probably be the way to go.
- Python 2.  I believe this is the default still in Ubuntu.  (`sudo apt-get install python`)
- Python Virtualenv.  All extensions should be installed in a virtualenv (described below) (`sudo apt-get install 
  python-virtualenv`).
- A Bitbucket account, which you should already have if you see this repository.
- Mercurial, which you should probably also have (`sudo apt-get install mercurial`).

## Setup Environment

1. In the directory you want to put the code, clone the repository (`hg clone https://bitbucket.org/cwru-hkn/hkn-site`).  
   It will prompt you for your Bitbucket username and password.  You can, of course, use SSH instead.
2. Change into the repository root directory (`cd hkn-site`).
3. Create a virtualenv (`virtualenv venv`).  Activate it (`source venv/bin/activate`).
4. Install the Python library requirements (`pip install -r requirements.txt`).  Psycopg2 is not necessary for 
   development, so if you have trouble installing, ignore it.
5. Create a symlink so that hkn_site/settings.py can find the development settings: `ln -s hkn_site/settings_dev.py 
   hkn_site/settings_local.py`.
6. Tell Django to sync the database (`./manage.py syncdb`).
7. Run the development server (`./manage.py runserver`).
8. Point your browser at http://localhost:8000 and have fun.

I'll have to grant permissions to make changes to the repository, so get in contact with me (Stephen) if you intend 
to submit changes.
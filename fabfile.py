#-------------------------------------------------------------------------------
#
# File:         fabfile.py
#
# Author:       Stephen Brennan
#
# Date Created: Friday, 10 October 2014
#
# Description:  Fabric File: Deploys website to server!
#
#-------------------------------------------------------------------------------

from datetime import datetime
from os import listdir
from os.path import join

from fabric.api import *
from fabric.contrib.console import confirm

# Use connection parameters from your ssh config!
env.use_ssh_config = True

# Locations for various things on the server.
params = {
    'hostname': 'hkn.case.edu',

    'static_dir': '/srv/www/static',
    'media_dir': '/srv/www/media',
    'virtualenv': '/home/django/venv',
    'sock_name': '/var/run/uwsgi/app/hkn/socket',
    'app_dir_container': '/home/django/hkn-site',

    'secrets': '/home/django/secrets',
    'ssl_cert': '/etc/nginx/ssl/server.crt',
    'ssl_key': '/etc/nginx/ssl/server.key',

    'pkg_ext': '.tar.gz',
}

# The secret files that need to be at the root of the django app.
secret_files = ['email_key.txt', 'db_key.txt', 'secret_key.txt']

# List of required packages from apt.
packages = [
    'python', 'python-pip', 'python-virtualenv',
    'nginx',
    'uwsgi', 'uwsgi-plugin-python',
    'postgresql', 'libpq-dev', 'python-dev',
    'git',
]


def _get_pkg_name():
    """Return a timestamp to the second for package naming."""
    return datetime.now().strftime('%Y-%m-%d_%H.%M.%S')


def _render(source, target, context):
    """
    Render a file using Python's (%) string formatting operator and a context.

    This is used to put correct locations into configuration files.
    Parameters:
    - source: Filename to read the template from.
    - target: Filename to write the rendered template.
    - context: Object to provide the formatter.
    """
    with open(source, 'r') as f:
        text = f.read()
    text = text % context
    with open(target, 'w') as f:
        f.write(text)


def render_config(pkg_name):
    """
    Create a 'config' directory and render all the 'conf' files into it.

    Takes the pkg_name so that it can add that to the context (some config files 
    need to know the app location).
    """
    local('mkdir config')

    context = {}
    context.update(params)
    context['app_dir'] = join(context['app_dir_container'], pkg_name)

    for conf_fname in listdir('conf'):
        _render(join('conf', conf_fname), join('config', conf_fname), context)


def delete_config():
    """
    Remove the rendered config file temp directory.
    """
    local('rm -rf config')


def package():
    """
    Package up necessary files into a neat little tarball.

    'Necessary files' are all HG tracked files, with the following exceptions:
    - .hgignore: No need for that if there's no HG repository.
    - conf/ directory: All tracked files in conf/ will have been rendered to
      the config directory.  So files from config/ will be packaged instead.
    """
    # Come up with a name for the package.
    pkg_name = _get_pkg_name()
    pkg_file = pkg_name + params['pkg_ext']

    # Render the config files.
    render_config(pkg_name)

    # hg locate: list all tracked files
    # grep ... : eliminate .hgignore from the list
    # sed ...  : replace conf/ with config/
    # xargs ...: provide each line in stdin as a param to 'tar czf'
    local('hg locate | '
          'grep -v "^\.hgignore/$" | '
          'sed "s/conf\//config\//g" | '
          'xargs -d "\n" tar czf %s'
          % pkg_file)

    # Remove the rendered config files.
    delete_config()

    # Return the name (timestamp, not the filename).
    return pkg_name


def send_package(pkg_name):
    """Send the package and extract it.  Symlink the secrets."""
    # Create the destination directory, and put the archive into it.
    filename = pkg_name + params['pkg_ext']
    dest_dir = join(params['app_dir_container'], pkg_name)
    sudo('mkdir -p ' + dest_dir, user='django')
    put(filename, join(params['app_dir_container'], pkg_name, filename),
        use_sudo=True)

    with cd(dest_dir):
        # Extract the archive.
        sudo('tar xzfm ' + filename, user='django')

        # Symlink each 'secret file' to its real location.
        for name in secret_files:
            sudo('ln -s %s %s' % (join(params['secrets'], name), name),
                 user='django')


def _symlinks(link_dict):
    """
    Create symlinks from a dict.

    Creates a link with name <key> pointing to <value>.  If a file exists at
    <key>, deletes it first.
    """

    for link_name, link_target in link_dict.iteritems():

        sudo('rm -f %s' % link_name)
        sudo('ln -s %s %s' % (link_target, link_name))


def activate_version(pkg_name, syncdb=False):
    """
    Activate a particular timestamped version of the site on the server.

    This involves modifying the links to some config files.  Then, need to pip
    install the requirements (in case they've changed).  Finally, collect the
    new static variables and synchronize the database (if requested).

    Parameters:
    - pkg_name: The name of the 'package' to activate.
    - syncdb: Whether or not to sync db after activating.
    """
    # Stop web and app server.
    sudo('service uwsgi stop')
    sudo('service nginx stop')


    appdir = join(params['app_dir_container'], pkg_name)
    venv_activate = join(params['virtualenv'], 'bin/activate')

    # Re-link the required config files.
    links = {
        '/etc/nginx/nginx.conf': join(appdir, 'config/hkn_nginx.conf'),
        '/etc/nginx/uwsgi_params': join(appdir, 'config/uwsgi_params'),
        '/etc/uwsgi/apps-enabled/hkn.ini': join(appdir, 'config/hkn_uwsgi.ini'),
    }
    _symlinks(links)

    with cd(appdir):

        # Install packages (in case there are new requirements).
        sudo('source %s && pip install -r requirements.txt' % venv_activate,
             user='django')

        # Collect static variables into the static dir.  Need to adjust owner so
        # that nginx/django can read/write.
        sudo('source %s && python manage.py collectstatic' % venv_activate)
        sudo('chown -R www-data /srv/www')

        # Synchronize the databases if requested.
        if syncdb:
            sudo('source %s && python manage.py syncdb' % venv_activate,
                 user='django')

    # Resume the servers with new configurations and things.
    sudo('service nginx start')
    sudo('service uwsgi start')


def deploy(syncdb=False):
    """
    Deploy the current project to the server.

    This process creates a package with the current version, sends it over, and
    activates it.
    Parameters:
    - syncdb: If we should run syncdb during activation.  (call fab deploy:True)
      from commandline if you want to do this.
    """
    # Check whether the repository is committed.  This is a friendly reminder --
    # you don't have to commit it to deploy it, but if it's uncommited, it
    # probably doesn't belong on the server.
    output = local('hg status', capture=True)
    if output != '' and not confirm('Local repository has uncommitted changes.'
                                    '  Continue?'):
        abort('Aborting at user request.')

    # Deploy!
    pkg_name = package()
    send_package(pkg_name)
    activate_version(pkg_name, syncdb)
    local('rm %s' % pkg_name + params['pkg_ext'])
    return pkg_name


def setup_new_server():
    """
    Setup a new HKN server from scratch!

    This task sets up a server exactly the way that it's "intended".  It
    installs all your necessary packages, sets up the correct users, creates
    your virtualenv, sends the secret files over, wires up SSL, creates a new
    database, and deploys the current version of the website (thus setting up
    the database schema).

    On the server side, this setup requires:
    - You have installed Ubuntu Server 14.04.
    - You have OpenSSH server installed and running, and you can connect.
    - You have configured SUDO to allow you to run anything and impersonate
      anyone without a password.  The line in sudoers would be:
          [username] ALL = (ALL) NOPASSWD: ALL
      Or something more complex, if you're familiar with sudoers.

    On the client side, this setup requires that you have a copy of
    'secrets.tar.gz', which contains the SSL certificates and some secret key
    values.  It's not kept in version control (obviously), and it can be deleted
    once the server is setup.
    """
    # Install packages
    sudo('echo Y | apt-get install ' + ' '.join(packages))

    # Add a django user
    sudo('adduser --disabled-password --gecos "" django')
    # Add some useful users to django group.
    sudo('usermod -aG django www-data')
    sudo('usermod -aG django postgres')

    # Create a virtualenv
    sudo('virtualenv %s' % params['virtualenv'], user='django')

    # Send secrets
    secfile = join(params['secrets'], 'secrets.tar.gz')
    sudo('mkdir -p ' + params['secrets'], user='django')
    put('secrets.tar.gz', secfile, use_sudo=True)
    sudo('mkdir -p /etc/nginx/ssl')
    cert = {
        '/etc/nginx/ssl/server.crt': join(params['secrets'], 'server.crt'),
        '/etc/nginx/ssl/server.key': join(params['secrets'], 'server.key'),
    }
    _symlinks(cert)
    with cd(params['secrets']):
        sudo('tar xvf secrets.tar.gz', user='django')
        sudo('chown django *')
        sudo('chgrp django *')
        sudo('chmod 440 *')

    # Add database user and database
    db_key = join(params['secrets'], 'db_key.txt')
    sudo('echo "CREATE USER django WITH PASSWORD \'`cat %s`\'" | psql' % db_key,
         user='postgres')
    sudo('createdb hkn_site -O django', user='postgres')
    # Swap the peer authentication for md5!
    sudo(r'sed -ibak -e "s/local\s\+all\s\+all\s\+peer/local all django md5/g"'
         ' /etc/postgresql/9.3/main/pg_hba.conf')
    sudo('service postgresql restart')

    # Deploy a version and sync database
    deploy(True)

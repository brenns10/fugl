# Production

## Deployment

Since we currently have a server set up with ACM, the most important thing to
have documented is how to deploy new versions of the site.  The site is deployed
using a Python tool called `fabric`.  This program and library manages running
commands and sending files on/to a remote machine over SSH.  It uses a 'fabfile'
(`fabfile.py`) to define tasks.  You can run a task with `fab [task-name]`, for
instance, `fab deploy`.

In fact, that is the very command you would use to deploy.  That will package up
the site and send it off to the server, where it will be unpacked, set up, and
fixed up over there.  If you deploy with uncommitted changes, you will get a
prompt about whether you're sure.  Feel free to ignore it and keep going --
committing isn't required.  It's just a friendly reminder.

If you need to set up a new server, that is why we have the other major fab
command: `fab setup_new_server`.  That's a ridiculously exciting command, but
for the gory details, check the docstring in the fabfile.  If you want to try it
out, the best way is in a VM.

NB: All the above `fab` commands are missing a directive, `-H [hostname]` to
specify the target.  Use a host that you have saved in `.ssh/config`.

## Server Details

### Environment

- OS: Ubuntu
- Web Server: Nginx (`sudo apt-get install nginx`)
- WSGI Server: uWSGI (`sudo apt-get install uwsgi uwsgi-plugin-python`)
- Database: PostgreSQL (`sudo apt-get install libpq-dev python-dev postgresql`)
- Python: Django, Django-CAS (requires `git`), Psycopg2

### Architecture

All of the code files are owned by the django user, in its home directory.  The
static files are served from `/srv/www/static`, and the media (PDFs) are from
`/srv/www/media`).  Configuration files for nginx and uWSGI are symlinked.
Secret files are symlinked as well, and located in `/home/django/secrets`.
Multiple versions of the app are stored (one for each deployment), all in
`/home/django/hkn-site`.

### Config Files

The configuration files are taken from the repository, have values plugged into
the template spots, and then sent to the server.  So, all the `%(...)s`'s were
there for a reason.

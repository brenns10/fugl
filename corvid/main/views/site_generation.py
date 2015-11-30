from django.views.generic.base import View
from django.utils.text import slugify
from django.template.response import TemplateResponse
from django.http import HttpResponse
from main.models import Project
from .protected_view import ProtectedViewMixin
from subprocess import Popen
from datetime import datetime
from collections import Counter
from pprint import pprint
import tempfile
import zipfile
import shlex
import os


class SiteGenerationView(ProtectedViewMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            return self._do_generate(request, args, kwargs)
        except Exception as e:
            pprint(e)
            ctx = {
                'message': "Actually, we derped. You can redeem this"
                           " page for a free hug from the Corvidae. Sorry :(",
                'link_url': '/project/{0}/{1}'.format(kwargs['owner'], kwargs['proj_title']),
                'link_text': 'Return to Project Home',
            }
            return TemplateResponse(request, 'error.html', context=ctx)

    def _do_generate(self, request, *args, **kwargs):
        project_title = request.resolver_match.kwargs['proj_title']
        project = Project.objects.get(owner=request.user, title=project_title)

        with tempfile.TemporaryDirectory() as site_dir:
            with open(os.path.join(site_dir, 'pelicanconf.py'), 'w') as f:
                f.write(project.get_pelican_conf())

            pagelike_counter = Counter()
            for page in project.page_set.all():
                page_dir = os.path.join(site_dir, 'content', 'pages')
                mkdirs(page_dir)

                filename = get_filename(page, pagelike_counter)
                page_file = os.path.join(page_dir, filename) + '.md'
                with open(page_file, 'w') as f:
                    f.write(page.get_markdown(slug=filename))

            for post in project.post_set.all():
                post_dir = os.path.join(site_dir, 'content', slugify(post.category.title))
                mkdirs(post_dir)

                filename = get_filename(post, pagelike_counter)
                post_file = os.path.join(post_dir, filename) + '.md'
                with open(post_file, 'w') as f:
                    f.write(post.get_markdown(slug=filename))

            # now that we've written out the file, call into pelican
            returncode = pelican_generate(site_dir, 'content', 'pelicanconf.py')
            if returncode != 0:
                raise RuntimeError('Pelican returned status: {0}'.format(returncode))

            # now zip the output (in RAM)...
            tempzipfile = tempfile.NamedTemporaryFile(delete=True)
            output_dir = os.path.join(site_dir, 'output')

            with zipfile.ZipFile(tempzipfile, 'w', zipfile.ZIP_DEFLATED) as arc:
                for dirpath, _, filenames in os.walk(output_dir):
                    for filename in filenames:
                        path = os.path.join(dirpath, filename)
                        arc_path = os.path.relpath(path, output_dir)
                        arc.write(path, arc_path)

            # load the zipfile's content into memory...
            with open(tempzipfile.name, 'rb') as f:
                content = f.read()
            tempzipfile.close()

            # ...and return the zipfile to the user
            filename = '{0}_output_{1}.zip'.format(project.title,
                                                   datetime.now().strftime('%Y-%m-%d_%H%M'))
            resp = HttpResponse(content, content_type='application/zip')
            resp['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
            resp['Content-Length'] = len(content)
            return resp


def get_filename(pagelike, pagelike_counter):
    """
    Return the filename for a Page/Post. Accomodates duplicates.
    """
    pagelike_filename = pagelike.filename
    while True:  # guaranteed to terminate for a finite number of pages
        pagelike_counter[pagelike_filename] += 1
        count = pagelike_counter[pagelike_filename]
        if count > 1:
            pagelike_filename += ('_%d' % (count,))
        else:
            break
    return pagelike_filename


def pelican_generate(site_dir, content_dir, settings_file, timeout=10):
    path_to_content = os.path.join(site_dir, content_dir)
    path_to_settings = os.path.join(site_dir, settings_file)
    cmd = ('pelican %(path_to_content)s -s %(path_to_settings)s' % {
        'path_to_content': path_to_content,
        'path_to_settings': path_to_settings,
    })
    p = Popen(shlex.split(cmd))
    p.wait(timeout=timeout)  # we don't have all day
    return p.returncode


def mkdirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        # if we fail, we don't care
        pass

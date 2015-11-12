"""
Tests for main.views.post classes: CreatePostView and UpdatePostView.

Tests:
CreatePostView:
- GET:
  - not logged in user redirected to login.
  - logged in user cannot access form to create a post for projects they don't
    own. (should 404)
  - logged in user can access form to create a post for projects they do own.
- POST:
  - not logged in user redirected to login
  - logged in user may not create post on project they don't own (should 404)
  - logged in user can create a post for project they do own (expected case)
- Invalid:
  - No such user GET/POST 404
  - No such project GET/POST 404
UpdatePostView:
- GET:
  - not logged in user redirected to login
  - logged in user cannot access post for project they don't own (should 404)
  - logged in user can access post for project they do own
    -> should return the post's existing content
- POST:
  - not logged in user redirected to login
  - logged in user cannot edit post for project they don't own (should 404)
  - logged in user can edit post contents
    - should be reflected in database
- Invalid:
  - No such user GET/POST 404
  - No such project GET/POST 404
  - No such post GET/POST 404
"""

from django.test import Client
from .base import CorvidTestCase
from main.models.post import Post
from main.models.user import User
from main.models.project import Project
from main.models.category import Category


class CreatePostViewTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()
        self.client = Client()
        self.otherpass = 'cock-of-the-rock'
        self.otheruser = User.objects.create_user('other_user',
                                                  'other@example.com',
                                                  self.otherpass)
        self.otheruser.save()
        self.project = Project.objects.create(
            title='testproj', description='test project', preview_url='',
            owner=self.admin_user, theme=self.default_theme
        )
        self.project.save()

        self.category = Category.objects.create(title='default',
                                                project=self.project)
        self.category.save()

    def tearDown(self):
        self.otheruser.delete()
        self.project.delete()
        super().tearDownTheme()

    def url_for(self, project):
        # return the new post url for a project
        return '/project/%s/%s/post/new' % (project.owner.username,
                                            project.title)

    def login_other(self):
        # login the client as "otheruser"
        self.client.login(username=self.otheruser.username,
                          password=self.otherpass)

    def test_get_not_logged_in_redirect(self):
        # When a not-logged-in user accesses the post, it should redirect.
        url = self.url_for(self.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_get_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_owner(self):
        # Should return the correct form when you own the project
        url = self.url_for(self.project)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add Post', response.content.decode('utf8'))

    def test_post_not_logged_in_redirect(self):
        url = self.url_for(self.project)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_post_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_owner(self):
        formdata = {'title':'testpost2', 'content': 'I am a test post.',
                    'category': self.category.id}
        url = self.url_for(self.project)
        self.login()
        response = self.client.post(url, formdata)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created!', response.content)

        # Also, there should be a corresponding post object in the DB.
        post_object = Post.objects.get(project=self.project,
                                       title=formdata['title'],
                                       category=self.category)
        self.assertEqual(post_object.content, formdata['content'])

        # Cleanup before the test is over.
        post_object.delete()

    def test_invalid_user(self):
        url = '/project/idontexist/ialsodontexist/post/new'
        self.login()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)

    def test_invalid_project(self):
        url = '/project/%s/ialsodontexist/post/new' % self.admin_user.username
        self.login()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)

"""
class UpdatePostViewTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()
        self.client = Client()
        self.otherpass = 'cock-of-the-rock'
        self.otheruser = User.objects.create_user('other_user',
                                                  'other@example.com',
                                                  self.otherpass)
        self.otheruser.save()
        self.project = Project.objects.create(
            title='testproj', description='test project', preview_url='',
            owner=self.admin_user, theme=self.default_theme
        )
        self.project.save()

        self.post = Post.objects.create(
            title='testpost1', content='test post 1', project=self.project)
        self.post.save()

    def tearDown(self):
        self.otheruser.delete()
        self.post.delete()
        self.project.delete()
        super().tearDownTheme()

    def url_for(self, post):
        # return the url for a project
        return '/project/%s/%s/post/edit/%s' % (post.project.owner.username,
                                                post.project.title,
                                                post.title)

    def login_other(self):
        # login the client as "otheruser"
        self.client.login(username=self.otheruser.username,
                          password=self.otherpass)

    def test_get_not_logged_in_redirect(self):
        # When a not-logged-in user accesses the post, it should redirect.
        url = self.url_for(self.post)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_get_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.post)
        self.login_other()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_owner(self):
        # Should return the correct form when you own the project
        url = self.url_for(self.post)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf8')
        self.assertIn('Edit Post', content)
        self.assertIn(self.post.content, content)
        self.assertIn(self.post.title, content)

    def test_post_not_logged_in_redirect(self):
        url = self.url_for(self.post)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_post_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.post)
        self.login_other()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_owner(self):
        # Data we will send in the form
        newdata = {
            'title': self.post.title,
            'content': 'new content',
        }

        # Post to the form.
        self.login()
        url = self.url_for(self.post)
        response = self.client.post(url, newdata)

        # Assert that it redirects to the project home.
        self.assertEqual(response.status_code, 302)
        redir_url = '/project/%s/%s'  % (self.admin_user.username,
                                         self.project.title)
        redir_url = 'http://testserver' + redir_url
        self.assertIn(redir_url, response.url)

        # Assert that the change happened.
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, newdata['content'])

    def test_invalid_user(self):
        url = '/project/idontexist/ialsodontexist/post/edit/meneither'
        self.login()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)

    def test_invalid_project(self):
        url = '/project/%s/ialsodontexist/post/edit/meneither' % self.admin_user.username
        self.login()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)

    def test_invalid_post(self):
        url = '/project/%s/%s/post/edit/meneither' % (self.admin_user.username,
                                                      self.project.title)
        self.login()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)
"""

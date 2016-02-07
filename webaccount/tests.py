from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client

from webaccount.views import AccountAuthView, AccountEditView
from website.views import index_page


class AccountPageTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.email = 'test@user.net'
        self.username = 'test'
        self.password = 'top_secret'
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password)

    def test_login_url_without_auth_user(self):
        request = self.factory.get('/accounts/login/')
        request.user = AnonymousUser()
        response = AccountAuthView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_url_with_auth_user(self):
        request = self.factory.get('/accounts/login/')
        request.user = self.user
        response = AccountAuthView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_login_button_without_auth_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index_page(request)

        self.assertContains(response, 'Логин/Регистрация')
        self.assertContains(response, 'href="/accounts/login/"')

    def test_login_button_with_auth_user(self):
        request = self.factory.get('/')
        request.user = self.user
        response = index_page(request)

        self.assertContains(response, 'Здравствуйте, test')
        self.assertContains(response, 'href="/accounts/profile/"')

    def test_login_user(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'login-username': 'test@user.net',
            'login-password': 'top_secret',
            'login_submit': 'Log in',
        })

        self.assertEqual(response.status_code, 302)
        # print(response.wsgi_request.__dict__)
        self.assertEqual(response.wsgi_request.user, User.objects.get(username='test'))

    def test_login_user_with_bad_password(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'login-username': 'test@user.net',
            'login-password': 'badpassword',
            'login_submit': 'Log in',
        })

        self.assertEqual(response.status_code, 200)
        # print(response.wsgi_request.__dict__)
        self.assertNotEqual(response.wsgi_request.user, User.objects.get(username='test'))
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.')

    def test_login_user_required_fields(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'login-username': '',
            'login-password': 'top_secret',
            'login_submit': 'Log in',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обязательное поле.')

        response = c.post('/accounts/login/', data={
            'login-username': 'test@user.net',
            'login-password': '',
            'login_submit': 'Log in',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обязательное поле.')

    def test_registration_user(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'registration-email': 'new@user.name',
            'registration-username': 'newuser',
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': 'Register',
        })

        self.assertEqual(response.status_code, 302)
        # print(response.wsgi_request.__dict__)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.wsgi_request.user, User.objects.get(username='newuser'))

    def test_registration_user_different_password(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'registration-email': 'new@user.name',
            'registration-username': 'newuser',
            'registration-password1': 'supersecret',
            'registration-password2': 'extrasecret',
            'registration_submit': 'Register',
        })

        self.assertEqual(response.status_code, 200)
        # print(response.wsgi_request.__dict__)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.wsgi_request.user, AnonymousUser())
        self.assertContains(response, 'Два поля с паролями не совпадают.')

    def test_registration_user_required_fields(self):
        c = Client()
        response = c.post('/accounts/login/', data={
            'registration-email': '',
            'registration-username': 'newuser',
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': 'Register',
        })

        self.assertContains(response, 'Обязательное поле.')

        response = c.post('/accounts/login/', data={
            'registration-email': 'new@user.name',
            'registration-username': '',
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': 'Register',
        })

        self.assertContains(response, 'Обязательное поле.')

        response = c.post('/accounts/login/', data={
            'registration-email': 'new@user.name',
            'registration-username': 'newuser',
            'registration-password1': '',
            'registration-password2': 'secret',
            'registration_submit': 'Register',
        })

        self.assertContains(response, 'Обязательное поле.')

        response = c.post('/accounts/login/', data={
            'registration-email': 'new@user.name',
            'registration-username': 'newuser',
            'registration-password1': 'secret',
            'registration-password2': '',
            'registration_submit': 'Register',
        })

        self.assertContains(response, 'Обязательное поле.')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.wsgi_request.user, AnonymousUser())

    def test_profile_url_without_auth_user(self):
        request = self.factory.get('/accounts/profile/')
        request.user = AnonymousUser()
        response = AccountEditView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_profile_url_with_auth_user(self):
        request = self.factory.get('/accounts/profile/')
        request.user = self.user
        response = AccountEditView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="{}"'.format(self.username))
        self.assertContains(response, 'value="{}"'.format(self.email))

    def test_profile_change_email(self):
        c = Client()
        c.login(username=self.email, password='top_secret')

        response = c.post('/accounts/profile/', data={
            'email': 'other@email.change',
            'username': self.username,
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username=self.username).email, 'other@email.change')

    def test_profile_change_username(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': self.username + 'other',
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(email=self.email).username, self.username+'other')

    def test_profile_change_password(self):
        c = Client()
        c.login(username=self.user.email, password='top_secret')

        newpassword = 'newpassword'

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': self.username,
            'old_password': self.password,
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=newpassword)

        self.assertTrue(user)
        self.assertEqual(response.status_code, 302)

    def test_profile_change_password_with_bad_old_password(self):
        c = Client()
        c.login(username=self.user.email, password='top_secret')

        newpassword = 'newpassword'

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': self.username,
            'old_password': 'not{}'.format(self.password),
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=newpassword)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.')

    def test_profile_change_password_without_old_password(self):
        c = Client()
        c.login(username=self.user.email, password='top_secret')

        newpassword = 'newpassword'

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': self.username,
            'old_password': '',
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=newpassword)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.')

    def test_profile_change_password_with_old_password_and_without_new_password(self):
        c = Client()
        c.login(username=self.user.email, password='top_secret')

        newpassword = ''

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': self.username,
            'old_password': self.password,
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 302)

    def test_profile_set_email_to_empty(self):
        c = Client()
        c.login(username=self.email, password='top_secret')

        response = c.post('/accounts/profile/', data={
            'email': '',
            'username': self.username,
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обязательное поле.')

    def test_profile_set_username_to_empty(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.post('/accounts/profile/', data={
            'email': self.email,
            'username': '',
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обязательное поле.')

    def test_logout(self):
        c = Client()
        c.login(username=self.email, password='top_secret')

        response = c.get('/accounts/logout/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user, AnonymousUser())

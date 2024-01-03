from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User,Group
# Create your tests here.
from .models import HOD_model,announcement_model#test_create_HOD
from .views import login_page
class HOD_test(TestCase):

    def test_create_HOD(self):
        av1=HOD_model.objects.create(HOD_name="mikasa",password="12345")
        #av2=HOD_model.objects.create(HOD_name="majora",password="12345")
        #av3=HOD_model.objects.create(HOD_name="miko",password="12345")
        #av4=HOD_model.objects.create(HOD_name="mirika",password="12345")
        '''
        self.assertEqual(HOD_model.HOD_name,"majora")
        self.assertEqual(HOD_model.password,"12345")'''
        mk=HOD_model.objects.get(HOD_name="mikasa")
        self.assertEqual(av1.HOD_name,"mikasa")
        self.assertEqual(av1.password,"12345")


class LoginviewTest(TestCase):

    def setUp(self):
        self.testuser=User.objects.create_user(username="mikasa")
        self.testuser.set_password='12345'
        grp=Group.objects.get_or_create(name="HOD")
        grp[0].user_set.add(self.testuser)
        self.testuser.save()
        self.announcement_create=announcement_model.objects.create(title="test",designation="HOD",
                                                                   announcement="this is a test announcement for test")
        self.announcement_create.save()
        self.cl=Client()



    def test_LoginPage(self):
        #self.cl=Client()
        #av1=HOD_model.objects.create(HOD_name="mikasa",password="12345")
        loginurl=reverse("login_page")
        response=self.cl.post(loginurl,{"username":"mikasa","password":"12345"})
        self.assertEqual(response.status_code,200)
        #self.assertRedirects(response,reverse("hodDashboard"))
        #self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_hodDashboard(self):
        readurl=reverse("hodDashboard")#,kwargs={"pk":self.announcement_create.pk})
        response=self.cl.get(readurl)
        self.assertEqual(response.status_code,302)

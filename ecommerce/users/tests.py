from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import *

class ModelCreationTests(TestCase):
    def test_create_reg_user(self):
        user = User.objects.create(username="reguser", is_registered_user=True)
        reg_user = Registered_User.objects.create(user=user, phone="1234567890")
        self.assertEqual(reg_user.user.username, "reguser")
        self.assertEqual(reg_user.phone, "1234567890")
        self.assertTrue(user.is_registered_user)
        self.assertFalse(reg_user.user.is_seller)

    def test_create_seller(self):
        user = User.objects.create(username="seller", is_seller=True)
        seller = Seller.objects.create(user=user, phone="0987654321", PIVA="IT123456789")
        self.assertEqual(seller.user.username, "seller")
        self.assertEqual(seller.phone, "0987654321")
        self.assertEqual(seller.PIVA, "IT123456789")
        self.assertFalse(seller.user.is_registered_user)
        self.assertTrue(seller.user.is_seller)


class FieldValidationTests(TestCase):
    def test_phone_max_length(self):
        user = User.objects.create(username="testuser")
        reg_user = Registered_User(user=user, phone="1" * 21)  # 21 characters
        with self.assertRaises(ValidationError):
            reg_user.full_clean()


class RelationshipTests(TestCase):
    def test_unique_user_relation(self):
        user = User.objects.create(username="uniqueuser")
        Registered_User.objects.create(user=user, phone="1234567890")
        with self.assertRaises(Exception):
            Registered_User.objects.create(user=user, phone="0987654321")



class HomeSignupViewTests(TestCase):
    def test_home_signup_page(self):
        response = self.client.get(reverse('users:home_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home_signup.html')


class LoginViewTests(TestCase):
    def setUp(self):
        # Create a user for test login
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='testpassword123'
        )
    def test_authenticated_user_redirect(self):
        self.client.logout()
        self.assertTrue(self.client.login(username='test', password='testpassword123'))
        response = self.client.get(reverse('users:user_signup'))
        self.assertRedirects(response, reverse('pages:home_page'))


class ReguserSignupViewTests(TestCase):
    def test_reg_user_signup_form(self):
        url = reverse('users:user_signup')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertIsNotNone(User.objects.get(username='testuser'))
        self.assertTrue(User.objects.get(username='testuser').is_registered_user)




class SellerSignupViewTests(TestCase):
    def test_seller_signup_form(self):
        url = reverse('users:seller_signup')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'PIVA': 'IT123456789',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertIsNotNone(User.objects.get(username='testuser'))
        self.assertTrue(User.objects.get(username='testuser').is_seller)



class ProfileViewTests(TestCase):
    def deny_profile_detail(self):
        self.client.logout()
        response = self.client.get(reverse('users:profile_user'))
        self.assertRedirects(response, reverse('pages:home_page'))
        response = self.client.get(reverse('users:profile_seller'))
        self.assertRedirects(response, reverse('pages:home_page'))


class UpdateProfileViewTests(TestCase):
    def test_seller_profile_update(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123", is_seller=True)
        seller = Seller.objects.create(user=user, phone="0987654321", PIVA="IT123456789")

        self.assertTrue(self.client.login(username="testuser", password="testpassword123"))
        response = self.client.get(reverse('users:update_profile_seller', kwargs={'pk': seller.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update_profile_seller.html')

        data = {
            'username':user.username,
            'email': user.email,
            'phone': '0987654321',
            'PIVA': 'IT987654321'
        }

        response = self.client.post(reverse('users:update_profile_seller', kwargs={'pk': seller.pk}), data)
        self.assertRedirects(response, reverse('users:profile_seller', kwargs={'pk': seller.pk}))


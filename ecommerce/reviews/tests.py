from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
import os

from django.urls import reverse

from .models import *
from listings.models import Product, Category
from users.models import *


class ReviewModelTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.reg_user = Registered_User.objects.create(user=User.objects.create_user(username='reguser', password='password'),
                                                       phone="1234567890")

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,

        )
        self.product.categories.add(self.category)

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_review_unique_constraint(self):
        review = Review.objects.create(product=self.product, reg_user=self.reg_user, title="Test Title", rating=3,
                                       comment="Test Comment")
        self.assertEqual(review.product, self.product)
        with self.assertRaises(IntegrityError):
            Review.objects.create(product=self.product, reg_user=self.reg_user, title="Test Title", rating=3, comment="Test Comment")


class CreateReviewTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user,phone="1234567890")

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,

        )
        self.product.categories.add(self.category)


    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_create_review(self):
        self.client.login(username='reguser', password='password')
        review_data = {
            'title': 'Test Title',
            'rating': 3,
            'comment': 'Test Comment'
        }
        response = self.client.post(reverse('reviews:create_review', kwargs={'pk': self.product.pk}), review_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertIsNotNone(Review.objects.filter(product=self.product, reg_user=self.reg_user).first())

    def test_create_seller_review(self):
        self.client.login(username='reguser', password='password')
        review_data = {
            'title': 'Test Title',
            'comment': 'Test Comment'
        }
        response = self.client.post(reverse('reviews:create_seller_review', kwargs={'pk': self.seller.pk}), review_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))
        self.assertIsNotNone(Seller_Review.objects.filter(seller=self.seller, reg_user=self.reg_user).first())


class UpdateReviewTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user,phone="1234567890")

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,

        )
        self.product.categories.add(self.category)
        self.review = Review.objects.create(product=self.product, reg_user=self.reg_user, title="Test Title", rating=3,
                                       comment="Test Comment")
        self.seller_review = Seller_Review.objects.create(seller=self.seller, reg_user=self.reg_user,
                                                          title="Test Title", comment="Test Comment")

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()


    def test_update_review(self):
        self.client.login(username='reguser', password='password')
        review_data = {
            'title': 'Updated Title',
            'rating': 4,
            'comment': 'Updated Comment'
        }
        response = self.client.post(reverse('reviews:update_review', kwargs={'pk': self.review.pk}), review_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Title')
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Updated Comment')


    def test_update_seller_review(self):
        self.client.login(username='reguser', password='password')
        review_data = {
            'title': 'Updated Title',
            'comment': 'Updated Comment'
        }
        response = self.client.post(reverse('reviews:update_seller_review', kwargs={'pk': self.seller_review.pk}), review_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))
        self.seller_review.refresh_from_db()
        self.assertEqual(self.seller_review.title, 'Updated Title')
        self.assertEqual(self.seller_review.comment, 'Updated Comment')


    def test_delete_review(self):
        self.client.login(username='reguser', password='password')
        response = self.client.post(reverse('reviews:delete_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_delete_seller_review(self):
        self.client.login(username='reguser', password='password')
        response = self.client.post(reverse('reviews:delete_seller_review', kwargs={'pk': self.seller_review.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))
        self.assertFalse(Seller_Review.objects.filter(pk=self.seller_review.pk).exists())



class ListReviewTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user,phone="1234567890")

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,

        )
        self.product.categories.add(self.category)
        self.review = Review.objects.create(product=self.product, reg_user=self.reg_user, title="Test Title", rating=3,
                                       comment="Test Comment")
        self.seller_review = Seller_Review.objects.create(seller=self.seller, reg_user=self.reg_user,
                                                          title="Test Title", comment="Test Comment")

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_list_review(self):
        response = self.client.get(reverse('reviews:list_user_review'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))


        self.client.login(username='reguser', password='password')
        response = self.client.get(reverse('reviews:list_user_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/list_user_review.html')
        self.assertQuerySetEqual(response.context['object_list'],
                                 Review.objects.all().order_by('-date'))  # Compare 2 query set


    def test_list_seller_review(self):
        response = self.client.get(reverse('reviews:list_seller_review', kwargs={'pk': self.seller.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/list_seller_review.html')
        self.assertQuerySetEqual(response.context['object_list'],
                                 Seller_Review.objects.all().order_by('-date'))



    def test_list_user_seller_review(self):
        response = self.client.get(reverse('reviews:list_user_seller_review'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))

        self.client.login(username='reguser', password='password')
        response = self.client.get(reverse('reviews:list_user_seller_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/list_user_seller_review.html')
        self.assertQuerySetEqual(response.context['object_list'],
                                 Seller_Review.objects.all().order_by('-date'))


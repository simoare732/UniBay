from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
import os

from django.urls import reverse

from .models import Favourite
from listings.models import Product, Category
from users.models import *


class FavouriteModelTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.user = User.objects.create_user(username='user', password='password')

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

    # Test if unique constraint is working
    def test_favourite_unique_constraint(self):
        favourite = Favourite.objects.create(user=self.user, product=self.product)
        self.assertEqual(favourite.user, self.user)

        with self.assertRaises(IntegrityError):
            Favourite.objects.create(user=self.user, product=self.product)


class ToggleFavoriteTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.user = User.objects.create_user(username='user', password='password')

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
        self.client.login(username='user', password='password')

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    # Test if the product is added to favorites
    def test_add_to_favorites(self):
        url = reverse('watchlist:toggle_favorite', args=[self.product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favourite.objects.filter(user=self.user, product=self.product).exists())
        self.assertJSONEqual(response.content, {'is_favorite': True})

    # Test if the product is removed from favorites
    def test_remove_from_favorites(self):
        Favourite.objects.create(user=self.user, product=self.product)
        url = reverse('watchlist:toggle_favorite', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favourite.objects.filter(user=self.user, product=self.product).exists())
        self.assertJSONEqual(response.content, {'is_favorite': False})


class RemoveFavoriteTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.user = User.objects.create_user(username='user', password='password')

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
        self.favorite = Favourite.objects.create(user=self.user, product=self.product)

        self.client.login(username='user', password='password')

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_remove_existing_favorite(self):
        url = reverse('watchlist:remove_favorite', args=[self.favorite.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favourite.objects.filter(id=self.favorite.id).exists())
        self.assertJSONEqual(response.content, {'success': True})

    def test_remove_non_existing_favorite(self):
        url = reverse('watchlist:remove_favorite', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'not_favorite'})


class ListFavoriteTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.user = User.objects.create_user(username='user', password='password')

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category = Category.objects.create(name="Test Category")
        self.product1 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product1",
            description="Test description1",
            price=10.00,
            quantity=20,

        )
        self.product2 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product2",
            description="Test description2",
            price=10.00,
            quantity=20,

        )

        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)
        self.favorite = Favourite.objects.create(user=self.user, product=self.product1)
        self.favorite = Favourite.objects.create(user=self.user, product=self.product2)

        self.client.login(username='user', password='password')

    def tearDown(self):
        product_image_path1 = os.path.join(f'listings/imgs/{self.product1.pk}', 'test_image.jpg')
        product_image_path2 = os.path.join(f'listings/imgs/{self.product2.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path1):
            os.remove(product_image_path1)
        if os.path.exists(product_image_path2):
            os.remove(product_image_path2)
        super().tearDown()

    def test_list_favorites_view(self):
        url = reverse('watchlist:list_favourites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'watchlist/list_favourites.html')
        self.assertQuerySetEqual(response.context['object_list'], Favourite.objects.all().order_by('-date')) #Compare 2 query set


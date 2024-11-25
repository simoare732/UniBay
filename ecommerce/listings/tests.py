from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from io import BytesIO
from PIL import (Image)


from .models import *
from users.models import Seller, User, Registered_User


def create_fake_image():
    # Create a red image
    image = Image.new('RGB', (100, 100), color='red')

    # Save the image to a BytesIO object
    img_io = BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Return a SimpleUploadedFile object
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type='image/jpeg')


class ProductModelTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'), phone="123456789", PIVA="123456789")
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

    # Basically this test pass at the function a fake function shutil.rmtree. The product is eliminated using mock_rmtree
    # to avoid deleting folders during test. Then with assert_called_once, we check if the function has been called once with
    # path passed as argument.
    @patch('listings.models.shutil.rmtree')
    def test_delete_product_folder(self, mock_rmtree):
        pk = self.product.pk
        self.product.save()
        self.product.delete()

        mock_rmtree.assert_called_once_with(f'listings/imgs/{pk}')

    def test_average_rating(self):
        print("Testing average rating for:", self.product)
        user1 = User.objects.create_user(username='user1', password='password')
        self.product.reviews.create(product=self.product, reg_user=Registered_User.objects.create(user=user1, phone="1234567890"),
                                    title="Test Review", rating=3)
        user2 = User.objects.create_user(username='user2', password='password')
        self.product.reviews.create(product=self.product, reg_user=Registered_User.objects.create(user=user2, phone="1234567890"),
                                    title="Test Review", rating=4)
        self.assertEqual(self.product.average_rating(), 3.5)


class ProductDeleteTests(TestCase):
    def test_missing_required_field(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")

        product = Product(
            seller=self.seller,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,
        )

        # The method full_clean() is used to validate the model fields
        with self.assertRaises(ValidationError):
            product.full_clean()


class ProductValidationTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
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


    def test_quantity_cannot_be_negative(self):
        self.product.decrease_quantity(30)
        self.assertEqual(self.product.quantity, 0)


    def test_price_precision(self):
        self.product.price = 99999.99
        self.product.save()
        self.assertEqual(self.product.price, 99999.99)


class ProductCreateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123",
                                        is_seller=True)
        self.seller = Seller.objects.create(user=user, phone="0987654321", PIVA="IT123456789")

        self.category = Category.objects.create(name="Test Category")

        self.fake_image = create_fake_image()


    def test_create_product_view(self):
        self.client.login(username='testuser', password='testpassword123')

        product_data = {
            'title': 'Test Product',
            'description': 'Test description',
            'price': 10.00,
            'quantity': 20,
            'categories': [self.category.id],
            'image1': self.fake_image
        }

        response = self.client.post(reverse('listings:create_product'), product_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile_seller', kwargs={'pk': self.seller.pk}))

        product = Product.objects.first()
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.seller, self.seller)



class ProductViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123",
                                        is_seller=True)
        self.seller = Seller.objects.create(user=user, phone="0987654321", PIVA="IT123456789")

        self.category = Category.objects.create(name="Test Category")

        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.product = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,
        )

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_list_products_view(self):
        self.client.login(username='testuser', password='testpassword123')

        response = self.client.get(reverse('listings:list_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/list_products.html')

        products = response.context['products']
        self.assertEqual(list(products.all()), [self.product])


    def test_delete_products_view(self):
        self.client.login(username='testuser', password='testpassword123')

        response = self.client.post(reverse('listings:delete_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:list_products'))

        # Check that the product has been deleted, so there is no products
        self.assertFalse(Product.objects.exists())

    def test_detail_product_view(self):
        response = self.client.get(reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/detail_product.html')


    def test_update_product_view(self):
        self.client.login(username='testuser', password='testpassword123')
        fi = create_fake_image()
        updated_data = {
            'image1': fi,
            'title' :"Updated Product",
            'description' : "Updated description",
            'price': 20.00,
            'quantity' : 30,
            'categories' : [self.category.id]
        }

        response = self.client.post(reverse('listings:update_product', kwargs={'pk': self.product.pk}),
                                    updated_data)

        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product')
        self.assertEqual(self.product.description, 'Updated description')
        self.assertEqual(self.product.price, 20.00)
        self.assertEqual(self.product.quantity, 30)














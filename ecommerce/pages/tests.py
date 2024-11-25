from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os

from listings.models import Product, Category
from users.models import Seller, User

class TestViews(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )

        self.category1 = Category.objects.create(name="Test Category 1")
        self.category2 = Category.objects.create(name="Test Category 2")
        self.category3 = Category.objects.create(name="Test Category 3")

        self.product1 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product 1",
            description="Test description 1",
            price=10.00,
            quantity=20,

        )
        self.product1.categories.add(self.category1)

        self.product2 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product 2",
            description="Test description 2",
            price=20.00,
            quantity=10,
        )
        self.product2.categories.add(self.category2)

        self.product3 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product 3",
            description="Test description 3",
            price=15.00,
            quantity=30,
        )
        self.product3.categories.add(self.category2, self.category3)

        self.product1.increase_sold(5)
        self.product2.increase_sold(8)
        self.product3.increase_sold(2)

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product1.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_order_products(self):
        response = self.client.get(reverse('pages:list_products'), {'sort': 'price-desc'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/list_products.html')

        self.assertEqual(list(response.context['products']), [self.product2, self.product3, self.product1])

        response = self.client.get(reverse('pages:list_products'), {'sort': 'price-asc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product1, self.product3, self.product2])

        response = self.client.get(reverse('pages:list_products'), {'sort': 'most-sold'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product2, self.product1, self.product3])

    def test_filter_category_products(self):
        response = self.client.get(reverse('pages:list_products'), {'category': 'Test Category 1'})
        self.assertEqual(response.status_code, 200)
        print(list(response.context['products']))
        self.assertEqual(list(response.context['products']), [self.product1])

        response = self.client.get(reverse('pages:list_products'), {'category': 'Test Category 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product3, self.product2])

        response = self.client.get(reverse('pages:list_products'), {'category': 'Test Category 3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product3])





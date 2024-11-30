from unittest.mock import patch

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import os

from .models import *
from users.models import *
from listings.models import *


class CartModelTests(TestCase):
    def setUp(self):
        self.reg_user = Registered_User.objects.create(user=User.objects.create_user(username='reguser', password='password'),
                                            phone="123456789")

        self.cart = Cart.objects.create(user=self.reg_user.user)

        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")


        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,
        )
        self.product2 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=30.00,
            quantity=20,
        )
        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)

    def tearDown(self):
        product_image_path1 = os.path.join(f'listings/imgs/{self.product1.pk}', 'test_image.jpg')
        product_image_path2 = os.path.join(f'listings/imgs/{self.product2.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path1):
            os.remove(product_image_path1)
        if os.path.exists(product_image_path2):
            os.remove(product_image_path2)
        super().tearDown()

    def test_cart_total_price(self):
        cart_item1 = Cart_Item.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item2 = Cart_Item.objects.create(cart=self.cart, product=self.product2, quantity=3)
        self.assertEqual(self.cart.total_price(), 110.00)

    def test_cart_total_items(self):
        cart_item = Cart_Item.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item = Cart_Item.objects.create(cart=self.cart, product=self.product2, quantity=5)
        self.assertEqual(self.cart.total_items(), 7)

    def test_cart_item_total_price(self):
        cart_item = Cart_Item.objects.create(cart=self.cart, product=self.product1, quantity=3)
        self.assertEqual(cart_item.total_price(), 30.00)


class OrderModelTests(TestCase):
    def setUp(self):
        self.reg_user = Registered_User.objects.create(user=User.objects.create_user(username='reguser', password='password'),
                                            phone="123456789")

        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")


        self.fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=10.00,
            quantity=20,
        )
        self.product2 = Product.objects.create(
            seller=self.seller,
            image1=self.fake_image,
            title="Test Product",
            description="Test description",
            price=30.00,
            quantity=20,
        )
        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)

        self.shipping = Shipping.objects.create(name='Shipping')
        self.payment = Payment.objects.create(card_number='1')

    def tearDown(self):
        product_image_path1 = os.path.join(f'listings/imgs/{self.product1.pk}', 'test_image.jpg')
        product_image_path2 = os.path.join(f'listings/imgs/{self.product2.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path1):
            os.remove(product_image_path1)
        if os.path.exists(product_image_path2):
            os.remove(product_image_path2)
        super().tearDown()


    def test_item_shipped(self):
        order = Order.objects.create(user=self.reg_user.user, total_price=20.00, shipping=self.shipping,
                                     payment=self.payment)
        order_item = Order_Item.objects.create(order=order, product=self.product1, status='Paid', quantity=2, price=20.00)
        self.assertEqual(order_item.status, 'Paid')
        self.assertEqual(order.status, 'In progress')
        order.order_paid()
        self.assertEqual(order.status, 'Paid')
        order_item.item_shipped()
        self.assertEqual(order_item.status, 'Shipped')
        self.assertEqual(order.status, 'Shipped')


class AddUpdateTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user, phone="1234567890")

        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")

        self.cart = Cart.objects.create(user=self.reg_user.user)

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

        self.shipping = Shipping.objects.create(name='Shipping')
        self.payment = Payment.objects.create(card_number='1')

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_add_to_cart(self):
        self.client.login(username='reguser', password='password')
        data = {
            'quantity': '3'
        }
        url = reverse('shopping:add_to_cart', args=[self.product.pk])
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.total_items(), 3)
        self.assertEqual(self.cart.total_price(), 30.00)


    def test_update_cart_item_quantity(self):
        self.client.login(username='reguser', password='password')
        cart_item = Cart_Item.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(self.cart.total_items(), 3)

        url = reverse('shopping:update_item_quantity', args=[cart_item.pk])
        response = self.client.post(url, {'action':'increment'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.total_items(), 4)

        response = self.client.post(url, {'action': 'decrement'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.total_items(), 3)

        response = self.client.post(url, {'action': 'delete'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.total_items(), 0)


class CheckoutTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user, phone="1234567890")

        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")

        self.cart = Cart.objects.create(user=self.reg_user.user)

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

        self.shipping = Shipping.objects.create(name='Shipping')
        self.payment = Payment.objects.create(card_number='1')

        self.session = self.client.session
        self.session['checkout_token'] = 'valid_token'
        self.session.save()

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('shopping:checkout'))
        self.assertRedirects(response, reverse('pages:home_page'))

    def test_checkout_view_invalid_token(self):
        self.client.login(username='reguser', password='password')
        # Request without token
        response = self.client.get(reverse('shopping:checkout'))
        self.assertRedirects(response, reverse('pages:home_page'))

        # Request with invalid token
        response = self.client.get(reverse('shopping:checkout') + '?token=invalid_token')
        self.assertRedirects(response, reverse('pages:home_page'))

    def test_checkout_view_valid_token(self):
        self.client.login(username='reguser', password='password')
        # Request with valid token
        response = self.client.get(reverse('shopping:checkout') + '?token=valid_token')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/checkout.html')

    def test_checkout_single_product(self):
        self.client.login(username='reguser', password='password')
        # Request with a single product
        response = self.client.get(
            reverse('shopping:checkout') + f'?token=valid_token&product_id={self.product.id}&quantity=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['total_price'], 10.00)

    def test_checkout_cart(self):
        self.client.login(username='reguser', password='password')
        # Request with a cart
        cart_item = Cart_Item.objects.create(cart=self.cart, product=self.product, quantity=2)

        response = self.client.get(reverse('shopping:checkout') + '?token=valid_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['items'], [{'product':cart_item.product, 'quantity':cart_item.quantity,
                                                      'total_price':cart_item.total_price()}])
        self.assertEqual(response.context['total_price'], 20.00)  # 2 x 10.00

    def test_checkout_invalid_forms(self):
        self.client.login(username='reguser', password='password')

        # Send incomplete forms
        data = {
            'country': 'Italy',
        }

        url = reverse('shopping:checkout') + f'?token=valid_token&product_id={self.product.id}&quantity=1'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page

    @patch('shopping.views.send_mail')  # Emulate the send_mail function
    def test_checkout_valid_forms(self, mock_send_mail):
        # Send valid forms
        self.client.login(username='reguser', password='password')

        data = {
            'country': 'Italy',
            'name': 'Test',
            'surname': 'User',
            'shipping_address': '123 Test Street',
            'city': 'Test City',
            'zip_code': '12345',
            'card_number': '4111111111111111',
            'expiration_date': '12/25',
            'cvv': '123',
        }

        url = reverse('shopping:checkout') + f'?token=valid_token&product_id={self.product.id}&quantity=1'
        response = self.client.post(url, data)

        # Verify the order has been created
        self.assertRedirects(response, reverse('shopping:order_success'))
        order = Order.objects.get(user=self.reg_user.user)
        self.assertEqual(order.total_price, 10.00)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(mock_send_mail.called)  # Verify the email has been sent
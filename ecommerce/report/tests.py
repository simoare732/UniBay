from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import os

from django.urls import reverse

from .models import *
from users.models import *
from listings.models import Product, Category


class ReportModelTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.reporter = Registered_User.objects.create(user=User.objects.create_user(username='reporter', password='password'))


    def test_report_creation(self):
        report = Report.objects.create(reporter=self.reporter, seller=self.seller, reason='SP', description='Spam')
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.get_reason(), 'Spam')
        self.assertEqual(report.is_seen(), False)

        report.set_seen()
        self.assertEqual(report.is_seen(), True)


class ReportCreateTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reporter = Registered_User.objects.create(user=user, phone="123456789")
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

    def test_report_create_view(self):
        self.client.login(username='reguser', password='password')
        report_data = {
            'reason': 'SP',
            'description': 'Test description'
        }
        response = self.client.post(reverse('report:create_report', kwargs={'pk': self.product.pk}), report_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertIsNotNone(Report.objects.filter(reporter=self.reporter, seller=self.seller).first())


class StrikeCreateTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.client.login(username='admin', password='password')

    def test_strike_create_view(self):
        strike_data = {
            'description': 'Test description'
        }
        response = self.client.post(reverse('report:create_strike', kwargs={'seller_pk': self.seller.pk}), strike_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report:list_reports'))
        self.assertIsNotNone(Strike.objects.filter(seller=self.seller).first())
        self.assertEqual(self.seller.strikes.count(), 1)


class ReportListViewTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")

        self.reporter1 = Registered_User.objects.create(
            user=User.objects.create_user(username='reporter1', password='password'))

        self.reporter2 = Registered_User.objects.create(
            user=User.objects.create_user(username='reporter2', password='password'))


        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.client.login(username='admin', password='password')

        self.report1 = Report.objects.create(reporter=self.reporter1, seller=self.seller, reason='SP', description='Spam')
        self.report2 = Report.objects.create(reporter=self.reporter2, seller=self.seller, reason='TR', description='Truffa')


    def test_report_list_view(self):
        response = self.client.get(reverse('report:list_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/report_list.html')
        self.assertQuerySetEqual(response.context['object_list'],
                                 Report.objects.all().order_by('-date'))


class MarkReportSeenTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='password'),
                                            phone="123456789", PIVA="123456789")

        self.reporter = Registered_User.objects.create(
            user=User.objects.create_user(username='reporter', password='password'))

        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.client.login(username='admin', password='password')

        self.report = Report.objects.create(reporter=self.reporter, seller=self.seller, reason='SP', description='Spam')

    def test_mark_report_seen(self):
        self.assertEqual(Report.objects.get(pk=self.report.pk).is_seen(), False)
        response = self.client.post(reverse('report:mark_report_seen', kwargs={'report_pk': self.report.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report:list_reports'))
        self.assertEqual(Report.objects.get(pk=self.report.pk).is_seen(), True)



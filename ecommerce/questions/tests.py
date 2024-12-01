from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch



from .models import Question, Answer
from listings.models import *
from users.models import *

class QuestionModelTest(TestCase):
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


    def test_answer(self):
        question = Question.objects.create(product=self.product, reg_user=self.reg_user, text="Test question")
        answer = Answer.objects.create(question=question, user=self.seller.user, text="Test answer")
        self.assertEqual(question.is_answered(), False)
        answer.approve()
        self.assertEqual(question.is_answered(), True)
        self.assertEqual(question.get_answer(), answer)


class QuestionCreateTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="reguser", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user = Registered_User.objects.create(user=user, phone="1234567890")

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


    def test_create_question(self):
        self.client.login(username='reguser', password='password')

        question_data = {
            'text' : 'Test question'
        }

        response = self.client.post(reverse('questions:create_question', kwargs={'pk': self.product.pk}), question_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first().product, self.product)
        self.assertEqual(Question.objects.first().reg_user, self.reg_user)
        self.assertEqual(Question.objects.first().text, 'Test question')


class QuestionListTests(TestCase):
    def setUp(self):
        self.reg_user = Registered_User.objects.create(user=User.objects.create_user(username='reguser', password='password'),
            phone="123456789")

        user = User.objects.create_user(username="seller", email="seller@example.com", password="password",
                                        is_seller=True)

        self.seller = Seller.objects.create(user=user,phone="123456789", PIVA="123456789")

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

        self.question1 = Question.objects.create(product=self.product, reg_user=self.reg_user, text="Test question 1")
        self.question2 = Question.objects.create(product=self.product, reg_user=self.reg_user, text="Test question 2")

    def tearDown(self):
        product_image_path = os.path.join(f'listings/imgs/{self.product.pk}', 'test_image.jpg')
        if os.path.exists(product_image_path):
            os.remove(product_image_path)
        super().tearDown()

    def test_list_questions_not_logged_in(self):
        response = self.client.get(reverse('questions:list_questions', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home_page'))

    def test_list_questions(self):
        self.client.login(username='seller', password='password')

        response = self.client.get(reverse('questions:list_questions', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_list.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertQuerySetEqual(response.context['object_list'],
                                 Question.objects.all().order_by('-date'))


class AddAnswerTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="reguser1", email="reguser@example.com", password="password",
                                        is_registered_user=True)
        self.reg_user1 = Registered_User.objects.create(user=user1, phone="1234567890")

        user2 = User.objects.create_user(username="seller", email="seller@example.com", password="password",
                                        is_seller=True)

        self.seller = Seller.objects.create(user=user2, phone="123456789", PIVA="123456789")

        user3 = User.objects.create_user(username="reguser2", email="reguser@example.com", password="password",
                                         is_registered_user=True)
        self.reg_user2 = Registered_User.objects.create(user=user3, phone="1234567890")

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

    def test_user_add_answer(self):
        self.client.login(username='reguser2', password='password')
        question = Question.objects.create(product=self.product, reg_user=self.reg_user1, text="Test question")
        answer_data = {
            'text': 'Test answer'
        }
        response = self.client.post(reverse('questions:add_answer', kwargs={'question_id': question.pk}), answer_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(Answer.objects.filter(question=question).first().text, 'Test answer')
        self.assertEqual(question.is_answered(), False)

    def test_seller_add_answer(self):
        self.client.login(username='seller', password='password')
        question = Question.objects.create(product=self.product, reg_user=self.reg_user1, text="Test question")
        answer_data = {
            'text': 'Test answer'
        }
        response = self.client.post(reverse('questions:add_answer', kwargs={'question_id': question.pk}), answer_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listings:detail_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(Answer.objects.filter(question=question).first().text, 'Test answer')
        self.assertEqual(question.is_answered(), True)
        self.assertEqual(Answer.objects.filter(question=question).first(), question.get_answer())

    @patch('questions.views.send_mail')  # Emulate the send_mail function
    def test_approve_answer(self, mock_send_mail):
        self.client.login(username='seller', password='password')
        question = Question.objects.create(product=self.product, reg_user=self.reg_user1, text="Test question")
        answer = Answer.objects.create(question=question, user=self.reg_user2.user, text="Test answer")
        response = self.client.post(reverse('questions:approve_answer', kwargs={'answer_pk': answer.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('questions:list_questions', kwargs={'pk': self.product.pk}))
        self.assertEqual(Answer.objects.get(pk=answer.pk).approved, True)
        self.assertEqual(Answer.objects.get(pk=answer.pk).question.is_answered(), True)
        self.assertEqual(Answer.objects.get(pk=answer.pk).question.get_answer(), answer)
        self.assertTrue(mock_send_mail.called)  # Verify the email has been sent

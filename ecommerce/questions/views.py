from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from .models import Question, Answer
from listings.models import Product, Category
from .forms import question_create_form
from django.views.decorators.http import require_POST
from users.mixins import question_owner_mixin


class create_question_view(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'questions/create_question.html'
    form_class = question_create_form

    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        product_id = self.kwargs.get('pk')
        form.instance.product = Product.objects.get(pk=product_id)
        form.instance.reg_user = self.request.user.registered_user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('listings:detail_product', kwargs={'pk': self.kwargs['pk']})


@require_POST
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        text = request.POST.get("text") # It can't be null
        if request.user.is_seller and request.user.seller == question.product.seller:
            ap = True
            msg = f"Il venditore ha risposto alla tua domanda riguardante il prodotto {question.product.title}"
            send_mail(
                'UniBay: Risposta alla tua domanda',
                msg,
                'simoaresta3@gmail.com',
                [question.reg_user.user.email],
                fail_silently=False,
            )
        else:
            ap = False

        Answer.objects.create(
            question=question,
            user=request.user,
            text=text,
            approved=ap  # If the user is the seller, the answer is automatically approved
        )

    if "list" in request.GET:
        return redirect("questions:list_questions", pk=question.product.pk)
    return redirect("listings:detail_product", pk=question.product.pk)



class question_list_view(question_owner_mixin, ListView):
    model = Question
    template_name = 'questions/question_list.html'

    def get_queryset(self):
        product_pk = self.kwargs.get('pk')
        return Question.objects.filter(product__pk=product_pk).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context


@require_POST
def approve_answer(request, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk)
    answer.approve()
    msg = f"L'utente {answer.user.username} ha risposto alla tua domanda riguardante il prodotto {answer.question.product.title}"
    send_mail(
        'UniBay: Risposta alla tua domanda',
        msg,
        'admin@admin.com',
        [answer.question.reg_user.user.email],
        fail_silently=False,
    )
    return redirect("questions:list_questions", pk=answer.question.product.pk)

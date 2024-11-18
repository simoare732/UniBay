from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from .models import Question, Answer
from listings.models import Product, Category
from .forms import question_create_form


class create_question_view(CreateView):
    model = Question
    template_name = 'questions/create_question.html'
    form_class = question_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        product_id = self.kwargs.get('pk')
        form.instance.product = Product.objects.get(pk=product_id)
        form.instance.user = self.request.user.registered_user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('listings:detail_product', kwargs={'pk': self.kwargs['pk']})


def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        text = request.POST.get("text")
        if request.user.is_seller and request.user.seller == question.product.seller:
            ap = True
        else:
            ap = False
        if text:
            Answer.objects.create(
                question=question,
                user=request.user,
                text=text,
                approved=ap  # If the user is the seller, the answer is automatically approved
            )
    if "list" in request.GET:
        return redirect("questions:list_questions", pk=question.product.pk)
    return redirect("listings:detail_product", pk=question.product.pk)



class question_list_view(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    paginate_by = 5

    def get_queryset(self):
        product_pk = self.kwargs.get('pk')
        return Question.objects.filter(product__pk=product_pk).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context


def approve_answer(request, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk)
    answer.approve()
    return redirect("questions:list_questions", pk=answer.question.product.pk)
from django.http import Http404
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from book.models import Product, Category, Comment
from django.conf import settings
from book.forms import ProductCreateForm, ProductCreateForm2, CategoryCreateForm, CommentCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search')
        order = self.request.GET.get('order')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if order == 'title':
            queryset = queryset.order_by('title')
        elif order == '-title':
            queryset = queryset.order_by('-title')
        elif order == 'created_at':
            queryset = queryset.order_by('created_at')
        elif order == '-created_at':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 1))
        max_page = self.get_queryset().__len__() / settings.PAGE_SIZE

        if max_page > round(max_page):
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        start = (page - 1) * settings.PAGE_SIZE
        end = page * settings.PAGE_SIZE
        products = self.get_queryset()[start:end]

        context['pages'] = range(1, max_page + 1)
        context['products'] = products
        return context


# def products_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#
#         search = request.GET.get('search')
#         order = request.GET.get('order')
#
#         if search:
#             # products = products.filter(title__icontains=search) | products.filter(description__icontains=search)
#             posts = products.filter(Q(title__icontains=search) | Q(description__icontains=search))
#
#         if order == 'title':
#             products = products.order_by('title')
#         elif order == '-title':
#             products = products.order_by('-title')
#         elif order == 'created_at':
#             products = products.order_by('created_at')
#         elif order == '-created_at':
#             products = products.order_by('-created_at')
#
#         max_page = products.__len__() / settings.PAGE_SIZE
#
#         if max_page > round(max_page):
#             max_page = round(max_page) + 1
#         else:
#             max_page = round(max_page)
#
#         # example: page = 1, PAGE_SIZE = 3
#         # (1 - 1) * 3 = 0
#         # 1 * 3 = 3
#         # posts[0:3]
#
#         # example: page = 2, PAGE_SIZE = 3
#         # (2 - 1) * 3 = 3
#         # 2 * 3 = 6
#         # posts[3:6]
#
#         # Formulas:
#         # start = (page - 1) * PAGE_SIZE
#         # end = page * PAGE_SIZE
#
#         page = int(request.GET.get('page', 1))
#         start = (page - 1) * settings.PAGE_SIZE
#         end = page * settings.PAGE_SIZE
#         products = products[start: end]
#         context = {
#             'pages': range(1, max_page + 1),
#             'products': products
#         }
#         return render(request, 'products/products.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category.html'
    context_object_name = 'category'


# def category_view(request):
#     if request.method == 'GET':
#         category = Category.objects.all()
#         context = {
#             'category': category,
#         }
#         return render(request, 'category/category.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'
    success_url = '/products/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreateForm
        return context

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            # Если продукт с указанным id не найден, вызываем ошибку 404
            raise Http404("Продукт с указанным id не найдену")

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = CommentCreateForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                name=form.cleaned_data['name'],
                text=form.cleaned_data['text'],
                product=product
            )
            return redirect(self.success_url)

        return render(request, self.template_name, {'product': product, 'form': form})


# def product_detail_view(request, product_id):
#     if request.method == 'GET':
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return HttpResponse('PAGE NOT FOUND')
#         context = {
#             'form': CommentCreateForm,
#             'product': product
#         }
#         return render(request, 'products/product_detail.html', context)
#
#     if request.method == 'POST':
#         form = CommentCreateForm(request.POST)
#         if form.is_valid():
#             Comment.objects.create(
#                 name=form.cleaned_data['name'],
#                 text=form.cleaned_data['text'],
#                 product_id=product_id
#             )
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return HttpResponse('PAGE NOT FOUND')
#         context = {
#             'form': CommentCreateForm,
#             'product': product
#         }
#         return render(request, 'products/product_detail.html', context)
#

class ProductCreateView(CreateView):
    template_name = 'products/create.html'
    form_class = ProductCreateForm2
    success_url = '/products/'

    def get_success_url(self):
        return f'{self.success_url}{self.object.id}/'


# def product_create_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': ProductCreateForm()
#         }
#         return render(request, 'products/create.html', context)
#     elif request.method == 'POST':
#         form = ProductCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             Product.objects.create(**form.cleaned_data)
#             return HttpResponse('OKEY!!!')
#         context = {
#             'form': form
#         }
#         return render(request, 'products/create.html', context)
#


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category/create.html'
    form_class = CategoryCreateForm

    def form_valid(self, form):
        return HttpResponse('SUPER!!!')


# def category_create_view(request):
#     if request.method == 'GET':
#         form = CategoryCreateForm
#         context = {
#             'form': form
#         }
#         return render(request, 'category/create.html', context)
#     if request.method == 'POST':
#         form = CategoryCreateForm(request.POST)
#         if form.is_valid():
#             Category.objects.create(
#                 title=form.cleaned_data['title']
#             )
#             return HttpResponse('SUPER!!!')
#         context = {
#             'form': form
#         }
#         return render(request, 'category/create.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/update.html'
    form_class = ProductCreateForm2
    pk_url_kwarg = 'product_id'
    success_url = '/products/'

    def get_success_url(self):
        return f'{self.success_url}{self.object.id}'

# def products_update_view(request, product_id):
#     try:
#         post = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return HttpResponse('PAGE NOT FOUND')
#
#     if request.method == 'GET':
#         context = {
#             'form': ProductCreateForm2(instance=post)
#         }
#         return render(request, 'products/update.html', context)
#
#     if request.method == 'POST':
#         form = ProductCreateForm2(request.POST, request.FILES, instance=post)
#
#         if form.is_valid():
#             form.save()
#             return redirect(f'/products/{product_id}')
#
#         return render(request, 'products/update.html', {"form": form})

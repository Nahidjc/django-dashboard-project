from django.views import generic
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import generics
from product.serializers import ProductSerializer, ProductVariantPriceSerializer


def productsViews(request):

    if request.GET.get('title'):
        title = request.GET.get('title')
        variant = request.GET.get('variant')
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        print("get url", title, variant, price_from, price_to)
        products = Product.objects.filter(
            title__icontains=title,
            productvariant__variant_title__icontains=variant,
            productvariantprice__price__range=[price_from, price_to]

        ).distinct()
        # products = Product.objects.filter(
        #     Q(title__icontains=title) | Q(productvariant__variant_title__icontains=variant) | Q(
        #         productvariantprice__price__range=[price_from, price_to])
        # ).distinct()
        paginator = Paginator(products, 2)

    else:
        products = Product.objects.all()
        paginator = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        products = paginator.get_page(page)

    except PageNotAnInteger:
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.get_page(paginator.num_pages)
    lastp = list(products.object_list)[-1]
    firstp = list(products.object_list)[0]
    firstind = firstp.id
    lastind = lastp.id
    variant = Variant.objects.all()
    return render(request, 'products/list.html', context={"products": products, 'variant': variant, 'page': products, "count": paginator.count, "first": firstind, "last": lastind})


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'
    print("create")

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    pass


class createProductViewset(generics.ListCreateAPIView):
    queryset = ProductVariantPrice.objects.all()
    print(queryset)
    serializer_class = ProductVariantPriceSerializer

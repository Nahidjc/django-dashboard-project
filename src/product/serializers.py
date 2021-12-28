from django.db.models import fields
from rest_framework import serializers
from .models import Product, ProductVariant, ProductVariantPrice, ProductImage


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = [
            "id",
        ]


class ProductSerializer(serializers.ModelSerializer):

    # productvariantprice = ProductVariantPriceSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductImage
        exclude = [
            "id",
        ]


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductVariantPrice
        exclude = [
            "id",
        ]

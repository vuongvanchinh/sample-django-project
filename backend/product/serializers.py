from rest_framework import serializers

from .models import (Category, Product, ProductImage, ProductVariant, ProductVariantCriterion,
                     ProductVariantOption)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_fields = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }
    def update(self, instance, validated_data):
        print(validated_data)
        return super(CategorySerializer, self).update(instance, validated_data)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductVariantOptionSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    class Meta:
        model = ProductVariantOption
        fields = ['id','option_name', 'images', 'criterion']
        extra_kwargs = {'criterion': {'required': False, 'write_only':True}}

class ProductVariantCriterionSerializer(serializers.ModelSerializer):
    options = ProductVariantOptionSerializer(many=True)
    class Meta:
        model = ProductVariantCriterion
        fields = '__all__'
        # read_only_fields = ['product']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        options = validated_data.pop('options', [])
        criterion = ProductVariantCriterion.objects.create(**validated_data)
        for option in options:
            ProductVariantOption.objects.create(criterion=criterion, **option)
        
        return criterion
        # extra_kwargs = {'id': {'read_only': False, 'required': False}}
    

class ProductVariantSerializer(serializers.ModelSerializer):

    # option_values =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'combind_string' ,'product', 'sku', 'price', 'quantity_in_stock', 'option_values']
        read_only_fields = ['combind_string']

    def create(self, validated_data):
        option_values = validated_data.get("option_values", [])
        instance = super().create(validated_data)
        combind_string = '-'.join([option.option_name for option in option_values])
        instance.combind_string = combind_string
        print(combind_string)
        return instance

    def update(self, instance ,validated_data):
        instance = super().update(instance, validated_data)
        option_values = validated_data.pop("option_values", [])
        combind_string = '-'.join([option.option_name for option in option_values])
        instance.combind_string = combind_string
        return instance
        
class ProductSerializer(serializers.ModelSerializer):
    criterions = ProductVariantCriterionSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = ['name','slug',
                'seo_title', 'seo_description',
                'price','weight', 'rating',
                'category','criterions', 'variants']
        lookup_fields = 'slug',
        read_only_fields=['updated_at']

        
    def create(self, validated_data):
        print("Create function:", validated_data)
        criterions = validated_data.pop('criterions', [])
        product = Product.objects.create(**validated_data)
        for criterion in criterions:
            options = criterion.pop('options',[])
            product_criterion = ProductVariantCriterion.objects.create(product_id=product.id, **criterion)
            for option in options:
                ProductVariantOption.objects.create(criterion = product_criterion, **option)
        return product
    



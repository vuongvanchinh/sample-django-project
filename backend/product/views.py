from product.models import Category, Product, ProductVariant, ProductVariantCriterion, ProductVariantOption
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import CategorySerializer, ProductSerializer, ProductVariantCriterionSerializer, ProductVariantOptionSerializer, ProductVariantSerializer
from rest_framework import status

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

    def update(self, request, slug):
        product = Product.objects.get(slug=slug)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        #Addition
        additions = data.pop('additional-external-data', None)
        if additions is not None:
            #criterion and itself options
            for criterion in additions.get('criterions', []):
                criterion['product'] = product.id
                print(criterion)
                criterion_serializer = ProductVariantCriterionSerializer(data=criterion)
                if criterion_serializer.is_valid():
                    criterion_serializer.save()
            
            #options to a criterion existed                         
            for option in additions.get('options', []):
                if ProductVariantCriterion.objects.filter(
                                id=option['criterion'],
                                product_id=product.id).exists():
                    
                    option_serializer= ProductVariantOptionSerializer(data=option)
                    if option_serializer.is_valid():
                        option_serializer.save()
        #update
        update = data.pop('update-external-data', None)
        if update:
            print("Update", update)
            for criterion in update.get('criterions', []):

                criterion_id = criterion.pop('id', None)
                if criterion_id:
                    ProductVariantCriterion.objects.filter(id=criterion_id, product_id=product.id).update(**criterion)
            #options to a criterion existed                         
            for option in update.get('options', []):
                option_id = option.pop('id', None)
                if option_id:
                    ProductVariantOption.objects.filter(id=option_id).update(**option)
        # delete
        delete = data.pop('delete-external-data', None)
        if delete:
            for criterion_id in delete.get('criterions', []):
                ProductVariantCriterion.objects.filter(id=criterion_id, product_id=product).delete()
            for option_id in delete.get('options', []):
                print(option_id)
                ProductVariantOption.objects.filter(id=option_id).delete()
        
        serializer = self.serializer_class(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProductAPIView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data)

def create_product_variant(product_id):
    pass

class ProductImageViewSet(viewsets.ModelViewSet):
    pass

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]




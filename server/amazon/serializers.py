from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model=Users
        fields=('user_id','username','email','password','first_name','last_name','phone_number','user_type','created_at','is_golden')
        
    def create(self, data):
        
        user=Users.objects.create(
            user_id=data['user_id'],
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            user_type=data['user_type'],
        )
        user.set_password(data['password'])
        user.save()
        return user
        
    def validate(self, data):
        
        if Users.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("phone number already exists")
        
        return data
        
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model=Categories
        fields=('category_id','category_name')
        
    def validate(self, data):
        
        if Categories.objects.filter(category_name=data['category_name']).exists():
            raise serializers.ValidationError("Category already exists")
        
        return data
    
class SpecificationSerializer(serializers.ModelSerializer):
    
    class Meta:
    
        model=Specifications
        fields=('spec_id','color','dimensions','size','manufacturer','material','weight')
        
class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        user_id=UserSerializer(source='user_id',read_only=True)
        model = Addresses
        fields = ('address_id','user_id','first_name','last_name','phone_number','address','state','city','pincode','landmark','country','is_default')
        
    def to_representation(self, instance):

        data = super().to_representation(instance)
        user_instance = instance.user_id
        user_data = Users.objects.filter(user_id=user_instance.user_id)
        serializer = UserSerializer(user_data,many=True)
        data['user'] = serializer.data
        return data

class CardSerializer(serializers.ModelSerializer):
    
    class Meta: 
        
        user_id = UserSerializer(source='user_id',read_only=True)
        model = Cards
        fields = '__all__'
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        user_instance = instance.user_id
        user_data = Users.objects.filter(user_id=user_instance.user_id)
        serializer = UserSerializer(user_data,many=True)
        data['user'] = serializer.data
        return data
    
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        category_id = CategorySerializer(source="category_id",read_only=True)
        spec_id = SpecificationSerializer(source="spec_id",read_only=True)
        model = Products
        fields = ('product_id','product_name','spec_id','category_id','quantity','price','description')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        category_instance = instance.category_id
        spec_instance = instance.spec_id
        spec_data = Specifications.objects.filter(spec_id=spec_instance.spec_id)
        category_data = Categories.objects.filter(category_id=category_instance.category_id)
        spec_serializer = SpecificationSerializer(spec_data,many=True)
        category_serializer = CategorySerializer(category_data,many=True)
        data['specs'] = spec_serializer.data
        data['category'] = category_serializer.data
        return data
    
class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        user_id = UserSerializer(source = "user_id", read_only=True)
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = Carts 
        fields = ('cart_id', 'product_id', 'user_id', 'quantity', 'date_added', 'time_added')
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        user_instance = instance.user_id
        product_instance = instance.product_id
        user_data = Users.objects.filter(user_id = user_instance.user_id)
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['user_id'] = UserSerializer(user_data, many=True).data
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data
    
class WishlistSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        user_id = UserSerializer(source = "user_id", read_only=True)
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = Wishlists 
        fields = ('wishlist_id', 'product_id', 'user_id', 'date_added', 'time_added')
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        user_instance = instance.user_id
        product_instance = instance.product_id
        user_data = Users.objects.filter(user_id = user_instance.user_id)
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['user_id'] = UserSerializer(user_data, many=True).data
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        user_id = UserSerializer(source = "user_id", read_only=True)
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = Reviews 
        fields = ('review_id', 'product_id', 'user_id', 'rating', 'feedback', 'date_added', 'time_added')
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        user_instance = instance.user_id
        product_instance = instance.product_id
        user_data = Users.objects.filter(user_id = user_instance.user_id)
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['user_id'] = UserSerializer(user_data, many=True).data
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = ProductImages
        fields = ('product_image_id','product_id','image_name')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        product_instance = instance.product_id
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data
    
class ReviewImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = ReviewImages
        fields = ('review_image_id','product_id','image_name')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        product_instance = instance.product_id
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data
    
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        user_id = UserSerializer(source = "user_id", read_only=True)
        model = Orders
        fields = ('orders_id', 'user_id', 'discounts','total','grand_total', 'status', 'date_added','time_added')
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        user_instance = instance.user_id
        user_data = Users.objects.filter(user_id=user_instance.user_id)
        serializer = UserSerializer(user_data,many=True)
        data['user'] = serializer.data
        return data
    
class OrderDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        product_id = ProductSerializer(source = "product_id", read_only=True)
        model = OrderDetails
        fields = ('order_details_id', 'order_id', 'product_id', 'price', 'quantity')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        product_instance = instance.product_id
        product_data = Products.objects.filter(product_id = product_instance.product_id)
        data['product_id'] = ProductSerializer(product_data, many=True).data
        return data
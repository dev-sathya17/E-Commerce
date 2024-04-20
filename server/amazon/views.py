from .serializers import *
from .models import *
from .functions import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.

#Register
class Register(APIView):
    
    def post(self, request):
        user_data=request.data
        try:
            user_data['user_id'] = get_ID("Users",request.data["user_type"])
            serializer = UserSerializer(data=user_data)
            print(user_data)
            if serializer.is_valid():
                print("here")
                serializer.save()
                return Response(
                    {
                        "message": "Registered successfully",
                        "status": status.HTTP_201_CREATED,
                        'data':request.data
                    }
                )
        except Exception as e:
            print(e)
            return Response({'status': '500',
                            'message':'Invalid Registration'})
        return Response({'status':'something went wrong'})

# Login
class Login(APIView):
    
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message': 'Invalid Login'})
        user=authenticate(request,username=serializer.data['username'] , password=serializer.data['password'])
        if not user:
            return Response({'status': status.HTTP_403_FORBIDDEN,'message': 'Invalid Credentials'})
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'status': status.HTTP_200_OK, 'token': str(token), 'user_id':user.user_id, 'user_type':user.user_type,'message': 'Login successful'})

# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class Category(APIView):
    
    def get(self,request):
        
        categories=Categories.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        })
        
    def post(self,request):
        
        data=request.data
        data['category_id']= get_ID('Categories',"")
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED, 'message':"Category added successfully"})
    
@permission_classes([IsAuthenticated])    
class CategoryInfo(APIView):
    
    def get_object(self, category_id):
        try:
            return Categories.objects.get(category_id=category_id)
        except Categories.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def get(self,request,category_id):
        
        try:
            data=self.get_object(category_id)
        except Categories.DoesNotExist as e:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':"Category does not exist"})
        
        serializer = CategorySerializer(data)
        return Response({'status':status.HTTP_201_CREATED, 'data':serializer.data})
    
    def patch(self,request,category_id):
        
        category=self.get_object(category_id=category_id)
        serializer = CategorySerializer(category,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'message':'Category has been updated successfully'})
        
    def delete(self,request,category_id):
        
        category=self.get_object(category_id)
        category.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'Category has been deleted successfully'})
    
@permission_classes([IsAuthenticated])
class Specification(APIView):
    
    def get(self, request):
        
        data=Specifications.objects.all()
        serializer = SpecificationSerializer(data,many=True)
        return Response({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        })
    
    def post(self,request):
        
        try:
            specs_data = request.data
            specs_data['spec_id']=get_ID("Specifications","")
            serializer = SpecificationSerializer(data=specs_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'message':'Spec added successfully'
                })
        except Exception as e:
            return Response({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message':'There was an error'
            })
            
class SpecInfo(APIView):
    
    def get(self,request,spec_id):
        
        try:
            spec=Specifications.objects.get(spec_id=spec_id)
        except Specifications.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Spec not found'
            })
        serializer = SpecificationSerializer(spec)
        return Response({'status':status.HTTP_201_CREATED, 'data':serializer.data})
    
    def patch(self,request,spec_id):
        
        try:
            spec=Specifications.objects.get(spec_id=spec_id)
        except Specifications.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Spec not found'
            })
        serializer = SpecificationSerializer(spec,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'Spec updated successfully'})
        
    def delete(self,request,spec_id):
        
        try:
            spec = Specifications.objects.get(spec_id=spec_id)
        except Specifications.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Spec not found'
            })
        
        spec.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'Specification has been deleted successfully'})
        
@permission_classes([IsAuthenticated])
class Address(APIView):
    
    def get(self, request):
        
        data=Addresses.objects.all().select_related('user_id')
        serializer = AddressSerializer(data,many=True)
        return Response({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        })
    
    def post(self,request):
        
        try:
            address_data = request.data
            address_data['address_id']=get_ID("Address","")
            serializer = AddressSerializer(data=address_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'message':'Address added successfully'
                })
        except Exception as e:
            return Response({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message':'There was an error'
            })

@permission_classes([IsAuthenticated])  
class AddressInfo(APIView):
    
    def patch(self,request,address_id):
        
        try:
            address=Addresses.objects.get(address_id=address_id)
        except Addresses.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'address not found'
            })
        serializer = AddressSerializer(address,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'address updated successfully'})
        
    def delete(self,request,address_id):
        
        try:
            address = Addresses.objects.get(address_id=address_id)
        except Addresses.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Address not found'
            })
        
        address.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'Address has been deleted successfully'})
    
@permission_classes([IsAuthenticated])  
class GetUserAddresses(APIView):
    
    def get(self,request,user_id):
        
        user_data = Addresses.objects.filter(user_id=user_id)
        serializer = AddressSerializer(user_data,many=True)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})

@permission_classes([IsAuthenticated])  
class GetUserDefaultAddress(APIView):
    
    def get(self,request,user_id):
        
        user_data = Addresses.objects.filter(user_id=user_id,is_default=True)
        serializer = AddressSerializer(user_data)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
    
@permission_classes([IsAuthenticated])
class Card(APIView):
    
    def get(self, request):
        
        data=Cards.objects.all().select_related('user_id')
        serializer = CardSerializer(data,many=True)
        return Response({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        })
    
    def post(self,request):
        
        try:
            card_data = request.data
            card_data['card_id']=get_ID("Cards","")
            serializer = CardSerializer(data=card_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'message':'Card added successfully'
                })
            else:
                return Response({
                    'message':'Error creating card'
                })
        except Exception as e:
            return Response({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message':'There was an error'
            })
            
@permission_classes([IsAuthenticated])
class CardInfo(APIView):
    
    def patch(self,request,card_id):
        
        try:
            card=Cards.objects.get(card_id=card_id)
        except Cards.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'card not found'
            })
        serializer = CardSerializer(card,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'card updated successfully'})
        
    def delete(self,request,card_id):
        
        try:
            card = Cards.objects.get(card_id=card_id)
        except Cards.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'card not found'
            })
        
        card.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'card has been deleted successfully'})

@permission_classes([IsAuthenticated])  
class GetUserCards(APIView):
    
    def get(self,request,user_id):
        
        user_data = Cards.objects.filter(user_id=user_id)
        serializer = CardSerializer(user_data,many=True)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def validate_card(request):
    
    data=request.data
    card = Cards.objects.filter(Q(card_number=data['card_number']) & Q(pin=data['pin'],name=data['name']) & Q(expiry_date=data['expiry_date']) & Q(card_type=data['card_type']))
    if card :
        return Response({'status':status.HTTP_200_OK, 'valid':True})
    else:
        return Response({'status':status.HTTP_404_NOT_FOUND, 'valid':False})

@permission_classes([IsAuthenticated])
class Product(APIView):
    
    def get(self, request):
        
        data=Products.objects.all().select_related('spec_id','category_id')
        serializer = ProductSerializer(data,many=True)
        return Response({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        })
    
    def post(self,request):
        
        try:
            product_data = request.data
            product_data['product_id']=get_ID("Products","")
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':status.HTTP_201_CREATED,
                    'message':'Product added successfully'
                })
        except Exception as e:
            return Response({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message':'There was an error'
            })

@permission_classes([IsAuthenticated])
class ProductInfo(APIView):
    
    def get(self,request,product_id):
        try:
            product_data = Products.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'product not found'
                })
        serializer = ProductSerializer(product_data)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})    
    def patch(self,request,product_id):
        
        try:
            product=Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'product not found'
            })
        serializer = ProductSerializer(product,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'product updated successfully'})
        
    def delete(self,request,product_id):
        
        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'card not found'
            })
        
        product.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'product has been deleted successfully'})
    
@permission_classes([IsAuthenticated])
class Cart(APIView):
    
    def get(self,request):
        
        data = Carts.objects.all().select_related('user_id', 'product_id')
        print(data)
        serializer = CartSerializer(data, many=True)
        return Response({'status':status.HTTP_200_OK, 'message':serializer.data})
    
    def post(self,request):
        
        data = request.data
        data['cart_id'] = get_ID("Cart","")
        serializer = CartSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED, 'message':'Added to Cart successfully'})
        return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'some error occurred'})
    
@permission_classes([IsAuthenticated])
class CartOperations(APIView):
    
    def patch(self, request, cart_id):
        
        try:
            cart_item = Carts.objects.get(cart_id=cart_id)
        except Carts.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Cart Item not found'})
        
        serializer = CartSerializer(cart_item, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'message':'Cart Item updated successfully'})

@permission_classes([IsAuthenticated]) 
class CartInfo(APIView): 
    
    def get(self, request, user_id):
        
        try:
            data = Carts.objects.filter(user_id=user_id).select_related('user_id', 'product_id')
            serializer = CartSerializer(data, many=True)
            return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':e.message})
        
    def delete(self, request,user_id):
        
        try:
            cart_items = Carts.objects.filter(user_id=user_id)
        except Carts.DoesNotExist as e:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':e.message})
        
        cart_items.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'Cart item deleted successfully'})

@permission_classes([IsAuthenticated])
class Wishlist(APIView):
    
    def get(self,request):
        
        data = Wishlists.objects.all().select_related('user_id', 'product_id')
        serializer = WishlistSerializer(data, many=True)
        return Response({'status':status.HTTP_200_OK, 'message':serializer.data})
    
    def post(self,request):
        
        data = request.data
        data['wishlist_id'] = get_ID("Wishlist","")
        print(data)
        serializer = WishlistSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED, 'message':'Added to Wishlist successfully'})
        return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'some error occurred'})
        
@permission_classes([IsAuthenticated]) 
class WishlistInfo(APIView): 
    
    def get(self, request, user_id):
        
        try:
            data = Wishlists.objects.filter(user_id=user_id).select_related('user_id', 'product_id')
            serializer = WishlistSerializer(data, many=True)
            return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':e.message})
    
@permission_classes([IsAuthenticated]) 
class WishlistOperations(APIView):
    
    def delete(self, request, product_id):
        
        try:
            wishlist_item = Wishlists.objects.get(product_id=product_id)
        except Wishlists.DoesNotExist as e:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':e.message})
        
        wishlist_item.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'Product deleted from Wishlist successfully'})
    
@permission_classes([IsAuthenticated])
class Review(APIView):
    
    def get(self,request):
        
        data = Reviews.objects.all().select_related('user_id', 'product_id')
        serializer = ReviewSerializer(data, many=True)
        return Response({'status':status.HTTP_200_OK, 'message':serializer.data})
    
    def post(self,request):
        
        data = request.data
        data['review_id'] = get_ID("Reviews","")
        print(data)
        serializer = ReviewSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED, 'message':'Review was added successfully'})
        return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'some error occurred'})

@permission_classes([IsAuthenticated])
class ReviewOperations(APIView):
    
    def get(self,request,review_id):
        try:
            review_data = Reviews.objects.get(review_id=review_id)
        except Reviews.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'review not found'
                })
        serializer = ReviewSerializer(review_data)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})    
    
    def patch(self,request,review_id):
        
        try:
            review=Reviews.objects.get(review_id=review_id)
        except Reviews.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'review not found'
            })
        serializer = ReviewSerializer(review,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'review updated successfully'})
        
    def delete(self,request,review_id):
        
        try:
            review = Reviews.objects.get(review_id=review_id)
        except Reviews.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'card not found'
            })
        
        review.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'review has been deleted successfully'})

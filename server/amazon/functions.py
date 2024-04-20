from .models import *

def get_ID(tablename,role):
    if tablename=="Users":
        last_id = Users.objects.filter(user_type=role).order_by('-user_id').values()
        if role=="User":
            role="USR"
        elif role=="Admin":
            role = "ADM"
        elif role=="Retailer":
            role = "RET"
    elif tablename=="Categories":
        last_id = Categories.objects.all().order_by('-category_id').values()
    elif tablename=="Specifications":
        last_id = Specifications.objects.all().order_by('-spec_id').values()
    elif tablename=="Address":
        last_id = Addresses.objects.all().order_by('-address_id').values()
    elif tablename=="Cards":
        last_id = Cards.objects.all().order_by('-card_id').values()
    elif tablename=="Products":
        last_id = Products.objects.all().order_by('-product_id').values()
    elif tablename=="Cart":
        last_id = Carts.objects.all().order_by('-cart_id').values()
    elif tablename=="Wishlist":
        last_id = Wishlists.objects.all().order_by('-wishlist_id').values()
    elif tablename=="Reviews":
        last_id = Reviews.objects.all().order_by('-review_id').values()
    
    if len(last_id)==0:
        if role=="":
            if tablename=="Specifications" or tablename=="Cards" or tablename=="Products" or tablename=="Cart" or tablename=="Wishlist":
                Id=tablename[0:4].upper()+"000001"
            else:
                Id=tablename[0:3].upper()+"000001"
        else:
            Id= role[0:3].upper()+"000001"
        return Id
    else:
        if tablename=="Users":
            lastID=last_id[0].get('user_id')
        elif tablename=="Categories":
            lastID=last_id[0].get('category_id')
        elif tablename=="Specifications":
            lastID=last_id[0].get('spec_id')
        elif tablename=="Address":
            lastID=last_id[0].get('address_id')
        elif tablename=="Cards":
            lastID=last_id[0].get('card_id')
        elif tablename=="Products":
            lastID=last_id[0].get('product_id')
        elif tablename=="Cart":
            lastID=last_id[0].get('cart_id')
        elif tablename=="Wishlist":
            lastID=last_id[0].get('wishlist_id')
        elif tablename=="Reviews":
            lastID=last_id[0].get('review_id')
            
        if tablename=="Specifications" or tablename=="Cards" or tablename=="Products" or tablename=="Cart" or tablename=="Wishlist":
            prefix=lastID[0:4]
        else:
            prefix=lastID[0:3]
        val=lastID[-6:]
        newValue="00000"+str(int(val)+1)
        Id=prefix+newValue[-6:]
        return Id
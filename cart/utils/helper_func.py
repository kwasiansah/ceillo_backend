from cart.models import Cart

def get_or_create_cart(user):
    cart = Cart.objects.filter(customer=user).last()
    if not cart:
        cart = Cart.objects.create(customer=user)
    return cart

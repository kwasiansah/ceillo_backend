# import pytest
# import json
# from django.urls.base import reverse


# def test_post_cart(db, product, client, login_details):
#     cart = reverse("cart")
#     response = client.post(
#         path=cart,
#         HTTP_AUTHORIZATION="Bearer " + login_details[0],
#         data=json.loads(f'{"cart_items": [{"url_slug": {product}, "quantity": 6},]}'))
#     assert True


# def test_get_cart(db, client, login_details):
#     endpoint = reverse("cart")
#     response = client.get(
#         path=endpoint, HTTP_AUTHORIZATION="Bearer " + login_details[0])
#     import pdb
#     pdb.set_trace()
# assert response.status_code == 200

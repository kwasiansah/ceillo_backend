from django.http import JsonResponse


def error_404(request, exception):
    message = ('Api Endpoint Not Found')

    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = ('A Mistake From The Backend')

    response = JsonResponse(data={'message': message, 'status_code': 500
                                  })
    response.status_code = 500
    return response

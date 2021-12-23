from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    print(str(exc))
    print(str(context["view"]))

    handlers = {
        "ValidationError": _handle_generic_error,
        "Http404": _handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error,
        "InvalidToken": _handle_invalid,
    }

    response = exception_handler(exc, context)
    if response is not None:
        if "MyTokenObtainPairView" in str(context["view"]) and exc.status_code == 401:
            response.data = {"message": "No Active Accounts"}
            return response

        # response.data['status_code'] = int(response.status_code)
        # response.data['code'] = 500

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_authentication_error(exc, context, response):
    response.data = {"message": "Please Login To Proceed"}
    return response


def _handle_generic_error(exc, context, response):
    return response


def _handle_invalid(exc, context, response):

    return response

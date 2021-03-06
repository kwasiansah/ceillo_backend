"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Polls API')


schema_view = get_schema_view(
    openapi.Info(
        title="Ceillo API'S",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.ceillo.com/policies/terms/",
        contact=openapi.Contact(email="ceillogh@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("auth/", include("customer.urls")),
    path("products/", include("product.urls")),
    path("cart/", include("cart.urls")),
    path("search/", include("search.urls")),
    path("admin/", admin.site.urls),
    path("docs/", include_docs_urls(title="Polls API")),
    path("__debug__/", include(debug_toolbar.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "customer.utils.views.error_404"

handler500 = "customer.utils.views.error_500"

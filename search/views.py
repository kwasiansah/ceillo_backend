from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models import Q
from product.models import Product
from rest_framework import serializers, views
from rest_framework.response import Response
from product.serializers import ProductSerializer


class Search(views.APIView):
    class SearchSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()

    def post(self, request):
        query = request.data["query"]
        # q = Product.objects.filter(
        #     Q(name__icontains=query) | Q(description__icontains=query)
        # )[:6]

        # search_vector = SearchVector("name", "description")
        # search_query = SearchQuery(query)

        # q = Product.objects.annotate(search=SearchVector("name", "description")).filter(search=query)

        # q = Product.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by("-rank")
        # q = Product.objects.annotate(similarity=TrigramSimilarity("name", query)).filter(similarity__gt=0.3).order_by('-similarity')
        q = (
            Product.objects.annotate(
                similarity=TrigramSimilarity("name", query),
            )
            .filter(similarity__gt=0)
            .order_by("-similarity")
        )
        print(q.query)
        print(q.explain(analyze=True))
        # query_results = list(q)
        # results = []
        # for product in query_results:
        #     serializer = self.SearchSerializer(product)
        #     results.append(serializer.data)
        # return Response(data=results)
        serializer = ProductSerializer(q, many=True)
        data = {
            "results": serializer.data,
        }
        return Response(data=data)

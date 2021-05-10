from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from django.db.models import F
from decimal import Decimal
import operator
from django.contrib.postgres.search import SearchVector
from slugify import slugify

class ViloyatList(generics.ListAPIView):
    queryset = Viloyat.objects.all()
    serializer_class = ViloyatSerializer


class TumanList(generics.ListAPIView):
    queryset = Tuman.objects.all()
    serializer_class = TumanSerializer


class DorixonaList(generics.ListAPIView):
    queryset = Dorixona.objects.all()
    serializer_class = DorixonaSerializer

class DorixonaDetail(generics.RetrieveAPIView):
    queryset = Dorixona.objects.all()
    serializer_class = DorixonaSerializer


def yaqinlik_boyicha_filter(queryset, user_location):
    location_results = {}
    for dorixona in queryset:
        natija = Decimal(user_location) - dorixona.location_sum()
        if natija < 0:
            natija *= -1
        location_results[dorixona.id] = natija
    location_results = dict(sorted(location_results.items(), key=operator.itemgetter(1)))
    natijalar = [Dorixona.objects.get(id=int(id)) for id in location_results.keys()]

    return natijalar[:10]

def narx_boyicha_filter(queryset, dori_nomi):
    narx_results = {}
    for dorixona in queryset:
        for dori in dorixona.dorilar.all():
            if slugify(dori_nomi) in slugify(dori.nomi):
                narx_results[dorixona.id] = dori.narx
    narx_results = dict(sorted(narx_results.items(), key=operator.itemgetter(1)))
    natijalar = [Dorixona.objects.get(id=int(id)) for id in narx_results.keys()]
    return natijalar[:10]


@api_view(['GET'])
def dori_list(request):
    if request.method == 'GET':
        dorilar = Dori.objects.all()
        serializers = DoriSerializer(dorilar, many=True)
        query = request.GET.get('search')
        uzunlik = request.GET.get('uz')
        kenglik = request.GET.get('keng')
        if uzunlik and kenglik:
            uzunlik = Decimal(uzunlik)
            kenglik = Decimal(kenglik)
        location = uzunlik + kenglik
        if query:
            dorixonalar = []
            for dorixona in Dorixona.objects.all():
                for dori in dorixona.dorilar.all():
                    if slugify(query) in slugify(dori.nomi):
                        dorixonalar.append(dorixona)
                        
            filter = request.GET.get('filter')
            if filter == 'yaqin':
                dorixonalar = yaqinlik_boyicha_filter(dorixonalar, location)
            elif filter == 'narx':
                dorixonalar = narx_boyicha_filter(dorixonalar, query)
            elif filter == 'ikkovi':
                dorixonalar = yaqinlik_boyicha_filter(dorixonalar, location)
                dorixonalar = narx_boyicha_filter(dorixonalar, query)
            serializers = DorixonaSerializer(dorixonalar, many=True)
            return Response(serializers.data)
        else:
            return Response(serializers.data)

        
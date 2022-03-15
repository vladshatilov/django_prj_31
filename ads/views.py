from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

import csv
import json

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ads.models import Ads, Categories, User, City, Selections
from ads.permissions import UserAccessPermission, IsAdminOrOwner, IsAdminOrOwnerForSelections
from ads.serializers import CategorySerializer, CreateUserSerializer, AdsSerializer, UserSerializer, LocationSerializer, \
    AdUpdateSerializer, AdCreateSerializer, SelectionsDetailSerializer, SelectionsListSerializer, \
    SelectionsCreateSerializer
from main_avito import settings


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get(request):
    # Convert to JSON
    # with open('./datasets/ads.csv', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     rows = list(reader)
    # with open('./datasets/ads.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(rows, ensure_ascii=False, indent=4))
    # with open('./datasets/categories.csv', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     rows = list(reader)
    # with open('./datasets/categories.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(rows, ensure_ascii=False, indent=4))

    # Load data into model
    # with open('./ads/categories.json', encoding='utf-8') as data_file:
    #     json_data = json.loads(data_file.read())
    #     i = 1
    #     for item_data in json_data:
    #         item = Categories()
    #         item.id = item_data['id']
    #         item.name = item_data['name']
    #         item.slug = 'name' + str(i)
    #         i += 1
    #         item.save()
    # with open('./ads/ads.json', encoding='utf-8') as data_file:
    #     json_data = json.loads(data_file.read())
    #     for item_data in json_data:
    #         item = Ads()
    #         item.id = item_data['id']
    #         item.name = item_data['name']
    #         item.author = item_data['author']
    #         item.price = item_data['price']
    #         item.description = item_data['description']
    #         item.address = item_data['address']
    #         item.is_published = str2bool(item_data['is_published'])  # .replace("“", "")
    #         item.save()
    return JsonResponse({"status": "ok"}, status=200)


# Categories section
@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Categories
    queryset = Categories.objects.all()

    # serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # cats = Categories.objects.all()
        # cats = self.object_list.all()
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_list = paginator.get_page(page_number)
        cat_list = []
        for cat_item in page_list:
            cat_list.append({
                "id": cat_item.id,
                "name": cat_item.name
            })
        response = {
            # "items": cat_list,
            "items": CategorySerializer(page_list, many=True).data,
            "page_number": paginator.num_pages,
            "total": page_list.paginator.count
        }
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, *args, **kwargs):

        user_data = CategorySerializer(data=json.loads(request.body))
        if user_data.is_valid():
            user_data.save()
        else:
            return JsonResponse(user_data.errors)
        return JsonResponse(user_data.data, status=201)
        # try:
        #     data = json.loads(request.body)
        #     cat_item = Categories()
        #     cat_item.name = data["name"]
        #     cat_item.save()
        #     return JsonResponse({"id": cat_item.id, "name": cat_item.name}, status=201)
        # except Exception:
        #     return JsonResponse({"error": "incorrect payload"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetail(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            # cat_item = Categories.objects.get(pk=pk)
            cat_item = self.get_object()
            cat_list = []
            cat_list.append({
                "id": cat_item.id,
                "name": cat_item.name
            })
            return JsonResponse(cat_list, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
        except Categories.DoesNotExist:
            return JsonResponse({"error": "do not exist"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.body)
        self.object.name = data.get('name', self.object.name)
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDelete(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})


# Ads section
class Ad(ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get(self, request, *args, **kwargs):
        # Все объявления в переданных категориях
        filter_category = request.GET.getlist('cat', None)
        filter_cat_q = None
        for category in filter_category:
            if not filter_cat_q:
                filter_cat_q = Q(category_id__exact=category)
            else:
                filter_cat_q |= Q(category_id__exact=category)
        if filter_cat_q:
            self.queryset = self.queryset.filter(filter_cat_q)

        # Поиск по словам
        filter_text = request.GET.get('text', None)
        if filter_text:
            filter_text_q = Q(name__icontains=filter_text)
            filter_text_q |= Q(description__icontains=filter_text)
            self.queryset = self.queryset.filter(filter_text_q)

        # Поиск по локациям
        filter_location = request.GET.get('location', None)
        if filter_location:
            # self.queryset = self.queryset.filter(address__icontains=filter_location)
            self.queryset = self.queryset.filter(author_id__locations__name__icontains=filter_location)

        # Диапазон цен
        filter_price_above = request.GET.get('price_from', None)
        filter_price_under = request.GET.get('price_to', None)
        if filter_price_above:
            self.queryset = self.queryset.filter(price__gte=filter_price_above)
        if filter_price_under:
            self.queryset = self.queryset.filter(price__lte=filter_price_under)
        return super().get(request, *args, **kwargs)


class AdCreateView(CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)


class AdDetail(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name='dispatch')
class AdDetail2(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            # ad_item = Ads.objects.get(pk=kwargs['pk'])
            ad_item = self.get_object()
            ads_resp = {
                "id": ad_item.id,
                "name": ad_item.name,
                "author": ad_item.author,
                "price": ad_item.price,
                "description": ad_item.description,
                "address": ad_item.address,
                "is_published": ad_item.is_published
            }
            return JsonResponse(ads_resp, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
        except Ads.DoesNotExist:
            return JsonResponse({"error": "do not exist"}, status=404)


class AdsUpdate(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAdminOrOwner]


class AdsDelete(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAdminOrOwner]


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['poster']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.poster = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "poster": self.object.poster.url
        }, status=201)


# Selections section
class SelectionsListView(ListAPIView):
    queryset = Selections.objects.all()
    serializer_class = SelectionsListSerializer
    # serializer_class = SelectionsDetailSerializer


class SelectionsDetailView(RetrieveAPIView):
    queryset = Selections.objects.all()
    serializer_class = SelectionsDetailSerializer
    permission_classes = [IsAuthenticated]


class SelectionsCreateView(CreateAPIView):
    queryset = Selections.objects.all()
    serializer_class = SelectionsCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     print(request.user.id)
    #     return super().create(request, *args, **kwargs)


class SelectionsUpdateView(UpdateAPIView):
    queryset = Selections.objects.all()
    serializer_class = SelectionsCreateSerializer
    permission_classes = [IsAdminOrOwnerForSelections]


class SelectionsDeleteView(DestroyAPIView):
    queryset = Selections.objects.all()
    serializer_class = SelectionsCreateSerializer
    permission_classes = [IsAdminOrOwnerForSelections]


# # Users section
# class UserListView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserCreateView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = CreateUserSerializer


# @method_decorator(csrf_exempt, name='dispatch')
# class UserDetailView(DetailView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         try:
#             item = self.get_object()
#             user_item = [{
#                 "id": item.id,
#                 "username": item.username,
#                 "first_name": item.first_name,
#                 "last_name": item.last_name,
#                 "role": item.role,
#                 "age": item.age,
#                 "locations": list(map(str, item.locations.all()))
#             }]
#             return JsonResponse(user_item, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
#         except Ads.DoesNotExist:
#             return JsonResponse({"error": "do not exist"}, status=404)


# @method_decorator(csrf_exempt, name='dispatch')
# class UserUpdate(UpdateView):
#     model = User
#     fields = ['username', 'first_name', 'last_name', 'role', 'age', 'locations']
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         data = json.loads(request.body)
#         self.object.username = data.get("username", self.object.username)
#         self.object.first_name = data.get("first_name", self.object.first_name)
#         self.object.last_name = data.get("last_name", self.object.last_name)
#         self.object.role = data.get("role", self.object.role)
#         self.object.age = data.get("age", self.object.age)
#         self.object.save()
#         for city in data.get("locations", list(map(str, self.object.locations.all()))):
#             city_obj, _ = City.objects.get_or_create(name=city)
#             self.object.locations.add(city_obj)
#         self.object.save()
#         return JsonResponse({
#             "username": self.object.username,
#             "first_name": self.object.first_name,
#             "last_name": self.object.last_name,
#             "role": self.object.role,
#             "age": self.object.age,
#             "locations": list(map(str, self.object.locations.all()))
#         }, status=201)


# @method_decorator(csrf_exempt, name='dispatch')
# class UserDelete(DeleteView):
#     model = User
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({"status": "ok"})


# Location Section
class LocationViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = LocationSerializer

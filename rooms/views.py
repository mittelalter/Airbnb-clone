from ast import Try
from logging import exception
from math import fabs
from django.http import Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.urls import reverse
from django_countries import countries
from django.core.paginator import Paginator
from . import models
from . import forms


class HomeView(
    ListView
):  # 어떻게 이 HomeView가 room_list.html로 렌더되는지 이해할 수가 없음. #아마 Listview 때문에?

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# def room_detail(reqeust, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(reqeust, "rooms/room_detail.html", {"room": room})

#     except models.Room.DoesNotExist:
#         raise Http404


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                price = form.cleaned_data.get("price")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilites")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                rooms = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                qs = rooms.order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page")

                page_obj = paginator.get_page(page)

                return render(
                    request,
                    "rooms/room_search.html",
                    {"form": form, "rooms": rooms, "page_obj": page_obj},
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/room_search.html", {"form": form})


# # value값을 템플릿에 넘겨주지 않으면 프론트앤드에서 입력한 값이 기억되지 않는다.
# def search(request):

#     country = request.GET.get("country")

#     if country:
#         form = forms.SearchForm(request.GET)

#         if form.is_valid():
#             city = form.cleaned_data.get("city")
#             price = form.cleaned_data.get("price")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilites")

#             filter_args = {}

#             if city != "Anywhere":
#                 filter_args["city__startswith"] = city

#             filter_args["country"] = country

#             if room_type is not None:
#                 filter_args["room_type"] = room_type

#             if price is not None:
#                 filter_args["price__lte"] = price

#             if guests is not None:
#                 filter_args["guests__gte"] = guests

#             if bedrooms is not None:
#                 filter_args["bedrooms__gte"] = bedrooms

#             if beds is not None:
#                 filter_args["beds__gte"] = beds

#             if baths is not None:
#                 filter_args["baths__gte"] = baths

#             if instant_book is True:
#                 filter_args["instant_book"] = True

#             if superhost is True:
#                 filter_args["host__superhost"] = True

#             rooms = models.Room.objects.filter(**filter_args)

#             for amenity in amenities:
#                 rooms = rooms.filter(amenities=amenity)

#             for facility in facilities:
#                 rooms = rooms.filter(facilities=facility)

#     else:
#         form = forms.SearchForm()

#     return render(request, "rooms/room_search.html", {"form": form, "rooms": rooms})

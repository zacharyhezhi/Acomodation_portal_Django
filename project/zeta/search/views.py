# search/views.py
from django.db.models import Count, F, Q
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse

from users.models import CustomUser
from advertising.models import Calendar, Listing
from request.models import Booking, Request
from review.models import Review

from collections import defaultdict
from functools import reduce
import calendar
import operator

search_fields = {'city', 'check_in', 'check_out', 'accommodates', 'room_type',
                 'min_price', 'max_price', 'beds', 'bedrooms', 'bathrooms'}
request_fields = {'city', 'check_in', 'check_out', 'accommodates', 'room_type',
                  'min_price', 'max_price', 'beds', 'bedrooms', 'bathrooms'}

# save user search parameters into session
def update_session(request):
    if request.POST['search_type'] == 'listing':
        search_attributes = {}
        for key in request.POST.keys():
            if key in search_fields:
                if key == 'room_type':
                    search_attributes[key] = request.POST.getlist(key)
                else:
                    search_attributes[key] = request.POST[key]
        print(search_attributes)
        if search_attributes:
            request.session['search_attributes'] = search_attributes
    elif request.POST['search_type'] == 'request':
        request_attributes = {}
        for key in request.POST.keys():
            if key in request_fields:
                if key == 'room_type':
                    request_attributes[key] = request.POST.getlist(key)
                else:
                    request_attributes[key] = request.POST[key]
        print(request_attributes)
        if request_attributes:
            request.session['request_attributes'] = request_attributes
    return request

def controller(request):
    next_page = 'search:listing-results'
    if request.method == 'POST':
        # do the specified user operation
        if 'navigation' in request.POST:
            if request.POST['navigation'] == 'clean':
                if request.POST['search_type'] == 'listing' \
                   and 'search_attributes' in request.session:
                    del request.session['search_attributes']
                elif request.POST['search_type'] == 'request' \
                   and 'request_attributes' in request.session:
                    del request.session['request_attributes']
                    next_page = 'search:request-results'
            elif request.POST['navigation'] == 'apply':
                print("APPLYING FILTER")
                request = update_session(request)
                if request.POST['search_type'] == 'request':
                    next_page = 'search:request-results'
    return redirect(reverse(next_page))


def get_listing_filter(request):
    filter_kwargs = {}
    for key in request.session['search_attributes']:
        if key == 'room_type' and request.session['search_attributes'][key]:
            filter_kwargs[key + '__in'] = request.session['search_attributes'][key]
        elif key == 'min_price' and request.session['search_attributes'][key]:
            filter_kwargs['daily_price__gte'] = request.session['search_attributes'][key]
        elif key == 'max_price' and request.session['search_attributes'][key]:
            filter_kwargs['daily_price__lte'] = request.session['search_attributes'][key]
        elif key == 'city' and request.session['search_attributes'][key]:
            filter_kwargs[key + '__icontains'] = request.session['search_attributes'][key]
        elif not (key == 'check_in' or key == 'check_out') \
             and request.session['search_attributes'][key]:
            filter_kwargs[key + '__gte'] = request.session['search_attributes'][key]
    return filter_kwargs

# NOTE:
# The Calendar table stores monthly availability of each listing as string.
# The length of the string is the number of days in that particular month and year,
# in which each character represents the availability of that particular day,
# starting from the left (0:not available, 1:available). 
def get_available_listings(request):
    year, month, day = [int(x) for x in request.session['search_attributes']['check_in'].split('-')]
    check_out = [int(x) for x in request.session['search_attributes']['check_out'].split('-')]
    # create monthly mask(s) based on check in and check out date
    q_objects = Q()
    required_nb_of_months = 1
    while not [year, month] == check_out[:2]:
        days_in_month = calendar.monthrange(year, month)[1]
        curr_month_availability = ''.join(['1' for _ in range(days_in_month-day+1)])
        q_objects |= Q(year=year, month=month, days__regex=r'^.{'+str(day-1)+'}'+curr_month_availability)
        required_nb_of_months += 1
        day = 1
        month += 1
        if month > 12:
            month -= 12
            year += 1
    days_in_month = calendar.monthrange(year, month)[1]
    curr_month_availability = ''.join(['1' for _ in range(check_out[2]-day+1)])
    q_objects |= Q(year=year, month=month, days__regex=r'^.{'+str(day-1)+'}'+curr_month_availability)
    # filter calendar using the monthly mask(s) to find all of the available listings
    calendar_qs = Calendar.objects.filter(q_objects)
    calendar_qs = calendar_qs.values('listing_id').annotate(nb_of_months=Count('listing_id')).filter(nb_of_months=required_nb_of_months)
    listing_ids = calendar_qs.values_list('listing_id', flat=True)
    return listing_ids

def listing_results(request):
    listing_qs = None
    if 'search_attributes' in request.session:
        filter_kwargs = get_listing_filter(request)
        listing_qs = Listing.objects.filter(**filter_kwargs)
        if 'check_in' in request.session['search_attributes'] \
           and request.session['search_attributes']['check_in'] \
           and 'check_out' in request.session['search_attributes'] \
           and request.session['search_attributes']['check_out']:
            listing_ids = get_available_listings(request)
            listing_qs = listing_qs.filter(id__in=listing_ids)
    else:
        listing_qs = Listing.objects.all()
    return render(request, 'search/listing-results.html', {'listings':listing_qs})


def get_request_filter(request):
    filter_kwargs = {}
    for key in request.session['request_attributes']:
        if request.session['request_attributes'][key]:
            if key == 'room_type':
                filter_kwargs[key + '__in'] = request.session['request_attributes'][key]
            elif key == 'min_price':
                filter_kwargs['max_price__gte'] = request.session['request_attributes'][key]
            elif key == 'max_price':
                filter_kwargs['min_price__lte'] = request.session['request_attributes'][key]
            elif key == 'city':
                filter_kwargs[key + '__icontains'] = request.session['request_attributes'][key]
            elif key == 'check_in' or key == 'check_out':
                filter_kwargs[key] = request.session['request_attributes'][key]
            else:
                filter_kwargs[key + '__gte'] = request.session['request_attributes'][key]
    return filter_kwargs

def request_results(request):
    request_qs = None
    if 'request_attributes' in request.session:
        filter_kwargs = get_request_filter(request)
        request_qs = Request.objects.filter(**filter_kwargs)
    else:
        request_qs = Request.objects.all()
    return render(request, 'search/request-results.html', {'requests':request_qs})


def index(request):
    listing_qs = Listing.objects.order_by('id')[:3]
    return render(request, 'search/index.html', {'listings':listing_qs})

# request/views.py
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import UpdateView

from datetime import date
import re

from users.models import CustomUser
from advertising.models import Listing
from request.models import Booking, Request

excluded_keys = {'csrfmiddlewaretoken', 'stage', 'navigation'}
value_to_int  = {'accommodates', 'bedrooms', 'beds', 'bathrooms', 'min_price', 'max_price'}
value_is_list = {'amenities', 'access'}
request_field = {field.name for field in Request._meta.get_fields()} - {'visitor'} | {'visitor_id'}

# save user data for "create a request" into session
def update_session(request):
    print('\nrequest.POST')
    for key in set(request.POST.keys()) - excluded_keys:
        print(key, request.POST[key])
        if request.POST[key]:
            # convert value if necessary
            value = request.POST[key]
            if key in value_to_int:
                value = int(re.findall('\d+', request.POST[key])[0])
            # save session
            request.session[key] = request.POST.getlist(key) if key in value_is_list else value
    print('\nrequest.session')
    for key in request.session.keys():
        print(key, request.session[key])

# get next page for "create a request"
def get_next_page(request):
    stage = int(request.POST['stage'])
    if request.POST['navigation'] == 'back':
        if stage == 1:
            return 'request:place-a-request'
        else:
            stage -= 1
    elif request.POST['navigation'] == 'next':
        if stage == 8:
            return 'request:place-a-request'
        else:
            stage += 1
    return 'request:{0:02d}'.format(stage)

# clean session data for "create a request"
def clean_session(request):
    keys = list(request.session.keys())
    for key in keys:
        if key in request_field:
            del request.session[key]

# save session data for "create a request" into the Request database
def save_session(request):
    # consider user now as visitor and update the database record
    if not request.user.is_visitor:
        user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
        user.is_visitor = True
        user.save()
    request.session['visitor_id'] = request.session['_auth_user_id']
    obj = {key:request.session[key] for key in request.session.keys() if key in request_field}
    Request.objects.create(**obj)

def book_a_listing(request):
    # consider user now as visitor and update the database record
    if not request.user.is_visitor:
        user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
        user.is_visitor = True
        user.save()
    Booking.objects.create(check_in=request.session['search_attributes']['check_in'],
                           check_out=request.session['search_attributes']['check_out'],
                           listing_id=request.POST['listing_id'],
                           visitor_id=request.session['_auth_user_id'],
                           status='P')

def controller(request):
    next_page = 'request:place-a-request'
    kwargs = {}
    if request.method == 'POST':
        # if the request comes with any user data for "create a request"
        if 'stage' in request.POST:
            update_session(request)
            next_page = get_next_page(request)
        # else do the specified user operation
        elif 'navigation' in request.POST:
            if request.POST['navigation'] == 'proceed':
                next_page = 'request:01'
            elif request.POST['navigation'] == 'clean':
                print("CLEANING SESSION")
                clean_session(request)
            elif request.POST['navigation'] == 'save':
                if '_auth_user_id' in request.session:
                    print("SAVING SESSION")
                    save_session(request)
                    clean_session(request)
                    next_page = 'request:manage-requests'
                else:
                    print("PLEASE LOGIN TO CONTINUE")
                    messages.info(request, "PLEASE LOGIN TO CONTINUE")
            elif request.POST['navigation'] == 'book':
                next_page = 'advertising:listing-details'
                kwargs['listing_id'] = request.POST['listing_id']
                if '_auth_user_id' in request.session:
                    if 'search_attributes' in request.session \
                       and 'check_in' in request.session['search_attributes'] \
                       and request.session['search_attributes']['check_in'] \
                       and 'check_out' in request.session['search_attributes'] \
                       and request.session['search_attributes']['check_out']:
                        print("BOOK A LISTING")
                        book_a_listing(request)
                    else:
                        print("PLEASE DETERMINE CHECK IN & CHECK OUT DATE")
                else:
                    print("PLEASE LOGIN TO CONTINUE")
                    messages.info(request, "PLEASE LOGIN TO CONTINUE")
    return redirect(reverse(next_page, kwargs=kwargs))


def place_a_request(request):
    return render(request, 'request/place-a-request.html')

def place(request):
    return render(request, 'request/01-place.html')
def bedrooms(request):
    return render(request, 'request/02-bedrooms.html')
def bathrooms(request):
    return render(request, 'request/03-bathrooms.html')
def location(request):
    return render(request, 'request/04-location.html')
def amenities(request):
    return render(request, 'request/05-amenities.html')
def facilities(request):
    return render(request, 'request/06-facilities.html')
def description(request):
    return render(request, 'request/07-description.html')
def further_information(request):
    return render(request, 'request/08-further-information.html')


def manage_bookings(request):
    context = {}
    if request.user.is_provider:
        print('PROVIDER')
        listing_qs = Listing.objects.filter(provider_id=request.session['_auth_user_id'])
        listing_ids = listing_qs.values_list('id', flat=True)
        context['pending_enquiries']  = Booking.objects.filter(listing_id__in=listing_ids, status='P').order_by('-submitted_on')
        context['accepted_enquiries'] = Booking.objects.filter(listing_id__in=listing_ids, status='A').order_by('-submitted_on')
        context['declined_enquiries'] = Booking.objects.filter(listing_id__in=listing_ids, status='D').order_by('-submitted_on')
        context['canceled_enquiries'] = Booking.objects.filter(listing_id__in=listing_ids, status='C').order_by('-submitted_on')
    if request.user.is_visitor:
        print('VISITOR')
        context['pending_bookings']  = Booking.objects.filter(visitor_id=request.session['_auth_user_id'], status='P').order_by('-submitted_on')
        context['accepted_bookings'] = Booking.objects.filter(visitor_id=request.session['_auth_user_id'], status='A').order_by('-submitted_on')
        context['declined_bookings'] = Booking.objects.filter(visitor_id=request.session['_auth_user_id'], status='D').order_by('-submitted_on')
        context['canceled_bookings'] = Booking.objects.filter(visitor_id=request.session['_auth_user_id'], status='C').order_by('-submitted_on')
    return render(request, 'request/manage-bookings.html', context)

def delete_booking(request, booking_id):
    if '_auth_user_id' in request.session:
        print("DELETE BOOKING")
        booking = Booking.objects.get(pk=booking_id)
        # make sure this operation is done by the booking creator
        if booking.visitor_id == int(request.session['_auth_user_id']):
            booking.delete()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('request:manage-bookings'))

def cancel_booking(request, booking_id, as_provider):
    if '_auth_user_id' in request.session:
        print("CANCEL BOOKING")
        booking = Booking.objects.get(pk=booking_id)
        # make sure this operation is done by the booking creator
        # or the corresponding listing provider
        if booking.check_in > date.today() \
           and ((as_provider and booking.listing.provider_id == int(request.session['_auth_user_id']))\
           or (not as_provider and booking.visitor_id == int(request.session['_auth_user_id']))):
            booking.status = 'C'
            booking.save()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('request:manage-bookings'))

def accept_booking(request, booking_id):
    if '_auth_user_id' in request.session:
        print("ACCEPT BOOKING")
        booking = Booking.objects.get(pk=booking_id)
        # make sure this operation is done by the corresponding listing provider
        if booking.listing.provider_id == int(request.session['_auth_user_id']):
            booking.status = 'A'
            booking.save()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('request:manage-bookings'))

def decline_booking(request, booking_id):
    if '_auth_user_id' in request.session:
        booking = Booking.objects.get(pk=booking_id)
        # make sure this operation is done by the corresponding listing provider
        if booking.listing.provider_id == int(request.session['_auth_user_id']):
            booking.status = 'D'
            booking.save()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('request:manage-bookings'))


def manage_requests(request):
    context = {}
    context['requests'] = Request.objects.filter(visitor_id=request.session['_auth_user_id'])
    return render(request, 'request/manage-requests.html', context)

def request_details(request, request_id):
    request_qs = Request.objects.prefetch_related('visitor').get(pk=request_id)
    return render(request, 'request/request-details.html', {'request':request_qs})

class EditRequest(UpdateView):
    model = Request
    fields = ['title', 'description', 'accommodates', 'bedrooms', 'beds', 'bathrooms',
              'min_price', 'max_price']
    template_name = 'request/edit-request.html'

    def get_form(self, form_class=None):
        form = super(EditRequest, self).get_form(form_class)
        for field in form.fields:
            form.fields[field].required = False
        return form

    def get_object(self):
        request_id = None
        if self.request.user.is_authenticated:
            request = Request.objects.get(pk=self.kwargs['request_id'])
            if request.visitor_id == self.request.user.id:
                request_id = self.kwargs['request_id']
        return get_object_or_404(Request, pk=request_id)

    def get_success_url(self):
        return reverse('request:manage-requests')

def delete_request(request, request_id):
    if '_auth_user_id' in request.session:
        print("DELETE REQUEST")
        req = Request.objects.get(pk=request_id)
        # make sure this operation is done by the request creator
        if req.visitor_id == int(request.session['_auth_user_id']):
            req.delete()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('request:manage-requests'))

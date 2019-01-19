# advertising/views.py
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import UpdateView

from datetime import date
import hashlib
import os
import random
import re

from users.models import CustomUser
from advertising.models import Listing
from request.models import Booking
from review.models import Review

excluded_keys = {'csrfmiddlewaretoken', 'stage', 'navigation'}
value_to_bool = {'is_dedicated', 'instant_bookable', 'special_offer'}
value_to_int  = {'square_feet', 'accommodates', 'bedrooms', 'beds', 'bathrooms',
                 'minimum_nights', 'maximum_nights', 'daily_price', 'weekly_discount',
                 'monthly_discount', 'security_deposit', 'cleaning_fee', 'extra_people'}
value_is_list = {'amenities', 'access', 'requirements'}
value_is_rule = {'infants', 'children', 'pets', 'smoking', 'events', 'additional_rules'}
listing_field = {field.name for field in Listing._meta.get_fields()} - {'provider'} | {'provider_id'}

# save user data for "host a home" into session
def update_session(request):
    print('\nrequest.POST')
    house_rules = []
    for key in set(request.POST.keys()) - excluded_keys:
        print(key, request.POST[key])
        if request.POST[key]:
            # convert value if necessary
            value = request.POST[key]
            if key in value_to_int:
                value = int(re.findall('\d+', request.POST[key])[0])
            elif key in value_to_bool:
                value = True if request.POST[key][0] == 'y' else False
            # save user data into session
            if key == 'weekly_discount' or key == 'monthly_discount':
                discount = value
                new_key = key.strip('discount') + 'price'
                days = 7 if key[0] == 'w' else 30
                request.session[new_key] = request.session['daily_price'] * days * (100 - discount) / 100
            elif key in value_is_rule:
                house_rules += request.POST.getlist(key) if key == 'additional_rules' else [request.POST[key]]
            else:
                request.session[key] = request.POST.getlist(key) if key in value_is_list else value
    if house_rules:
        request.session['house_rules'] = house_rules
    if 'picture' in request.FILES and request.FILES['picture']:
        picture = request.FILES['picture']
        extension = picture.name[picture.name.rfind("."):]
        temp_picture_name = hashlib.sha256((picture.name + str(random.randint(0, 1024))).encode('utf-8')).hexdigest() + extension
        fs = FileSystemStorage()
        fs.save(temp_picture_name, picture)
        request.session['picture_url'] = fs.url(temp_picture_name)
    print('\nrequest.session')
    for key in request.session.keys():
        print(key, request.session[key])

# get next page for "host a home"
def get_next_page(request):
    stage = [int(x) for x in request.POST['stage'].split('-')]
    if request.POST['navigation'] == 'back':
        if stage[1] == 1:
            return 'advertising:become-a-host'
        else:
            stage[1] -= 1
    elif request.POST['navigation'] == 'next':
        if (stage[0] == 1 and stage[1] == 6) \
           or (stage[0] == 2 and stage[1] == 3) \
           or stage[0] == 3 and stage[1] == 11:
            return 'advertising:become-a-host'
        else:
            stage[1] += 1
    return 'advertising:{0:d}-{1:02d}'.format(stage[0], stage[1])

# clean session data for "host a home"
def clean_session(request):
    keys = list(request.session.keys())
    for key in keys:
        if key in listing_field:
            del request.session[key]

# save session data for "host a home" into the Listing database
def save_session(request):
    # consider user now as provider and update the database record
    if not request.user.is_provider:
        user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
        user.is_provider = True
        user.save()
    # extract all listing values from session and save into db
    request.session['provider_id'] = request.session['_auth_user_id']
    values = {key:request.session[key] for key in request.session.keys() if key in listing_field}
    obj = Listing.objects.create(**values)
    # rename listing photo based on the assigned pk and update db
    fs = FileSystemStorage()
    temp_picture_name = obj.picture_url.replace(fs.base_url, '')
    initial_path = settings.MEDIA_ROOT + '/' + temp_picture_name
    extension = temp_picture_name[temp_picture_name.rfind("."):]
    new_picture_name = 'listing_' + str(obj.pk) + extension
    new_path = settings.MEDIA_ROOT + '/' + new_picture_name
    os.rename(initial_path, new_path)
    request.session['picture_url'] = fs.url(new_picture_name)
    Listing.objects.filter(pk=obj.pk).update(picture_url=request.session['picture_url'])

def controller(request):
    next_page = 'advertising:become-a-host'
    if request.method == 'POST':
        # if the request comes with any user data for "host a home"
        if 'stage' in request.POST:
            update_session(request)
            next_page = get_next_page(request)
        # else clean session data or save them into the database
        elif 'navigation' in request.POST:
            if request.POST['navigation'] == 'clean':
                print("CLEANING SESSION")
                clean_session(request)
            elif request.POST['navigation'] == 'save':
                if '_auth_user_id' in request.session:
                    print("SAVING SESSION")
                    save_session(request)
                    clean_session(request)
                    next_page = 'advertising:manage-listings'
                else:
                    print("PLEASE LOGIN TO CONTINUE")
                    messages.info(request, "PLEASE LOGIN TO CONTINUE")
    return redirect(reverse(next_page))


def become_a_host(request):
    return render(request, 'advertising/become-a-host.html')

# Step 1: Start with the basics
def place(request):
    return render(request, 'advertising/step1-01-place.html')
def bedrooms(request):
    return render(request, 'advertising/step1-02-bedrooms.html')
def bathrooms(request):
    return render(request, 'advertising/step1-03-bathrooms.html')
def location(request):
    return render(request, 'advertising/step1-04-location.html')
def amenities(request):
    return render(request, 'advertising/step1-05-amenities.html')
def spaces(request):
    return render(request, 'advertising/step1-06-spaces.html')

# Step 2: Set the scene
def photos(request):
    return render(request, 'advertising/step2-01-photos.html')
def description(request):
    return render(request, 'advertising/step2-02-description.html')
def title(request):
    return render(request, 'advertising/step2-03-title.html')

# Step 3: Get ready for guests
def guest_requirements(request):
    return render(request, 'advertising/step3-01-guest-requirements.html')
def house_rules(request):
    return render(request, 'advertising/step3-02-house-rules.html')
def review_guest_requirements(request):
    return render(request, 'advertising/step3-03-review-guest-requirements.html')
def keep_calendar_up_to_date(request):
    return render(request, 'advertising/step3-04-keep-calendar-up-to-date.html')
def availability_settings(request):
    return render(request, 'advertising/step3-05-availability-settings.html')
def calendar(request):
    return render(request, 'advertising/step3-06-calendar.html')
def price(request):
    return render(request, 'advertising/step3-07-price.html')
def promotion(request):
    return render(request, 'advertising/step3-08-promotion.html')
def additional_pricing(request):
    return render(request, 'advertising/step3-09-additional-pricing.html')
def booking_scenarios(request):
    return render(request, 'advertising/step3-10-booking-scenarios.html')
def local_laws(request):
    return render(request, 'advertising/step3-11-local-laws.html')


def manage_listings(request):
    listing_qs = Listing.objects.filter(provider_id=request.session['_auth_user_id'])
    return render(request, 'advertising/manage-listings.html', {'listings':listing_qs})

def listing_details(request, listing_id):
    listing_qs     = Listing.objects.prefetch_related('provider').get(pk=listing_id)
    review_qs      = Review.objects.filter(listing_id=listing_id).prefetch_related('visitor')
    # get the average rating of the listing if any review(s) exist
    rating         = review_qs.aggregate(Avg('rating'))['rating__avg'] if review_qs else None
    # get the listing booking status of the authenticated user
    status         = None
    review_allowed = False
    if '_auth_user_id' in request.session:
        booking_qs  = Booking.objects.filter(listing_id=listing_id,
                                             visitor_id=request.session['_auth_user_id'])
        status = None
        for booking in booking_qs:
            if booking.status == 'P':
                status = 'P'
            elif booking.status == 'C':
                status = 'C'

        booking_qs = Booking.objects.filter(listing_id=listing_id,
                                            visitor_id=request.session['_auth_user_id'],
                                            check_out__lt=date.today(),
                                            status='A')
        review_allowed = True if booking_qs else False
    return render(request, 'advertising/listing-details.html', {'listing':listing_qs,
                                                                'reviews':review_qs,
                                                                'rating':rating,
                                                                'status':status,
                                                                'review_allowed':review_allowed})

class EditListing(UpdateView):
    model = Listing
    fields = ['title', 'summary', 'description', 'notes', 'neighbourhood_overview',
              'transit', 'minimum_nights', 'maximum_nights', 'instant_bookable',
              'daily_price', 'weekly_price', 'monthly_price', 'special_offer', 
              'security_deposit', 'cleaning_fee', 'extra_people']
    template_name = 'advertising/edit-listing.html'
    
    def get_form(self, form_class=None):
        form = super(EditListing, self).get_form(form_class)
        for field in form.fields:
            form.fields[field].required = False
        return form
    
    def get_object(self):
        listing_id = None
        if self.request.user.is_authenticated:
            listing = Listing.objects.get(pk=self.kwargs['listing_id'])
            if listing.provider_id == self.request.user.id:
                listing_id = self.kwargs['listing_id']
        return get_object_or_404(Listing, pk=listing_id)

    def get_success_url(self):
        return reverse('advertising:listing-details', kwargs={'listing_id':self.kwargs['listing_id']})

def delete_listing(request, listing_id):
    if '_auth_user_id' in request.session:
        print("DELETE LISTING")
        listing = Listing.objects.get(pk=listing_id)
        # make sure this operation is done by the listing owner
        if listing.provider_id == int(request.session['_auth_user_id']):
            # delete the listing's database record, along with its stored picture
            fs = FileSystemStorage()
            if fs.exists(settings.MEDIA_ROOT[:-6] + listing.picture_url):
                fs.delete(settings.MEDIA_ROOT[:-6] + listing.picture_url)
            listing.delete()
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    return redirect(reverse('advertising:manage-listings'))

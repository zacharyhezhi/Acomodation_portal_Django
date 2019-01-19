# review/views.py
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import UpdateView

from datetime import date

from advertising.models import Listing
from request.models import Booking
from review.models import Review

def user_has_finished_their_stay(listing_id, visitor_id):
    booking_qs = Booking.objects.filter(listing_id=listing_id,
                                        visitor_id=visitor_id,
                                        check_out__lt=date.today(),
                                        status='A')
    return True if booking_qs else False

def add_visitor_review(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_visitor:
            if user_has_finished_their_stay(request.POST['listing_id'], request.user.id):
                print("ADD VISITOR REVIEW")
                listing = Listing.objects.get(pk=request.POST['listing_id'])
                Review.objects.create(review_type=0,
                                      rating=0,
                                      content=request.POST['content'],
                                      listing_id=request.POST['listing_id'],
                                      provider_id=listing.provider_id,
                                      visitor_id=request.user.id)
            else:
                print("UNAUTHORIZED ACTION")
        else:
            print("PLEASE LOGIN TO CONTINUE")
        return redirect(reverse('advertising:listing-details',
                                kwargs={'listing_id':request.POST['listing_id']}))
    else:
        raise Http404("UNAUTHORIZED ACTION")

def delete_visitor_review(request, review_id):
    listing_id = None
    if request.user.is_authenticated and request.user.is_visitor:
        review = Review.objects.get(pk=review_id)
        listing_id = review.listing_id
        if user_has_finished_their_stay(review.listing_id, review.visitor_id):
            print("DELETE VISITOR REVIEW")
            # make sure this operation is done by the review creator
            if review.visitor_id == int(request.session['_auth_user_id']):
                review.delete()
            else:
                print("UNAUTHORIZED ACTION")
        else:
            print("UNAUTHORIZED ACTION")
    else:
        print("PLEASE LOGIN TO CONTINUE")
    if listing_id:
        return redirect(reverse('advertising:listing-details',
                                kwargs={'listing_id':listing_id}))
    else:
        raise Http404("UNAUTHORIZED ACTION")

class EditReview(UpdateView):
    model = Review
    fields = ['rating', 'content']
    template_name = 'review/edit-review.html'

    def get_form(self, form_class=None):
        form = super(EditReview, self).get_form(form_class)
        for field in form.fields:
            form.fields[field].required = False
        return form

    def get_object(self):
        review_id = None
        if self.request.user.is_authenticated:
            review = Review.objects.get(pk=self.kwargs['review_id'])
            if review.visitor_id == self.request.user.id:
                review_id = self.kwargs['review_id']
                self.listing_id = review.listing_id
        return get_object_or_404(Review, pk=review_id)

    def get_success_url(self):
        return reverse('advertising:listing-details',
                       kwargs={'listing_id':self.listing_id})

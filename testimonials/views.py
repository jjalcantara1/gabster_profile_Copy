from django.db.models import Avg

from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestimonialForm
from accounts.models import UserAccount
from django.contrib.auth.decorators import login_required


# def testimonials(request):
#     context = {
#         'testimonials': Testimonial.objects.all()
#     }
#     return render(request, 'testimonial/testimonials.html', context)


# Create your views here.
# class TestimonialListView(ListView):
#     model = Testimonial
#     queryset = Testimonial.objects.all()
#     template_name = 'testimonial/testimonials.html'
#     context_object_name = 'testimonials'
#     ordering = ['-date_posted']
#
#
# class TestimonialDetailView(DetailView):
#     model = Testimonial
#     template_name = 'testimonial/testimonial_detail.html'
#     context_object_name = 'testimonial'

@login_required
def add_testimonial(request, user_to_username):
    user_to = get_object_or_404(UserAccount, username=user_to_username)

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user_from = request.user
            testimonial.user_to = user_to
            testimonial.save()
            print("Testimonial saved successfully")
            form.cleaned_data['content'] = ""
            form.cleaned_data['rating'] = None  # Clear the rating field

            return redirect('view_testimonials', username=user_to_username)
        else:
            print("Form errors:", form.errors)
    else:
        form = TestimonialForm(initial={'user_to': user_to})

    return render(request, 'posts/testimonials.html', {'form': form})


def view_testimonials(request, user_to_username):
    user = get_object_or_404(UserAccount, username=user_to_username)
    testimonials_received = Testimonial.objects.filter(user_to=user).order_by('-createdAt')

    return render(request, 'testimonial/view_testimonial.html', {
        'user': user,
        'testimonials_received': testimonials_received,
    })


def testimonial_detail(request, user_to_username, testimonial_id):
    user = get_object_or_404(UserAccount, username=user_to_username)
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id, user_to=user)
    return render(request, 'testimonial/testimonial_detail.html', {'testimonial': testimonial})

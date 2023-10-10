from django.db.models import Avg


def calculate_average_rating(user):
    average_rating = user.testimonials_received.filter(rating__isnull=False).aggregate(Avg('rating__rating'))[
        'rating__rating__avg']
    return average_rating if average_rating is not None else 0

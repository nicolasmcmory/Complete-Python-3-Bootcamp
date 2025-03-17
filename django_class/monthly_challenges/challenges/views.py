from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

monthly_challenges = {
    "january": "Eat no meat for the entire month",
    "february": "Walk for at least 20 minutes every day!",
    "march": "Learn Django for at least 20 minutes every day!",
    "april": "Eat no meat for the entire month",
    "may": "Walk for at least 20 minutes every day!",
    "june": "Learn Django for at least 20 minutes every day!",
    "july": "Eat no meat for the entire month",
    "august": "Walk for at least 20 minutes every day!",
    "september": "Learn Django for at least 20 minutes every day!",
    "october": "Eat no meat for the entire month",
    "november": "Walk for at least 20 minutes every day!",
    "december": None,
}

# Create your views here.


def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())
    try:
        month = months[month - 1]
        redirect_path = reverse("month-challenge", args=[month])
        return HttpResponseRedirect(redirect_path)
    except:
        return HttpResponse("This month is not supported!")


def monthly_challenge(request, month):
    try:
        monthly_challenge = monthly_challenges[month]
        response_data = f"<h2>{monthly_challenge}</h2><br><a href='{reverse("index")}'>Back to Home</a>"
        return HttpResponse(response_data)
    except:  # KeyError:
        return HttpResponse("<h2>This month is not supported!</h2>")


def index(request):
    months_list = list(monthly_challenges.keys())
    response_data = "<ul>"
    for month in months_list:
        response_data += f"<li><a href='{reverse('month-challenge', args=[month])}'>{month.capitalize()}</a></li>"
    response_data += "</ul>"

    return HttpResponse(response_data)

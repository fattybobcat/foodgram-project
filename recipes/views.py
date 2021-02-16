import json
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    Ingredient,
    Recipe,
)



# Create your views here.
def index(request):
    #receip_list = Recipe.objects.select_related("author").all()
    #paginator = Paginator(post_list, 10)
    #page_number = request.GET.get("page")
    #page = paginator.get_page(page_number)
    latest = Recipe.objects.order_by('-pub_date')[:10]
    output = []
    for item in latest:
        output.append(item.title)
    #return HttpResponse('\n'.join(output))
    return render(request,
                  "index.html",
                  )
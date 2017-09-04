# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse

import random


# Create your views here.
def home(request):
    num = random.randint(1, 5)
    context = {
        "num": num
    }
    return render(request, "hello.html", context=context)

def randomNumbers(request):
    num = random.randint(1, 5)
    rand_list = []
    for i in range(num):
        rand_list.append(random.randint(1, 1000000))
    context = {
        "num": num,
        "item_list": rand_list
    }
    return render(request, "randNums.html", context=context)
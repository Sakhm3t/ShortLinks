from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from django.db import IntegrityError

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .models import Links

import random


def index(request):
    return render(request, 'linkcutter/base.html', {"invalid_link": request.session.get("invalid_link", None)})


def jump_to_target(request, short_link):
    try:
        redirect_link = Links.objects.get(short_link=short_link).full_link
        return redirect(redirect_link)
    except ObjectDoesNotExist as e:
        # call an appropriate renderer here
        return render(request, 'linkcutter/page_not_found.html')


def logout_view(request):
    logout(request)
    return render(request, 'linkcutter/base.html')


list_for_random = list(map(chr, range(ord("a"), ord("z"))))
list_for_random.extend(map(chr, range(ord("A"), ord("Z"))))
list_for_random.append(map(chr, range(ord("0"), ord("9"))))


def gen_short_link():
    """   Short link generation   """
    return ''.join([random.choice(list_for_random) for _ in range(0, 8)])


def try_to_insert_unique_short_link(request, full_link):
    """   Checking unique short link   """
    short_link = gen_short_link()
    full_short_link = f"{request.scheme}://{get_current_site(request)}/{short_link}"
    a = Links(full_link=full_link, short_link=short_link,
              user_id_id=request.user.id if request.user.is_authenticated else None)
    try:
        a.save()
    except IntegrityError as e:
        return None
    return full_short_link


def check_input_link(full_link):
    """   Checking input link   """
    validator = URLValidator()
    try:
        validator(full_link)
    except ValidationError:
        return False
    return True


def cutter(request):
    """   Link shortener   """
    full_link = request.POST["full_link"]
    if not check_input_link(full_link):
        request.session["invalid_link"] = "Wrong link. Try to input right link."
        return redirect("linkcutter:index")
    else:
        request.session["invalid_link"] = None

    full_short_link = None
    while not full_short_link:
        full_short_link = try_to_insert_unique_short_link(request, full_link)

    return render(request, 'linkcutter/cutter.html',
                  {"full_link": full_link, "cut_link": full_short_link})


class LoginUser(LoginView):
    """   Login existing users   """
    template_name = 'linkcutter/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('linkcutter:index')


class RegisterUserView(CreateView):
    """  Registration new users   """
    form_class = UserCreationForm
    template_name = 'linkcutter/register.html'
    success_url = reverse_lazy('linkcutter:login')


class LinksListView(LoginRequiredMixin, generic.ListView):
    """   Class shows links list (after login) """
    model = Links
    login_url = '/login/'
    paginate_by = 15
    template_name = 'linkcutter/links_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['absolute_short_url_prefix'] = f"{self.request.scheme}://{get_current_site(self.request)}/"
        return context

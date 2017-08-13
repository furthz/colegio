from django.views.generic import DetailView

from profiles.models import Profile

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from register.forms import PersonaForm


class CreatePersonaView(CreateView):

    model = Profile
    form_class = PersonaForm
    template_name = "create_persona.html"

    def form_valid(self, form):
        return super(CreatePersonaView, self).form_valid(form)

class PersonaDetail(DetailView):

    model = Profile
    template_name = "persona_detail.html"
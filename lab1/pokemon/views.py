from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from pokemon.forms import PokemonForm
from pokemon.models import Pokemon


def add_form_errors_to_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.warning(request, f'{form.fields[field].label}: {error}')





class EmailBackendService:
    def __init__(self):
        self.email_credentials = "Something something"
    def send_email(self, email,message):
        print(message)




def index(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            form = PokemonForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Pokemon created.")

            else:
                add_form_errors_to_messages(request, form)
            return redirect("index")

    pokemons = Pokemon.objects.all()
    for p in pokemons:
        p.form = PokemonForm(instance=p)

    user = request.user
    username = user.first_name if user.is_authenticated else "Anonymous user"
    context = {
        "username": username,
        "pokemons": pokemons,
        "create_form": PokemonForm(),
    }
    return render(request, "index.html", context)


@require_POST
def update_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    form = PokemonForm(request.POST, request.FILES, instance=pokemon)
    if form.is_valid():
        form.save()
        messages.success(request, "Pokemon updated.")
    else:
        add_form_errors_to_messages(request, form)
    return redirect("index")


@require_POST
def delete_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    pokemon.delete()
    messages.success(request, "Pokemon deleted.")
    return redirect("index")

def logout_request(request):
    logout(request)
    return redirect('/')
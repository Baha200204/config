from django.shortcuts import render
from .models import *
from django.utils.timezone import now
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    upcoming_games = Game.objects.all().filter(game_date__gte=now()).order_by('game_date')[:3]
    recent_news = News.objects.all().order_by('-news_date')[:3]
    spotlights = Team.objects.all().filter(top_player__isnull=False)
    return render(request, 'index.html', {'upcoming_games': upcoming_games, 'recent_news': recent_news, 'spotlights': spotlights})

def contacts(request):
    return render(request, 'contacts.html')

def standings(request):
    teams = Team.objects.all()
    standings = []
    for team in teams:
        wins = Game.objects.all().filter(home_team=team, home_team_score__gt=F('away_team_score')).count() + Game.objects.all().filter(away_team=team, away_team_score__gt=F('home_team_score')).count()
        losses = Game.objects.all().filter(home_team=team, home_team_score__lt=F('away_team_score')).count() + Game.objects.all().filter(away_team=team, away_team_score__lt=F('home_team_score')).count()
        standings.append({'team': team, 'wins': wins, 'losses': losses})
    standings = sorted(standings, key=lambda x: x['wins'], reverse=True)
    for i in range(len(standings)):
        standings[i]['rank'] = i + 1
    for team in standings:
        if team['wins'] + team['losses'] == 0:
            team['win_percentage'] = "-"
        else:
            team['win_percentage'] = team['wins'] / (team['wins'] + team['losses'])
    return render(request, 'standings.html', {'standings': standings})

def teams(request):
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})

def news(request):
    latest_news = News.objects.all().order_by('-news_date')[:8]
    return render(request, 'news.html', {'latest_news': latest_news})

def schedule(request):
    games = Game.objects.all().order_by('game_date')

    return render(request, 'schedule.html', {'games': games})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:home')  
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'sign_in.html')
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, str(form.errors))
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('core:home')

def team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    recent_matches = Game.objects.filter(away_team = team) | Game.objects.filter(home_team = team)
    players = Player.objects.filter(team_id = team)
    return render(request, 'team.html', {'team': team, 'games': recent_matches, 'players': players})

def article(request, news_id):
    article = get_object_or_404(News, news_id=news_id)
    return render(request, 'article.html', {'article': article})
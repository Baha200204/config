from django.db import models

class Coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    coach_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.coach_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, unique=True)
    coach_id = models.ForeignKey(Coach, related_name='teams', on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    top_player = models.ForeignKey('Player', related_name='top_player', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.team_name

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    game_date = models.DateTimeField()
    home_team_score = models.IntegerField(blank=True, null=True)
    away_team_score = models.IntegerField(blank=True, null=True)
    choices = [('Home', 'Home'), ('Away', 'Away')]
    home_or_away = models.CharField(max_length=100, choices=choices)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.game_date}"
    
class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    team_id = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, choices=[
        ('Point Guard', 'PG'),
        ('Shooting Guard', 'SG'), 
        ('Small Froward', 'SF'), 
        ('Power Forward', 'PF'), 
        ('Center', 'C')
        ])
    age = models.IntegerField(blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.player_name

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    news_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""
Views for GitHub Analyzer Application.
Handles fetching GitHub user data from API,
storing in database, and retrieving from DB.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import GitHubUser
import requests


def home(request):
    """
    Renders the home page where user can input a GitHub username.
    """
    return render(request, 'github_api/home.html')


def fetch_user_data(request):
    """
    Fetches GitHub user profile and repositories using GitHub API.
    Saves/updates the data in the database.
    Renders user details page on success.
    """
    if request.method == 'POST':
        username = request.POST.get('username')

        # Fetch user profile
        user_url = f'https://api.github.com/users/{username}'
        response = requests.get(user_url)

        if response.status_code == 404:
            messages.error(request, f'User "{username}" not found on GitHub.')
            return redirect('home')

        if response.status_code != 200:
            messages.error(request, f'Error fetching data: {response.status_code}')
            return redirect('home')

        user_data = response.json()

        # Save or update user in DB
        user, _ = GitHubUser.objects.update_or_create(
            username=user_data['login'],
            defaults={
                'name': user_data.get('name', ''),
                'public_repos': user_data['public_repos'],
                'followers': user_data['followers'],
                'following': user_data['following'],
                'created_at': parse_datetime(user_data['created_at']),
            }
        )

        # Fetch repositories
        repos_url = user_data['repos_url']
        repos_response = requests.get(repos_url)

        if repos_response.status_code != 200:
            messages.error(request, f'Error fetching repositories: {repos_response.status_code}')
            return redirect('home')

        repos_data = repos_response.json()

        # Prepare repository details
        repos_info = [
            {
                'name': repo['name'],
                'language': repo['language'],
                'stargazers_count': repo['stargazers_count'],
                'forks_count': repo['forks_count'],
                'updated_at': repo['updated_at'],
            }
            for repo in repos_data
        ]

        context = {
            'user': user_data,
            'repos': repos_info,
            'user_db': user,
        }

        return render(request, 'github_api/user_details.html', context)

    return redirect('home')


@csrf_exempt
def fetch_from_db(request):
    """
    Retrieves GitHub user data from the database if already stored.
    Renders user details page on success.
    """
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = GitHubUser.objects.get(username=username)
            context = {
                'user_db': user,
                'from_db': True,
            }
            return render(request, 'github_api/user_details.html', context)

        except GitHubUser.DoesNotExist:
            messages.error(request, f'User "{username}" not found in database.')
            return redirect('home')

    return redirect('home')

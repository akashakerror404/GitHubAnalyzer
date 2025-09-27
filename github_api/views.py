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




from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime

@csrf_exempt
@require_http_methods(["POST"])
def school_demo_request(request):
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Extract form data
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        school_name = data.get('schoolName', '').strip()
        school_type = data.get('schoolType', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not all([name, phone, school_name, school_type]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields: name, phone, schoolName, schoolType'
            }, status=400)
        
        # Create email subject and message
        subject = f"🎓 New School VR Demo Request - {school_name}"
        
        # HTML version for better formatting
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(45deg, #00FF87, #A855F7); color: white; padding: 30px 20px; text-align: center; }}
                .content {{ padding: 30px 20px; }}
                .field {{ margin-bottom: 20px; }}
                .label {{ font-weight: bold; color: #00FF87; font-size: 16px; display: block; margin-bottom: 8px; }}
                .message-box {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #A855F7; border-radius: 4px; }}
                .details {{ background: #f1f3f4; padding: 15px; border-radius: 8px; margin-top: 20px; }}
                .footer {{ margin-top: 30px; padding: 20px; background: #f9f9f9; font-size: 12px; color: #666; text-align: center; }}
                .info-item {{ margin-bottom: 8px; }}
                .highlight {{ color: #A855F7; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0; font-size: 28px;">🎓 New School VR Demo Request</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">MiraQ VR Education Program</p>
                </div>
                
                <div class="content">
                    <div class="field">
                        <span class="label">📧 Contact Information</span>
                        <div class="info-item"><strong>Name:</strong> {name}</div>
                        <div class="info-item"><strong>Phone:</strong> {phone}</div>
                        <div class="info-item"><strong>School:</strong> {school_name}</div>
                        <div class="info-item"><strong>School Type:</strong> <span class="highlight">{school_type}</span></div>
                    </div>
                    
                    <div class="field">
                        <span class="label">💬 Additional Message</span>
                        <div class="message-box">
                            {message if message else 'No additional message provided'}
                        </div>
                    </div>
                    
                    <div class="details">
                        <div class="field">
                            <span class="label">📋 Request Details</span>
                            <div class="info-item"><strong>Submission Type:</strong> School Demo</div>
                            <div class="info-item"><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                            <div class="info-item"><strong>Source:</strong> Website Form</div>
                            <div class="info-item"><strong>Priority:</strong> <span style="color: #00FF87; font-weight: bold;">High - Educational Institution</span></div>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <p style="margin: 0 0 10px 0;">This email was automatically generated from the MiraQ VR website.</p>
                    <p style="margin: 0; font-weight: bold;">⏰ Please respond to this inquiry within 24 hours.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version as fallback
        text_body = f"""
        NEW SCHOOL VR DEMO REQUEST
        
        Contact Information:
        • Name: {name}
        • Phone: {phone}
        • School: {school_name}
        • School Type: {school_type}
        
        Additional Message:
        {message if message else 'No additional message provided'}
        
        Request Details:
        • Submission Type: School Demo
        • Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        • Source: Website Form
        • Priority: High - Educational Institution
        
        ---
        This email was automatically generated from the MiraQ VR website.
        Please respond to this inquiry within 24 hours.
        """
        
        # Send email using SMTP
        try:
            email = EmailMessage(
                subject=subject,
                body=html_body,  # Use HTML body as primary content
                from_email='eshserala7@gmail.com',
                to=["miraq.vr@gmail.com"],
                reply_to=['eshserala7@gmail.com'],  # Use your actual email for replies
            )
            email.content_subtype = "html"  # This tells Django it's HTML content
            
            # Add alternative text version for email clients that don't support HTML
            email.alternatives = [
                (text_body, "text/plain")
            ]
            
            email.send(fail_silently=False)
            
            # Log the successful submission
            print(f"School demo request sent: {school_name} - {name} - {phone}")
            
            return JsonResponse({
                'success': True,
                'message': 'School demo request submitted successfully. We will contact you within 24 hours.',
                'data': {
                    'name': name,
                    'phone': phone,
                    'school_name': school_name,
                    'school_type': school_type,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as email_error:
            print(f"Email sending failed: {str(email_error)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to send email notification. Please try again later.'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Server error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def book_demo_request(request):
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Extract form data
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        source = data.get('source', 'website-demo-request')
        
        # Validate required fields
        if not all([name, phone]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields: name, phone'
            }, status=400)
        
        # Create email subject and message
        subject = f"🚀 New VR Demo Booking Request - {name}"
        
        email_body = f"""
        NEW VR DEMO BOOKING REQUEST
        
        Contact Information:
        • Name: {name}
        • Phone: {phone}
        • Source: {source}
        
        Customer Message:
        {message if message else 'No additional message provided'}
        
        Request Details:
        • Submission Type: VR Demo Booking
        • Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        • Priority: High - Demo Request
        
        ---
        This email was automatically generated from the MiraQ VR website.
        Please contact the customer within 24 hours to schedule their demo.
        """
        
        # HTML version for better formatting
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(45deg, #4FD9D6, #D700CE); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #4FD9D6; }}
                .message-box {{ background: #f5f5f5; padding: 15px; border-left: 4px solid #D700CE; }}
                .priority {{ background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107; }}
                .footer {{ margin-top: 20px; padding: 15px; background: #f9f9f9; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 New VR Demo Booking Request</h1>
                <p>MiraQ VR Experience Demo</p>
            </div>
            
            <div class="content">
                <div class="field">
                    <span class="label">Contact Information:</span><br>
                    • <strong>Name:</strong> {name}<br>
                    • <strong>Phone:</strong> {phone}<br>
                    • <strong>Source:</strong> {source}
                </div>
                
                <div class="field">
                    <span class="label">Customer Message:</span>
                    <div class="message-box">
                        {message if message else 'No additional message provided'}
                    </div>
                </div>
                
                <div class="priority">
                    <strong>🚨 High Priority - Demo Request</strong><br>
                    Please contact this potential customer within 24 hours to schedule their VR demo experience.
                </div>
                
                <div class="field">
                    <span class="label">Request Details:</span><br>
                    • <strong>Submission Type:</strong> VR Demo Booking<br>
                    • <strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    • <strong>Status:</strong> Awaiting Response
                </div>
            </div>
            
            <div class="footer">
                This email was automatically generated from the MiraQ VR website.<br>
                <strong>Action Required:</strong> Contact customer within 24 hours.
            </div>
        </body>
        </html>
        """
        
        # Send email using SMTP
        try:
            email = EmailMessage(
                subject=subject,
                body=html_body,
                from_email='eshserala7@gmail.com',
                to=["miraq.vr@gmail.com"],
                reply_to=[f"{name} <{name.replace(' ', '').lower()}@customer.demo>"],  # Fake email for reply-to
            )
            email.content_subtype = "html"  # Set content to HTML
            email.send(fail_silently=False)
            
            # Log the successful submission
            print(f"Demo booking request sent: {name} - {phone}")
            
            return JsonResponse({
                'success': True,
                'message': 'Demo request submitted successfully. We will contact you within 24 hours to schedule your VR experience.',
                'data': {
                    'name': name,
                    'phone': phone,
                    'source': source,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as email_error:
            print(f"Email sending failed: {str(email_error)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to send booking notification. Please try again later.'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Server error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
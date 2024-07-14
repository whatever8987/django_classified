from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('django_classified.urls', namespace='django_classified')),
    path('social/', include('social_django.urls', namespace='social')),
    path('email-sent/', TemplateView.as_view(template_name='users/email_sent.html')),
    path('register/', user_views.register, name='register'),
    path('add-credit/', user_views.add_credit, name='add_credit'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

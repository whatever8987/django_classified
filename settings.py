"""
Default settings for Django Classified app.
"""
from django.conf import settings

from django_classified import get_version

# Site currency
CURRENCY = getattr(settings, 'DCF_CURRENCY', 'USD')

# Display credits in footer
DISPLAY_CREDITS = getattr(settings, 'DCF_DISPLAY_CREDITS', False)

# Max items per page
ITEM_PER_PAGE = getattr(settings, 'DCF_ITEM_PER_PAGE', 40)

# Max items per user
ITEM_PER_USER_LIMIT = getattr(settings, 'DCF_ITEM_PER_USER_LIMIT', 20)

# Hide contact details for unauthorized users
LOGIN_TO_CONTACT = getattr(settings, 'DCF_LOGIN_TO_CONTACT', False)

# Max related items displayed on page
RELATED_LIMIT = getattr(settings, 'DCF_RELATED_LIMIT', 4)

# Max items included to the RSS feed
RSS_LIMIT = getattr(settings, 'DCF_RSS_LIMIT', 100)

# Site default description
SITE_DESCRIPTION = getattr(settings, 'DCF_SITE_DESCRIPTION', 'Classified Advertisements Powered by Django')

# Default site name
SITE_NAME = getattr(settings, 'DCF_SITE_NAME', 'Localrubmap')

# Sitemap items limit
SITEMAP_LIMIT = getattr(settings, 'DCF_SITEMAP_LIMIT', 1000)

# Display empty group in the groups list
DISPLAY_EMPTY_GROUPS = getattr(settings, 'DCF_DISPLAY_EMPTY_GROUPS', False)

VERSION = get_version()

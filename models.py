from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField
from unidecode import unidecode
from decimal import Decimal
from . import settings as dcf_settings
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(('Contact phone'), max_length=30, null=True, blank=True)
    receive_news = models.BooleanField(('Receive news'), default=True, db_index=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def allow_add_item(self):
        return self.user.item_set.count() < dcf_settings.ITEM_PER_USER_LIMIT
    
    def __str__(self):
        return f'{self.user.username}'
    
    def contact_phone(self):
        return self.user.profile.phone
    


    @staticmethod
    def get_or_create_for_user(user):
        if hasattr(user, 'profile'):
            return user.profile
        else:
            return Profile.objects.create(user=user)

    def save(self, *args, **kwargs):  # Add *args and **kwargs here
        super().save(*args, **kwargs)  # Pass *args and **kwargs to the super method


class Area(models.Model):
    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('area')
        verbose_name_plural = _('areas')
        
    def get_absolute_url(self):
        return reverse('django_classified:area')
    

    @classmethod
    def get_for_request(cls, request):
        if 'area_pk' in request.session:
            try:
                return cls.objects.get(pk=request.session['area_pk'])
            except cls.DoesNotExist:
                return None
        return None

    def set_for_request(self, request):
        request.session['area_pk'] = self.pk

    @classmethod
    def delete_for_request(cls, request):
        if 'area_pk' in request.session:
            del request.session['area_pk']


class Section(models.Model):
    title = models.CharField(_('title'), max_length=100)
    area = models.ForeignKey(Area, verbose_name=_('area'), on_delete=models.CASCADE, default=1)  # Set default to an existing Area instance or an appropriate default value

    def __str__(self):
        return self.title

    @cached_property
    def count(self):
        return Item.objects \
            .filter(is_active=True) \
            .filter(group__section=self) \

    class Meta:
        ordering = ['title']
        verbose_name = _('section')
        verbose_name_plural = _('sections')

class Group(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)
    section = models.ForeignKey('Section', verbose_name=_('section'), on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.section.title, self.title)

    @cached_property
    def count(self):
        return self.item_set.filter(is_active=True).count()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ['section__title', 'title', ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('django_classified:group', kwargs={'pk': self.pk, 'slug': self.slug})


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)



class Payment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        item_id = kwargs.pop('item_id', None)  # Get item_id from kwargs
        if item_id:
            from .models import Item  # Import Item model here to avoid circular import
            self.item = Item.objects.get(id=item_id)
        super().save(*args, **kwargs)


class Item(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_('group'), null=True, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_('area'), on_delete=models.CASCADE, null=True, blank=True)
    

    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(_('description'))
    phone = models.CharField(_('Contact phone'), max_length=30, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)
    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        if not self.is_active:
            return '[%s] %s' % (_('in active'), self.title)
        else:
            return self.title

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('-updated', )

    def get_absolute_url(self):
        return reverse('django_classified:item', kwargs={
            'pk': self.pk,
            'slug': self.slug
        })

    @cached_property
    def get_keywords(self):
        return ",".join(set(self.description.split()))

    @cached_property
    def contact_phone(self):
        return self.phone()

    @cached_property
    def image_count(self):
        return self.image_set.count()

    @cached_property
    def featured_image(self):
        return self.image_set.all().first()

    @cached_property
    def related_items(self):
        qs = Item.objects \
            .filter(is_active=True) \
            .filter(group=self.group) \
            .exclude(pk=self.pk)

        return qs[:dcf_settings.RELATED_LIMIT]
    
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new object
            user = self.user
            payment_amount = Decimal('10.0')  # Convert the float value to Decimal
            profile = user.profile  # Assuming you have a one-to-one relationship between User and Profile
            if profile.balance >= payment_amount:  # Check if the user has sufficient balance
                profile.balance -= payment_amount  # Deduct the payment amount from the user's balance
                profile.save()
                payment = Payment.objects.create(user=profile, amount=payment_amount, timestamp=timezone.now())
            else:
                raise ValueError("Insufficient balance")
        super().save(*args, **kwargs)

class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = ImageField(_('image'), upload_to='images')

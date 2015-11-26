import datetime
from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from tagging.fields import TagField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maxinum 250 characters.')
    slug = models.SlugField(unique=True,
                            help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/categories/%s/" % self.slug

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden')
    )

    # Core fields.
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateField(default=datetime.datetime.now)

    # Fileds to store generated HTML
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text="Suggested Value automatically generated from title. Must be unique")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)

    # Categorization
    categories = models.ManyToManyField(Category)
    tags = TagField(help_text="Seprate tags with spaces")

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)

        super(Entry, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), {
            'year': self.pub_date.strftime('%Y'),
            'month': self.pub_date.strftime('%m'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug
        })

class Link(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text='The name of the person whose site you spotted the link On')
    url = models.URLField(unique=True)

    post_by = models.ForeignKey(User)
    pub_date = models.DateField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')

    tags = TagField(help_text="Seprate tags with spaces")

    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)

    class Meta:
        ordering = ['-pub_date']

    def save(self, force_insert=False, force_update=False):
        if self.description:
            self.description_html = markdown(self.description)

        # if not self.id and self.post_elsewhere:
        #     print(u'Post %s to some where.' % self.title)

        super(Link, self).save(force_insert, force_update)

    def __unicode__(self):
        self.title

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), {
            'year': self.pub_date.strftime('%Y'),
            'month': self.pub_date.strftime('%m'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug
        })



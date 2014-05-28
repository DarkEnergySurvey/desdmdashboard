from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class DashboardBase(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='metrics')
    title = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        abstract = True


class DashboardSection(DashbaordBase):

    slug = models.SlugField()
    # use prepopulated_fields = {"slug": ("title",)} in admin

    text = models.TextField(blank=True, null=True)


class Snippet(models.Model):

    code = models.TextField()

    show_linenos = models.BooleanField(default=True)
    code_display_style = models.CharField(choices=STYLE_CHOICES,
            default='friendly', max_length=100)


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


class DashboardSection(DashboardBase):

    slug = models.SlugField()
    # use prepopulated_fields = {"slug": ("title",)} in admin

    text = models.TextField(blank=True, null=True)


'''
we do not use dashboard elements right now

class DashboardElement(DashboardBase):

    section = models.ForeignKey(DashboardSection)

    content = models.TextField()

    MARKDOWN_CONTENT_TYPE = 0
    PYTHON_CODE_CONTENT_TYPE = 1
    CONTENT_TYPE_CHOICES = (
            (MARKDOWN_CONTENT_TYPE, 'markdown'),
            (PYTHON_CODE_CONTENT_TYPE, 'python code'),
            )
    content_type = models.PositiveSmallIntegerField(
            choices=CONTENT_TYPE_CHOICES)

    show_linenos = models.BooleanField(default=True)
    code_display_style = models.CharField(choices=STYLE_CHOICES,
            default='friendly', max_length=100)
'''


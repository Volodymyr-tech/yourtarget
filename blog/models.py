import slugify
from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.

class BlogPsot(models.Model):

    PUBLISHED = 'Published'
    IN_WORK = 'In work'
    DELETED = 'Deleted'

    STATUS_CHOISES = [
        ('PUBLISHED', 'Published'),
        ('IN_WORK', 'In work') ,
        ('DELETED', 'Deleted' )
    ]

    title = models.CharField(max_length=155)
    meta_description = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, max_length=155, db_index=True, verbose_name='slug')
    content = RichTextField(config_name='awesome_ckeditor')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOISES, verbose_name='Post status', default=IN_WORK, blank=True)
    views = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Blog Post'
        #verbose_name_prular = 'Blog posts'
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)


    def __str__(self):
        return self.title



class CategoriesPost(models.Model):

    WEB_DEVELOPMENT_SEO = ' Web Development & SEO'
    ADVERTISING_PERFORMANCE = 'Advertising & Performance'
    SMM = 'SMM'
    AI_AUTOMATION = 'AI & Automation'

    CATEGORIES_NAMES_CHOICES = [
        ('WEB_DEVELOPMENT_SEO', ' Web Development & SEO'),
        ('ADVERTISING_PERFORMANCE', 'Advertising & Performance'),
        ('SMM', 'SMM'),
        ('AI_AUTOMATION', 'AI & Automation'),
    ]

    name = models.CharField(choices=CATEGORIES_NAMES_CHOICES, verbose_name='Category post name')


    class Meta:
        # db_table = os.getenv("NAME")
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


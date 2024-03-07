from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field


class BlogPost(models.Model):
    class Meta:
        verbose_name = "article de blog"
        verbose_name_plural = "articles de blog"
        ordering = ["-display_date"]

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    title = models.TextField(verbose_name="titre")
    tagline = models.TextField(null=True, blank=True, verbose_name="description courte")
    display_date = models.DateField(default=timezone.now, verbose_name="date affichée")
    body = CKEditor5Field(null=True, blank=True, verbose_name="contenu")
    published = models.BooleanField(default=False, verbose_name="publié")
    author = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="auteur",
        related_name="blog_posts",
    )

    @property
    def url_path(self):
        return f"/blog/{self.id}"

    def __str__(self):
        return f'Blog post "{self.title}"'

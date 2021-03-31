from django.db import models

# Create your models here.


class Faq(models.Model):

    de_question = models.CharField(
        max_length=200, verbose_name="Faq-question in german"
    )

    de_answer = models.TextField(max_length=500, verbose_name="Faq-answer in german")

    en_question = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Faq-question in english"
    )

    en_answer = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Faq-answer in english"
    )

from django.db import models
import uuid as uuid

# Create your models here.
class Wizard(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)

class Spell(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    wizard = models.ForeignKey(Wizard, on_delete=models.CASCADE, null=True, blank=True)

class Guild(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    spells = models.ManyToManyField(Spell)
    wizards = models.ManyToManyField(Wizard)

from django.db import models
import uuid as uuid


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


class Campus(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=12, null=False)


class Building(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256, null=False)
    campus = models.ForeignKey(Campus, null=True, related_name="buildings", on_delete=models.SET_NULL)


class Floor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256, null=False)
    building = models.ForeignKey(Building, null=False, related_name="floors", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

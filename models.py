from django.db import models

#Model profile
class ModelProfile(models.Model):
    name = models.CharField(max_length=140)
    weapon_skill = models.SmallIntegerField()
    ballistic_skill = models.SmallIntegerField()
    strength = models.SmallIntegerField()
    toughness = models.SmallIntegerField()
    wounds = models.SmallIntegerField()
    initiative = models.SmallIntegerField()
    attacks = models.SmallIntegerField()
    leadership = models.SmallIntegerField()
    armour_save = models.SmallIntegerField()

    def __unicode__(self):
        return self.name

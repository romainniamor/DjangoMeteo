from django.db import models


class Departement(models.Model):
    id_departement = models.SmallAutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=3)

    class Meta:
        managed = True
        db_table = 'departement'


class Prevision(models.Model):
    id_prevision = models.AutoField(primary_key=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_matin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_apres_midi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_nuit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pression_atmospherique = models.SmallIntegerField(blank=True, null=True)
    humidite = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=30)
    direction_vent = models.SmallIntegerField(blank=True, null=True)
    force_vent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    jour = models.DateField()
    last_update = models.DateField()
    id_ville = models.ForeignKey('Ville', models.DO_NOTHING, db_column='id_ville')

    class Meta:
        managed = True
        db_table = 'prevision'


class Ville(models.Model):
    id_ville = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=60, blank=True, null=True)
    id_departement = models.ForeignKey(Departement, models.DO_NOTHING, db_column='id_departement')
    code_postal = models.IntegerField()
    
    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'ville'


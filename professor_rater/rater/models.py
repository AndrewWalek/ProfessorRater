from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length = 256)
    module_code = models.CharField(max_length = 10, unique = True)

    def __str__(self):
        return self.name + ' (' + self.module_code + ')'

class Professors(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    professor_id = models.CharField(max_length = 10, unique = True)

    def __str__(self):
        return self.name + ' (' + self.professor_id + ')'

class ModuleInstances(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    year = models.IntegerField(
        validators = [MinValueValidator(0)]
    )
    semester = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(2)]
    )
    professors = models.ManyToManyField(Professors)

    def __str__(self):
        return self.module.name + ' ' + str(self.year) + ' ' + str(self.semester)

class Rating(models.Model):
    module = models.ForeignKey(ModuleInstances, on_delete = models.CASCADE)
    professor = models.ForeignKey(Professors, on_delete = models.CASCADE)
    rating = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.module.module.name + ' ' + self.professor.name + ' ' + str(self.rating)
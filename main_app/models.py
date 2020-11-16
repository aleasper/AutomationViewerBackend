from djongo import models

# Create your models here.
class TestModel(models.Model):
    name = models.CharField('Name', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Test model'
        verbose_name_plural = 'Test models'

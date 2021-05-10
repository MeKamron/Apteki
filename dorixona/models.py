from django.db import models
from decimal import Decimal

class Viloyat(models.Model):
    nomi = models.CharField('nomi', max_length=200)

    class Meta:
        verbose_name_plural = "Viloyatlar"

    def __str__(self):
        return self.nomi


class Tuman(models.Model):
    nomi = models.CharField('nomi', max_length=200)
    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.CASCADE,
        related_name="tumanlar")

    class Meta:
        verbose_name_plural = "Tumanlar"
    
    def __str__(self):
        return self.nomi



class Dorixona(models.Model):
    STATUS_CHOICES = (
        ('faol', 'Faol'),
        ('nofaol', 'Nofaol'),
        ('tekshirilmagan', 'Tekshirilmagan')
    )
    nomi = models.CharField(max_length=300)
    yuridik_nomi = models.CharField(max_length=300)
    logo = models.ImageField(upload_to="logolar/")
    ish_24_soat = models.BooleanField(default=True)
    manzil = models.CharField(max_length=400)
    telfon = models.CharField(max_length=20)
    xolati = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tekshirilmagan')
    uzunlik = models.CharField(max_length=100)
    kenglik = models.CharField(max_length=100)
    map_url = models.URLField(max_length=1000)
    qoshilgan = models.DateTimeField(auto_now_add=True)
    yangilangan = models.DateTimeField(auto_now=True)
    tuman = models.ForeignKey(Tuman, on_delete=models.CASCADE, related_name="dorixonalar")

    class Meta:
        verbose_name_plural = "Dorixonalar"

    def __str__(self):
        return self.nomi

    def location_sum(self):
        return Decimal(self.uzunlik) + Decimal(self.kenglik)

class Dori(models.Model):
    nomi = models.CharField('nomi', max_length=300)
    narx = models.DecimalField('narx', max_digits=10, decimal_places=2)
    dorixona = models.ForeignKey(Dorixona, on_delete=models.CASCADE, related_name="dorilar")

    class Meta:
        verbose_name_plural = "Dorilar"

    def __str__(self):
        return self.nomi
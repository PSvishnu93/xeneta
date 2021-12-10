from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey('Region', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return self.name

class Port(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16, unique=True)

    class Meta:
        db_table = 'port'

    def __str__(self) -> str:
        return self.name

class PortRegion(models.Model):
    port = models.ForeignKey('Port', null=True, on_delete=models.CASCADE, related_name='regions')
    region = models.ForeignKey('Region', null=True, on_delete=models.CASCADE, related_name='ports')

    class Meta:
        db_table = 'port_region'

    def __str__(self):
        return "{} - {}".format(self.port.name, self.region.name)

class Price(models.Model):
    origin = models.ForeignKey('Port', on_delete=models.CASCADE, related_name='port_origin')
    destination = models.ForeignKey('Port', on_delete=models.CASCADE, related_name='port_destination')
    day = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'price'

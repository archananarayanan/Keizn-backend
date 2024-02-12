from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique= True, primary_key=True, blank=False)
    
    def __str__(self):
        return str(self.name)
    
class Tags(models.Model):
    name = models.CharField(max_length=100, unique= True, primary_key=True, blank=False)
    
    def __str__(self):
        return str(self.name)
    
class Stock(models.Model):
    sku = models.CharField(max_length=10, unique= True, primary_key=True, blank=False)
    name = models.CharField(max_length=100, unique= True, blank=False)
    price = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.sku)
    

class Quantity(models.Model):
    sku = models.ForeignKey('Stock', on_delete=models.CASCADE)
    allocated = models.IntegerField(default=0)
    alloc_build = models.IntegerField(default=0)
    alloc_sales = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    incoming = models.IntegerField(default=0)
    build_order = models.IntegerField(default=0)
    net_stock = models.IntegerField(default=0)
    can_build = models.BooleanField(default=False)
    instock = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sku)
    
class TagMap(models.Model):
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)
    sku = models.ForeignKey('Stock', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tag', 'sku')

    


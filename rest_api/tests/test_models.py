from django.test import TestCase

from rest_api.models import Category, Quantity, Tags, Stock

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='test')

    def test_name_label(self):
        category = Category.objects.get(name='test')
        name = f'{category.name}'
        self.assertEqual(str(category), name)


class StockModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='test')
        cat = Category.objects.get(name="test")
        Stock.objects.create(sku='test', name="test", price=8, category=cat)

    def test_sku_label(self):
        stock = Stock.objects.get(name='test')
        sku = f'{stock.sku}'
        self.assertEqual(str(stock), sku)

class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Tags.objects.create(name='test')

    def test_name_label(self):
        tag = Tags.objects.get(name='test')
        name = f'{tag.name}'
        self.assertEqual(str(tag), name)

class QuantityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='test')
        cat = Category.objects.get(name="test")
        Stock.objects.create(sku='test', name="test", price=8, category=cat)
        st = Stock.objects.get(sku="test")
        Quantity.objects.create(sku=st, allocated=0, alloc_build=23, alloc_sales=2, available=1, incoming=1, build_order=2, net_stock=1, can_build=1, instock=786)

    def test_sku_label(self):
        stock = Quantity.objects.get(sku='test')
        sku = f'{stock.sku}'
        self.assertEqual(str(stock), sku)
   
from django.db import models
from django.core.urlresolvers import reverse
import datetime


class Filter(models.Model):
    title = models.CharField(max_length=30, default="")
    logo_url = models.CharField(max_length=250, default="")
    description = models.CharField(max_length=500)
    site = models.CharField(max_length=30, choices=(('ebay.co.uk','ebay.co.uk'),('ebay.com','ebay.com')), default='ebay.co.uk')
    search_text = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=30, choices=(('12576','Bussiness & Industrial'),('15032','Cell Phones & Accessories'),('58058','Computers/Tablets & Networking')), default='12576')
    min_price = models.FloatField(default=0)
    max_price = models.FloatField(default=1e+100)

    date_created = models.DateTimeField(default=datetime.datetime.now())
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Condition(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    cond_choices=(('New', 'New'), ('New other', 'New other'),
     ('Manufacturer refurbished', 'Manufacturer refurbished'),
     ('Seller refurbished', 'Seller refurbished'), ('Used', 'Used'),
     ('For parts or not working', 'For parts or not working'),
     ('Not specified', 'Not specified'))
    true_condition = models.CharField(max_length=30, choices=cond_choices)

    def __str__(self):
        return self.filter.title + ': condition - ' + self.true_condition

class Keyword(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    word = models.CharField(max_length=50, default="")
    is_numerical_range = models.BooleanField(default=False)
    is_in_front = models.BooleanField(default=False) # if it is numerical range then
    lower_limit = models.IntegerField(default=0)
    upper_limit = models.IntegerField(default=3000)
    logic = models.BooleanField(default=True)

    def __str__(self):
        return self.filter.title + ': Keyword (Positive=' + str(self.logic) + ') - ' + self.word


class Result(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    date_found = models.DateTimeField(default=datetime.datetime.now())
    time_left = models.CharField(max_length=20)
    price = models.CharField(max_length=15)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

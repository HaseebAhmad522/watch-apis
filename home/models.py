from django.db import models


class Watch(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField(default=None, null=True)
    # description = models.TextField(blank=True)x``
    brand = models.CharField(max_length=300)
    gender = models.CharField(max_length=100)
    # year = models.IntegerField(default=None, null=True)
    condition = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    band_color = models.CharField(max_length=300)

    # Additional Fields (Compulsory)
    listing_code = models.CharField(max_length=300)
    # model = models.CharField(max_length=100)
    # reference_number = models.CharField(max_length=200)
    # dealer_product_code = models.CharField(max_length=100)
    movement = models.CharField(max_length=300)
    # movement_caliber = models.CharField(max_length=255)
    # frequency = models.CharField(max_length=100)
    year_of_production = models.CharField(max_length=300)
    # scope_of_delivery = models.CharField(max_length=200)
    # location = models.CharField(max_length=200)
    # lug_width = models.CharField(max_length=200)
    # power_reserve = models.CharField(max_length=200)
    water_resistance = models.CharField(max_length=300)
    bracelet_color = models.CharField(max_length=300)
    availability = models.CharField(max_length=300)
    # base_caliber = models.CharField(max_length=200)
    case_material = models.CharField(max_length=300)
    bezel_material = models.CharField(max_length=300)
    bracelet_material = models.CharField(max_length=300)
    # case_diameter = models.CharField(max_length=200)
    # thickness = models.CharField(max_length=200)
    crystal = models.CharField(max_length=300)
    dial = models.CharField(max_length=300)
    clasp = models.CharField(max_length=300)
    clasp_material = models.CharField(max_length=300)
    # number_of_jewels = models.CharField(max_length=200)
    dial_numerals = models.CharField(max_length=300)
    # functions = models.TextField(blank=True)  # Using TextField for longer descriptions
    

    class Meta:
        ordering = ['id']


# class Watch(models.Model):
#     BRAND_CHOICES = [
#         ('Rolex', 'Rolex'),
#         ('Omega', 'Omega'),
#         ('Seiko', 'Seiko'),
#         ('Casio', 'Casio'),
#         ('Timex', 'Timex'),
#         ('Glashutte', 'Glashutte'),
#         ('Patek Philippe', 'Patek Philippe'),
#         ('Audemars Piguet', 'Audemars Piguet'),
#         ('Girard Perragaux', 'Girard Perragaux'),
#         ('Jaeger LeCoultre', 'Jaeger LeCoultre'),
#         ('IWC', 'IWC'),
#     ]
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     ]

#     CONDITION_CHOICES = [
#         ('Good', 'Good'),
#         ('Very Good', 'Very Good'),
#         ('New', 'New'),
#         ('Unknown', 'Unknown'),
#     ]

#     title = models.CharField(max_length=100, null=True, blank=True)
#     price = models.FloatField(null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     brand = models.CharField(max_length=100, choices=BRAND_CHOICES, null=True, blank=True)
#     gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True, blank=True)
#     year = models.IntegerField(null=True, blank=True)
#     condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, null=True, blank=True)
#     image = models.ImageField(upload_to='', default='watches/images/placeholder.png', null=True, blank=True)

#     # Additional Fields
#     listing_code = models.CharField(max_length=100, null=True, blank=True)
#     model = models.CharField(max_length=100, null=True, blank=True)
#     reference_number = models.CharField(max_length=100, null=True, blank=True)
#     dealer_product_code = models.CharField(max_length=100, null=True, blank=True)
#     movement = models.CharField(max_length=100, null=True, blank=True)
#     movement_caliber = models.CharField(max_length=100, null=True, blank=True)
#     frequency = models.CharField(max_length=100, null=True, blank=True)
#     year_of_production = models.IntegerField(null=True, blank=True)
#     scope_of_delivery = models.CharField(max_length=100, null=True, blank=True)
#     location = models.CharField(max_length=100, null=True, blank=True)
#     lug_width = models.CharField(max_length=100, null=True, blank=True)
#     power_reserve = models.CharField(max_length=100, null=True, blank=True)
#     water_resistance = models.CharField(max_length=100, null=True, blank=True)
#     bracelet_color = models.CharField(max_length=100, null=True, blank=True)
#     availability = models.CharField(max_length=100, null=True, blank=True)
#     base_caliber = models.CharField(max_length=100, null=True, blank=True)
#     case_material = models.CharField(max_length=100, null=True, blank=True)
#     bezel_material = models.CharField(max_length=100, null=True, blank=True)
#     bracelet_material = models.CharField(max_length=100, null=True, blank=True)
#     case_diameter = models.CharField(max_length=100, null=True, blank=True)
#     thickness = models.CharField(max_length=100, null=True, blank=True)
#     crystal = models.CharField(max_length=100, null=True, blank=True)
#     dial = models.CharField(max_length=100, null=True, blank=True)
#     clasp = models.CharField(max_length=100, null=True, blank=True)
#     clasp_material = models.CharField(max_length=100, null=True, blank=True)
#     number_of_jewels = models.CharField(max_length=100, null=True, blank=True)
#     dial_numerals = models.CharField(max_length=100, null=True, blank=True)
#     functions = models.CharField(max_length=100, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)












# class Watch(models.Model):
#     BRAND_CHOICES = [
#         ('Rolex', 'Rolex'),
#         ('Omega', 'Omega'),
#         ('Seiko', 'Seiko'),
#         ('Casio', 'Casio'),
#         ('Timex', 'Timex'),
#         ('Glashutte', 'Glashutte'),
#         ('Patek Philippe', 'Patek Philippe'),
#         ('Audemars Piguet', 'Audemars Piguet'),
#         ('Girard Perragaux', 'Girard Perragaux'),
#         ('Jaeger LeCoultre', 'Jaeger LeCoultre'),
#         ('IWC', 'IWC'),
#     ]
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     ]

#     CONDITION_CHOICES = [
#         ('Good', 'Good'),
#         ('Very Good', 'Very Good'),
#         ('New', 'New'),     
#         ('Unknown', 'Unknown'),

#     ]

#     title = models.CharField(max_length=100, null=True, blank=True)
#     price = models.FloatField(null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     brand = models.CharField(max_length=100, choices=BRAND_CHOICES, null=True, blank=True)
#     gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True, blank=True)
#     year = models.IntegerField(null=True, blank=True)
#     condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, null=True, blank=True)
#     image = models.ImageField(upload_to='', default='watches/images/placeholder.png', null=True, blank=True)

    # def __str__(self):
    #     return self.title
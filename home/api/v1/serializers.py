from rest_framework import serializers
from home.models import Watch
from django_filters import rest_framework as filters
import django_filters



class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = '__all__'


class WatchTitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Watch
        fields = ['title']



class WatchFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')


    class Meta:
        model = Watch
        fields = ['title', 'brand', 'movement', 'min_price', 'max_price']



# class WatchSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100, required=True)
#     price = serializers.FloatField(default=None, allow_null=True)
#     description = serializers.CharField(allow_blank=True)
#     brand = serializers.CharField(max_length=100)
#     gender = serializers.CharField(max_length=50)
#     year = serializers.IntegerField(default=None, allow_null=True)
#     condition = serializers.CharField(max_length=100)
#     image = serializers.CharField(max_length=200, required=True)

#     # Additional Fields (Compulsory)
#     listing_code = serializers.CharField(max_length=100, required=True)
#     model = serializers.CharField(max_length=100, required=True)
#     reference_number = serializers.CharField(max_length=100, required=True)
#     dealer_product_code = serializers.CharField(max_length=100, required=True)
#     movement = serializers.CharField(max_length=100, required=True)
#     movement_caliber = serializers.CharField(max_length=100, required=True)
#     frequency = serializers.CharField(max_length=100, required=True)
#     year_of_production = serializers.IntegerField(default=None, allow_null=True)
#     scope_of_delivery = serializers.CharField(max_length=100, required=True)
#     location = serializers.CharField(max_length=100, required=True)
#     lug_width = serializers.CharField(max_length=100, required=True)
#     power_reserve = serializers.CharField(max_length=100, required=True)
#     water_resistance = serializers.CharField(max_length=100, required=True)
#     bracelet_color = serializers.CharField(max_length=100, required=True)
#     availability = serializers.CharField(max_length=100, required=True)
#     base_caliber = serializers.CharField(max_length=100, required=True)
#     case_material = serializers.CharField(max_length=100, required=True)
#     bezel_material = serializers.CharField(max_length=100, required=True)
#     bracelet_material = serializers.CharField(max_length=100, required=True)
#     case_diameter = serializers.CharField(max_length=100, required=True)
#     thickness = serializers.CharField(max_length=100, required=True)
#     crystal = serializers.CharField(max_length=100, required=True)
#     dial = serializers.CharField(max_length=100, required=True)
#     clasp = serializers.CharField(max_length=100, required=True)
#     clasp_material = serializers.CharField(max_length=100, required=True)
#     number_of_jewels = serializers.CharField(max_length=100, required=True)
#     dial_numerals = serializers.CharField(max_length=100, required=True)
#     functions = serializers.CharField(allow_blank=True)




# class CSVUploadSerializer(serializers.Serializer):
#     csv_file = serializers.FileField()
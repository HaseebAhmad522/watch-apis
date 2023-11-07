import csv
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from home.models import Watch
from .serializers import WatchSerializer, WatchTitleFilter, WatchFilter
from django.db import models 
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']

        if file_obj.name.endswith('.csv'):
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                # Map column names in CSV to model field names
                field_mapping = {
                    "Title": "title",
                    "Image": "image",
                    "Brand": "brand",
                    "Model": "model",
                    "Reference number": "reference_number",
                    "Dealer product code": "dealer_product_code",
                    "Movement": "movement",
                    "Movement/caliber": "movement_caliber",
                    "Frequency": "frequency",
                    "Year of production": "year_of_production",
                    "Condition": "condition",
                    "Scope of delivery": "scope_of_delivery",
                    "Gender": "gender",
                    "Location": "location",
                    "Lug width": "lug_width",
                    "Power reserve": "power_reserve",
                    "Water resistance": "water_resistance",
                    "Bracelet color": "bracelet_color",
                    "Price": "price",
                    "Availability": "availability",
                    "Base caliber": "base_caliber",
                    "Case material": "case_material",
                    "Bezel material": "bezel_material",
                    "Bracelet material": "bracelet_material",
                    "Case diameter": "case_diameter",
                    "Thickness": "thickness",
                    "Crystal": "crystal",
                    "Dial": "dial",
                    "Clasp": "clasp",
                    "Clasp material": "clasp_material",
                    "Number of jewels": "number_of_jewels",
                    "Dial numerals": "dial_numerals",
                    "Functions": "functions",
                    "Description": "description"
                    # Add mappings for other fields
                }

                # Map column names to model field names
                mapped_row = {field_mapping.get(key, key): value for key, value in row.items()}

                # Handle the 'year_of_production' field
                year_of_production = row.get('Year of production')
                if year_of_production:
                    try:
                        year_of_production = int(year_of_production)
                    except ValueError:
                        year_of_production = None  # Set to None if not a valid integer
                else:
                    year_of_production = None
                mapped_row['year_of_production'] = year_of_production

                # Set default values for missing fields
                for field in Watch._meta.get_fields():
                    if field.name not in mapped_row:
                        if isinstance(field, models.CharField):
                            mapped_row[field.name] = 'not available'
                        elif isinstance(field, models.IntegerField):
                            mapped_row[field.name] = None

                serializer = WatchSerializer(data=mapped_row)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)

class FilterView(APIView, PageNumberPagination):

    def get(self, request):
        title = request.query_params.get('title', '')  # Get the title from query parameters
        watches = Watch.objects.filter(title__icontains=title)
        page = self.paginate_queryset(watches, request)
        if page is not None:
          serializer = WatchSerializer(page, many=True)
          return self.get_paginated_response(serializer.data)
        
        serializer = WatchSerializer(watches, many=True)
        return Response(serializer.data)
    
class WatchFilter(APIView, PageNumberPagination):
    # pagination_class = PageNumberPagination

    def get(self, request):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        # Check if both min_price and max_price are provided
        if not min_price or not max_price:
            return Response({'error': 'Both min_price and max_price are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            min_price = float(min_price)
            max_price = float(max_price)
        except ValueError:
            return Response({'error': 'Invalid price format, expected numbers'}, status=status.HTTP_400_BAD_REQUEST)

        if min_price >= max_price:
            return Response({'error': 'min_price should be less than max_price'}, status=status.HTTP_400_BAD_REQUEST)

        watches = Watch.objects.filter(price__range=(min_price, max_price))
        page = self.paginate_queryset(watches, request)
        if page is not None:
            serializer = WatchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = WatchSerializer(watches, many=True)
        return Response(serializer.data)

    # def get(self, request):
    #     min_price = request.query_params.get('min_price', '')
    #     max_price = request.query_params.get('max_price', '')
    #     watches = Watch.objects.filter(price__range=(min_price, max_price))
    #     serializer = WatchSerializer(watches, many=True)
    #     return Response(serializer.data)
    
class WatchListAPIView(APIView, PageNumberPagination):
    
    def get(self, request):
        # Get the query parameters from the request
        query_params = request.query_params

        # Apply sorting
        sort_by = query_params.get('sort', 'id')  # Default sorting by 'id' if not specified
        queryset = Watch.objects.all().order_by(sort_by)

        # Apply field selection
        fields = query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Filter fields in the serializer, not the queryset
            serializer = WatchSerializer(queryset, many=True, fields=fields)
        else:
            serializer = WatchSerializer(queryset, many=True)

        # Apply pagination
        page = self.paginate_queryset(serializer.data, request)
        if page is not None:
            return self.get_paginated_response(page)
        # page = int(query_params.get('page', 1))
        # limit = int(query_params.get('limit', 100))
        # start = (page - 1) * limit
        # end = page * limit
        # paginated_data = serializer.data[start:end]

        return Response(serializer.data)


    # def get(self, request):
    #     # Get the query parameters from the request
    #     query_params = request.query_params

    #     # Apply sorting
    #     sort_by = query_params.get('sort', 'id')
    #     queryset = Watch.objects.all().order_by(sort_by)

    #     # Apply field selection
    #     fields = query_params.get('fields')
    #     if fields:
    #         fields = fields.split(',')
    #         queryset = queryset.only(*fields)
    #     else:
    #         queryset = queryset.only()

    #     # Apply pagination
    #     page = int(query_params.get('page', 1))
    #     limit = int(query_params.get('limit', 100))
    #     queryset = queryset[(page - 1) * limit:page * limit]

    #     serializer = WatchSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # def get(self, request):
    #     price = request.query_params.get('price', '')  # Get the price from query parameters
    #     watches = Watch.objects.filter(price__icontains=price)
    #     serializer = WatchSerializer(watches, many=True)
    #     return Response(serializer.data)

# class CSVUploadView(APIView):

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES['file']

#         if file_obj.name.endswith('.csv'):
#             decoded_file = file_obj.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(decoded_file)

#             for row in reader:
#                 # Map column names in CSV to model field names
#                 field_mapping = {
#                 "Title": "title",
#                 "Image": "image",  # Adjust the field name as needed
#                 "Brand": "brand",
#                 "Model": "model",
#                 "Reference number": "reference_number",
#                 "Dealer product code": "dealer_product_code",
#                 "Movement": "movement",
#                 "Movement/caliber": "movement_caliber",
#                 "Frequency": "frequency",
#                 "Year of production": "year_of_production",
#                 "Condition": "condition",
#                 "Scope of delivery": "scope_of_delivery",
#                 "Gender": "gender",
#                 "Location": "location",
#                 "Lug width": "lug_width",
#                 "Power reserve": "power_reserve",
#                 "Water resistance": "water_resistance",
#                 "Bracelet color": "bracelet_color",
#                 "Price": "price",
#                 "Availability": "availability",
#                 "Base caliber": "base_caliber",
#                 "Case material": "case_material",
#                 "Bezel material": "bezel_material",
#                 "Bracelet material": "bracelet_material",
#                 "Case diameter": "case_diameter",
#                 "Thickness": "thickness",
#                 "Crystal": "crystal",
#                 "Dial": "dial",
#                 "Clasp": "clasp",
#                 "Clasp material": "clasp_material",
#                 "Number of jewels": "number_of_jewels",
#                 "Dial numerals": "dial_numerals",
#                 "Functions": "functions",
#                 "Description": "description"
#                     # Add mappings for other fields
#                 }

#                 # Map column names to model field names
#                 mapped_row = {field_mapping.get(key, key): value for key, value in row.items()}

#                 # Set default values for missing fields
#                 for field in Watch._meta.get_fields():
#                     if field.name not in mapped_row:
#                         if isinstance(field, models.CharField):
#                             mapped_row[field.name] = 'not available'
#                         elif isinstance(field, models.IntegerField):
#                             mapped_row[field.name] = None

#                 # Handle the 'image' field as a CharField (store the URL or data as needed)
#                 image_data = mapped_row['image']
#                 # Process the image_data and save it as a CharField

#                 serializer = WatchSerializer(data=mapped_row)
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)


    # def post(self, request, *args, **kwargs):
    #     file_obj = request.FILES['file']

    #     if file_obj.name.endswith('.csv'):
    #         decoded_file = file_obj.read().decode('utf-8').splitlines()
    #         reader = csv.DictReader(decoded_file)

    #         # Map column names in CSV to model field names
    #         field_mapping = {
    #             "Title": "title",
    #             "Image": "image",  # Adjust the field name as needed
    #             "Brand": "brand",
    #             "Model": "model",
    #             "Reference number": "reference_number",
    #             "Dealer product code": "dealer_product_code",
    #             "Movement": "movement",
    #             "Movement/caliber": "movement_caliber",
    #             "Frequency": "frequency",
    #             "Year of production": "year_of_production",
    #             "Condition": "condition",
    #             "Scope of delivery": "scope_of_delivery",
    #             "Gender": "gender",
    #             "Location": "location",
    #             "Lug width": "lug_width",
    #             "Power reserve": "power_reserve",
    #             "Water resistance": "water_resistance",
    #             "Bracelet color": "bracelet_color",
    #             "Price": "price",
    #             "Availability": "availability",
    #             "Base caliber": "base_caliber",
    #             "Case material": "case_material",
    #             "Bezel material": "bezel_material",
    #             "Bracelet material": "bracelet_material",
    #             "Case diameter": "case_diameter",
    #             "Thickness": "thickness",
    #             "Crystal": "crystal",
    #             "Dial": "dial",
    #             "Clasp": "clasp",
    #             "Clasp material": "clasp_material",
    #             "Number of jewels": "number_of_jewels",
    #             "Dial numerals": "dial_numerals",
    #             "Functions": "functions",
    #             "Description": "description"
    #         }

    #         for row in reader:
    #             # Map column names to model field names
    #             mapped_row = {field_mapping.get(key, key): value for key, value in row.items()}

    #             # Set default values for missing fields
    #             for field in Watch._meta.get_fields():
    #                 if field.name not in mapped_row:
    #                     if isinstance(field, models.CharField):
    #                         mapped_row[field.name] = 'not available'
    #                     elif isinstance(field, models.IntegerField):
    #                         mapped_row[field.name] = None

    #             serializer = WatchSerializer(data=mapped_row)
    #             if serializer.is_valid():
    #                 serializer.save()
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
     
    # def post(self, request, *args, **kwargs):
    #     file_obj = request.FILES['file']

    #     if file_obj.name.endswith('.csv'):
    #         decoded_file = file_obj.read().decode('utf-8').splitlines()
    #         reader = csv.DictReader(decoded_file)
    #         for row in reader:
    #             # Set default values for missing fields
    #             for field in Watch._meta.get_fields():
    #                 if field.name not in row:
    #                     if isinstance(field, models.CharField):
    #                         row[field.name] = 'not available'
    #                     elif isinstance(field, models.IntegerField):
    #                         row[field.name] = None

    #             serializer = WatchSerializer(data=row)
    #             if serializer.is_valid():
    #                 serializer.save()
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)



    # def post(self, request, *args, **kwargs):
    #     file_obj = request.FILES.get('file', None)

    #     if file_obj and file_obj.name.endswith('.csv'):
    #         decoded_file = file_obj.read().decode('utf-8').splitlines()
    #         reader = csv.DictReader(decoded_file)
    #         for row in reader:
    #             serializer = WatchSerializer(data=row)
    #             print(serializer)
    #             if serializer.is_valid():
    #                 serializer.save()
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)

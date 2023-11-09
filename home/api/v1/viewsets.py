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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import random
import pandas as pd
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField


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
                    # "Model": "model",
                    # "Reference number": "reference_number",
                    # "Dealer product code": "dealer_product_code",
                    "Movement": "movement",
                    # "Movement/caliber": "movement_caliber",
                    # "Frequency": "frequency",
                    "Year of production": "year_of_production",
                    "Condition": "condition",
                    # "Scope of delivery": "scope_of_delivery",
                    "Gender": "gender",
                    # "Location": "location",
                    # "Lug width": "lug_width",
                    # "Power reserve": "power_reserve",
                    "Water resistance": "water_resistance",
                    "Bracelet color": "bracelet_color",
                    "Price": "price",
                    "Availability": "availability",
                    # "Base caliber": "base_caliber",
                    "Case material": "case_material",
                    "Bezel material": "bezel_material",
                    "Bracelet material": "bracelet_material",
                    # "Case diameter": "case_diameter",
                    # "Thickness": "thickness",
                    "Crystal": "crystal",
                    "Dial": "dial",
                    "Clasp": "clasp",
                    "Clasp material": "clasp_material",
                    # "Number of jewels": "number_of_jewels",
                    "Dial numerals": "dial_numerals",
                    "Band Color": "band_color",
                    "Listing code": "listing_code",
                    
                    # "Functions": "functions",
                    # "Description": "description"
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

        # Apply filters based on user query parameters for all fields
        filter_params = {}

        model_fields = [field.name for field in Watch._meta.get_fields()]
        for key, value in query_params.items():
            if key in model_fields:
                filter_params[f"{key}__icontains"] = value

        # Apply filters directly using the filter method
        queryset = Watch.objects.filter(**filter_params)

        # Apply sorting
        sort_by = query_params.get('sort', 'id')  # Default sorting by 'id' if not specified
        queryset = queryset.order_by(sort_by)

        # Apply pagination
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serialized_data = WatchSerializer(page, many=True).data
            return self.get_paginated_response(serialized_data)

        # Serialize the queryset to JSON
        serialized_data = WatchSerializer(queryset, many=True).data

        return Response(serialized_data)
    

class RecommendationAPI(APIView):

    def post(self, request):
        # Get the user query from the request data
        user_query = request.data.get('title', '')  # Assuming the key is 'title', adjust as needed

        # Check if the user query is provided
        if not user_query:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Call the recommendation function
        result = self.get_top_recommendations(user_query)

        # Serialize the result and return it in the response
        serializer = WatchSerializer(result, many=True)
        return Response(serializer.data)

    
    def get_top_recommendations(self, user_query):
        # Your recommendation function implementation here
        # Initialize the TF-IDF vectorizer with the entire dataset
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(Watch.objects.values_list('title', flat=True))

        # Calculate cosine similarity between the user query and all items in the dataset
        user_query_vector = tfidf_vectorizer.transform([user_query])

        cosine_sim = linear_kernel(user_query_vector, tfidf_matrix)
#        print(cosine_sim[0][3655])
        print(cosine_sim[0])
        print(len(Watch.objects.values_list('title', flat=True)))
        wt = Watch.objects.values_list('id', flat=True)
        test_df = pd.DataFrame([wt,cosine_sim[0]]).T
        #print(test_df)
        test_df.columns=['Id','Similarity']
        print(max(cosine_sim[0]))
        #print(test_df)
        sort_df = test_df.sort_values(by=['Similarity'],ascending=False)
        print(sort_df)
        indices=list(sort_df['Id'][:200])

        
        # Find the index with the highest similarity (excluding the first, which is the query itself)
        max_similarity_index = cosine_sim[0][1:].argmax() + 1
        # Check if the highest similarity is below a threshold and shuffle the indices
        if cosine_sim[0][max_similarity_index] < 0.00001:
            np.random.shuffle(indices)
        # Get the top 10 recommendations (excluding the query itself)
        print(indices)
        top_indices = indices[0:100]
        ordering = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(top_indices)],
        default=Value(len(top_indices), output_field=IntegerField())
)
     
        # print("Filtered Watches:", Watch.objects.filter(pk__in=top_indices))

        return Watch.objects.filter(pk__in=top_indices).order_by(ordering)

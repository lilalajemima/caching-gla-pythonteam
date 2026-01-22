from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response  
from django.core.cache import cache           
from django.conf import settings              

from users.models import User
from users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        Overriding the default list method to add caching.
        """
        cache_key = 'user_list'
        
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print("Fetching from Cache ⚡")
            return Response(cached_data)
        
        print("Fetching from Database 🐢")
        response = super().list(request, *args, **kwargs)
        
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        
        return response
    
    def perform_create(self, serializer):
        # The list has changed, so the old cache is wrong. Delete it!
        cache.delete('user_list')
        print("Cache 'user_list' CLEARED! 🗑️") 
        super().perform_create(serializer)

    def perform_update(self, serializer):
        # A user changed, so the list might look different.
        cache.delete('user_list')
        print("Cache 'user_list' CLEARED! 🗑️")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        # A user was deleted.
        cache.delete('user_list')
        print("Cache 'user_list' CLEARED! 🗑️")
        super().perform_destroy(instance)
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response  
from django.core.cache import cache           
from django.conf import settings              

from users.models import User
from users.serializers import UserSerializer
from users.utils import cache_performance

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
            print("Fetching from Cache ")
            return Response(cached_data)
        
        print("Fetching from Database ")
        response = super().list(request, *args, **kwargs)
        
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        
        return response
    
    def perform_create(self, serializer):
        
        cache.delete('user_list')
        print("Cache 'user_list' CLEARED! ") 
        super().perform_create(serializer)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        
        # 1. Update the main list (Write-Through)
        fresh_list = self.get_serializer(self.get_queryset(), many=True).data
        cache.set('user_list', fresh_list, timeout=settings.CACHE_TTL)
        
        # 2. Update the individual user cache (Write-Through)
        user_id = serializer.instance.id
        fresh_user_data = serializer.data
        cache.set(f"user_{user_id}", fresh_user_data, timeout=settings.CACHE_TTL)
        
        print(f"Cache for 'user_{user_id}' and 'user_list' UPDATED ")

    def perform_destroy(self, instance):
        # A user was deleted.
        cache.delete('user_list')
        print("Cache 'user_list' CLEARED! ")
        super().perform_destroy(instance)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk') 
        
        cache_key = f"user_{user_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"Fetching User {user_id} from Cache ⚡")
            return Response(cached_data)
            
        print(f"Fetching User {user_id} from Database 🐢")
        response = super().retrieve(request, *args, **kwargs)
        
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response
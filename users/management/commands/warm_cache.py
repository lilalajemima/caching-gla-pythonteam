import time
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
from users.models import User
from users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Warms up the Redis cache with essential data'

    def handle(self, *args, **options):
        self.stdout.write("Starting cache warm-up...")
        start_time = time.time()

        # 1. Fetch all data from DB
        users = User.objects.all()
        
        # 2. Serialize it (convert to JSON format)
        serializer = UserSerializer(users, many=True)
        
        # 3. Store in Redis
        cache.set('user_list', serializer.data, timeout=settings.CACHE_TTL)

        duration = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f" Successfully cached {users.count()} users in {duration:.2f} seconds!"))
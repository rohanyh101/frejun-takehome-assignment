from django.core.management.base import BaseCommand
from rooms.models import Room


class Command(BaseCommand):
    help = 'Create initial room data as per requirements'

    def handle(self, *args, **options):
        """Create the 15 rooms as specified in requirements:
        - 8 Private Rooms
        - 4 Conference Rooms  
        - 3 Shared Desks (each allows up to 4 users)
        """
        
        # Delete existing rooms
        Room.objects.all().delete()
        
        rooms_to_create = []
        
        # Create 8 Private Rooms (capacity 1)
        for i in range(1, 9):
            rooms_to_create.append(Room(
                room_number=f"P{i:02d}",
                room_type='PRIVATE',
                capacity=1
            ))
        
        # Create 4 Conference Rooms (capacity varies, but typically larger)
        for i in range(1, 5):
            rooms_to_create.append(Room(
                room_number=f"C{i:02d}",
                room_type='CONFERENCE',
                capacity=8  # Assuming 8 person capacity for conference rooms
            ))
        
        # Create 3 Shared Desks (capacity 4 each)
        for i in range(1, 4):
            rooms_to_create.append(Room(
                room_number=f"S{i:02d}",
                room_type='SHARED',
                capacity=4
            ))
        
        # Bulk create all rooms
        Room.objects.bulk_create(rooms_to_create)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(rooms_to_create)} rooms:\n'
                f'- 8 Private Rooms (P01-P08)\n'
                f'- 4 Conference Rooms (C01-C04)\n'
                f'- 3 Shared Desks (S01-S03)'
            )
        )

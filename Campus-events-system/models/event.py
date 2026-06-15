import uuid
from datetime import datetime


class Event:
    
    def __init__(self, name, date, location, capacity, organizer_id = None):
        self.event_id = str(uuid.uuid4())[:8]
        self.name = name   
        self.date = date  # store as string "DD-MM-YYYY"
        self.location = location
        self.capacity = capacity
        self.organizer_id = organizer_id
        self.attendees = []

    def is_full(self):
        return len(self.attendees) >= self.capacity
    
    def spots_left(self):
        return self.capacity - len(self.attendees)

    def __str__(self):
        return (f"[{self.event_id}] {self.name} | {self.date}"
                f"{self.location} | {len(self.attendees)}/{self.capacity} attendees")

class Eventmanager:
    """Handles all event operations - create, update, delete, view"""

    def __init__(self):
        self.events = []

    # --- Add ---
    def create_event(self):
        print("\n---- Create New Event ----")

        name = input("Event name: ").strip()
        if not name:
            print("   Error: Event name cannot be empty")
            return
        
        # Validate date format
        date_str = input("Date (DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            print("   Error: Invalid date format: Use DD-MM-YYYY")
            return
        
        # Enter location
        location = input("Location: ").strip()
        if not location:
            print("   Error: Location cannot be empty")
            return
        
        # Validate capacity
        capacity_str = input("Capacity (max attendees): ").strip()
        if not capacity_str.isdigit() or int(capacity_str) <= 0:
            print("   Error: Capacity must be a positive number.")
            return

        event = Event(name, date_str, location, int(capacity_str))
        self.events.append(event)
        print(f"\n ✓ Event '{name}' created successfully! (ID: {event.event_id})")

    def view_all_events(self):
        if not self.events:
            print("\n No events found")
            return
        
        print("\n---- All events -----")
        for i, event in enumerate(self.events, 1):
            print(f"  {i}. {event}")

    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event
            return None
        
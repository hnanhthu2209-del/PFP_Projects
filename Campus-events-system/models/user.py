class User:
    
    def __init__(self, user_id, name, password): #with 'self', the data saves to the object permanently
        self.user_id = user_id
        self.name = name
        self.password = password
        self.role = "user"
    
    def get_role(self):
        return self.role
    
    def get_menu(self):
        return []

    def __str__(self): #Defines how your object looks when printed
        return f"[{self.role.upper()}] {self.name} (ID: {self.user_id})"
    

class Admin (User):
    
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password) #inheriting from a parent and add extra
        self.role = "admin"

    def get_menu(self):
        return [
            "Create event",
            "Update event",
            "Delete event",
            "View all event",
            "View attendees for an event",
            "Export report to CSV",
            "Logout",
        ]


class Organizer(User):
    
    def __init__(self, user_id, name, password, assigned_events = None):
        super().__init__(user_id, name, password)
        self.role = "organizer"
        self.assigned_events = assigned_events or [] #used to add assigned events with attendees or check exist event

    def get_menu(self):
        return [
            "View my events"
            "View attendees for my events",
            "Remove an attendee",
            "Logout",
        ]
    
class Student(User):

    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.role = "student"
        self.registered_events = []  #list of event IDs, enter the events has registered

    def get_menu(self):
        return [
            "Browse all events",
            "Search events",
            "Register for an event",
            "View my registered events",
            "Cancel a registration",
            "Logout",
        ]


    

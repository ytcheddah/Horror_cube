

class UserInterface:
    """A parent class which provides a framework for all classes 
    displayed on the user interface"""

    def __init__(self, location, size):
        """
        Initializes the attributes of the user interface. Where 
        things will be displayed, and the size of the item on the
        screen.
        """
        
        self.location = location
        self.size = size
    
    def display_location(self, location):
        """A function that sets the location of what you wish to display."""
        
    def display_size(self, size):
        """
        A function that sets the size and orientation of the displayed object.
        """

class PsycheBar(UserInterface):
    """Subclass of UserInterface simulating the psyche of the player."""
    def __init__(self, location, size):
        """Initialize the attributes of the psyche bar."""
        super.__init__(location, size)
        self.percentage = 100

    def draw_psyche_bar(percentage):
        """Draws the psyche bar and the base decay rate"""

    #     inner_bar_width = int(BAR_WIDTH *(percentage / 100))

    # # determine the color of the bar based on the percentage
    #     if self.percentage > 67:
    #         color = GREEN
    #     elif 33 <= percentage <= 67:
    #         color = YELLOW
    #     else:
    #         color = RED

class HealthBar(UserInterface):
    def __init__(self, location, size):
        """Initialize the attributes of the player's health"""
        super.__init__(location, size)

    def adjust_health(self, percentage):
        """Defines a function which adjusts the health bar by given increments"""

    def death(self):
        """Defines a function simulating the death of the player."""

class HotMenu(UserInterface):
    def __init__(self, location, size):
        """Initialize the attributes of an interactable menu while playing."""
        super.__init__(location, size)

    def cycle_menu(self):
        """
        Defines a function for cycling left and right through items in
        the player's hotbar.
        """
    
    def use_item(self):
        """
        Defines a function which uses the selected item in the player's
        hotbar.
        """




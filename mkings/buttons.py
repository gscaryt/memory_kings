import pygame
from .assets import Asset


class Button:
    '''
    A Button is used to call a function/method when clicked.
    - button(surface) method prints a normal Button.
    - switch(surface, condition) method prints a Switch
        that stays pressed while a "condition" is True.
    - toggle(surface, condition) method prints a Toggle
        that flips left and right depending of a "condition".
    '''
    def __init__(
        self,
        center_x,
        center_y,
        width,
        height,
        rest_image,
        hover_image=None,
        action_func=None,
        action_arg=None,
        path="images/",
    ):
        self.center_x = int(center_x)
        self.center_y = int(center_y)
        self.width = int(width)
        self.height = int(height)
        self.rest = rest_image
        self.hover = hover_image
        self.action_func = action_func
        self.action_arg = action_arg
        self.path = path

    def _get_image(self, state="rest"):
        if state == "hover" and self.hover is not None:
            image = self.hover
        else:
            image = self.rest
        button_image = Asset.image[image].convert_alpha()
        scaled_image = pygame.transform.smoothscale(button_image, (self.width, self.height))
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.center_x, self.center_y)
        return scaled_image, image_rect

    def _call_function(self):
        if self.action_func is not None:
            if self.action_arg is not None:
                self.action_func(self.action_arg)
            else:
                self.action_func()

    def button(self, surface, event):
        '''
        Prints on the Surface a normal button.
        '''
        mouse = pygame.mouse.get_pos()

        rest = self._get_image()
        hover = self._get_image("hover")

        if rest[1].collidepoint(mouse):
            surface.blit(*hover)
        else:
            surface.blit(*rest)

        if rest[1].collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            surface.blit(*rest)
            self._call_function()


    def switch(self, surface, event, condition):
        """
        Prints on the Surface a button that stays pressed 
        if a condition is True.

        # EXAMPLE #
        1) Create the Switch:
        button = Button(50,50,20,20,"rest.png","pressed.png",choose_attribute,value))

        2) Define the Function:
        def choose_attribute(self, value):
            attribute = value

        3) Place the Switch:
        tog.switch(SURFACE, (attribute == "value"))
        """
        mouse = pygame.mouse.get_pos()

        rest = self._get_image()
        hover = self._get_image("hover")

        if rest[1].collidepoint(mouse):
            surface.blit(*hover)
        elif condition is True:
            surface.blit(*hover)
        else:
            surface.blit(*rest)
        
        if rest[1].collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            surface.blit(*rest)
            self._call_function()


    def toggle(self, surface, event, condition):
        '''
        A Toggle is used to choose between two options.
        It should be linked to a function or method that changes 
        a given attribute (or global variable) value.

        # EXAMPLE #
        1) Create the Toggle:
        button = Button(50,50,20,20,"toggle_left.png","toggle_right.png",choose_attribute))

        2) Define the Function:
        def choose_attribute(self):
            if attribute == option_1:
                attribute = option_2
            else:
                attribute = option_1

        3) Place the Toggle:
        tog.toggle(SURFACE, (attribute == "option 2"))
        '''
        mouse = pygame.mouse.get_pos()

        left = self._get_image()
        right = self._get_image("hover")

        if condition is True:
            surface.blit(*right)
        else:
            surface.blit(*left)

        if left[1].collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            self._call_function()
import pygame


class Button:
    '''
    A Button is used to call a function/method when clicked.
    - button(surface) method prints the Button as normal.
    - lock_button(surface, condition) method prints the Button
        that stays pressed while a "condition" is True.
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
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.rest = rest_image
        self.hover = hover_image
        self.action_func = action_func
        self.action_arg = action_arg
        self.path = path

    def _get_image(self, state="rest"):
        if state == "hover" and self.hover is not None:
            image_path = self.path + self.hover
        else:
            image_path = self.path + self.rest
        button_image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(button_image, (self.width, self.height))
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.center_x, self.center_y)
        return scaled_image, image_rect

    def _call_function(self):
        if self.action_func is not None:
            if self.action_arg is not None:
                self.action_func(self.action_arg)
            else:
                self.action_func()

    def button(self, surface):
        '''
        Prints on the Surface a normal button.
        '''
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        rest = self._get_image()
        hover = self._get_image("hover")

        if rest[1].collidepoint(mouse):
            surface.blit(*hover)
        else:
            surface.blit(*rest)

        if (rest[1].collidepoint(mouse) and click[0] == 1):
            surface.blit(*rest)
            self._call_function()

    def lock_button(self, surface, condition):
        """
        Prints on the Surface a button that stays pressed 
        if a condition is True.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        rest = self._get_image()
        hover = self._get_image("hover")

        if rest[1].collidepoint(mouse):
            surface.blit(*hover)
        elif condition is True:
            surface.blit(*hover)
        else:
            surface.blit(*rest)

        if (rest[1].collidepoint(mouse) and click[0] == 1):
            surface.blit(*rest)
            self._call_function()


class Toggle:
    '''
    A Toggle is used to choose between two options.
    It should be linked to a function or method that changes 
    a given attribute (or global variable) value.

    # EXAMPLE #
    1) Create the Toggle:
    tog = Toggle(50,50,20,20,choose_attribute))

    2) Define the Function:
    def choose_attribute(self):
        if attribute == option_1:
            attribute = option_2
        else:
            attribute = option_1

    3) Place the Button:
    tog.switch(SURFACE)
    '''
    def __init__(
        self,
        center_x,
        center_y,
        width,
        height,
        action_func=None,
        togleft_image="toggle_left.png",
        togright_image="toggle_right.png",
        state="left",
        path = "images/",
    ):

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.action_func = action_func
        self.togleft_image = togleft_image
        self.togright_image = togright_image
        self.state = state
        self.path = path

    def _get_image(self):
        """
        Returns a tuple with the image and image_rect
        of the current Toggle state.
        """
        if self.state == "left":
            image_path = self.path + self.togleft_image
        elif self.state == "right":
            image_path = self.path + self.togright_image
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(image, (self.width, self.height))
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.center_x, self.center_y)
        return scaled_image, image_rect

    def _change_state(self):
        """Changes the current state."""
        if self.state == "right":
            self.state = "left"
        else:
            self.state = "right"

    def _call_function(self):
        """Calls the function that switches the option."""
        if self.action_func is not None:
            self.action_func()
      
    def switch(self, surface):
        """
        Prints the Toggle Switch with its functionality
        on the Surface.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        image = self._get_image() # Tuple (image, image_rect)
        surface.blit(*image)

        if image[1].collidepoint(mouse) and click[0] == 1:
            self._change_state()
            self._call_function()
            image = self._get_image()
            surface.blit(*image)

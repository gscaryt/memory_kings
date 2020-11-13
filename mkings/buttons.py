import pygame


class Button:
    """
    For a button to have an "action_func()" with several
    arguments (action_arg), add them as a single tuple
    (e.g. action_func((a, b, c, d))) and separate it in
    the beginning of that function.
    I think I can clean this up a bit.
    """

    def __init__(
        self,
        center_x,
        center_y,
        width,
        height,
        image,
        hover_image=None,
        action_func=None,
        action_arg=None,
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.image = image
        self.hover_image = hover_image
        self.action_func = action_func
        self.action_arg = action_arg

    def button(self, surface):
        image_path = "images/" + self.image
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(button_image, (self.width, self.height))
        self.image_rect = scaled_image.get_rect()
        self.image_rect.center = (self.center_x, self.center_y)

        if self.image_rect.collidepoint(mouse) and self.hover_image is not None:
            hover_path = "images/" + self.hover_image
            hover = pygame.image.load(hover_path).convert_alpha()
            scaled_hover = pygame.transform.scale(hover, (self.width, self.height))
            self.hover_rect = scaled_hover.get_rect()
            self.hover_rect.center = (self.center_x, self.center_y)
            surface.blit(scaled_hover, self.hover_rect)
        else:
            surface.blit(scaled_image, self.image_rect)

        if (
            self.image_rect.collidepoint(mouse)
            and self.action_func is not None
            and click[0] == 1
        ):
            surface.blit(scaled_image, self.image_rect)
            if self.action_arg is not None:
                self.action_func(self.action_arg)
            else:
                self.action_func()


class Toggle(Button):
    def __init__(
        self,
        center_x,
        center_y,
        width,
        height,
        action_func=None,
        togleft_image="toggle_left.png",
        togright_image="toggle_right.png",
        toggle="left",
    ):

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.action_func = action_func
        self.togleft_image = togleft_image
        self.togright_image = togright_image
        self.toggle = toggle

    def switch(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.toggle == "left":
            image_path = "images/" + self.togleft_image
        elif self.toggle == "right":
            image_path = "images/" + self.togright_image
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(image, (self.width, self.height))
        self.image_rect = scaled_image.get_rect()
        self.image_rect.center = (self.center_x, self.center_y)
        surface.blit(scaled_image, self.image_rect)

        if self.image_rect.collidepoint(mouse) and click[0] == 1:
            if self.toggle == "right":
                self.toggle = "left"
            else:
                self.toggle = "right"
            if self.action_func is not None:
                self.action_func()
            surface.blit(scaled_image, self.image_rect)

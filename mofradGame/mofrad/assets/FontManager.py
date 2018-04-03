import pygame

class Font:
    def __init__(self, name, size=32, bold=False, italic=False):
        self.name = name
        self.size = size
        self.pyfont = pygame.font.SysFont(name, size, bold=bold, italic=italic)

class FontManager:
    def __init__(self):
        self.cache = {}
        self.fonts = {}

    def load_font(self, name, font: Font):
        self.fonts[name] = font

    def load(self, name, font_name, size=32, bold=False, italic=False):
        self.fonts[name] = Font(font_name, size=size, bold=bold, italic=italic)

    def get(self, font_name):
        return self.fonts[font_name]

    def render_font(self, font, text, color=(255, 255, 255)):
        render = font.pyfont.render(str(text), 0, color)
        return render

    def render(self, font_name, text, color=(255, 255, 255)):
        if font_name in self.cache and text in self.cache[font_name]:
            render = self.cache[font_name][text]
            return render
        else:
            render = self.render_font(self.fonts[font_name], text, color)
            if not font_name in self.cache:
                self.cache[font_name] = {}
            self.cache[font_name][text] = render
            return render





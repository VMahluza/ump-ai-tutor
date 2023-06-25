class FeatureItemData:
    def __init__(self, title, description, icon_div):
        self.title = title
        self.description = description
        self.icon_div = icon_div

class IconDiv:
    def __init__(self, icon_class, color, delay):
        self.icon_class = icon_class
        self.color = color
        self.delay = delay
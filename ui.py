import pygame
from enum import Enum, auto

class container:
    containerlist = []
    class DISPLAY(Enum):
        VERTICAL = auto()
        HORIZONTAL = auto()
        
    class ALIGNITEMS(Enum):
        CENTER = auto()
        TOPCENTER = auto()
        BOTTOMCENTER = auto()
        LEFTCENTER = auto()
        RIGHTCENTER = auto()
        TOPRIGHT = auto()
        TOPLEFT = auto()
        BOTTOMRIGHT = auto()
        BOTTOMLEFT = auto()
        
    def __init__(self, display=DISPLAY.HORIZONTAL, size=(100, 100), pos=pygame.Vector2(0,0), margins=10, allignitems=ALIGNITEMS.TOPLEFT):
        self.display = display
        self.allignitems = allignitems
        self.size = size
        self.pos = pos
        self.childs = []  
        self.packedlist = [] 
        self.margins = margins
        self.expandable = True
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y + margins*2, self.size[0] + margins*2, self.size[1])
        container.containerlist.append(self)

    def add(self, child):
        self.childs.append(child)

    def pack(self):
        self.packedlist.clear()

        def getoffset(totalsize, containersize, align):
            if align in [self.ALIGNITEMS.CENTER, self.ALIGNITEMS.TOPCENTER, self.ALIGNITEMS.BOTTOMCENTER]:
                return (containersize - totalsize) / 2
            elif align in [self.ALIGNITEMS.RIGHTCENTER, self.ALIGNITEMS.TOPRIGHT, self.ALIGNITEMS.BOTTOMRIGHT]:
                return containersize - totalsize - self.margins
            else:  
                return self.margins
            
        if self.display == self.DISPLAY.VERTICAL:
            columns = []
            col = []
            yoffset = 0
            maxwidthincol = 0
            for child in self.childs:
                if yoffset + child.rect.height > self.size[1] - self.margins:
                    columns.append((col, maxwidthincol))
                    col = []
                    yoffset = 0
                    maxwidthincol = 0
                col.append(child)
                yoffset += child.rect.height + self.margins
                if child.rect.width > maxwidthincol:
                    maxwidthincol = child.rect.width
            if col:
                columns.append((col, maxwidthincol))
            totalwidth = sum(w for _, w in columns) + self.margins * (len(columns) - 1)
            xstart = getoffset(totalwidth, self.size[0], self.allignitems)
            x = xstart
            for colchildren, colwidth in columns:
                totalcolheight = sum(c.rect.height for c in colchildren) + self.margins * (len(colchildren) - 1)
                ystart = getoffset(totalcolheight, self.size[1], self.allignitems)
                y = ystart
                for c in colchildren:
                    xpos = self.pos.x + x
                    if self.allignitems in [self.ALIGNITEMS.CENTER, self.ALIGNITEMS.TOPCENTER, self.ALIGNITEMS.BOTTOMCENTER]:
                        xpos += (colwidth - c.rect.width) / 2
                    c.rect.topleft = (xpos, self.pos.y + y)
                    self.packedlist.append(c)
                    y += c.rect.height + self.margins
                x += colwidth + self.margins
        elif self.display == self.DISPLAY.HORIZONTAL:
            rows = []
            row = []
            xoffset = 0
            maxheightinrow = 0
            for child in self.childs:
                if xoffset + child.rect.width > self.size[0] - self.margins:
                    rows.append((row, maxheightinrow))
                    row = []
                    xoffset = 0
                    maxheightinrow = 0
                row.append(child)
                xoffset += child.rect.width + self.margins
                if child.rect.height > maxheightinrow:
                    maxheightinrow = child.rect.height
            if row:
                rows.append((row, maxheightinrow))
            totalheight = sum(h for _, h in rows) + self.margins * (len(rows) - 1)
            ystart = getoffset(totalheight, self.size[1], self.allignitems)
            y = ystart
            for rowchildren, rowheight in rows:
                totalrowwidth = sum(c.rect.width for c in rowchildren) + self.margins * (len(rowchildren) - 1)
                xstartrow = getoffset(totalrowwidth, self.size[0], self.allignitems)
                x = xstartrow
                for c in rowchildren:
                    ypos = self.pos.y + y
                    if self.allignitems in [self.ALIGNITEMS.CENTER, self.ALIGNITEMS.LEFTCENTER, self.ALIGNITEMS.RIGHTCENTER]:
                        ypos += (rowheight - c.rect.height) / 2
                    c.rect.topleft = (self.pos.x + x, ypos)
                    self.packedlist.append(c)
                    x += c.rect.width + self.margins
                y += rowheight + self.margins



class BUTTON:
    buttonslist = []
    class STATE(Enum):
            DEFAULT = auto()
            HOVER = auto()
            CLICKED = auto()
            PRESSED = auto()
            
    def __init__(self, font=None ,width=0, height=0, onclick=None,pos=pygame.Vector2(50, 50),   text=None, color=None, bordersize=2, bordercolor=None, padding=10, margins=10, cornerradius=0):
        if font == None:self.font = pygame.font.Font(None, size=10)
        else: self.font = font
        self.pos = pos.copy()
        self.pos.x = pos.x - margins
        self.pos.y = pos.y - margins
        if width == 0 and height == 0:    
            self.width, self.height = self.font.size(text)
            self.width = self.width + padding *2
            self.height = self.height + padding *2
        else:
            self.width = width + padding *2
            self.height = height + padding *2
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.width + margins *2, self.height + margins *2)
        self.color = color
        if isinstance(text, str):self.text = self.font.render(text, True, (255, 255, 255))
        else:self.text = text
        self.bordercolor = bordercolor
        self.cornerradius = cornerradius
        self.padding = padding
        self.changetextsize = True
        self.hovercolor = color
        self.clickcolor = color
        self.pressedcolor = color
        self.hoversize = 1.0
        self.clicksize = 1.0
        self.pressedsize = 1.0
        self.bordersize = bordersize
        self.sizechangeduritation = None
        self.state = BUTTON.STATE.DEFAULT
        self.onclick = onclick
        BUTTON.buttonslist.append(self)
        
    def draw(self, screen):
        if self.color == None:
            self.color = screen.get_at((0, 0))
        if self.hovercolor == None:
            self.hovercolor = screen.get_at((0, 0))
        if self.clickcolor == None:
            self.clickcolor = screen.get_at((0, 0))
        match self.state:
            case BUTTON.STATE.DEFAULT:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=self.cornerradius)
            case BUTTON.STATE.HOVER:
                rect = pygame.Rect(self.rect.centerx - self.rect.width*self.hoversize/2,self.rect.centery - self.rect.height*self.hoversize/2,self.rect.width*self.hoversize,self.rect.height*self.hoversize)
                pygame.draw.rect(screen, self.hovercolor, rect, border_radius=self.cornerradius)
            case BUTTON.STATE.CLICKED:
                rect = pygame.Rect(self.rect.centerx - self.rect.width*self.clicksize/2,self.rect.centery - self.rect.height*self.clicksize/2,self.rect.width*self.clicksize,self.rect.height*self.clicksize)
                pygame.draw.rect(screen, self.clickcolor, rect, border_radius=self.cornerradius)
            case BUTTON.STATE.PRESSED:
                rect = pygame.Rect(self.rect.centerx - self.rect.width*self.pressedsize/2,self.rect.centery - self.rect.height*self.pressedsize/2,self.rect.width*self.pressedsize,self.rect.height*self.pressedsize)
                pygame.draw.rect(screen, self.pressedcolor, rect, border_radius=self.cornerradius)
                
        if self.changetextsize:
            match self.state:
                case BUTTON.STATE.DEFAULT:
                    text_rect = self.text.get_rect(center=self.rect.center)
                case BUTTON.STATE.HOVER:
                    scaled_rect = pygame.Rect(self.rect.centerx - self.rect.width*self.hoversize/2,self.rect.centery - self.rect.height*self.hoversize/2,self.rect.width*self.hoversize,self.rect.height*self.hoversize)
                    text_rect = self.text.get_rect(center=scaled_rect.center)
                case BUTTON.STATE.CLICKED:
                    scaled_rect = pygame.Rect(self.rect.centerx - self.rect.width*self.clicksize/2,self.rect.centery - self.rect.height*self.clicksize/2,self.rect.width*self.clicksize,self.rect.height*self.clicksize)
                    text_rect = self.text.get_rect(center=scaled_rect.center)
                case BUTTON.STATE.PRESSED:
                    scaled_rect = pygame.Rect(self.rect.centerx - self.rect.width*self.pressedsize/2,self.rect.centery - self.rect.height*self.pressedsize/2,self.rect.width*self.pressedsize,self.rect.height*self.pressedsize)
                    text_rect = self.text.get_rect(center=scaled_rect.center)
        else:
            screen.blit(self.text, (self.pos.x + self.padding, self.pos.y + self.padding))
        screen.blit(self.text, text_rect)

class LABEL:
    class STATE(Enum):
            DEFAULT = auto()
            HOVER = auto()
    labellist = []
    def __init__(self, font=None ,width=0, height=0, pos=pygame.Vector2(50, 50), text="text", color=None,bordersize=2, bordercolor=None, padding=10, margins=10, cornerradius=0):
        if font == None:self.font = pygame.font.Font(None, size=10)
        else: self.font = font
        self.pos = pos.copy()
        self.pos.x = pos.x - margins
        self.pos.y = pos.y - margins
        if width == 0 and height == 0:    
            self.width, self.height = self.font.size(text)
            self.width = self.width + padding *2
            self.height = self.height + padding *2
        else:
            self.width = width + padding *2
            self.height = height + padding *2
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.width + margins *2, self.height + margins *2)
        self.color = color
        if isinstance(text, str):self.text = self.font.render(text, True, (255, 255, 255))
        else:self.text = text
        self.bordercolor = bordercolor
        self.cornerradius = cornerradius
        self.padding = padding
        self.changetextsize = False
        self.hovercolor = None
        self.hoversize = 1
        self.bordersize = bordersize
        self.state = LABEL.STATE.DEFAULT
        LABEL.labellist.append(self)
        
    def draw(self, screen):
        if self.color == None:
            self.color = screen.get_at((0, 0))
        if self.hovercolor == None:
            self.hovercolor = screen.get_at((0, 0))
        match self.state:
            case LABEL.STATE.DEFAULT:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=self.cornerradius)
            case LABEL.STATE.HOVER:
                rect = pygame.Rect(self.rect.centerx - self.rect.width*self.hoversize/2,self.rect.centery - self.rect.height*self.hoversize/2,self.rect.width*self.hoversize,self.rect.height*self.hoversize)
                pygame.draw.rect(screen, self.hovercolor, rect, border_radius=self.cornerradius)
        screen.blit(self.text, (self.rect.x + self.padding + 7, self.rect.y + self.padding))


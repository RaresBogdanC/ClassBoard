import pygame

class SimpleGUI:
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    Widgets = []
    Selection = None
    class Widget():
        def __init__(self,x=0,y=0,width=None,height=None,min_width = None,min_height = None,
                     max_width = None,max_height = None,text="",font = pygame.font.SysFont("Arial",20,None),
                     fg=(255,255,255,0),bg=None,image=None,image_size=(None,None),anchor = "C",
                     border=0, border_radius = 0, border_color = None,
                     command=None,on_hover=None, active_fg=None,
                     entry = False,extend_entry=True,show_entry=None, active_bg=None,
                     timer = None,on_timer_tick = None,on_timer_end = None,caret_color=(200,200,200),
                     caret_blink_delay = 1000):
            
            self.min_width = min_width 
            self.min_height = min_height 
            self.max_width = max_width 
            self.min_height = max_height
            self.anchor = anchor
            self.on_timer_tick = on_timer_tick
            if on_timer_end!=None:
                self.on_timer_end = on_timer_end
            else:
                self.on_timer_end = self.Destroy
            if timer!=None:
                self.timer = timer*100 
            else:
                self.timer = None
            self.entry = entry
            self.show_entry = show_entry
            self.extend_entry = extend_entry
            self.caret_index = 0
            self.caret_color = caret_color
            self.caret_blink = caret_blink_delay
            self.caret_delay = caret_blink_delay
            self.font = font 
            self.fg = fg 
            self.bg = bg 
            self.widget_image = None 
            self.widget_text = None
            self.image_size = image_size
            if image!=None:
                self.image = image 
                self.widget_image = pygame.image.load(self.image)
                if self.image_size!=(None,None):
                    self.widget_image = pygame.transform.scale(self.widget_image,self.image_size)
            else:
                self.image = None 
            if text!=None:
                self.text = text 
                if self.entry == True and self.show_entry!=None:
                    if self.bg!=None:
                        self.widget_text = self.font.render(self.show_entry*len(self.text),True,self.fg,self.bg)
                    else:
                        self.widget_text = self.font.render(self.show_entry*len(self.text),True,self.fg)
                else:
                    if self.bg!=None:
                        self.widget_text = self.font.render(self.text,True,self.fg,self.bg)
                    else:
                        self.widget_text = self.font.render(self.text,True,self.fg)
            else:
                self.text = None

            if self.widget_image!= None and self.widget_text!=None:
                if self.widget_image.get_rect().width*self.widget_image.get_rect().height>self.widget_text.get_rect().width*self.widget_text.get_rect().height:
                    self.rect = self.widget_image.get_rect()
                else:
                    self.rect = self.widget_text.get_rect()
            elif self.widget_image!=None:
                self.rect = self.widget_image.get_rect()
            elif self.widget_text!=None:
                self.rect = self.widget_text.get_rect()

            if self.image!=None and image_size==(None,None):
                self.widget_image = pygame.transform.scale(self.widget_image,(self.rect.width,self.rect.height))

            self.rect.x = x 
            self.rect.y = y
            if width!=None:
                self.rect.width = width
                if self.min_width == None:
                    self.min_width = width
            if height!=None:
                self.rect.height = height  
                if self.min_height == None:
                    self.min_height = height

            self.border = border 
            if border_color!=None:
                self.border_color = border_color 
            else:
                if self.bg!=None:
                    self.border_color = self.bg 
                else:
                    self.border_color = (50,50,50)
            self.border_radius = border_radius 
            
            self.on_hover = on_hover
            self.command = command 
            if active_fg==None:
                self.active_fg = fg 
            else:
                self.active_fg = active_fg
            if active_bg == None:
                if self.bg!=None:
                    self.active_bg = self.bg
                else:
                    self.active_bg = (50,50,50)
            else:
                self.active_bg = active_bg

            self.SavedColors = [self.bg,self.fg,self.border_color]
            
            SimpleGUI.Widgets.append(self)

        def Update(L):
            'Updates a specific widget (L) from the SimpleGUI widgets list.'
            if L.image!=None:
                L.widget_image = pygame.image.load(L.image)
                if L.image_size!=(None,None):
                    L.widget_image = pygame.transform.scale(L.widget_image,L.image_size)
            if L.text!=None:
                if L.show_entry !=None:
                    L.widget_text = L.font.render(L.show_entry*len(L.text),True,L.fg)
                else:
                    L.widget_text = L.font.render(L.text,True,L.fg)
            
            if L.widget_image!= None and L.widget_text!=None:
                if L.widget_image.get_rect().width*L.widget_image.get_rect().height>L.widget_text.get_rect().width*L.widget_text.get_rect().height:
                    if L.extend_entry == True:
                        L.rect.width = L.widget_image.get_rect().width
                    L.rect.height = L.widget_image.get_rect().height
                else:
                    if L.extend_entry == True:
                        L.rect.width = L.widget_text.get_rect().width
                    L.rect.height = L.widget_text.get_rect().height
            elif L.widget_image!=None:
                if L.extend_entry == True:
                    L.rect.width = L.widget_image.get_rect().width
                L.rect.height = L.widget_image.get_rect().height
            elif L.widget_text!=None:
                if L.extend_entry == True:
                    if L.min_width!=None:
                        L.rect.width = max([L.min_width,L.widget_text.get_rect().width])  
                L.rect.height = L.widget_text.get_rect().height

            if L.image!=None and L.image_size==(None,None):
                L.widget_image = pygame.transform.scale(L.widget_image,(L.rect.width,L.rect.height))
        def Destroy(self):
            'Removes a specific widget from the SimlpeGUI widgets list.'
            SimpleGUI.Widgets.remove(self)
    def Draw(screen):
        'Draw all SimpleGUI widgets on a given screen(pygame.display).'
        for L in SimpleGUI.Widgets:
            if L.bg!=None:
                pygame.draw.rect(screen,L.bg,pygame.rect.Rect(L.rect.x-L.border,L.rect.y-L.border,L.rect.width+L.border*2,L.rect.height+L.border*2),0,L.border_radius)
            if L.border>0:
                pygame.draw.rect(screen,L.border_color,pygame.rect.Rect(L.rect.x-L.border,L.rect.y-L.border,L.rect.width+L.border*2,L.rect.height+L.border*2),L.border,L.border_radius)
            if L.image!=None:
                if L.anchor == "NW":
                    screen.blit(L.widget_image,L.rect)
                if L.anchor == "W":
                    screen.blit(L.widget_image,(L.rect.x,L.rect.y+int(L.rect.height/2)-int(L.widget_image.get_rect().height/2)))
                if L.anchor == "SW":
                    screen.blit(L.widget_image,(L.rect.x,L.rect.y+int(L.rect.height)-int(L.widget_image.get_rect().height)))
                if L.anchor == "S":
                    screen.blit(L.widget_image,(L.rect.x+int(L.rect.width/2)-int(L.widget_image.get_rect().width/2),L.rect.y+int(L.rect.height-L.widget_image.get_rect().height)))
                if L.anchor == "SE":
                    screen.blit(L.widget_image,(L.rect.x+L.rect.width-L.widget_image.get_rect().width,L.rect.y+int(L.rect.height)-int(L.widget_image.get_rect().height)))
                if L.anchor == "E":
                    screen.blit(L.widget_image,(L.rect.x+L.rect.width-L.widget_image.get_rect().width,L.rect.y+int(L.rect.height/2)-int(L.widget_image.get_rect().height/2)))
                if L.anchor == "NE":
                    screen.blit(L.widget_image,(L.rect.x+L.rect.width-L.widget_image.get_rect().width,L.rect.y))
                if L.anchor == "N":
                    screen.blit(L.widget_image,(L.rect.x+int(L.rect.width/2)-int(L.widget_image.get_rect().width/2),L.rect.y))
                if L.anchor == "C":
                    screen.blit(L.widget_image,(L.rect.x+int(L.rect.width/2)-int(L.widget_image.get_rect().width/2),L.rect.y+int(L.rect.height/2)-int(L.widget_image.get_rect().height/2)))

            if L.text!=None:
                if L.anchor == "NW":
                    screen.blit(L.widget_text,L.rect)
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+LeftTextObject.get_rect().width,L.rect.y,2,L.rect.height))
                if L.anchor == "W":
                    screen.blit(L.widget_text,(L.rect.x,L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2),2,L.rect.height))
                if L.anchor == "SW":
                    screen.blit(L.widget_text,(L.rect.x,L.rect.y+int(L.rect.height)-int(L.widget_text.get_rect().height)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height)-int(L.widget_text.get_rect().height),2,L.rect.height))
                if L.anchor == "S":
                    screen.blit(L.widget_text,(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2),L.rect.y+int(L.rect.height-L.widget_text.get_rect().height)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2)+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height-L.widget_text.get_rect().height),2,L.rect.height))
                if L.anchor == "SE":
                    screen.blit(L.widget_text,(L.rect.x+L.rect.width-L.widget_text.get_rect().width,L.rect.y+int(L.rect.height)-int(L.widget_text.get_rect().height)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+L.rect.width-L.widget_text.get_rect().width+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height)-int(L.widget_text.get_rect().height),2,L.rect.height))
                if L.anchor == "E":
                    screen.blit(L.widget_text,(L.rect.x+L.rect.width-L.widget_text.get_rect().width,L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+L.rect.width-L.widget_text.get_rect().width+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2),2,L.rect.height))
                if L.anchor == "NE":
                    screen.blit(L.widget_text,(L.rect.x+L.rect.width-L.widget_text.get_rect().width,L.rect.y))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+L.rect.width-L.widget_text.get_rect().width+LeftTextObject.get_rect().width,L.rect.y,2,L.rect.height))
                if L.anchor == "N":
                    screen.blit(L.widget_text,(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2),L.rect.y))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2)+LeftTextObject.get_rect().width,L.rect.y,2,L.rect.height))
                if L.anchor == "C":
                    screen.blit(L.widget_text,(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2),L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2)))
                    if L.entry == True and L == SimpleGUI.Selection and L.caret_blink>0:
                        if L.show_entry!=None:
                            rect_text = L.show_entry*len(L.text)
                        else:
                            rect_text = L.text
                        LeftTextObject = L.font.render(rect_text[:L.caret_index],True,L.fg)
                        pygame.draw.rect(screen,L.caret_color,pygame.rect.Rect(L.rect.x+int(L.rect.width/2)-int(L.widget_text.get_rect().width/2)+LeftTextObject.get_rect().width,L.rect.y+int(L.rect.height/2)-int(L.widget_text.get_rect().height/2),2,L.rect.height))
                L.caret_blink-=1
                if L.caret_blink == -L.caret_delay:
                    L.caret_blink = L.caret_delay

            if L.timer!=None:
                if L.timer>0:
                    if L.on_timer_tick!=None:
                        L.on_timer_tick(L)
                    L.timer-=1
                elif L.timer==0:
                    L.timer = None
                    L.on_timer_end()
    def Clear():
        'Clear all widgets from the SimpleGUI widgets list.'
        SimpleGUI.Widgets = []
    def MouseClick(pos=(None,None)):
        'MouseClick(pos=(x,y)) -> Checks all widgets for mouse click event.'
        if pos!=(None,None):
            for L in SimpleGUI.Widgets:
                if L.rect.collidepoint(pos):
                    if L.command!=None:
                        L.command(L)
                    if L.entry == True:
                        # make auto clear on focus system:
                        if SimpleGUI.Selection!=L:
                            L.caret_index = len(L.text)
                        SimpleGUI.Selection = L
    def MouseHover(pos=(None,None)):
        'MouseHover(pos=(x,y)) -> Checks all widgets for mouse hover event.'
        for L in SimpleGUI.Widgets:
                if L.rect.collidepoint(pos) and ((L.widget_text!=None and (L.command!=None or L.entry==True)) or L==SimpleGUI.Selection):
                    if L.entry == True and L.show_entry!=None:
                        L.widget_text = L.font.render(L.show_entry*len(L.text),True,L.active_fg)
                        L.bg = L.active_bg
                        L.border_color = L.active_bg
                    else:
                        L.widget_text = L.font.render(L.text,True,L.active_fg)
                        L.bg = L.active_bg
                        L.border_color = L.active_bg
                else:
                    if L.entry == True and L.show_entry!=None:
                        L.widget_text = L.font.render(L.show_entry*len(L.text),True,L.fg)
                        L.bg = L.SavedColors[0]
                        L.border_color = L.SavedColors[2]
                    else:
                        L.widget_text = L.font.render(L.text,True,L.fg)
                        L.bg = L.SavedColors[0]
                        L.border_color = L.SavedColors[2]
                if L.rect.collidepoint(pos) and L.on_hover!=None:
                    L.on_hover(L)
                
    def GetKeyPress(key = pygame.event.get()):
        'GetKeyPress(key = pygame.event.get()) -> Checks all widgets for KeyPress event.'
        if SimpleGUI.Selection != None:
            for E in SimpleGUI.Widgets:
                if E == SimpleGUI.Selection:
                    if key.key == 1073741904:
                        E.caret_index = max(0, E.caret_index-1)
                    elif key.key == 1073741903:
                        E.caret_index = min(E.caret_index+1, len(E.text))
                    elif key.unicode == "\x08":
                        if E.caret_index>0:
                            E.text = E.text[:E.caret_index-1] + E.text[E.caret_index:]
                            E.caret_index = max(0, E.caret_index-1)
                    else:
                        if E.extend_entry == False:
                            if E.widget_text.get_rect().width<E.rect.width-E.border and (key.key>31 and key.key<127):
                                E.text = E.text[:E.caret_index] + f"{key.unicode}" + E.text[E.caret_index:]
                                E.caret_index+=1
                        elif E.max_width!=None:
                            if E.widget_text.get_rect().width<E.max_width and (key.key>31 and key.key<127):
                                E.text = E.text[:E.caret_index] + f"{key.unicode}" + E.text[E.caret_index:]
                                E.caret_index+=1
                        elif key.key>31 and key.key<127:
                            E.text = E.text[:E.caret_index] + f"{key.unicode}" + E.text[E.caret_index:]
                            E.caret_index+=1
                    E.Update()

SimpleGUI.W = "w"

if __name__ == "__main__":
    import pygame 

    # SimpleGUI module will init: pygame.init()
    #                             pygame.mixer.init()
    #                             pygame.font.init()

    screen = pygame.display.set_mode((1000,500),pygame.RESIZABLE)
    pygame.display.set_caption("pyGUI SimpleGUI")

    def on_submit(e):
        global MesagePopUp,UsernameEntry,SubmitButton,PasswordEntry
        if len(UsernameEntry.text)<3 or len(PasswordEntry.text)<3:
            # Re - initialize the message popup(timer = 50ms) with text value:
            if MesagePopUp.timer==None: # if the timer has finished
                MesagePopUp = SimpleGUI.Widget(x=0,y=SubmitButton.rect.y+SubmitButton.rect.height + 50,
                                        text="Username and password must be longer than 3 characters!",
                                        font = pygame.font.SysFont("Arial",20,None),bg=(100,5,5),border=10,
                                        border_radius=25,timer=50)
        else:
            SimpleGUI.Clear() # Clear the screen of SimpleGUI widgets
            # Re - initialize the message popup(timer = 50ms) with text value:
            MesagePopUp = SimpleGUI.Widget(x=0,y=50,
                                        text=f"Username: {UsernameEntry.text}  Password: {PasswordEntry.text}",
                                        font = pygame.font.SysFont("Arial",20,None),bg=(5,100,5),border=10,
                                        border_radius=25,timer=50)
                
    # Build all SimpleGUI widgets (buttons / labels / entrys and popups)
    Title = SimpleGUI.Widget(x = 0,y = 50,font=pygame.font.SysFont("Arial",40,None),
                            text = "The SimpleGUI Examples:")
    UsernameEntry = SimpleGUI.Widget(x = 0,y = Title.rect.y+Title.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            text = "",width=150,bg=(10,10,10),entry=True,
                            active_bg=(50,50,50),border=5,border_radius=25,extend_entry=False,show_entry=None)
    UsernameLabel = SimpleGUI.Widget(x=0,y = Title.rect.y+Title.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            text = "Username :")
    PasswordEntry = SimpleGUI.Widget(x = 0,y = UsernameEntry.rect.y+UsernameEntry.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            text = "",width=150,bg=(10,10,10),entry=True,
                            active_bg=(50,50,50),border=5,border_radius=25,extend_entry=False,show_entry="X")
    PasswordLabel = SimpleGUI.Widget(x = 0,y = UsernameEntry.rect.y+UsernameEntry.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            text = "Password :")
    SubmitButton = SimpleGUI.Widget(x=0,y = PasswordLabel.rect.y+PasswordLabel.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            text = "Submit",bg = (15, 2, 26),active_bg=(57, 8, 94),command=on_submit,border=10,border_radius=25)
    MesagePopUp = SimpleGUI.Widget(x=0,y=SubmitButton.rect.y+SubmitButton.rect.height + 50,font = pygame.font.SysFont("Arial",20,None),
                            bg=(255,5,5),border=10,border_radius=25,timer=0)
    
    # keep the simple pygame screen running
    run = True 
    while run:
        screen.fill((0,0,0))

        # check all events on pygame screen object
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # let the pygame screen collapse
                run = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                SimpleGUI.MouseClick(event.pos) # Check Mouse click event with SimpleGUI
            if event.type == pygame.MOUSEMOTION:
                SimpleGUI.MouseHover(event.pos) # Check Mouse hoover over SimpleGUI Widgets
            if event.type == pygame.KEYDOWN:
                SimpleGUI.GetKeyPress(event) # Get key event and insert it in the entry widget if selected

        # Set the label position to always be relative to the middle of the screen : 
        Title.rect.x = int(pygame.display.get_window_size()[0]/2) - int(Title.rect.width/2)
        UsernameLabel.rect.x = int(pygame.display.get_window_size()[0]/2 - UsernameLabel.rect.width - 20)
        UsernameEntry.rect.x = int(pygame.display.get_window_size()[0]/2)
        PasswordLabel.rect.x = int(pygame.display.get_window_size()[0]/2 - PasswordLabel.rect.width - 20)
        PasswordEntry.rect.x = int(pygame.display.get_window_size()[0]/2)
        SubmitButton.rect.x = int(pygame.display.get_window_size()[0]/2-SubmitButton.rect.width/2)
        MesagePopUp.rect.x = int(pygame.display.get_window_size()[0]/2-MesagePopUp.rect.width/2)
        
        SimpleGUI.Draw(screen) # Draw the SimpleGUI Widgets on the pygame screen
        pygame.display.update()
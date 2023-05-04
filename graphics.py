import pygame
from math import ceil,sqrt


def rect_from_image(img,x1,y1,x2,y2):
    if type(img)==type(str):
        img=pygame.image.load(img)
    if x1>x2:x1,x2=x2,x1
    if y1>y2:y1,y2=y2,y1
    W=x2-x1
    H=y2-y1
    surface=pygame.Surface((W,H))
    surface.blit(img,(x1,y1))
    return surface

def circle_from_image(img,cx,cy,r):
    if type(img)==type(str):
        img=pygame.image.load(img)
    W=H=int(ceil(2*r))
    r-=0.5
    surface=pygame.Surface((W,H),pygame.SRCALPHA)
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            if (x-cx)**2+(y-cy)**2>(r+5)**2:
                continue
            sx=x-cx+W//2
            sy=y-cy+H//2
            if sx<0 or sx>=W or sy<0 or sy>=H:
                continue
            pixel=img.get_at((x,y))
            delta=sqrt((x-cx)**2+(y-cy)**2)-r
            if delta<0:
                surface.set_at((sx,sy),pixel)
                continue
            delta=(5-delta)/5
            a=pixel[3]
            a=a*(delta**5)
            pixel_surf=pygame.Surface((1,1),pygame.SRCALPHA)
            pixel_surf.fill((*pixel[:3],int(a)))
            surface.blit(pixel_surf, (sx,sy))
    return surface

def circle_from_color(clr,r):
    W=H=int(ceil(2*r))
    r-=0.5
    surface=pygame.Surface((W,H),pygame.SRCALPHA)
    for x in range(W):
        for y in range(H):
            if (x-r)**2+(y-r)**2>(r+5)**2:
                continue
            sx=int(x-r+W//2)
            sy=int(y-r+H//2)
            if sx<0 or sx>=W or sy<0 or sy>=H:
                continue
            pixel=(*clr,255)
            delta=sqrt((x-r)**2+(y-r)**2)-r
            if delta<0:
                surface.set_at((sx,sy),pixel)
                continue
            delta=(5-delta)/5
            a=pixel[3]
            a=a*(delta**5)
            pixel_surf=pygame.Surface((1,1),pygame.SRCALPHA)
            pixel_surf.fill((*pixel[:3],int(a)))
            surface.blit(pixel_surf, (sx,sy))
    return surface
            


from render import main_activity, show_image

OBJ_LINK = 'data/african_head.obj'
TGA_LINK = 'data/african_head_diffuse.tga'

height = 512
weight = 512
show_image(main_activity(weight, height, OBJ_LINK, TGA_LINK))

######Minecarft Code By Kessi-Hacker
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from landscale import Map

import pymesh
import gmsh
from ursina.shaders import lit_with_shadows_shader
app = Ursina()


for x in range(1,16): 
   for z in range(1,16):
       Entity(model="cube", texture=load_texture('image/minecraft.png'), position=Vec3(x,0,z))
grass_texture=load_texture('image/minecraft.png')
for x_dynamic in range(1,16):
    for z_dynamic in range(1,16):
        Entity (model='cube', scale=1, texture=grass_texture,position=Vec3(x_dynamic,0,z_dynamic))
player = FirstPersonController(speed=7)
player.gravity = 0.0
    
arm_texture = load_texture('assets/arm_texture.png')
hand = Entity(parent = camera.ui, model = 'assets/arm',
             texture = arm_texture, scale = 0.2,
             rotation = Vec3(150, -5,0), position = Vec2(0.5,-0.6))
sky_texture=load_texture('assets/skybox.jpg')
sky=Entity(
      model='sphere',texture=sky_texture,
      scale=1000, double_sided=True
      )
'''map = Map(1371)
terrain = MeshTerrain(map.landscale_mask)'''
def input(key):
   if key == 'control':
         if player.y < 0.15:
               player.animate_y(-2, duration=-0.4, curve=curve.out_sine)
               player.animate_y(0, duration=-0.4, delay=-0.4, curve=curve.in_sine)
               print(2)
   if key == 'space':
        if player.y < 0.05:
               player.animate_y(2, duration=0.4, curve=curve.out_sine)
               player.animate_y(0, duration=0.4, delay=0.4, curve=curve.in_sine)
               print(1)
   if key == 'o': # кнопка выхода из игры
      quit()
   
class Voxel(Button):
   def __init__(self, position=(0, 0, 0), texture=load_texture('image/grass.jpg')):
       super().__init__(
           parent=scene, model='cube', 
           scale=1, texture=load_texture('image/cube.jpg'),collider='box', position=position,
           origin_y=1, color = color.color(0,0,random.uniform(0.9,1))
       )
   
   #     		если нажали на ПКМ — появится блок
   #     		если нажали на ЛКМ — удалится 
   def input(self, key):
       if self.hovered:
           if key == 'right mouse down':
               Voxel(position=self.position + mouse.normal, texture=texture)

           if key == 'left mouse down':
               destroy(self)

# генерация платформы из блоков Voxel
for x_dynamic in range(1,16):
   for z_dynamic in range(1,16):
       Voxel(position=(x_dynamic,0,z_dynamic))
noise = PerlinNoise(octaves=2, seed=4522)
amp = 6
freq = 24
terrain_width = 300

landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

for position in range(terrain_width**2):
   x = floor(position / terrain_width)
   z = floor(position % terrain_width)
   y = floor(noise([x/freq, z/freq])*amp)

   landscale[int(x)][int(z)] = int(y)

plt.imshow(landscale)
plt.show()
def update():
   print(player.x, player.y, player.z)

###ГЕНЕРАЦИЯ МИРА



class Map(object):
    def __init__(self, seed):
        self.seed = seed
        self.noise = PerlinNoise(octaves=1, seed=self.seed)
        self.amp = 8
        self.freq = 24
        self.terrain_width = 128
        self.levels = 10

        self.landscale_mask = [[0 for i in range(self.terrain_width)] for i in range(self.terrain_width)]
        self.mine_mask = [0 for level in range(self.levels)]

        self.__landscale()
        #self.__mine()

    def __landscale(self):
        for position in range(self.terrain_width ** 2):
            x = floor(position / self.terrain_width)
            z = floor(position % self.terrain_width)
            y = floor(self.noise([x / self.freq, z / self.freq]) * self.amp)

            self.landscale_mask[int(x)][int(z)] = int(y)

    def __mine(self):
        for level in range(self.levels):
            local_mask = [[0 for i in range(self.terrain_width)] for i in range(self.terrain_width)]
            for position in range(self.terrain_width ** 2):
                koef = 0.9 + 0.1*level
                x = floor(position / self.terrain_width)
                z = floor(position % self.terrain_width)
                y = floor(self.noise([x / (self.freq * koef), z / (self.freq * koef)]) * (self.amp))
                if y > 0:
                    y = 0
                elif y < 0:
                    y = -1

                local_mask[int(x)][int(z)] = int(y)
                self.mine_mask[level] = local_mask

map = Map(2325)
####
  
camera.fov -= -30
window.size = window.fullscreen_size
window.position = Vec2(0, 0)
app.run()

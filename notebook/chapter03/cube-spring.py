# 画面収録用に独立のpythonプログラムとして準備

# -*- coding: utf-8 -*-
import numpy as np
import vpython as vp

# キャンバスの作成
scene = vp.canvas(width=600, height=300, title='Cube-Spring') # Enable to restart
scene.camera.pos  = vp.vector(0, 3, 3)
scene.camera.axis = vp.vector(0, -2, -4) - scene.camera.pos

# 3次元空間内の原点を見るために，球を原点に配置。
orig = vp.sphere(pos=vp.vector(0,0,0), radius=0.1, color=vp.color.red)
# オブジェクトの作成
# 立方体
cube_size = 1
cube = vp.box(size=vp.vector(cube_size, cube_size, cube_size), color=vp.color.orange)
cube.pos = vp.vector(0, cube.height/2, 0)
# 床
floor = vp.box(length=5.0, height=0.1, width=cube_size+0.2, color=vp.color.green)
floor.pos = vp.vector(0, -floor.height/2, 0)
# 壁
wall  = vp.box(length=0.1, height=1.5, width=floor.width, color=vp.color.yellow)
wall.pos = vp.vector((-wall.length/2-floor.length/2), (wall.height/2 - floor.height) , 0)

#equi_length = box_size/2+floor.height/2 #バネの自然長
#wall_surface_pos = cube_size/2+floor.height/2

# バネ
spring_pos_wall = vp.vector((wall.pos.x+wall.length/2), cube.pos.y, cube.pos.z )
spring_pos_cube = vp.vector( (cube.pos.x-cube.length/2), cube.pos.y, cube.pos.z)
spring = vp.helix(pos=spring_pos_wall, axis=(spring_pos_cube - spring_pos_wall), 
                  radius=0.2,     # バネ径の半径
                  thickness=0.05, # バネ寸法
                  coils=8,        # バネ巻数
                  color=vp.vector(0, 1, 1) # cyan
                 )

def func_pos(k):
    return np.sin(k*0.1)

vp.sleep(5.0)   # 画面収録を始める準備のためのバッファー

for k in range(100):
    scene.capture('cube-spring_{}'.format(k))   #パラパラ漫画として保存、ダウンロードフォルダにしか保存できない
    vp.sleep(0.1)
    x_pos = func_pos(k)
    cube.pos = vp.vector(x_pos, cube.pos.y, 0)
    spring_pos_cube = vp.vector( (cube.pos.x-cube.length/2), cube.pos.y, cube.pos.z)
    spring.axis = spring_pos_cube - spring_pos_wall
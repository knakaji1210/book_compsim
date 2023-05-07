# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import vpython as vp

# Create Scene
scene = vp.canvas(width=600, height=400, title='Animation') # Enable to restart
scene.camera.pos  = vp.vector(0, 6, 10)
scene.camera.axis = vp.vector(0, -2, -8) - scene.camera.pos

# 床の作成，床の真ん中を原点とする
floor = vp.box(length=40, height=0.8, width=60, color=vp.color.green)
floor.pos = vp.vector( 0, -(floor.height/2), -floor.width/2)

# 球の作成
ball_radius = 0.5 # 半径

# 的球の初期位置のx座標
b2_x_init = 2*ball_radius - ball_radius  # theta2 -> 30 [deg]
#b2_x_init = 2*ball_radius - 0.59*ball_radius # theta2 -> 45 [deg]
#b2_x_init = 2*ball_radius - 0.0076*ball_radius # almost theta2 -> 85 [deg]

# 手球b1, 的球b2
b1 = vp.sphere(pos=vp.vector(0, ball_radius, 0), radius=ball_radius, \
               color=vp.color.white)
b2 = vp.sphere(pos=vp.vector(b2_x_init, ball_radius, -8), radius=ball_radius, \
               color=vp.color.red)
# 各パラメータ
v1, v2 = 0.4, 0   # 初期速度
theta1, theta2=0, 0 # 初期角度
c_rest = 0.8 # 反発係数，coefficient of restitution
flag = False  # 衝突判定フラグ，Trueは衝突検知

def ball_step(ball, v, theta):
    coef1 = 1
    x = coef1*v*np.sin(theta)
    z = -coef1*v*np.cos(theta) # 奥行きがマイナスｚ軸方向ゆえ"-"がつく
    ball.pos += vp.vector(x, 0, z)

def check_collision():
#def check_collision(b1, b2, flag):
    global b1, b2, flag, v1, v2, theta1, theta2, c_rest
    dx = b1.pos.x - b2.pos.x
    dz = b1.pos.z - b2.pos.z
    d = np.sqrt(dx*dx + dz*dz)
    if d <= (b1.radius + b2.radius):
        flag = True
        theta2 = np.arcsin(-(b1.pos.x-b2.pos.x)/(2*b1.radius) )
        theta1 = theta2 - np.pi/2
        v2 = 0.5*v1*(1.0 + c_rest)
        v1 = 0.5*v1*(1.0 - c_rest)
    
vp.sleep(3.0)  

for k in range(100):
    vp.sleep(0.01)
    ball_step(b1, v1, theta1)
    ball_step(b2, v2, theta2)
    if not flag:
        check_collision()
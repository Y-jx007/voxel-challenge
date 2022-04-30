from scene import Scene
import taichi as ti
from taichi.math import *

scene=Scene(voxel_edges=0,exposure=1.6)
scene.set_floor(0,(1,1,1))
scene.set_background_color((0.949,0.769,0.110))
scene.set_directional_light((1,0.2,1),0.3,(1,1,1))
scene.renderer.set_camera_pos(0,2,2.5)

sqrt3=1.732

@ti.func
def modposition(l,shift,uv):
    return vec2((uv.x-uv.y/sqrt3-shift.x)%l,((uv.y-shift.y)/sqrt3*2)%l)

@ti.kernel
def initialize_voxels():
    side = 0.1
    line = 0.0064
    for i,j in ti.ndrange(61,56):
        uv = vec2(i/120,(j+4)/120)
        X = modposition(side,vec2(0),uv).x
        Y=modposition(side,vec2(0),uv).y
        if not ((abs(X+Y/2-side/2)>line or Y>side/3) and
                (abs(X+Y/2-side)>line or Y<2.*side/3) and
                (abs(X/sqrt3+Y*2/sqrt3-side/sqrt3)>line or X>side/3) and
                (abs(X/sqrt3+Y*2/sqrt3-2*side/sqrt3)>line or X<2*side/3) and
                (abs(X/sqrt3-Y/sqrt3)>line
                 or sqrt3*X+sqrt3*Y<2*side/sqrt3
                 or sqrt3*X+sqrt3*Y>4*side/sqrt3)):
            col=ti.cos((uv.y-0.25)*(uv.x-0.25)*8)*vec3(0.949,0.769,0.110)
            scene.set_voxel(vec3(i-30,j,52),1,col)
            scene.set_voxel(vec3(i-30,j,-52),1,col)
            scene.set_voxel(vec3(i/2+30,j,52-i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i/2+30,j,-52+i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i/2-60,j,-i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i / 2 - 60, j, i / 2 * sqrt3), 1, col)
    for i,j in ti.ndrange(80,70):
        I,J=i-40,j-35
        if -sqrt3*I+70>J>-sqrt3*I-70 and sqrt3*I+70>J>sqrt3*I-70:
            if I<-20 or (I<20 and J>I/sqrt3):
                scene.set_voxel(vec3(I,0,J),2,vec3(0.6))
            else:
                scene.set_voxel(vec3(I, 0, J), 1, vec3(0.2, 0.3, 0.4))
            if -3<I<3 and -23<J<-17:
                scene.set_voxel(vec3(I,0,J),2,vec3(0.6))
            if -3<I<3 and 17<J<23:
                scene.set_voxel(vec3(I,0,J),1,vec3(0.2,0.3,0.4))

initialize_voxels()

scene.finish()

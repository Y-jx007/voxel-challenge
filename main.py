from scene import Scene
import taichi as ti
from taichi.math import *

scene=Scene(voxel_edges=0,exposure=2)
scene.set_floor(-1,(121/256,85/256,72/256))
scene.set_background_color((179/300,229/300,252/300))
scene.set_directional_light((1,0.3,1),0.3,(1,1,1))
scene.renderer.set_camera_pos(1,2,4)

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
            col=vec3(255, 202, 40)/256*ti.cos((i**2+j**2)/2000) +\
            vec3(255, 255, 0)/256*(1 - ti.cos((i**2+j**2)/2000))
            scene.set_voxel(vec3(i-30,j-64,52),1,col)
            scene.set_voxel(vec3(i-30,j-64,-52),1,col)
            scene.set_voxel(vec3(i/2+30,j-64,52-i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i/2+30,j-64,-52+i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i/2-60,j-64,-i/2*sqrt3),1,col)
            scene.set_voxel(vec3(i / 2 - 60, j-64, i / 2 * sqrt3), 1, col)
    for i,j,k in ti.ndrange(80,80,40):
        I,J,K=i-40,j-40,k
        if abs(-sqrt3*I+2*sqrt3*J-6*K)<6\
                and 0<-12*I+J+5*sqrt3*K<320 and 0<12*I+7*J+3*sqrt3*K<320:
                for n in range(6):
                    scene.set_voxel(vec3(I*ti.cos(n*3.14/3)-J*ti.sin(n*3.14/3),
                                         K-34,I*ti.sin(n*3.14/3)+J*ti.cos(n*3.14/3)),1,
                                    vec3(100,181,246)/256*(n/2+3)*ti.cos(I*J/160)/3+
                                    vec3(103,58,183)/256*(n/2+3)*(1-ti.cos(I*J/160))/3
                                    )
        if abs(I**2+J**2)<4 and K<30:
            scene.set_voxel(vec3(I,K-64,J),2,vec3(100,221,23)/256)

initialize_voxels()

scene.finish()

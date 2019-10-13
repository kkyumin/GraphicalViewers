import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

leftPressed = False
rightPressed = False
originX = 0
originY = 0
rotateX= 90
rotateY=15
originPanningX =0
originPanningY =0
panningX = 0
panningY = 0
radius = 8
offset = np.identity(4)


oldPointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]
pointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]

targetX = 0
targetY = 0
targetZ = 0
x =0
y=0
z=0
def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()


def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) /float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def mouseCallback(window, button, action, mods):
    global leftPressed
    global rightPressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            leftPressed = True
        elif action== glfw.RELEASE:
            leftPressed = False
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            rightPressed = True
        elif action== glfw.RELEASE:
            rightPressed = False

def cursorCallback(window, xpos, ypos):
    global rotateX,rotateY
    global originX,originY
    global originPanningX,originPanningY
    global panningX,panningY
    if (leftPressed == True):

        rotateX = rotateX+(xpos- originX)
        rotateX = rotateX % 360

        rotateY = rotateY+(ypos- originY)
        rotateY = rotateY % 360

        #to avoid "Gimbal lock"
        if (rotateY % 90 == 0):
            rotateY += 0.1
    originX = xpos
    originY = ypos


    if(rightPressed == True):
        panningX = panningX+ (xpos-originPanningX)
        panningY = panningY+ (ypos-originPanningY)
    originPanningX = xpos
    originPanningY = ypos

    #



def scrollCallback(window,xoffset,yoffset):
    global radius

    radius -= yoffset
    if(radius > 50):
        radius = 50
    if(radius <0):
        radius = 0

def myLookAt(eye, at, up):
#
#     #implement here

    global pointOffset
    global oldPointOffset
    global x,y,z
    w = (eye-at)/(np.sqrt(np.dot((eye-at),(eye-at))))
    u = (np.cross(up,w)) / (np.sqrt(np.dot(np.cross(up,w), np.cross(up,w))))
    v = np.cross(w,u)


    Ma = np.array([
        [u[0], v[0], w[0], eye[0]],
        [u[1], v[1], w[1],  eye[1]],
        [u[2], v[2], w[2],  eye[2]],
        [0, 0, 0, 1]
    ])


    Mview = np.array([
        [u[0], u[1], u[2],-u@eye],
        [v[0],v[1],v[2],-v@eye],
        [w[0],w[1],w[2],-w@eye],
        [0,0,0,1]
    ])


    translateView = np.array([
        [1, 0, 0,-0.005*panningX],
        [0,1,0,0.005*panningY],
        [0,0,1,0],
        [0,0,0,1]
    ])


    #offset = translateView @ Mview
    offset = Ma@translateView
    MInv = np.linalg.inv(offset)
    offset = np.transpose(offset)
    pointOffset = offset[3]
    x = oldPointOffset[0] - pointOffset[0]
    y = oldPointOffset[1] - pointOffset[1]
    z = oldPointOffset[2] - pointOffset[2]

    #print(oldPointOffset, pointOffset)
    translateView = np.transpose(translateView)
    Mview = np.transpose(Mview)


    oldPointOffset = pointOffset
#     print("X",x)
#     print("Y",y)
#     print("Z",z)
    # offset = oldOffset - offset


    glMultMatrixf(MInv.T)
    # glMultMatrixf(translateView)
    # glMultMatrixf(Mview)


def drawXFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([-5., 0., 0.]))
    glVertex3fv(np.array([5., 0., 0.]))
    glEnd()

def drawZFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0, 0., -5.]))
    glVertex3fv(np.array([0, 0., 5.]))
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)

    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1, 0., 0.]))

    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1, 0.]))
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1]))
    glEnd()

def drawXFrameArray():
            for k in range(10):
                glPushMatrix()
                glTranslatef(0,0,.5 * (k+1))
                #glScalef(.5,.5,.5)
                drawXFrame()
                glPopMatrix()
            for k in range(10):
                glPushMatrix()
                glTranslatef(0, 0, .5* (-k -1))
                # glScalef(.5,.5,.5)
                drawXFrame()
                glPopMatrix()

def drawZFrameArray():
    for k in range(10):
        glPushMatrix()
        glTranslatef(.5 * (k + 1), 0, 0)
        # glScalef(.5,.5,.5)
        drawZFrame()
        glPopMatrix()
    for k in range(10):
        glPushMatrix()
        glTranslatef(.5* (-k -1), 0, 0)
        # glScalef(.5,.5,.5)
        drawZFrame()
        glPopMatrix()

def render():
    global rotateX, rotateY
    global radius
    global offset,oldOffset
    global x,y,z
    global targetX
    global targetY
    global targetZ

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    # Above two lines must behaves exactly same as the below two lines
    # glRotatef(c[0], 0, 1, 0)
    # glRotatef(c[1], 1, 0 ,0)

    gluPerspective(60, 1, 1,100)
    rotateXB = np.radians(rotateX)
    rotateYB = np.radians(rotateY)

    targetX += x
    targetY += y
    targetZ += z

    # print("Target:" ,targetX,targetY,targetZ)


    if(rotateY <90):
        #gluLookAt(radius*np.cos(rotateXB)*np.cos(rotateYB), radius*np.sin(rotateYB), radius*np.cos(rotateYB)*np.sin(rotateXB), 0,0,0, 0,1,0)
        myLookAt(np.array([radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB),radius * np.cos(rotateYB) * np.sin(rotateXB)]), np.array([0,0,0]), np.array([0, 1, 0]))
    elif(rotateY>=90 and rotateY<270):
        myLookAt(np.array(
            [radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB), radius * np.cos(rotateYB) * np.sin(rotateXB)]),
            np.array([0, 0, 0]), np.array([0, -1, 0]))
    elif(rotateY >= 270):
        myLookAt(np.array(
            [radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB), radius * np.cos(rotateYB) * np.sin(rotateXB)]),
                 np.array([0,0,0]), np.array([0, 1, 0]))

    M = np.identity(4)

    # glMultMatrixf(M.T)


    drawFrame()
    drawXFrameArray()
    drawZFrameArray()

    glColor3ub(255, 255, 255)
    # drawCube()

    t = glfw.get_time()
    t = t*2

    drawXFrameArray()
    drawZFrameArray()

    glColor3ub(255, 255, 255)

    walk = t
    glRotatef(t* (180 / np.pi), 0, 1, 0)

    glPushMatrix()
    glTranslatef(0,3.0,0)
    glTranslatef(0,0,0)
    # glTranslatef(0, 0,0.5*walk)

    # if(rotateOffset % 1500 > 750):
    #     glRotatef(45,0,1,0)
    #     glTranslatef(0, 0, 0.1 * walk)
    # if (rotateOffset % 1500 < 750):
    #     glRotatef(-45, 0, 1, 0)
    #     glTranslatef(0, 0, 0.1 * walk)
    # if( np.floor(t*100) % 200 == 0):
    #     glRotatef(180, 0, 1, 0)



    #body : hierarchy 1
    glPushMatrix()
    glRotatef(-5,1,0,0)
    glRotatef(5* np.sin(t*5),1,0,0)
    glScalef(0.3,0.4,0.2)

    glTranslatef(0,np.sin(5*t),0)
    glPushMatrix()
    glColor3f(1,0,0)
    drawCube()
    glPopMatrix()

    #head : hierarchy 2
    glPushMatrix()

    glTranslatef(0,1.8,0)
    glTranslatef(0,0,np.sin(5*t))
    #glRotatef(-30*(np.sin(t*5)),0,1,0)
    glScalef(0.5,.6,.8)
    glColor3f(1,1,0)
    drawSphere()
    glPopMatrix()


    #left upper arm : hierarchy 2
    glPushMatrix()
    glColor3f(1,0,0)
    glTranslatef(-1.5,0.5,0)
    glRotatef(-60,0,0,1)
    glRotatef(-10*(1+np.sin(5*t)),1,0,0)
  # glScalef(0.35,.5,0.4)
    glScalef(0.3, 0.6, 0.5)
    drawCube()


    #left lower arm : hierarchy 3
    glPushMatrix()

    glColor3f(1,1,0)

    glRotatef(-110,0,0,1)
    glRotatef(30,1,0,0)
    glRotatef(-60*(1+np.sin(5*t)),1,0,0)
    glTranslatef(1,-2,0)


    glScalef(0.7,2,1)

    glPushMatrix()
    drawCube()
    glPopMatrix()

    #left hand : hierarchy 4
    glPushMatrix()
    glTranslatef(0,-1.5,.0)
    glScalef(1.0,0.5,1.0)
    glTranslatef((-1+np.sin(5*t)),0,0)
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


    #right upper arm : hierarchy 2

    glPushMatrix()
    glColor3f(1,0,0)
    glTranslatef(1.2,0.4,0)
    glRotatef(-30,1,0,0)
    glRotatef(20*(1+np.sin(5*t)),1,0,0)
    glTranslatef(0,0,0.5*np.sin(5*t))

    glScalef(0.3, 0.6, 0.5)

    drawCube()
    #right lower arm : hierarchy 3

    glPushMatrix()
    glTranslatef(0,-2.0,.0)
    glColor3f(1,1,0)
    glRotatef(-15,1,0,0)
    glRotatef(20*(np.sin(5*t)),0,1,0)
    glScalef(0.6,2,0.8)

    drawCube()
    #right hand : hierarchy 4

    glPushMatrix()
    glTranslatef(0,-1.5,.0)
    glScalef(1.0,0.5,1.0)
    glTranslatef(0,0.5*np.sin(5*t),0.5*np.sin(5*t))
    drawSphere()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


    #right upper leg : hierarchy 2
    glPushMatrix()
    glScalef(0.5,1.0,1)
    glColor3ub(50, 240, 240)
    glTranslatef(1,-2.5,0)
    glTranslatef(0,0.3* (0.4+np.sin(5*t)),0.8*np.sin(5*t))
    drawCube()

    #right lower leg : hierarchy 3
    glPushMatrix()
    glScalef(1,1.5,1)
    glTranslatef(0,-1.5,0)
    glTranslatef(0.4*np.sin(5*t),0,0)
    glRotatef( 10,1,0,0)
    drawCube()

    #right lower foot : hierarchy 4
    glPushMatrix()
    glScalef(0.9,0.3,1.25)
    glTranslatef(0,-4,0.5)
    glRotatef( -50*np.sin(5*t),1,0,0)
    drawCube()

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    #left upper leg: hierarchy 2
    glScalef(0.5,1.0,1)
    glTranslatef(-1,-2.5,0)
    glRotatef(-25, 1, 0, 0)
    glTranslatef(0, 0, np.sin(5*t))
    drawCube()
    #left lower leg :: KICK: hierarchy 3
    glPushMatrix()
    glScalef(1,1.5,1)
    glTranslatef(0,-1.5,-1)
    glRotatef(60, 1, 0, 0)
    glRotatef(-60*(0.2+np.sin(t*5)),1,0,0)
    drawCube()

    #left foot: hierarchy 4
    glPushMatrix()
    glScalef(0.9,0.3,1.25)
    glTranslatef(0,-4,0.5)
    glRotatef( -15*(np.sin(t*5)+0.2),1,0,0)
    drawCube()
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()



def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2015028077-Assingnment-1", None, None)
    if not window:
        glfw.terminate()
        return


    glfw.set_cursor_pos_callback(window,cursorCallback)
    glfw.set_mouse_button_callback(window,mouseCallback)
    glfw.set_input_mode(window, glfw.STICKY_MOUSE_BUTTONS, 1)
    glfw.set_scroll_callback(window,scrollCallback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        #calculatePositionDiff(window)
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

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
mode = 1
forced = 1
vlist = list()
vnlist = list()
flist = list()

gVertexArray = list()
gNormalArray = list()
gForcedNormalArray = list()
gVertexArray = np.array(gVertexArray)
gNormalArray = np.array(gNormalArray )

oldPointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]
pointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]

targetX = 0
targetY = 0
targetZ = 0
x =0
y=0
z=0



def drawObjectSeperate():
    # print("start")

    for i in flist:
        glBegin(GL_POLYGON)
        # print(i)
        i = i[:3]
        for j in i:
            # print(j)
            if '/' in j:
                j = j.split('/')
                # print(j)
            # print(vlist[int(j[0])-1])
                glNormal3fv(vnlist[int(j[2]) - 1])
                glVertex3fv(vlist[int(j[0])-1])
                print(vlist[int(j[0])-1])
            else:
                glVertex3fv(vlist[int(j)-1])
        glEnd()
    # print("end")


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

def dropCallback(window,paths):

    global vlist
    global vnlist
    global flist
    global gVertexArray
    global gNormalArray
    global gForcedNormalArray
    gVertexArray= list()
    gNormalArray = list()
    gForcedNormalArray = list()
    gVertexArray.clear()
    gNormalArray.clear()
    gForcedNormalArray.clear()
    file = open(paths[0],"r", encoding='UTF8')
    vlist.clear()
    vnlist.clear()
    flist.clear()

    num3vface = 0
    num4vface = 0
    numMvface = 0
    numtotalface = 0
    while True:
        line = file.readline()
        if not line:
            break
        line = line.replace("\n","")
        if not line:
            continue
        splited = line.split()
        # print(splited)
        # print(splited)

        if(splited[0] == 'v'):
            toFloatList = map(float,splited[1:])

            toFloatList = list(toFloatList)
            vlist.append(toFloatList)
        elif(splited[0] == 'vn'):
            toFloatList = map(float,splited[1:])

            toFloatList = list(toFloatList)
            vnlist.append(toFloatList)
        elif(splited[0] == 'f'):
            numtotalface +=1
            splited = splited[1:]
            if(len(splited) == 3):
                num3vface+=1
            if(len(splited) == 4):
                num4vface+=1
            if(len(splited) > 4):
                numMvface+=1
            flist.append(splited)
    # print(vnlist)
    print("File Loading..")
    print("File name: ",paths[0])
    print("Total Face: ",numtotalface)
    print("Total 3 Vertex Face: ",num3vface)
    print("Total 4 Vertex Face: ", num4vface)
    print("Total Multi Vertex Face: ",numMvface)
    file.close()

    vertexIndexList = list()
    for i in flist:
        # print(i)
        i = i[:3]
        # print(i)
        for indexSplited in i:
            # print(indexSplited)
            if '/' in indexSplited:
                indexSplited = indexSplited.split('/')
                # print(indexSplited)
                # print(len(indexSplited))
                # print(vlist[int(indexSplited[0])-1])
                # gNormalArray.append(tuple(vnlist[int(indexSplited[2]) - 1]))
                if len(indexSplited) == 3:
                    gNormalArray.append(tuple(vnlist[int(indexSplited[2]) - 1]))
                    # gVertexArray.append(tuple(vnlist[int(indexSplited[2]) - 1]))
                    # print(vnlist[int(indexSplited[2]) - 1])
                    gVertexArray.append(tuple(vlist[int(indexSplited[0]) - 1]))
                    vertexIndexList.append(int(indexSplited[0]))
                    # print(vlist[int(indexSplited[0]) - 1])
                elif len(indexSplited) ==2:
                    # gVertexArray.append(tuple(vnlist[int(indexSplited[2]) - 1]))
                    # print(vnlist[int(indexSplited[2]) - 1])
                    gVertexArray.append(tuple(vlist[int(indexSplited[0]) - 1]))
                    vertexIndexList.append(int(indexSplited[0]))
                # print(int(indexSplited[0]))
                # gVertexArray = np.append(gVertexArray,vlist[int(indexSplited[0])-1])
            else:
                gVertexArray.append(tuple(vlist[int(indexSplited)-1]))
                vertexIndexList.append(int(indexSplited[0]))




    #get face normal


    vertexIndexList = np.array(vertexIndexList)
    vertexIndexList = vertexIndexList.reshape(int(vertexIndexList.size/3),3)
    forcedNormalList = list()
    # print(vertexIndexList)

    faceNormalList = []
    for i in vertexIndexList:
        v1 = np.array(vlist[i[1]-1]) - np.array(vlist[i[0]-1])
        v2 = np.array(vlist[i[2] - 1]) - np.array(vlist[i[0] - 1])
        crossed = np.cross(v1,v2)
        if(math.isnan(crossed[0]) or math.isnan(crossed[1] or math.isnan(math.isnan(crossed[2])))):
            crossed = [0.00001,0.00001,0.00001]
        result = crossed / np.sqrt(np.dot(crossed,crossed))
        faceNormalList.append(result)

    try:
        for i in range(len(vlist)):
            i = i+1
            index = -1
            sum = 0
            for j in vertexIndexList:
                index += 1
                for k in j:
                    if (k ==i):
                        sum+= faceNormalList[index]
                        break
            result = sum / np.sqrt(np.dot(sum,sum))
            forcedNormalList.append(result)


        forcedNormalList = np.array(forcedNormalList,"float32")
        for i in vertexIndexList:
            for j in i:
                gForcedNormalArray.append(forcedNormalList[j-1])
        gForcedNormalArray = np.array(gForcedNormalArray, "float32")
    except:
        forcedNormalList.clear()
        gForcedNormalArray.clear()



    # gVertexArray = np.asarray(gVertexArray)
    gVertexArray = np.array(gVertexArray,"float32")
    gNormalArray = np.array(gNormalArray,"float32")

    print("File Load End: Start Rendering")


def drawObjectArray():
    global gVertexArray
    global gNormalArray
    global gForcedNormalArray
    global forced

    varr = gVertexArray
    if(forced>0):
        narr = gNormalArray
    else:
        narr = gForcedNormalArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT,3*varr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))
    # glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    # glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    # glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))




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



def key_callback(window, key, scancode, action, mods):
    global mode
    global forced
    global objectColor, lightColor;
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Z:
            mode *= -1
        if key==glfw.KEY_S:
            forced *= -1

def scrollCallback(window,xoffset,yoffset):
    global radius

    radius -= yoffset
    if(radius > 100):
        radius = 100
    if(radius <0):
        radius = 0

def myLookAt(eye, at, up):
#


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
    global mode

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Above two lines must behaves exactly same as the below two lines
    # glRotatef(c[0], 0, 1, 0)
    # glRotatef(c[1], 1, 0 ,0)
    gluPerspective(60, 1, 1,100)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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

    if mode>0:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glPushMatrix()
    glDisable(GL_LIGHTING)
    drawFrame()
    drawXFrameArray()
    drawZFrameArray()
    glPopMatrix()




    glPushMatrix()
    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)

    lightPos = (3,4,5,0)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    lightColor = (1.,0.,0,1.)
    lightSpecularColor = (1., 1., 1, 1.)
    ambientLightColor = (0,0.3,0,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecularColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    glEnable(GL_LIGHT1)
    lightPos1 = (-3,-4,-5,1)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    lightColor1 = (0,0.,0.5,1.)
    lightSpecularColor1 = (1., 1., 1, 1.)
    ambientLightColor1 = (0,.0,0.5,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightSpecularColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)



    # objectColor = (0.46,0.73,0.70,1.)
    # objectColor = (1,1,1,1.)
    # specularObjectColor = (1.,1.,1.,1.)
    # glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    # glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    # glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    # drawObjectSeperate()
    drawObjectArray()
    glPopMatrix()
    # drawCube()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2015028077-Assingnment-2", None, None)
    if not window:
        glfw.terminate()
        return


    glfw.set_cursor_pos_callback(window,cursorCallback)
    glfw.set_key_callback(window,key_callback)
    glfw.set_mouse_button_callback(window,mouseCallback)
    glfw.set_input_mode(window, glfw.STICKY_MOUSE_BUTTONS, 1)
    glfw.set_scroll_callback(window,scrollCallback)
    glfw.set_drop_callback(window,dropCallback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        #calculatePositionDiff(window)
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
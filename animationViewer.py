import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import numpy.linalg as lin


position = list()

class StackJoint:
    def __init__(self, name, parent):
        self.name = name
        self.offset = list()
        self.channelOrder = list()
        self.channelNum = 0
        self.parent = parent
        self.channel = list()
        self.child = list()
        self.position = list()
        self.rotMatrix = list()
    def addOffset(self,outOffset):
        self.offset.append(outOffset)
    def addChannelOrder(self,outChannel):
        self.channelOrder.append(outChannel)
    def addChannelNum(self,outChannelNum):
        self.channelNum = outChannelNum
    def getChannelNum(self):
        return self.channelNum
    def addPosition(self,otherPosition):
        self.position.append(otherPosition)
    def getPosition(self):
        return self.position

    def addRotMatrix(self,otherRotMatrix):
        self.rotMatrix.append(otherRotMatrix)
    def getRotMatrix(self):
        return self.rotMatrix


    def getOffset(self):
        return self.offset
    def addChannel(self,someList):
        self.channel.append(someList)
    def getChannelOrder(self):
        return self.channelOrder
    def getChild(self):
        return self.child
    def getChannel(self):
        return self.channel
    def getParent(self):
        return self.parent
    def addChild(self,otherChild):
        self.child.append(otherChild)
    def getName(self):
        return self.name

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
rotateMatrixf = list()
frame = 1
animate = 1
gVertexArray = list()
gNormalArray = list()
gForcedNormalArray = list()
gVertexArray = np.array(gVertexArray)
gNormalArray = np.array(gNormalArray )

jointStack = list()
pressTime = 0
# When start, it is the first value of Camera point :: I feel shame to hardcode this.
oldPointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]
pointOffset = [4.73167189e-16,2.07055236e+00,7.72740661e+00,1.00000000e+00]

targetX = 0
targetY = 0
targetZ = 0
x =0
y=0
z=0



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
def xRotate(theta):
    theta = np.radians(-theta)
    return np.array([[1,0,0,0],[0,np.cos(theta),-np.sin(theta),0],[0,np.sin(theta),np.cos(theta),0],[0,0,0,1]])

def yRotate(theta):
    theta = np.radians(-theta)
    return np.array([[np.cos(theta),0,np.sin(theta),0],[0,1,0,0],[-np.sin(theta),0,np.cos(theta),0],[0,0,0,1]])

def zRotate(theta):
    theta = np.radians(-theta)
    return np.array([[np.cos(theta),-np.sin(theta),0,0],[np.sin(theta),np.cos(theta),0,0],[0,0,1,0],[0,0,0,1]])

def dropCallback(window,paths):

    global number
    global animate

    global joinStack
    global position
    global frame
    global frametime
    global rotateMatrixf
    file = open(paths[0],"r", encoding='UTF8')

    animate = 1
    number = 0
    jointNameList =list()
    jointStack.clear()
    rotateMatrixf.clear()
    name = " "
    index = 0
    joint =None
    mode = 0
    frame = 0
    frametime = .0
    endsite = 0
    parent = None
    position.clear()
    for line in file:
        line = line.replace("\n", "")
        line = line.strip()
        line = line.split()
        # print(line)
        if ("HIERARCHY" in line):
            mode = 0
            continue
        if(mode == 0):
            if ("ROOT" in line):
                number += 1
                name = line[1]
                jointNameList.append(name)
                joint = StackJoint(name, None)
                jointStack.append(joint)
                continue
            if ("JOINT" in line):
                number += 1
                name = line[1]
                jointNameList.append(name)
                joint = StackJoint(name, parent)
                joint.getParent().addChild(joint)
                jointStack.append(joint)
                index += 1
                continue
            if "End" in line[0] and "Site" in line[1]:
                joint = StackJoint("EndSite", parent)
                joint.getParent().addChild(joint)
                jointStack.append(joint)
                index += 1
                endsite = 1
                continue
            if("{" in line):
                if(endsite !=1):
                    parent = joint
                # parent = joint
                jointStack.append(StackJoint("{",None))
                continue
            if ("}" in line):
                if(endsite==1):
                    endsite = 0
                else:
                    joint = joint.getParent()
                    parent = joint.getParent()
                # joint = joint.getParent()
                jointStack.append(StackJoint("}",None))

                continue
            if("OFFSET" in line):
                line.remove("OFFSET")
                line = list(map(float, line))
                for i in line:
                    joint.addOffset(i)
                continue
            if("CHANNELS" in line):
                line.remove("CHANNELS")
                line = line[1:]
                channelCount = 0
                for i in line:
                    if("rotation" in i.lower()):
                        joint.addChannelOrder(i)
                        channelCount += 1
                    # joint.addChannelNum()
                # print(channelCount)
                joint.addChannelNum(channelCount)
                # joint.addChannelNum(len(line))
                # joint.addChannel(line)
                continue

        if ("MOTION" in line):
            mode = 1
            continue
        if(mode == 1):
            if("Frames:" == line[0]):
                frame = int(line[1])
                continue
            if ("Frame" == line[0] and "Time:" == line[1]):
                frametime = float(line[2])
                continue
            else:
                # print("============")
                line = list(map(float, line))
                jointPointer = 3
                # print(line)
                position.append(line[0:3])
                for joint in jointStack:
                    channum = joint.getChannelNum()
                    if(channum != 0):
                        # print(line[jointPointer:jointPointer+channum])
                        joint.addPosition(line[0:3])
                        joint.addChannel(line[jointPointer:jointPointer+channum])
                        jointPointer+= channum



    # print(position)
    # for joint in jointStack:
    #     channum = joint.getChannelNum()
    #     if(channum != 0):
    #         print(joint.getChannelOrder())


    count = 0
    for joint in jointStack:
        if(joint.getChannelNum() == 0):
            continue
        # for i in range(frame):
        #     for j in range(joint.getChannelNum()):
        #         print(joint.getChannelOrder()[j])
        #         print(joint.getChannel()[i][j])
        #     print(joint.getPosition()[i])
        for i in joint.getChannel():
            # print(i)
            rotateM = np.identity(4)
            for j in range(len(i)):
                # print(i[j])
                # print(joint.getChannelOrder()[j].lower())
                if(joint.getChannelOrder()[j].lower() == "xrotation"):
                     rotateM = xRotate( i[j] ) @ rotateM
                if (joint.getChannelOrder()[j].lower() == "yrotation"):
                    rotateM = yRotate(i[j]) @ rotateM
                if (joint.getChannelOrder()[j].lower() == "zrotation"):
                    rotateM = zRotate(i[j]) @ rotateM
            joint.addRotMatrix(rotateM)


    #
    # for joint in jointStack:
    #     if(joint.name != "{" and joint.name != "}"):
    #         print("Name: "+ joint.name)
    #         # if(joint.getParent() != None):
    #         #     print("Parent"+ joint.getParent().name)
    #         # if(joint.getParent() == None):
    #         #     print("Parent NONE")
    #         # if(joint.getChild() != None):
    #         #     for i in joint.getChild():
    #         #         print("Child"+i.name)
    #         # if(joint.getChild() == None):
    #         #     print("Child : NONE")
    #         # print(joint.offset)
    #         # print(joint.getChannel())
    #         # print(joint.getRotMatrix())

    rotateMatrixf = jointStack[0].getRotMatrix()

    print("Name: " + paths[0])
    print("Number of Frame: " +  str(frame))
    print("FPS: "+str(1/frametime))
    print("Number of Joint: " +str(number))
    print("Joint Name List")
    for jointName in jointNameList:
        print("   "+ jointName)





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
    global animate
    global pressTime
    global objectColor, lightColor;
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Z:
            mode *= -1
        if key==glfw.KEY_S:
            forced *= -1
        if key==glfw.KEY_SPACE:
            animate *= -1
            pressTime = glfw.get_time()

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
        [1, 0, 0,-0.015*panningX],
        [0,1,0,0.015*panningY],
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
    # print(offset)

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
    glVertex3fv(np.array([-100., 0., 0.]))
    glVertex3fv(np.array([100., 0., 0.]))
    glEnd()

def drawZFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([0, 0., -100.]))
    glVertex3fv(np.array([0, 0., 100.]))
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)

    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1, 0., 0.]))

    glColor3ub(0, 255,0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1, 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1]))
    glEnd()

def drawLine(offset):
    # glBegin(GL_LINES)
    # glColor3ub(255, 255, 255)
    # glVertex3fv(np.array([-offset[0],-offset[1],-offset[2]]))
    # glVertex3fv(np.array([0., 0., 0.]))
    # glEnd()
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3fv(offset)
    glEnd()

def drawXFrameArray():
            for k in range(200):
                glPushMatrix()
                glTranslatef(0,0,.5 * (k))
                #glScalef(.5,.5,.5)
                drawXFrame()
                glPopMatrix()
            for k in range(200):
                glPushMatrix()
                glTranslatef(0, 0, .5* (-k ))
                # glScalef(.5,.5,.5)
                drawXFrame()
                glPopMatrix()

def drawZFrameArray():
    for k in range(200):
        glPushMatrix()
        glTranslatef(.5 * (k ), 0, 0)
        # glScalef(.5,.5,.5)
        drawZFrame()
        glPopMatrix()
    for k in range(200):
        glPushMatrix()
        glTranslatef(.5* (-k ), 0, 0)
        # glScalef(.5,.5,.5)
        drawZFrame()
        glPopMatrix()

def render(time):
    global rotateX, rotateY
    global radius
    global offset,oldOffset
    global x,y,z
    global targetX
    global targetY
    global targetZ
    global mode
    global jointStack
    global position
    global frame
    global rotateMatrixf
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Above two lines must behaves exactly same as the below two lines
    # glRotatef(c[0], 0, 1, 0)
    # glRotatef(c[1], 1, 0 ,0)
    gluPerspective(60, 1, 1,10000)


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


    # print(time)
    renderJoint = StackJoint("Temp",0)



    glPushMatrix()

    if position:
        tempPos = position[time]
        tempM = np.array(
            [[1., .0, .0, 0], [.0, 1., .0, .0], [.0, .0, 1., .0], [tempPos[0], tempPos[1], tempPos[2], 1.]])
        # glTranslatef(tempPos[0],tempPos[1],tempPos[2])
        glMultMatrixf(tempM)
        glMultMatrixf(rotateMatrixf[time])

    for joint in jointStack:
        if "{" in joint.name:
            glPushMatrix()
            offset = renderJoint.offset

            # channelOrder = joint.getChannelOrder
            # for i in joint.getChannelNum:
            #     if(channelOrder[i] == "XROTATION"):
            #         glRotatef(,1,0,0)
            #     if (channelOrder[i] == "YROTATION"):
            #         glRotatef()
            #     if (channelOrder[i] == "ZROTATION"):

            #         glRotatef()
            parent = renderJoint.getParent()
            if(parent == None):
                parentOffset = [0,0,0]
            else:
                parentOffset = parent.getOffset()
                # offset = parentOffset
                translateM = np.array([[1.,.0,.0,0],[.0,1.,.0,.0],[.0,.0,1.,.0],[offset[0],offset[1],offset[2],1.]])
                # glTranslatef(offset[0],offset[1],offset[2])

                rotateM = np.identity(4)

                if(renderJoint.getRotMatrix()):
                    rotateM = renderJoint.getRotMatrix()[time]
                    # print(rotateM)

                invertRotateM = lin.inv(rotateM)
                invertRotateM = lin.inv(rotateM).T
                glMultMatrixf(translateM)
                glMultMatrixf(rotateM)

                invertTranslateM = lin.inv(translateM)
                invertTranslateM = invertTranslateM.T


                glBegin(GL_LINES)
                glColor3ub(0, 0, 255)
                glVertex3f(0, 0, 0)
                glVertex3fv((invertRotateM @ invertTranslateM @ np.array([0,0,0,1]))[:-1] )
                glEnd()

                continue
        if "}" in joint.name:
            glPopMatrix()
            continue
        else:
            renderJoint = joint
    glPopMatrix()

def render2():
    global rotateX, rotateY
    global radius
    global offset, oldOffset
    global x, y, z
    global targetX
    global targetY
    global targetZ
    global mode
    global jointStack
    global position
    global frame
    global rotateMatrixf
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Above two lines must behaves exactly same as the below two lines
    # glRotatef(c[0], 0, 1, 0)
    # glRotatef(c[1], 1, 0 ,0)
    gluPerspective(60, 1, 1, 10000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    rotateXB = np.radians(rotateX)
    rotateYB = np.radians(rotateY)

    targetX += x
    targetY += y
    targetZ += z

    # print("Target:" ,targetX,targetY,targetZ)

    if (rotateY < 90):
        # gluLookAt(radius*np.cos(rotateXB)*np.cos(rotateYB), radius*np.sin(rotateYB), radius*np.cos(rotateYB)*np.sin(rotateXB), 0,0,0, 0,1,0)
        myLookAt(np.array([radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB),
                           radius * np.cos(rotateYB) * np.sin(rotateXB)]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    elif (rotateY >= 90 and rotateY < 270):
        myLookAt(np.array(
            [radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB),
             radius * np.cos(rotateYB) * np.sin(rotateXB)]),
            np.array([0, 0, 0]), np.array([0, -1, 0]))
    elif (rotateY >= 270):
        myLookAt(np.array(
            [radius * np.cos(rotateXB) * np.cos(rotateYB), radius * np.sin(rotateYB),
             radius * np.cos(rotateYB) * np.sin(rotateXB)]),
            np.array([0, 0, 0]), np.array([0, 1, 0]))

    M = np.identity(4)

    # glMultMatrixf(M.T)

    if mode > 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glPushMatrix()
    glDisable(GL_LIGHTING)
    drawFrame()
    drawXFrameArray()
    drawZFrameArray()
    glPopMatrix()

    # print(time)
    renderJoint = StackJoint("Temp", 0)

    glPushMatrix()

    # if position:
        # tempPos = position[0]
        # tempM = np.array(
        #     [[1., .0, .0, 0], [.0, 1., .0, .0], [.0, .0, 1., .0], [tempPos[0], tempPos[1], tempPos[2], 1.]])
        # glTranslatef(tempPos[0],tempPos[1],tempPos[2])


        # glMultMatrixf(tempM)
        # glMultMatrixf(rotateMatrixf[0])
    for joint in jointStack:
        if "{" in joint.name:
            glPushMatrix()
            offset = renderJoint.offset

            # channelOrder = joint.getChannelOrder
            # for i in joint.getChannelNum:
            #     if(channelOrder[i] == "XROTATION"):
            #         glRotatef(,1,0,0)
            #     if (channelOrder[i] == "YROTATION"):
            #         glRotatef()
            #     if (channelOrder[i] == "ZROTATION"):

            #         glRotatef()
            parent = renderJoint.getParent()
            if (parent == None):
                parentOffset = [0, 0, 0]
            else:
                parentOffset = parent.getOffset()
                # offset = parentOffset
                translateM = np.array(
                    [[1., .0, .0, 0], [.0, 1., .0, .0], [.0, .0, 1., .0], [offset[0], offset[1], offset[2], 1.]])
                # glTranslatef(offset[0],offset[1],offset[2])


                glMultMatrixf(translateM)

                invertTranslateM = lin.inv(translateM)
                invertTranslateM = invertTranslateM.T

                glBegin(GL_LINES)
                glColor3ub(0, 0, 255)
                glVertex3f(0, 0, 0)
                glVertex3fv((invertTranslateM @ np.array([0, 0, 0, 1]))[:-1])
                glEnd()

                continue
        if "}" in joint.name:
            glPopMatrix()
            continue
        else:
            renderJoint = joint
    glPopMatrix()

    # drawCube()

def renderWrapper():
    global animate,frame
    global pressTime
    global frametime
    if(animate> 0):
        render2()
    else:
        time = glfw.get_time()-pressTime
        render(int(time* (1/frametime))%frame)
def main():
    global frame
    global animate

    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2015028077-Assingnment-3", None, None)
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
    # if (animate < 1):
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        #calculatePositionDiff(window)

        glfw.poll_events()
        # if(animate > 1):
        #     render()
        # if(animate<1):
        renderWrapper()
        # render(int(t*50)%frame)
        glfw.swap_buffers(window)


    glfw.terminate()

if __name__ == "__main__":
    main()
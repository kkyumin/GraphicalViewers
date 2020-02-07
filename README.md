# Blender-Like Graphical Renderer

 **PyOpenGL**을 사용한 그래픽 렌더러 모음. 외부 라이브러리의 메소드 사용은 최소화하였고, Numpy를 이용하여 최대한 수식 계산을 통해 직접 메소드를 만들어서 렌더링 하려고 노력하였음


## Files

1. 카메라 시스템  cameraSystem,py
 
    Quaternion이나 Rotation Axis 개념을 알기 이전에 만든 Camera System.
    Spherical Coordinate를 이용한 카메라 배치
    카메라의 위치가 중심점을 기준으로 구의 표면을 돈다는 가정.

    구의 표면을 통한 위치 변화 = Rotating
    구의 반지름 변화 = Zooming
    구의 중심점 변화 = Panning

    실행시 Animation은 Hierarchial한 구조와 Local Coordiante 개념 이해 용으로 코딩해봤음      
2. 오브젝트 파일 뷰어 objviewer,py

     obj file drag-drop시 렌더링 시작

     Flat-shading과 Gouraud Shading 둘 다 구현
     Gouraud Shading은 주변 Vector 값 이용하여 직접 계산하는 Function 구현

3. bvh 파일 뷰어 animationViewer,py

     Hierarchial한 구조와 local coordinate 개념, Stack을 활용.
     bvh 파일의 내용을 Stack에 담은 이후 Parent-Child 관계일 경우 local coordinate로 Animating 해 주었다.

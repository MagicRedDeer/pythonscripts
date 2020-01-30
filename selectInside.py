
import pymel.core as pc


def selectInside(geo, sphere):

    bar = pc.ui.PyUI(pc.MelGlobals.get('gMainProgressBar'))

    pc.select(cl=True)
    center = pc.dt.Point(sphere.firstParent().t.get())
    try:
        limit = sphere.inMesh.inputs()[0].radius.get()
    except AttributeError:
        pc.error("Sphere with history not found")
        return
    bar.setMaxValue(len(geo.f)/1000)
    bar.beginProgress()
    for face in geo.f:
        select = True
        for point in face.getPoints():
            point = pc.dt.Point(*point)
            if (point - center).length() > limit:
                select = False
                break
        if select:
            pc.select(face, add=True)
        if face.index() % 1000 == 0:
            bar.step()
    bar.endProgress()

if __name__ == "__main__":
    # geo = 'L_eye_L_eye_ballShape'
    # sphere = 'pSphereShape1'
    # selectInside(pc.PyNode(geo), pc.PyNode(sphere))
    sel = pc.ls(type='mesh', dag=True, sl=True)
    if len(sel) < 2:
        pc.error("Select Mesh first and then sphere Before running script")
    selectInside(*sel[:2])


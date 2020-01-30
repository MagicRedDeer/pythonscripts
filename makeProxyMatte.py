
value = True

import pymel.core as pc


def makeProxyMatte(val=True):
    cl = pc.editRenderLayerGlobals(q=True, currentRenderLayer=True)
    default = False
    if cl.startswith('default'):
        pc.warning('Could not override attribute on Default Render Layer')
        default = True

    meshes = pc.ls(sl=True, type='mesh', dag=True)
    proxies = []
    for mesh in meshes:
        proxies.extend(mesh.inMesh.listHistory(type='RedshiftProxyMesh'))
    if not proxies:
        pc.warning('No Proxy found in the selection')
        return
    for proxy in proxies:
        if not default:
            pc.editRenderLayerAdjustment(proxy.visibilityMode)
        proxy.visibilityMode.set(val)

makeProxyMatte(value)


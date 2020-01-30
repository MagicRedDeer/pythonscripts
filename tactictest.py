import tactic_client_lib as tcl
import app.checkoutin.src.backend as be
import imaya

reload(be)
reload(imaya)

stub = tcl.TacticServerStub()

# snap = stub.query('sthpw/snapshot', filters=[('code', 'SNAPSHOT00357478')],
# single=True)
# imaya.newScene()
# be.checkout(snap['__search_key__'], r=False, with_texture=True)

stub.set_project('test_mansour_ep')
tex = stub.get_by_code('vfx/texture', 'TEXTURE00042')
snap = stub.get_by_code('sthpw/snapshot', 'SNAPSHOT00066760')

print tex
print snap

tex_path = stub.checkout(
        tex['__search_key__'],
        snap['context'],
        to_sandbox_dir=True,
        mode='copy',
        file_type='*')

print tex_path

# load python script with the same name as the blender file
import bpy
import os


dir_blend = os.path.dirname(bpy.data.filepath)
name_blend = os.path.basename(bpy.data.filepath)
name_py = name_blend.replace('.blend', '.py')
path_py = os.path.join(dir_blend, name_py)

print ('Executing script found at', path_py)

exec(compile(open(path_py).read(), path_py, 'exec'))

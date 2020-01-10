# import sys, os
# import subprocess
# from ldraw.tools import vector_position
# from ldr2pov import*
# import numpy as np
# try:
#     import numpy
#     numpy_found=True
# except IOError:
#     numpy_found=False
#
# try:
#     from IPython.display import Image
#     ipython_found=True
# except:
#     ipython_found=False
#
# sys.path.append(os.getcwd())
# POVRAY_BINARY = ("povray.exe" if os.name=='nt' else "povray")
#
#
# def ppm_to_numpy(filename=None, buffer=None, byteorder='>'):
#     """Return image data from a raw PGM/PPM file as numpy array.
#
#     Format specification: http://netpbm.sourceforge.net/doc/pgm.html
#
#     """
#
#     if not numpy_found:
#         raise IOError("Function ppm_to_numpy requires numpy installed.")
#
#     if buffer is None:
#         with open(filename, 'rb') as f:
#             buffer = f.read()
#     try:
#         header, width, height, maxval = re.search(
#             b"(^P\d\s(?:\s*#.*[\r\n])*"
#             b"(\d+)\s(?:\s*#.*[\r\n])*"
#             b"(\d+)\s(?:\s*#.*[\r\n])*"
#             b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
#     except AttributeError:
#         raise ValueError("Not a raw PPM/PGM file: '%s'" % filename)
#
#     cols_per_pixels = 1 if header.startswith(b"P5") else 3
#
#     dtype = 'uint8' if int(maxval) < 256 else byteorder + 'uint16'
#     arr = numpy.frombuffer(buffer, dtype=dtype,
#                            count=int(width) * int(height) * 3,
#                            offset=len(header))
#
#     return arr.reshape((int(height), int(width), 3))
#
# # This function renders pov into image file.
# # Here, it uses povray.exe and gets ready necessary parameters for it.
# def render_povstring(pov_file, outfile='ipython', height=416, width=416,
#                      quality=None, antialiasing=None,
#                      show_window=False, includedirs=None,
#                      output_alpha=False):
#     f = open(pov_file, 'r')
#     string = f.read()
#     return_np_array = (outfile is None)
#     display_in_ipython = (outfile=='ipython')
#
#     format_type = "P" if return_np_array else "N"
#
#     if return_np_array:
#         outfile='-'
#
#     if display_in_ipython:
#         outfile = '__temp_ipython__.png'
#
#     # Prepare the command argument to feed povray.exe to render
#     cmd = [POVRAY_BINARY, pov_file]
#     if height is not None: cmd.append('+H%d'%height)
#     if width is not None: cmd.append('+W%d'%width)
#     if quality is not None: cmd.append('+Q%d'%quality)
#     if antialiasing is not None: cmd.append('+A%f'%antialiasing)
#     if output_alpha: cmd.append('Output_Alpha=on')
#     if not show_window:
#         cmd.append('-D')
#     else:
#         cmd.append('+D')
#     if includedirs is not None:
#         for dir in includedirs:
#             cmd.append('+L%s'%dir)
#     cmd.append("Output_File_Type=%s"%format_type)
#     cmd.append("+O%s"%outfile)
#     process = subprocess.Popen(cmd, stderr=subprocess.PIPE,
#                                     stdin=subprocess.PIPE,
#                                     stdout=subprocess.PIPE)
#
#     out, err = process.communicate(string.encode('ascii'))
#
#     if process.returncode:
#         print(type(err), err)
#         raise IOError("POVRay rendering failed with the following error: "+err.decode('ascii'))
#
#     if return_np_array:
#         return ppm_to_numpy(buffer=out)
#
#     if display_in_ipython:
#         if not ipython_found:
#             raise("The 'ipython' option only works in the IPython Notebook.")
#         return Image(outfile)
#
#
# if __name__ == '__main__':
#     # icosahedron coordinates (12 directional vectors)
#     coorsOfIcosahedron = np.array([[-0.26286500, 0.0000000, 0.42532500], [0.26286500, 0.0000000, 0.42532500],
#                           [-0.26286500, 0.0000000, -0.42532500], [0.26286500, 0.0000000, -0.42532500],
#                           [0.0000000, 0.42532500, 0.26286500], [0.0000000, 0.42532500, -0.26286500],
#                           [0.0000000, -0.42532500, 0.26286500], [0.0000000, -0.42532500, -0.26286500],
#                           [0.42532500, 0.26286500, 0.0000000], [-0.42532500, 0.26286500, 0.0000000],
#                           [0.42532500, -0.26286500, 0.0000000], [-0.42532500, -0.26286500, 0.0000000]])
#
#     if not os.path.exists('./dataset'):
#         os.mkdir('./dataset')
#     dirModel = 'D:/2019-12/Lego_Classification/complete/ldraw/parts/'
#     datFileName = '4738'
#
#     count = 0
#     for jj in range(0, 2):
#         strTemp = '1 5 0 -16 0 1 0 0 0 1 0 0 0 1 ' + datFileName + '.dat'
#         if jj == 1:
#             strTemp = '1 2 0 -16 0 1 0 0 0 1 0 0 0 1 ' + datFileName + '.dat'
#         ldrFileName = datFileName + '.ldr'
#
#         # Write model informatino to ldr file
#         with open(dirModel + ldrFileName, 'w') as f:
#             f.write(strTemp)
#         if not os.path.exists('./dataset/' + datFileName):
#             os.mkdir('./dataset/' + datFileName)
#
#         for ii in range(0, 3): # Loop on 3 different background colors
#             # Specify 3 different background colors
#             if ii == 0:
#                 skyStr = '1.0, 1.0, 1.0'
#             elif ii == 1:
#                 skyStr = '0.0, 1.0, 1.0'
#             else:
#                 skyStr = '1.0, 1.0, 0.0'
#
#             for idxDirection in range(0, 12): # Loop on 12 directional vector
#                 count = count + 1
#                 camPos = np.copy(coorsOfIcosahedron[idxDirection])
#                 for idx in range(0, 3):
#                     camPos[idx] = 230 * camPos[idx]
#                 camPosStr = str(camPos[0]) + ',' + str(camPos[1]) + ',' + str(camPos[2])
#
#                 # Convert ldr to pov file
#                 ldr2pov(dirModel + ldrFileName, '_temp_.pov',
#                         camera_position = vector_position(camPosStr),
#                         look_at_position = vector_position('0, 0, 0'),
#                         sky = skyStr)
#
#                 # Render pov file to png file
#                 render_povstring('_temp_.pov', './dataset/' + datFileName + '/' + str(count) + '.png', show_window=True)
#
#     print('Finish!')
#

import re
import sympy
from sympy import expand, symbols
# ss = input()
x, y = symbols('x y')
gfg_exp = x + y
ss = "(-2x^3)(2x^3+2)"
ss = ss.replace(")(", ")*(")
ss = ss.replace("^", "**")

pattern = re.compile(r'(\d?)(x)')
ss = pattern.sub(r"\1*\2", ss)
# Use sympy.expand() method
exp = sympy.expand(ss)



print(exp)
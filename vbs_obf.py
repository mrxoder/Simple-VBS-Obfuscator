import sys

camouflage = "\'Your use of this software is governed by the terms of the license agreement under which you acquired this software. If you are a volume licensing customer, the use of this software is governed by your volume license agreement. You are not authorized to use this software if you have not acquired a valid license for the software from Microsoft or one of its authorized distributors.\n\'Copyright (C) 2015"
func_name = "wh"
func0_name = "w"
payload_name = "k"
deobfuc_vbs = 'Function '+ func_name +'(f) : For y = 1 To Len(f) Step 2 : ub = ub & Chr(Clng("&H" & Mid(f, y, 2))) : Next : h = ub : End Function'
executor = '''
Function '''+ func0_name +'''(text)
text = text
ExecuteGlobal text
End Function
'''

def obfuscate(s):
    out = ''.join(format(ord(c), '02x') for c in s)
    return out

if len( sys.argv ) < 3:
   print("Usage: ", sys.argv[0], "input_vbs_filename   output_vbs_filename")
   sys.exit()


in_file = open( sys.argv[1] )
original_string = in_file.read()
out_string = obfuscate( original_string )

chunks = []
for i in range( 0, len(out_string), 256):
    chunks.append( payload_name + "=" + payload_name + "&"+ func_name +"(\"" + out_string[ i:i+256 ] + "\")" )

out_file = open( sys.argv[2], "w" )
out_file.write( camouflage+"\n")
out_file.write( payload_name+"=\"\"\n" )
out_file.write( '\n'.join( chunks ) )
out_file.write( "\n"+ func0_name + " "+ payload_name )
out_file.write( executor )
out_file.write( deobfuc_vbs )
out_file.close()
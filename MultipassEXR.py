# Blender Python Script to Connect Enabled Render Passes to Multiple Output File Nodes
# Author: Gabriel Moro
# Version: 0.9
#URL: https://blender.community/c/rightclickselect/D0qY/?sorting=hot
import bpy

# Ensure the compositor is activated
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# Clear default nodes
for node in tree.nodes:
    tree.nodes.remove(node)

# Create Render Layer and File Output nodes
render_layers_node = tree.nodes.new('CompositorNodeRLayers')
file_output_node = tree.nodes.new('CompositorNodeOutputFile')
file_output_node_jpeg = tree.nodes.new('CompositorNodeOutputFile')  # New JPEG output node

# Position nodes for visibility (optional)
render_layers_node.location = (0,0)
file_output_node.location = (400,0)
file_output_node_jpeg.location = (400, -200)  # Position of the new JPEG output node

# Reset File Output node layer slots and match them to enabled Render Layers
file_output_node.layer_slots.clear()

# Configure the new JPEG output node
file_output_node_jpeg.format.file_format = 'JPEG'

# Only keep the enabled outputs
for socket in render_layers_node.outputs:
    if socket.enabled:
        file_output_node.layer_slots.new(socket.name)

# Connect the sockets between the two nodes
for i, socket in enumerate([s for s in render_layers_node.outputs if s.enabled]):
    tree.links.new(file_output_node.inputs[i], socket)

# Connect the Image output to the new JPEG File Output node
image_socket = render_layers_node.outputs.get('Image')
if image_socket and image_socket.enabled:
    tree.links.new(file_output_node_jpeg.inputs[0], image_socket)

print("Enabled Render Passes and JPEG Image have been connected to the Output File Nodes.")

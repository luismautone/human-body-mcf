# Imports & Settings
import torch
import trimesh
import scipy
import numpy as np
import robust_laplacian
import plotly.io as pio
from plot import animate_mesh_frames
from mcf import mean_curvature_flow
from smpl_setup import smpl_create
pio.renderers.default = "browser"

# Setup Variables
batch_size = 1
limit = 30.0 # 45.0 for right arm partiality
start_vertex_index = 6866 # 5907 for right hand vertex
smpl_layer = smpl_create()
model_faces = smpl_layer.th_faces

# SMPL model
pose_params = torch.rand(batch_size, 72) * 0. # Generate pose parameters (T-Pose)
shape_params = torch.Tensor([np.random.uniform(-5., 5., 10).tolist()]) # Generate random shape parameters
print("Creating human body model...")
verts, Jtr = smpl_layer(pose_params, th_betas=shape_params) # Forward from the SMPL layer

# Matrix of Distances
adjacency, edges = trimesh.graph.face_adjacency(model_faces, return_edges=True) # Convert list of triangles in adjacency matrices
coo = trimesh.graph.edges_to_coo(edges) # Transform edges matrix into a sparse matrix
csr = coo.tocsr()
distances = scipy.sparse.csgraph.dijkstra(csr, directed=False) # Dijkstra Algorithm
distances_from_start_vertex = distances[start_vertex_index]

# border indices [POSITION in verts array], distance from start_vertex == limit
border_indices = [i for i in range(len(distances_from_start_vertex)) if distances_from_start_vertex[i] == limit]
# partial verts indices [POSITION in verts array] in the total shape, with distance from start_vertex <= limit
partial_shape_indices = [i for i in range(len(distances_from_start_vertex)) if distances_from_start_vertex[i] <= limit]
# partial verts position [VALUE in verts array] respect to the total shape
partial_shape_verts = []
for index in partial_shape_indices:
    partial_shape_verts.append(verts[0][index].numpy().tolist())
# correspondence between indices in total/partial verts arrays
verts_indices_corr = []
for index in partial_shape_indices:
    verts_indices_corr.append([index, partial_shape_indices.index(index)])
# faces containing partial verts indices
partial_shape_faces = []
for face in model_faces: # for all faces
    face_list = face.numpy().tolist()
    vertex_count = 0
    for index in partial_shape_indices: 
        if index in face_list:
            vertex_count = vertex_count + 1
            if vertex_count > 2: # if a face contains partial shape indices
                partial_shape_faces.append(face_list) # append the face
# map selected faces to selected vertices
partial_shape_faces_mapped = [x[:] for x in partial_shape_faces]
for i, face in enumerate(partial_shape_faces_mapped):
    for j, vertex_index in enumerate(face):
        # get the index position in "partial_shape_indices" of the vertex index
        partial_shape_faces_mapped[i][j] = partial_shape_indices.index(vertex_index)
# select partial shape border indices [POSITION in partial_shape_verts] in total shape
partial_shape_border_indices = []
for l in verts_indices_corr:
    if l[0] in border_indices:
        partial_shape_border_indices.append(l[1])

# Define new shape
V = np.array(partial_shape_verts) # 'partial_shape_verts'
F = np.array(partial_shape_faces_mapped) # 'partial_shape_faces_mapped'
L, _ = robust_laplacian.mesh_laplacian(V, F)
U = V

# MCF
print("Performing MCF...")
delta = 0.0001
max_iter = 50 # 35 for right arm
flow = [(np.array(verts)[0, :, :], model_faces)]
flow = mean_curvature_flow(L, F, U, partial_shape_border_indices, max_iter, delta, flow, verts, verts_indices_corr, model_faces)

print("Preparing MCF visualization...")
animate_mesh_frames(flow).show()
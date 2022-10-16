from tqdm import tqdm
import numpy as np
import robust_laplacian
from scipy.sparse.linalg import spsolve

def mean_curvature_flow(L, F, U, partial_shape_border_indices, max_iter, delta, flow, verts, verts_indices_corr, model_faces):
    for _ in tqdm(range(max_iter)):
        _, M = robust_laplacian.mesh_laplacian(U, F)

        A = M + delta*L
        A = A.tolil()
        B = M@U

        for j in range(A.shape[0]):
            if j in partial_shape_border_indices:
                for k in range(A.shape[1]):
                    A[j, k] = 1. if j == k else 0.
                B[j] = U[j]
            else:
                for k in range(A.shape[1]):
                    if k in partial_shape_border_indices:
                        B[j] = B[j] - U[j]*A[j,k]
                        A[j, k] = 0.

        A = A.tocsc()
        U = spsolve(A, B)
        
        full_verts = np.array(verts)[0, :, :]
        full_verts[np.array(verts_indices_corr)[:, 0]] = U
        flow.append((full_verts, model_faces))
    return flow
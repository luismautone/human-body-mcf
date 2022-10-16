import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import torch

def plot_traces(*traces, names=None):
    x = np.arange(traces[0].shape[-1])
    if not names:
        names = [f'Trace {idx}' for idx in range(len(traces))]
    fig = go.Figure()
    for trace, name in zip(traces, names):
        fig.add_trace(go.Scatter(x=x, y=trace[0],
                                 mode='lines+markers',
                                 name=name))
    fig.update_layout(
        autosize=True,
        margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4),
    )
    fig.update_yaxes(automargin=True)
    return fig


def plot_histogram(errors):
    fig = go.Figure([go.Bar(x=np.arange(0, errors.size), y=errors)])
    return fig


def plot_mesh(V, T):
    x, y, z = V.T
    I, J, K = T.T

    tri_points = V[T]

    pl_mygrey=[0, 'rgb(153, 153, 153)'], [1., 'rgb(255,255,255)']

    pl_mesh = go.Mesh3d(x=x,
                        y=y,
                        z=z,
                        colorscale=pl_mygrey,
                        intensity= z,
                        flatshading=True,
                        i=I,
                        j=J,
                        k=K,
                        name='Beethoven',
                        showscale=False
                        )

    pl_mesh.update(cmin=-7,# atrick to get a nice plot (z.min()=-3.31909)
                   lighting=dict(ambient=0.18,
                                 diffuse=1,
                                 fresnel=0.1,
                                 specular=1,
                                 roughness=0.05,
                                 facenormalsepsilon=1e-15,
                                 vertexnormalsepsilon=1e-15),
                   lightposition=dict(x=100,
                                      y=200,
                                      z=0
                                      )
                   )

    Xe = []
    Ye = []
    Ze = []
    for T in tri_points:
        Xe.extend([T[k%3][0] for k in range(4)]+[ None])
        Ye.extend([T[k%3][1] for k in range(4)]+[ None])
        Ze.extend([T[k%3][2] for k in range(4)]+[ None])

    #define the trace for triangle sides
    lines = go.Scatter3d(
        x=Xe,
        y=Ye,
        z=Ze,
        mode='lines',
        name='',
        line=dict(color= 'rgb(70,70,70)', width=1))

    layout = go.Layout(
        font=dict(size=16, color='white'),
        width=700,
        height=700,
        autosize=True,
        scene=dict(
            aspectmode="data",
            aspectratio=dict(x=1, y=1, z=1)),
        margin=dict(r=20, l=10, b=10, t=10),
        scene_xaxis_visible=False,
        scene_yaxis_visible=False,
        scene_zaxis_visible=False,
       # paper_bgcolor='rgb(50,50,50)',
    )

    fig = go.Figure(data=[pl_mesh, lines], layout=layout)
    return fig


def animate_traces_frames(frames_data, names):
    num_traces = len(frames_data[0])
    x = np.arange(frames_data[0][0].shape[-1])

    fig = go.Figure(data=[go.Scatter(x=x, y=frames_data[0][i][0],
                                     mode='lines+markers',
                                     name=names[i]) for i in range(num_traces)],
                    layout=go.Layout(
                        autosize=True,
                        scene=dict(
                            aspectmode="data",
                            aspectratio=dict(x=1, y=1, z=1)),
                        margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4),
                        updatemenus=[dict(
                            type="buttons",
                            buttons=[dict(label="Play",
                                          method="animate",
                                          args=[None])])]),
                    frames=[go.Frame(data=[go.Scatter(x=x, y=traces[i][0],
                                                      mode='lines+markers',
                                                      name=names[i])
                                           for i in range(num_traces)]) for traces in frames_data[1:]])
    fig.update_yaxes(automargin=True)
    return fig


def animate_mesh_frames(frames_data):
    fig = go.Figure(data=go_mesh(frames_data[0][0], frames_data[0][1]),
                    layout=go.Layout(
                        font=dict(size=16, color='white'),
                        width=700,
                        height=700,
                        autosize=True,
                        scene=dict(
                            aspectmode="data",
                            aspectratio=dict(x=1, y=1, z=1)),
                        margin=dict(r=20, l=10, b=10, t=10),
                        scene_xaxis_visible=False,
                        scene_yaxis_visible=False,
                        scene_zaxis_visible=False,
                        #paper_bgcolor='rgb(50,50,50)',
                        updatemenus=[dict(
                            type="buttons",
                            buttons=[dict(label="Play",
                                          method="animate",
                                          args=[None])])]),
                    frames=[go.Frame(data=go_mesh(V, T)) for V, T in frames_data[1:]])
    return fig


def go_mesh(V, T):
    # x_0, y_0, z_0 = V.T
    # i_0, j_0, k_0 = T.T
    # return go.Mesh3d(x=x_0, y=y_0, z=z_0, i=i_0, j=j_0, k=k_0,
    #                  lighting=dict(roughness=0.1, ambient=0.35,
    #                                specular=0.1),
    #                  color='green',
    #                  colorscale='Viridis')
    x, y, z = V.T
    I, J, K = T.T

    tri_points = V[T]

    pl_mygrey=[0, 'rgb(153, 153, 153)'], [1., 'rgb(255,255,255)']

    pl_mesh = go.Mesh3d(x=z,
                        y=x,
                        z=y,
                        colorscale=pl_mygrey,
                        intensity= z,
                        flatshading=True,
                        i=I,
                        j=J,
                        k=K,
                        name='Beethoven',
                        showscale=False
                        )

    pl_mesh.update(cmin=-7,# atrick to get a nice plot (z.min()=-3.31909)
                   lighting=dict(ambient=0.18,
                                 diffuse=1,
                                 fresnel=0.1,
                                 specular=1,
                                 roughness=0.05,
                                 facenormalsepsilon=1e-15,
                                 vertexnormalsepsilon=1e-15),
                   lightposition=dict(x=100,
                                      y=200,
                                      z=0
                                      )
                   )

    Xe = []
    Ye = []
    Ze = []
    for T in tri_points:
        Xe.extend([T[k%3][0] for k in range(4)]+[ None])
        Ye.extend([T[k%3][1] for k in range(4)]+[ None])
        Ze.extend([T[k%3][2] for k in range(4)]+[ None])

    #define the trace for triangle sides
    lines = go.Scatter3d(
        x=Ze,
        y=Xe,
        z=Ye,
        mode='lines',
        name='',
        line=dict(color= 'rgb(70,70,70)', width=1))
    # fig = pl_mesh #go.Figure(data=[pl_mesh, lines])
    return pl_mesh, lines

    # return go.Mesh3d(x=x_0, y=y_0, z=z_0, i=i_0, j=j_0, k=k_0,
    #              lighting=dict(roughness=0.1, ambient=0.35,
    #                            specular=0.1),
    #              color='green',
    #              colorscale='Viridis')


def plot_points(pos, edge_index=None, index=None, c=None):
    fig, ax = plt.subplots()
    if edge_index is not None:
        for (src, dst) in edge_index.t().tolist():
            src = pos[src].tolist()
            dst = pos[dst].tolist()
            ax.plot([src[0], dst[0]], [src[1], dst[1]], linewidth=1, color='black')
    if index is None:
        ax.scatter(pos[:, 0], pos[:, 1], s=50, zorder=1000, c=c)
    else:
        mask = torch.zeros(pos.size(0), dtype=torch.bool)
        mask[index] = True
        ax.scatter(pos[~mask, 0], pos[~mask, 1], s=50, color='lightgray', zorder=1000)
        ax.scatter(pos[mask, 0], pos[mask, 1], s=50, zorder=1000)

    ax.axis('equal')
    return fig, ax


def update_points(ax, pos, edge_index=None, index=None, c=None):
    ax.clear()
    # ax.axis('off')
    if edge_index is not None:
        for (src, dst) in edge_index.t().tolist():
            src = pos[src].tolist()
            dst = pos[dst].tolist()
            ax.plot([src[0], dst[0]], [src[1], dst[1]], linewidth=1, color='black')
    if index is None:
        ax.scatter(pos[:, 0], pos[:, 1], s=50, zorder=1000, c=c)
    else:
        mask = torch.zeros(pos.size(0), dtype=torch.bool)
        mask[index] = True
        ax.scatter(pos[~mask, 0], pos[~mask, 1], s=50, color='lightgray', zorder=1000)
        ax.scatter(pos[mask, 0], pos[mask, 1], s=50, zorder=1000)
    ax.axis('equal')
    return ax

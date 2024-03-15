#!/usr/bin/env python3
from utils.viz import plot_mesh
import matplotlib.pyplot as plt
import yaml
from meshes import gmsh_model_to_mesh
from meshes.tdcb_2D import mesh_tdcb
import sys
from mpi4py import MPI
import petsc4py
from dolfinx import log

sys.path.append("../")

# sys.path.append("../../damage")
# from mesh import gmsh_to_dolfin, merge_meshtags

petsc4py.init(sys.argv)
log.set_log_level(log.LogLevel.WARNING)


comm = MPI.COMM_WORLD


# Get mesh parameters


with open(os.path.join(os.path.dirname(__file__), "parameters.yml")) as f:
    parameters = yaml.load(f, Loader=yaml.FullLoader)

_tdcb_params = """
general:
    dim: 2

#  === Geometry === #
geometry:
    geometric_dimension: 2
    Lx: 1.
    L1: .4
    L2: .5
    Lcrack: .5
    Cx: .1
    Cy: .1
    rad: .05
    eta: .0005
    geom_type: "tdcb"
"""

_tdcb = yaml.load(_tdcb_params)
lc = 0.05

# Create the mesh of the specimen with given dimensions
gmsh_model, tdim, tag_names = mesh_tdcb(
    _tdcb.get("geometry").get("geom_type"),
    _tdcb.get("geometry"),
    lc,
    msh_file="output/tdcb2d.msh",
)

# Get mesh and meshtags
mesh, cell_tags, facet_tags = gmsh_model_to_mesh(
    gmsh_model, cell_data=True, facet_data=True, gdim=2
)

# domains_keys = tag_names["cells"]
# boundary_keys = tag_names["facets"]

# dx = ufl.Measure("dx", subdomain_data=cell_tags, domain=mesh)
# ds = ufl.Measure("ds", subdomain_data=facet_tags, domain=mesh)

plt.figure()
ax = plot_mesh(mesh)
fig = ax.get_figure()
fig.savefig(f"output/tdcb-mesh.png")

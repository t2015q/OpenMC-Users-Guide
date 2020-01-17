import openmc


clad=openmc.Material(1,'cladding')
clad.add_element('Si',1.3603E-3)
clad.add_element('Ti',5.9844E-4)
clad.add_element('Cr',1.6532E-2)
clad.add_nuclide('Mn55',1.3039E-3)
clad.add_element('Fe',5.9088E-2)
clad.add_element('Ni',8.1369E-3)
clad.set_density('atom/b-cm',8.701954E-02)
clad.temperature=300


fuel=openmc.Material(2,'fuel')
fuel.add_nuclide('U234',6.7481E-7)
fuel.add_nuclide('U235',7.6403E-5)
fuel.add_nuclide('U238',6.7271E-4)
fuel.add_nuclide('O16',3.7473E-2)
fuel.add_nuclide('H1',5.8854E-2)
fuel.add_nuclide('N14',2.3185E-3)
fuel.set_density('atom/b-cm',9.939529E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')
fuel.temperature=300

mats=openmc.Materials([clad,fuel])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


sph1=openmc.Sphere(R=32.9537)
sph2=openmc.Sphere(R=33.1037,boundary_type='vacuum')
zp3=openmc.ZPlane(z0=16.4073)


cell1=openmc.Cell()
cell1.region= -sph1 & -zp3
cell1.fill=fuel

cell2=openmc.Cell()
cell2.region= +sph1 & -sph2
cell2.fill=clad

cell3=openmc.Cell()
cell3.region= -sph1 & +zp3


root=openmc.Universe(cells=(cell1,cell2,cell3))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space = openmc.stats.Box((-1, -1, -1), (1, 1, 1))
src.energy=openmc.stats.Discrete([14.0e6],[1.0])
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 10
settings.particles = 2000
settings.output={'tallies':False}
settings.export_to_xml()

openmc.run()





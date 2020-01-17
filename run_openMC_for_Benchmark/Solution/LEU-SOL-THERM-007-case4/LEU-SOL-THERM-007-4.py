import openmc


clad=openmc.Material(1,'cladding')
clad.add_element('C',4.3736e-5)
clad.add_element('Si',1.0627e-3)
clad.add_element('S',2.9782e-6)
clad.add_element('Ni',8.3403e-3)
clad.add_element('Cr',1.6775e-2)
clad.add_nuclide('P31',4.3170e-5)
clad.add_element('Fe',5.9421e-2)
clad.add_nuclide('Mn55',1.1561e-3)
clad.set_density('atom/b-cm',8.68449842E-02)


air=openmc.Material(2,'water')
air.add_nuclide('N14',3.9016e-5)
air.add_nuclide('O16',1.0409e-5)
air.set_density('atom/b-cm',4.94250000E-05)


fuel=openmc.Material(3,'fuel')
fuel.add_nuclide('H1',5.8115E-02)
fuel.add_nuclide('N14',2.6292E-03)
fuel.add_nuclide('O16',3.7560E-02)
fuel.add_nuclide('U234',5.2265E-07)
fuel.add_nuclide('U235',6.4857E-05)
fuel.add_nuclide('U236',6.4776E-08)
fuel.add_nuclide('U238',5.7769E-04)
fuel.set_density('atom/b-cm',9.89471078E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')



mats=openmc.Materials([clad,air,fuel])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()

zp1=openmc.ZPlane(z0=0.0)
zp2=openmc.ZPlane(z0=83.55)
zp3=openmc.ZPlane(z0=150.0)
zp4=openmc.ZPlane(z0=152.5,boundary_type='vacuum')
zp5=openmc.ZPlane(z0=-2.0,boundary_type='vacuum')

zc10=openmc.ZCylinder(x0=0,y0=0,R=29.5)
zc20=openmc.ZCylinder(x0=0,y0=0,R=29.8,boundary_type='vacuum')




cell1=openmc.Cell()
region1=+zp1 & -zp2 & -zc10
cell1.region= region1
cell1.fill=fuel

cell2=openmc.Cell()
region2=+zp2 & -zp3 & -zc10
cell2.region= region2
cell2.fill=air

cell3=openmc.Cell()
cell3.region= -zp1 | +zp3 | +zc10
cell3.fill=clad

u1=openmc.Universe(cells=(cell1,cell2,cell3))

cell4=openmc.Cell()
cell4.region=+zp5 & -zp4 & -zc20
cell4.fill=u1

root=openmc.Universe(cells=(cell4,))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space = openmc.stats.Box((5, 5, 5), (10, 10, 10))
settings = openmc.Settings()
settings.source = src
settings.batches = 1000
settings.inactive = 100
settings.particles = 5000
settings.output={'tallies':False}
settings.export_to_xml()

openmc.run()




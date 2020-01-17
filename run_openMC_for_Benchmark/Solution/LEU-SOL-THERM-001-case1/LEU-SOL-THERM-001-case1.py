import openmc


ss304=openmc.Material(1,'ss304')
ss304.add_nuclide('Cr53',1.6348e-2)
ss304.add_nuclide('Mn55',1.7192e-3)
ss304.add_nuclide('Fe57',6.0038e-2)
ss304.add_nuclide('Ni64',7.2418e-3)
ss304.set_density('atom/b-cm',8.5347E-02)

air=openmc.Material(2,'air')
air.add_nuclide('N14',3.5214e-5)
air.add_nuclide('O16',1.5092e-5)
air.set_density('atom/b-cm',5.0306E-05)
air.temperature=300

fuel=openmc.Material(3,'fuel')
fuel.add_nuclide('H1',5.6179e-2)
fuel.add_nuclide('O16',3.2967e-2)
fuel.add_nuclide('F19',5.1035e-3)
fuel.add_nuclide('U234',6.7855e-7)
fuel.add_nuclide('U235',1.2377e-4)
fuel.add_nuclide('U236',1.2085e-6)
fuel.add_nuclide('U238',2.3508e-3)
fuel.set_density('atom/b-cm',9.6726E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')
fuel.temperature=300

mats=openmc.Materials([ss304,air,fuel])
mats.export_to_xml()

yp1=openmc.YPlane(y0=-40.0)
yp2=openmc.YPlane(y0=-37.1425)
yp3=openmc.YPlane(y0=7.6575)
yp4=openmc.YPlane(y0=39.375)
yp5=openmc.YPlane(y0=41.28)
yc6=openmc.YCylinder(x0=0,z0=0,R=2.54)
yc7=openmc.YCylinder(x0=0,z0=0,R=3.175)
yc8=openmc.YCylinder(x0=0,z0=0,R=24.4475)
yc9=openmc.YCylinder(x0=0,z0=0,R=25.4)
sph=openmc.Sphere(R=60.0)
sph.boundary_type='vacuum'

cell1=openmc.Cell()
cell1.region= +yp1 & -yp5 & -yc6
cell1.fill=air

cell2=openmc.Cell()
cell2.region= +yc6 & +yp1 & -yp2 & -yc9
cell2.fill=ss304

cell3=openmc.Cell()
cell3.region= +yp2 & -yp4 & +yc6 & -yc7
cell3.fill=ss304

cell4=openmc.Cell()
cell4.region= +yp2 & -yp3 & +yc7 & -yc8
cell4.fill=fuel

cell5=openmc.Cell()
cell5.region= +yp3 & -yp4 & +yc7 & -yc8
cell5.fill=air

cell6=openmc.Cell()
cell6.region= +yp2 & -yp4 & +yc8 & -yc9
cell6.fill=ss304

cell7=openmc.Cell()	
cell7.region= +yp4 & -yp5 & +yc6 & -yc9
cell7.fill=ss304

cell8=openmc.Cell()
cell8.region= -sph & (+yp5 | +yc9 | -yp1)



root=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space=openmc.stats.Point((0,0,0))
src.energy=openmc.stats.Discrete([14.0e6],[1.0])
settings = openmc.Settings()
settings.source = src
settings.batches = 250
settings.inactive = 10
settings.particles = 3000
settings.output={'tallies':False}
settings.export_to_xml()





openmc.run()







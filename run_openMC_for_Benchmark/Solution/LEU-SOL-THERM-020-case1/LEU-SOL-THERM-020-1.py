import openmc


clad=openmc.Material(1,'cladding')
clad.add_element('C',4.3736E-05)
clad.add_element('Si',1.0627e-3)
clad.add_nuclide('P31',4.3170e-5)
clad.add_element('S',2.9782e-6)
clad.add_element('Ni',8.3403e-3)
clad.add_element('Cr',1.6775e-2)
clad.add_element('Fe',5.9421e-2)
clad.add_nuclide('Mn55',1.1561e-3)
clad.set_density('atom/b-cm',8.68450000E-02)


water=openmc.Material(2,'water')
water.add_nuclide('H1',6.6658E-02)
water.add_nuclide('O16',3.3329E-02)
water.set_density('atom/b-cm',9.9987E-02)
water.add_s_alpha_beta('c_H_in_H2O')
water.temperature=300

fuel=openmc.Material(3,'fuel')
fuel.add_nuclide('H1',6.0297E-02)
fuel.add_nuclide('N14',1.8157E-03)
fuel.add_nuclide('O16',3.6535E-02)
fuel.add_nuclide('U234',5.0042E-07)
fuel.add_nuclide('U235',6.2098E-05)
fuel.add_nuclide('U236',6.2021E-08)
fuel.add_nuclide('U238',5.5312E-04)
fuel.set_density('atom/b-cm',9.92630348E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')
fuel.temperature=300

air=openmc.Material(4,'air')
air.add_nuclide('N14',3.9016e-5)
air.add_nuclide('O16',1.0409e-5)
air.set_density('atom/b-cm',4.94510000E-05)
air.temperature=300

mats=openmc.Materials([clad,water,fuel,air])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()

zp1=openmc.ZPlane(z0=0.0)
zp2=openmc.ZPlane(z0=41.46)
zp3=openmc.ZPlane(z0=149.71)
zp4=openmc.ZPlane(z0=152.64)
zp5=openmc.ZPlane(z0=-2.06)
zp6=openmc.ZPlane(z0=172.64,boundary_type='vacuum')
zp7=openmc.ZPlane(z0=-34.5,boundary_type='vacuum')

zc10=openmc.ZCylinder(R=39.505)
zc20=openmc.ZCylinder(R=39.815)
zc30=openmc.ZCylinder(R=69.8,boundary_type='vacuum')



cell1=openmc.Cell()
region1=+zp1 & -zp2 & -zc10
cell1.region= region1
cell1.fill=fuel

cell2=openmc.Cell()
region2=+zp2 & -zp3 & -zc10
cell2.region= region2
cell2.fill=air

cell3=openmc.Cell()
cell3.region= ~region1 & ~region2
cell3.fill=clad

univ1=openmc.Universe(cells=(cell1,cell2,cell3))

cell4=openmc.Cell()
region4=  -zp4  & +zp5 & -zc20
cell4.region=region4
cell4.fill=univ1

cell5=openmc.Cell()
cell5.region=~region4
cell5.fill=water

univ2=openmc.Universe(cells=(cell4,cell5))

cell6=openmc.Cell()
cell6.region=-zp6 & +zp7 & -zc30
cell6.fill=univ2


root=openmc.Universe(cells=(cell6,))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space=openmc.stats.Point((0,0,0))
src.space = openmc.stats.Box((-37, -37, -20), (37, 37, 20))
src.energy=openmc.stats.Watt( )
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 50
settings.particles = 5000
settings.output={'tallies':False}
settings.export_to_xml()


plot=openmc.Plot()
plot.origin=[0,0,80]
plot.width=[200,300]
plot.pixels=[1000,1000]
plot.basis='xz'
plot.color_by='material'
plot.colors={air:'white'}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()




openmc.run()




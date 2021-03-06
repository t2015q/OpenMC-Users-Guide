import openmc


fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('H1',5.5582E-02)
fuel.add_nuclide('O16',3.8481E-02)
fuel.add_nuclide('N14',2.8647E-03)
fuel.add_nuclide('U234',9.5555E-07)
fuel.add_nuclide('U235',1.1858E-04)
fuel.add_nuclide('U236',1.1843E-07)
fuel.add_nuclide('U238',1.0562E-03)
fuel.set_density('atom/b-cm',9.81034711E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')
fuel.temperature=300

sus304=openmc.Material(2,'sus304')
sus304.add_element('C',7.1567E-05)
sus304.add_element('Si',7.1415E-04)
sus304.add_nuclide('Mn55',9.9095E-04)
sus304.add_nuclide('P31',5.0879E-05)
sus304.add_element('S',1.0424E-05)
sus304.add_element('Ni',8.5600E-03)
sus304.add_element('Cr',1.6725E-02)
sus304.add_element('Fe',5.9560E-02)
sus304.set_density('atom/b-cm',8.66829700E-02)


water=openmc.Material(3,'water')
water.add_nuclide('H1',6.6658E-02)
water.add_nuclide('O16',3.3329E-02)
water.set_density('atom/b-cm',9.9987E-02)
water.add_s_alpha_beta('c_H_in_H2O')
water.temperature=300

air=openmc.Material(4,'air')
air.add_nuclide('N14',3.9016E-05)
air.add_nuclide('O16',1.0409E-05)
air.set_density('atom/b-cm',4.94250000E-05)



mats=openmc.Materials([fuel,sus304,water,air])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel
xp1=openmc.XPlane(x0= -34.515)
xp2=openmc.XPlane(x0=34.515)
yp3=openmc.YPlane(y0= -14.04)
yp4=openmc.YPlane(y0= 14.04)
zp5=openmc.ZPlane(z0= 0.0)
zp6=openmc.ZPlane(z0= 149.75)
zp7=openmc.ZPlane(z0= 40.09) #critical level

#sus304
xp11=openmc.XPlane(x0=-37.045 )
xp12=openmc.XPlane(x0= 37.045)
yp13=openmc.YPlane(y0=-16.57 )
yp14=openmc.YPlane(y0=16.57 )
zp15=openmc.ZPlane(z0= -2.04)
zp16=openmc.ZPlane(z0= 152.63)

#water
xp21=openmc.XPlane(x0=-67.045 ,boundary_type='vacuum')
xp22=openmc.XPlane(x0=67.045,boundary_type='vacuum')
yp23=openmc.YPlane(y0=-46.57,boundary_type='vacuum')
yp24=openmc.YPlane(y0=46.57,boundary_type='vacuum' )
zp25=openmc.ZPlane(z0= -35.0,boundary_type='vacuum')
zp26=openmc.ZPlane(z0= 172.5,boundary_type='vacuum')



##堆芯部分
cell1=openmc.Cell()
core_region=+xp1 & -xp2 & +yp3 & -yp4  & +zp5 & -zp7
cell1.region= core_region
cell1.fill=fuel

cell2=openmc.Cell()
core_up= +xp1 & -xp2 & +yp3 & -yp4  & +zp7 & -zp6
cell2.region=core_up
cell2.fill=air

cell3=openmc.Cell( )
region3=  +xp11 &  -xp12 & +yp13 &  -yp14 &  +zp15  & -zp16  & (-xp1 | +xp2 | -yp3 | +yp4  | -zp5 |+zp6  )
cell3.region=region3
cell3.fill=sus304


cell4=openmc.Cell()
cell4.region= +xp21 & -xp22  &  +yp23 & -yp24  &  +zp25 & -zp26  & (-xp11 | +xp12 | -yp13 | +yp14 | -zp15 | +zp16 )
cell4.fill=water


root=openmc.Universe(cells=(cell1,cell2,cell3,cell4))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space = openmc.stats.Box((-34.5, -14, 0),(34.5,14 ,40.))
src.energy=openmc.stats.Watt( )
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 50
settings.particles = 5000
settings.output={'tallies':False}
settings.export_to_xml()


plot=openmc.Plot()
plot.origin=[0,0,40]
plot.width=[150,150]
plot.pixels=[1000,1000]
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()



openmc.run()



import openmc

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('H1',5.8747E-02)
fuel.add_nuclide('O16',3.7170E-02)
fuel.add_nuclide('N14',2.1648E-03)
fuel.add_nuclide('U234',6.4595E-07)
fuel.add_nuclide('U235',8.0158E-05)
fuel.add_nuclide('U236',8.0058E-08)
fuel.add_nuclide('U238',7.1398E-04)
fuel.set_density('atom/b-cm',9.88764316E-02)
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


concrete=openmc.Material(3,'concrete')
concrete.add_nuclide('H1',1.4528e-02)
concrete.add_nuclide('O16',4.4590E-02)
concrete.add_nuclide('Na23',1.0533E-03)
concrete.add_element('Mg',1.9573E-04)
concrete.add_nuclide('Al27',1.5533E-03)
concrete.add_element('Si',1.4749E-02)
concrete.add_element('S',1.0906E-04)
concrete.add_element('Cl',9.0027E-07)
concrete.add_element('K',1.9179E-04)
concrete.add_element('Ca',3.9337E-03)
concrete.add_element('Fe',2.7830E-04)
concrete.set_density('atom/b-cm',8.11829800E-02)
concrete.add_s_alpha_beta('c_H_in_H2O')
concrete.temperature=300


air=openmc.Material(4,'air')
air.add_nuclide('N14',3.9016E-05)
air.add_nuclide('O16',1.0409E-05)
air.set_density('atom/b-cm',4.94240000E-05)

aluminum=openmc.Material(5,'aluminum')
aluminum.add_nuclide('Al27',5.9559E-02)
aluminum.add_element('Si',8.0751E-05)
aluminum.add_element('Fe',1.7114E-04)
aluminum.add_element('Cu',1.7845E-05)
aluminum.set_density('atom/b-cm',5.98285201E-02)

futa304=openmc.Material(6,'futa304')
futa304.add_element('C',2.0675E-04)
futa304.add_element('Si',6.6314E-04)
futa304.add_nuclide('Mn55',1.0083E-03)
futa304.add_nuclide('P31',4.9337E-05)
futa304.add_element('S',1.6380E-05)
futa304.add_element('Ni',6.6885E-03)
futa304.add_element('Cr',1.6798E-02)
futa304.add_element('Fe',6.1435E-02)
futa304.set_density('atom/b-cm',8.68654070E-02)


mats=openmc.Materials([fuel,sus304,concrete,air,aluminum,futa304])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel
xp1=openmc.XPlane(x0= -34.515)
xp2=openmc.XPlane(x0=34.515)
yp3=openmc.YPlane(y0= -14.04)
yp4=openmc.YPlane(y0= 14.04)
zp5=openmc.ZPlane(z0= 0.0)
zp6=openmc.ZPlane(z0= 149.75)
zp7=openmc.ZPlane(z0= 65.56) #critical level

#sus304
xp11=openmc.XPlane(x0=-37.045 )
xp12=openmc.XPlane(x0= 37.045)
yp13=openmc.YPlane(y0=-16.57 )
yp14=openmc.YPlane(y0=16.57 )
zp15=openmc.ZPlane(z0= -2.04)
zp16=openmc.ZPlane(z0= 152.63)

#c150 reflector
xp21=openmc.XPlane(x0=-38.7 )
xp22=openmc.XPlane(x0=38.7)
zp23=openmc.ZPlane(z0=-3.0)
zp24=openmc.ZPlane(z0=153.6)
zp25=openmc.ZPlane(z0= 0.0 )
zp26=openmc.ZPlane(z0= 150.6 )
xp27=openmc.XPlane(x0= -35.7 )
xp28=openmc.XPlane(x0= 35.7)

yp31=openmc.YPlane(y0=16.79 )
yp32=openmc.YPlane(y0=17.6)
yp33=openmc.YPlane(y0=22.61)
yp34=openmc.YPlane(y0=23.42)
yp35=openmc.YPlane(y0=-16.79)
yp36=openmc.YPlane(y0=-17.6)

yp37=openmc.YPlane(y0=-22.61)
yp38=openmc.YPlane(y0=-23.42)
yp39=openmc.YPlane(y0=23.5)
yp40=openmc.YPlane(y0=24.31)
yp41=openmc.YPlane(y0=39.31)
yp42=openmc.YPlane(y0=40.12)
yp43=openmc.YPlane(y0=-23.5)
yp44=openmc.YPlane(y0=-24.31)
yp45=openmc.YPlane(y0=-39.31)
yp46=openmc.YPlane(y0=-40.12)


#Pool
zp85=openmc.ZPlane(z0= -34.5 ,boundary_type='vacuum')
zp86=openmc.ZPlane(z0= 172.63,boundary_type='vacuum')
yp83=openmc.YPlane(y0=-100.,boundary_type='vacuum')
yp84=openmc.YPlane(y0=100.,boundary_type='vacuum')
xp81=openmc.XPlane(x0=-111.0,boundary_type='vacuum' )
xp82=openmc.XPlane(x0=291.0,boundary_type='vacuum')




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
cell3.region= +xp11 &  -xp12 & +yp13 &  -yp14 &  +zp15  & -zp16  & (-xp1 | +xp2 | -yp3 | +yp4  | -zp5 |+zp6  )
cell3.fill=sus304


#中间栅元，对称
cell4=openmc.Cell()
cell4.region=+xp27 & -xp28 & +yp32 & -yp33 & +zp25 & -zp26 |  (+xp27 & -xp28 & +yp37 & -yp36 & +zp25 & -zp26)
cell4.fill=concrete

cell5=openmc.Cell()
cell5.region= +xp21 & -xp22 & +yp31 & -yp32 & +zp23 & -zp24 | (+xp21 & -xp22 & +yp38 & -yp37 & +zp23 & -zp24 )
cell5.fill=futa304

cell6=openmc.Cell()
cell6.region=+xp21 & -xp22 & +yp33 & -yp34 & +zp23 & -zp24 | (+xp21 & -xp22 & +yp36 & -yp35 & +zp23 & -zp24 )
cell6.fill=aluminum

cell7=openmc.Cell()
cell7.region=(+xp21 & -xp22  & +yp32 & -yp33 & +zp23 & -zp24 & (-xp27 | +xp28  | +zp26 | -zp25  )) | (+xp21 & -xp22  & +yp37 & -yp36 & +zp23 & -zp24 & (-xp27 | +xp28  | +zp26 | -zp25  ))
cell7.fill=sus304
#外层 对称
cell8=openmc.Cell()
cell8.region=+xp27 & -xp28 & +yp40 & -yp41 & +zp25 & -zp26 |  (+xp27 & -xp28 & +yp45 & -yp44 & +zp25 & -zp26)
cell8.fill=concrete

cell9=openmc.Cell()
cell9.region= +xp21 & -xp22 & +yp39 & -yp40 & +zp23 & -zp24
cell9.fill=futa304

cell10=openmc.Cell()
cell10.region=+xp21 & -xp22 & +yp41 & -yp42 & +zp23 & -zp24 | (+xp21 & -xp22 & +yp44 & -yp43 & +zp23 & -zp24) | (+xp21 & -xp22 & +yp46 & -yp45 & +zp23 & -zp24)
cell10.fill=aluminum

cell11=openmc.Cell()
cell11.region=(+xp21 & -xp22  & +yp45 & -yp44 & +zp23 & -zp24 & (-xp27 | +xp28  | +zp26 | -zp25  )) | (+xp21 & -xp22  & +yp40 & -yp41 & +zp23 & -zp24 & (-xp27 | +xp28  | +zp26 | -zp25  ))
cell11.fill=sus304



cell12=openmc.Cell()
cell12.region=+xp81 & -xp82 & +yp83 & -yp84 & +zp85 & -zp86 & (+xp12 | -xp11 | -yp13 | +yp14 | +zp16 | -zp15) & (+xp22 | -xp21 | -yp38 | +yp35 | +zp24 | -zp23) & (+xp22 | -xp21 | -yp31 | +yp34 | +zp24 | -zp23) & (+xp22 | -xp21 | -yp46 | +yp43 | +zp24 | -zp23) & (+xp22 | -xp21 | -yp39 | +yp42 | +zp24 | -zp23) 




root=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9,cell10,cell11,cell12))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space = openmc.stats.Box((-34.5, -14, 0),(34.5,14 ,65.56))
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
plot.basis='yz'
plot.color_by='material'
plot.colors={air:'white'}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()



openmc.run()


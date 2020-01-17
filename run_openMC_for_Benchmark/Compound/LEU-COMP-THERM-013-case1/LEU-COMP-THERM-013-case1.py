import openmc
import numpy as np

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('O16',4.6753e-2)
fuel.add_nuclide('U234',5.1835e-6)
fuel.add_nuclide('U235',1.0102e-3)
fuel.add_nuclide('U236',5.1395e-6)
fuel.add_nuclide('U238',2.2157e-2)
fuel.set_density('atom/b-cm',0.069930423)


water=openmc.Material(2,'water')
water.add_nuclide('H1',6.6706e-2)
water.add_nuclide('O16',3.3353e-2)
water.set_density('g/cm3',0.997766)
water.add_s_alpha_beta('c_H_in_H2O')



clad6061=openmc.Material(3,'clad6061')
clad6061.add_element('Mg',6.6651e-4)
clad6061.add_nuclide('Al27',5.8433e-2)
clad6061.add_element('Si',3.4607e-4)
clad6061.add_element('Ti',2.5375e-5)
clad6061.add_element('Cu',6.3731e-5)
clad6061.add_element('Zn',3.0967e-5)
clad6061.add_element('Ni',8.3403e-3)
clad6061.add_element('Cr',6.2310e-5)
clad6061.add_element('Fe',1.0152e-4)
clad6061.add_nuclide('Mn55',2.2115e-5)
clad6061.set_density('g/cm3',2.69)


rubber=openmc.Material(4,'rubber')
rubber.add_nuclide('H1',5.8178e-2)
rubber.add_element('Si',9.6360e-5)
rubber.add_nuclide('C0',4.3562e-2)
rubber.add_element('Ca',2.5660e-3)
rubber.add_nuclide('S32',4.7820e-4)
rubber.add_nuclide('O16',1.2461e-2)
rubber.add_s_alpha_beta('c_H_in_CH2')
rubber.set_density('g/cm3',1.498)


acrylic=openmc.Material(5,'acrylic')
acrylic.add_nuclide('H1',5.6642e-2)
acrylic.add_nuclide('O16',1.4273e-2)
acrylic.add_nuclide('C0',3.5648e-2)
acrylic.add_s_alpha_beta('c_H_in_CH2')
acrylic.set_density('g/cm3',1.185)


ss_plate=openmc.Material(6,'ss_plate')
ss_plate.add_element('Cr',1.7046e-2)
ss_plate.add_nuclide('Mn55',1.3734e-3)
ss_plate.add_element('Cu',2.0291e-4)
ss_plate.add_element('Fe',5.8353e-2)
ss_plate.add_element('Ni',9.0238e-3)
ss_plate.add_element('Mo',1.2942e-4)
ss_plate.set_density('g/cm3',7.93)

steel=openmc.Material(7,'steel')
steel.add_element('Fe',8.1810e-2)
steel.add_nuclide('C0',7.4686e-4)
steel.add_nuclide('Mn55',1.1e-3)
steel.add_nuclide('P31',6.0971e-6)
steel.add_nuclide('S32',8.8332e-6)
steel.add_element('Si',3.6983e-4)
steel.add_element('Ni',6.3552e-4)
steel.add_element('Mo',2.4114e-4)
steel.add_element('Cr',1.0896e-4)
steel.add_element('Cu',9.6587e-5)
steel.set_density('atom/b-cm',0.0851238)


mats=openmc.Materials([fuel,water,clad6061,acrylic,ss_plate,steel,rubber])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()



zc1=openmc.ZCylinder(x0=0,y0=0,R=0.6325) #fuel
zc2=openmc.ZCylinder(x0=0,y0=0,R=0.6415) #gap
zc12=openmc.ZCylinder(x0=0,y0=0,R=0.7075) #clad


zp7=openmc.ZPlane(z0= 0.0)
zp8=openmc.ZPlane(z0= 92.075) # top fuel
zp9=openmc.ZPlane(z0= 94.2975) # top clad
zp23=openmc.ZPlane(z0= -2.2225) #bottom clad
zp29=openmc.ZPlane(z0= -4.7625)  #bottom acrylic

zp30=openmc.ZPlane(z0= -20.0625,boundary_type='vacuum')
zp28=openmc.ZPlane(z0= 107.075,boundary_type='vacuum')


xp11=openmc.XPlane(x0=0.0)
xp10=openmc.XPlane(x0= 22.704)
xp14=openmc.XPlane(x0=59.158)
xp15=openmc.XPlane(x0=36.454)
xp16=openmc.XPlane(x0=95.612)
xp17=openmc.XPlane(x0=72.908)

yp19=openmc.YPlane(y0=0.0 )
yp20=openmc.YPlane(y0=30.272 )

yp37=openmc.YPlane(y0=-1.956 )#steel walll
yp31=openmc.YPlane(y0=-19.806 )
yp32=openmc.YPlane(y0=32.228 )#steel wall
yp38=openmc.YPlane(y0= 50.078)
zp22=openmc.ZPlane(z0=101.8375) #top wall


xp24=openmc.XPlane(x0=121.456,boundary_type='vacuum')
yp26=openmc.YPlane(y0=-30.5,boundary_type='vacuum')
xp25=openmc.XPlane(x0=-25.844,boundary_type='vacuum' )
yp27=openmc.YPlane(y0=60.772,boundary_type='vacuum' )
##absorb plate
zp38=openmc.ZPlane(z0= 91.5)  # top absorb plae
xp41=openmc.XPlane(x0=36.152)
xp42=openmc.XPlane(x0= 36.454)
xp43=openmc.XPlane(x0=59.158)
xp44=openmc.XPlane(x0=59.46)
yp45=openmc.YPlane(y0=30.2)


##堆芯部分
#uo2 fuel
cell1=openmc.Cell()
core_region=-zc1 & +zp7 & -zp8
cell1.region= core_region
cell1.fill=fuel

#gap
cell2=openmc.Cell()
core_up= +zc1 & -zc2 & +zp7 & -zp8
cell2.region=core_up

#clad
cell3=openmc.Cell( )
cell3.region=-zc12 & +zc2
cell3.fill=clad6061

#rubber top
cell4=openmc.Cell()
cell4.region= -zc2 & +zp8
cell4.fill=rubber

#rubber bottom
cell5=openmc.Cell()
cell5.region= -zc2 & -zp7
cell5.fill=rubber

#water
cell6=openmc.Cell()
cell6.region= +zc12
cell6.fill=water

u1=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6))

all_water=openmc.Cell(fill=water)
u2=openmc.Universe(cells=(all_water,))

#Rectangular Lattices 12*16  x*y
lattice1 = openmc.RectLattice()
lattice1.lower_left = (0, 0)
lattice1.pitch = (1.892, 1.892)
lattice1.universes = np.tile(u1, (16, 12))
lattice1.outer=u2



lattice2 = openmc.RectLattice()
lattice2.lower_left = (36.454, 0)
lattice2.pitch = (1.892, 1.892)
lattice2.universes = np.tile(u1, (16, 12))
lattice2.outer=u2


lattice3 = openmc.RectLattice()
lattice3.lower_left = (72.908, 0)
lattice3.pitch = (1.892, 1.892)
lattice3.universes = np.tile(u1, (16, 12))
lattice3.outer=u2


cell8=openmc.Cell()
region8=-xp10 & +xp11 & -yp20 & +yp19 & -zp9 & +zp23
cell8.region= region8
cell8.fill=lattice1


cell9=openmc.Cell()
region9=+xp15 & -xp14 & +yp19 & -yp20 & +zp23 & -zp9
cell9.region= region9
cell9.fill=lattice2


cell10=openmc.Cell()
region10=+yp19 & -yp20 & +xp17 & -xp16 & +zp23 & -zp9
cell10.region= region10
cell10.fill=lattice3


cell13=openmc.Cell()
region13=+yp19 & -yp20 & +xp11 & -xp16 & -zp23 & +zp29
cell13.region=region13
cell13.fill=acrylic

cell11=openmc.Cell()
region11=+yp19 & -yp45 & +xp41 & -xp42 & +zp7 & -zp38
cell11.region=region11
cell11.fill=ss_plate

cell12=openmc.Cell()
region12=+yp19 & -yp45 & +xp43 & -xp44 & +zp7 & -zp38
cell12.region=region12
cell12.fill=ss_plate




cell14=openmc.Cell()
region14=+yp31 & -yp37 & +xp25 & -xp24 & +zp30 & -zp22
cell14.region=region14
cell14.fill=steel


cell15=openmc.Cell()
region15=+yp32 & -yp38 & +xp25 & -xp24 & +zp30 & -zp22
cell15.region=region15
cell15.fill=steel

cell16=openmc.Cell()
cell16.region=+yp26 & -yp27 & +xp25 & -xp24 & +zp30 & -zp28 & ~region8 & ~region9 & ~region10 & ~region11 & ~region12 & ~region13 & ~region14 & ~region15
cell16.fill=water



root=openmc.Universe(cells=(cell8,cell9,cell10,cell11,cell12,cell13,cell14,cell15,cell16))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()

bounds = [0, 0, 0, 73, 20, 91]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 50
settings.particles = 2500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[48,15,50]
plot.width=[160,150]
plot.pixels=[800,800]
plot.color_by='material'
plot.colors={ss_plate:'yellow'}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()

openmc.run()



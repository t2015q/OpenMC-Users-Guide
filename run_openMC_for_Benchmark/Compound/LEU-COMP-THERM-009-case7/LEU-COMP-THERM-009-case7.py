import openmc
import numpy as np

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('O16',4.6753e-2)
fuel.add_nuclide('U234',5.1835e-6)
fuel.add_nuclide('U235',1.0102e-3)
fuel.add_nuclide('U236',5.1395e-6)
fuel.add_nuclide('U238',2.2157e-2)
fuel.set_density('g/cm3',10.4)


water=openmc.Material(2,'water')
water.add_nuclide('H1',6.6675e-2)
water.add_nuclide('O16',3.3338e-2)
water.set_density('g/cm3',.997297)
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


sus304=openmc.Material(6,'sus304')
sus304.add_nuclide('B10',1.3953e-3)
sus304.add_nuclide('B11',5.6163e-3)
sus304.add_nuclide('Mn55',1.4394e-3)
sus304.add_element('Cr',1.7638e-2)
sus304.add_element('Cu',1.9145e-4)
sus304.add_element('Fe',5.5634e-2)
sus304.add_element('Ni',8.0684e-3)
sus304.add_element('Mo',1.5119e-4)
sus304.set_density('g/cm3',7.77)



mats=openmc.Materials([fuel,water,clad6061,rubber,acrylic,sus304])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel cylinder
zc1=openmc.ZCylinder(x0=0,y0=0,R=0.6325)
zc2=openmc.ZCylinder(x0=0,y0=0,R=0.6415)

zp7=openmc.ZPlane(z0= 0.0)
zp8=openmc.ZPlane(z0=92.075)
zp9=openmc.ZPlane(z0= 94.2975) #top 0f clad


xp10=openmc.XPlane(x0=38.1 ) #first cluster
xp11=openmc.XPlane(x0= 0.0)
zc12=openmc.ZCylinder(x0=0,y0=0,R=0.7075)#clad outer surface

xp14=openmc.XPlane(x0=81.96)   #second cluster
xp15=openmc.XPlane(x0=43.86)  #second cluster

xp16=openmc.XPlane(x0=125.82)   #third cluster
xp17=openmc.XPlane(x0=87.72)   #third cluster

yp19=openmc.YPlane(y0=0.0 )
yp20=openmc.YPlane(y0=20.32 )

zp23=openmc.ZPlane(z0= -2.2225)

#side of water reflector
xp24=openmc.XPlane(x0=155.82 ,boundary_type='vacuum')
xp25=openmc.XPlane(x0=-30,boundary_type='vacuum')
yp26=openmc.YPlane(y0=50.32,boundary_type='vacuum' )
yp27=openmc.YPlane(y0=-30,boundary_type='vacuum')
zp28=openmc.ZPlane(z0=107.075,boundary_type='vacuum') #top of water
zp29=openmc.ZPlane(z0=-4.7625)
zp35=openmc.ZPlane(z0=-20.0625,boundary_type='vacuum' ) #bottom of water

##ss plate
yp41=openmc.YPlane(y0=-7.64)
yp42=openmc.YPlane(y0=27.96)

xp43=openmc.XPlane(x0=40.98)  #first
xp44=openmc.XPlane(x0=41.278)
xp45=openmc.XPlane(x0=84.84)  #second
xp46=openmc.XPlane(x0=85.138)

zp47=openmc.ZPlane(z0=91.5)


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


#Rectangular Lattices 15*8
lattice1 = openmc.RectLattice()
lattice1.lower_left = (0, 0)
lattice1.pitch = (2.54, 2.54)
lattice1.universes = np.tile(u1, (8, 15))  # 15*8
lattice1.outer=u2



lattice2 = openmc.RectLattice()
lattice2.lower_left = (43.86, 0)
lattice2.pitch = (2.54, 2.54)
lattice2.universes = np.tile(u1, (8, 15))  # 15*8
lattice2.outer=u2


lattice3 = openmc.RectLattice()
lattice3.lower_left = (87.72, 0)
lattice3.pitch = (2.54, 2.54)
lattice3.universes = np.tile(u1, (8, 15))  # 15*8
lattice3.outer=u2


cell8=openmc.Cell()
region8=-xp10 & +xp11 & -yp20 & +yp19 & -zp9 & +zp23
cell8.region= region8
cell8.fill=lattice1


cell9=openmc.Cell( )
region9=+xp15 & -xp14 & +yp19 & -yp20 & +zp23 & -zp9
cell9.region= region9
cell9.fill=lattice2


cell10=openmc.Cell()
region10= +yp19 & -yp20 & +xp17 & -xp16 & +zp23 & -zp9
cell10.region=region10
cell10.fill=lattice3

cell11=openmc.Cell()
region11=+yp19 & -yp20 & +xp11 & -xp16 & -zp23 & +zp29
cell11.region=region11
cell11.fill=acrylic



cell12=openmc.Cell()
region12=+yp41 & -yp42 & +xp43 & -xp44 & +zp7 & -zp47
cell12.region=region12
cell12.fill=sus304

cell13=openmc.Cell()
region13=+yp41 & -yp42 & +xp45 & -xp46 & +zp7 & -zp47
cell13.region=region13
cell13.fill=sus304


cell14=openmc.Cell()
r8=+xp10 | -xp11 | +yp20 | -yp19 | +zp9 | -zp23
r9=-xp15 | +xp14 | -yp19 | +yp20 | -zp23 | +zp9
r10= -yp19 | +yp20 | -xp17 | +xp16 | -zp23 | +zp9
r11=-yp19 | +yp20 | -xp11 | +xp16 | +zp23 | -zp29

cell14.region= r8 & r9 & r10 & r11  & ~region12 & ~region13 & -xp24 & +xp25 &  -yp26  & +yp27 & -zp28 & +zp35  
cell14.fill=water


root=openmc.Universe(cells=(cell8,cell9,cell10,cell11,cell12,cell13,cell14))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [0, 0, 0, 90, 10, 90]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 160
settings.inactive = 72
settings.particles = 1500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[60,10.16,50]
plot.width=[200,200]
plot.pixels=[1000,1000]
plot.color_by='material'
plot.colors={sus304:'yellow'}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.run()



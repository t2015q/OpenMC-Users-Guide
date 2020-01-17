import openmc
import numpy as np

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('O16',4.1202e-2)
fuel.add_nuclide('U234',2.8563e-6)
fuel.add_nuclide('U235',4.8785e-4)
fuel.add_nuclide('U236',3.5348e-6)
fuel.add_nuclide('U238',2.0009e-2)
fuel.set_density('g/cm3',9.2)


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


clad1100=openmc.Material(4,'clad1100')
clad1100.add_nuclide('Al27',5.9660e-2)
clad1100.add_element('Si',2.3302e-4)
clad1100.add_element('Cu',3.0705e-5)
clad1100.add_element('Zn',1.2433e-5)
clad1100.add_element('Fe',1.1719e-4)
clad1100.add_nuclide('Mn55',7.3991e-6)
clad1100.set_density('g/cm3',2.7)


acrylic=openmc.Material(6,'acrylic')
acrylic.add_nuclide('H1',5.6642e-2)
acrylic.add_nuclide('O16',1.4273e-2)
acrylic.add_nuclide('C0',3.5648e-2)
acrylic.add_s_alpha_beta('c_H_in_CH2')
acrylic.set_density('g/cm3',1.185)

clad5052=openmc.Material(5,'clad5052')
clad5052.add_element('Mg',1.6663e-3)
clad5052.add_nuclide('Al27',5.8028e-2)
clad5052.add_element('Si',1.2978e-4)
clad5052.add_element('Cu',1.2746e-5)
clad5052.add_element('Zn',1.2387e-5)
clad5052.add_element('Cr',7.7888e-5)
clad5052.add_element('Fe',6.5265e-5)
clad5052.add_nuclide('Mn55',1.4743e-5)
clad5052.set_density('g/cm3',2.69)

lead=openmc.Material(7,'lead')
lead.add_element('Pb',3.2132e-2)
lead.set_density('g/cm3',11.07)

mats=openmc.Materials([fuel,water,clad6061,clad5052,acrylic,clad1100,lead])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel cylinder
zc1=openmc.ZCylinder(x0=0,y0=0,R=0.5588)
zc2=openmc.ZCylinder(x0=0,y0=0,R=0.635)

zp7=openmc.ZPlane(z0= 0.0)
zp8=openmc.ZPlane(z0=91.44)
zp9=openmc.ZPlane(z0= 91.92) #top 0f clad


xp10=openmc.XPlane(x0=38.608 )
xp11=openmc.XPlane(x0= 0.0)
xp15=openmc.XPlane(x0=51.708)
xp14=openmc.XPlane(x0=90.316)
xp17=openmc.XPlane(x0=103.416)
xp16=openmc.XPlane(x0=142.024)


yp20=openmc.YPlane(y0=32.512 )
yp21=openmc.YPlane(y0=0.0 )
zp22=openmc.ZPlane(z0= 96.52)
zp23=openmc.ZPlane(z0= -1.27)

#side of water reflector
xp24=openmc.XPlane(x0=183.512 ,boundary_type='vacuum')
xp25=openmc.XPlane(x0=-41.488,boundary_type='vacuum')
yp26=openmc.YPlane(y0=63.012,boundary_type='vacuum' )
yp27=openmc.YPlane(y0=-30.5,boundary_type='vacuum')
zp28=openmc.ZPlane(z0=111.72,boundary_type='vacuum') #top of water
zp29=openmc.ZPlane(z0=-3.81)

yp31=openmc.YPlane(y0=-10.2)
yp32=openmc.YPlane(y0=42.712)
xp33=openmc.XPlane(x0=-10.988)
xp34=openmc.XPlane(x0=153.012)
zp35=openmc.ZPlane(z0=-19.11,boundary_type='vacuum')
zp36=openmc.ZPlane(z0=104.29)

##堆芯部分
#uo2 fuel
cell1=openmc.Cell()
core_region=-zc1 & +zp7 & -zp8
cell1.region= core_region
cell1.fill=fuel

#gap
cell2=openmc.Cell()
core_up= +zc1 & -zc2  & -zp9
cell2.region=core_up
cell2.fill=clad6061


#clad
cell3=openmc.Cell( )
cell3.region=-zc1 & +zp8 & -zp9
cell3.fill=clad1100


cell4=openmc.Cell()
cell4.region= -zc2 & +zp9
cell4.fill=clad1100

#rubber bottom
cell5=openmc.Cell()
cell5.region= -zc1 & -zp7
cell5.fill=clad5052

#water
cell6=openmc.Cell()
cell6.region= +zc2
cell6.fill=water

u1=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6))




all_water=openmc.Cell(fill=water)
u2=openmc.Universe(cells=(all_water,))

#Rectangular Lattices 19*16
lattice1 = openmc.RectLattice()
lattice1.lower_left = (0, 0)
lattice1.pitch = (2.032, 2.032)
lattice1.universes = np.tile(u1, (16, 19))
lattice1.outer=u2

#Rectangular Lattices 19*16
lattice2 = openmc.RectLattice()
lattice2.lower_left = (51.708, 0)
lattice2.pitch = (2.032, 2.032)
lattice2.universes = np.tile(u1, (16, 19))
lattice2.outer=u2


#Rectangular Lattices 19*16
lattice3 = openmc.RectLattice()
lattice3.lower_left = (103.416, 0)
lattice3.pitch = (2.032, 2.032)
lattice3.universes = np.tile(u1, (16, 19))  # 19*16
lattice3.outer=u2

cell8=openmc.Cell()
region8=-xp10 & +xp11 & -yp20 & +yp21 & -zp9 & +zp23
cell8.region= region8
cell8.fill=lattice1


cell9=openmc.Cell()
region9=+xp15 & -xp14 & +yp21 & -yp20 & +zp23 & -zp9
cell9.region= region9
cell9.fill=lattice2


cell10=openmc.Cell()
region10=+yp21 & -yp20 & +xp17 & -xp16 & +zp23 & -zp9
cell10.region= region10
cell10.fill=lattice3

cell11=openmc.Cell()
region11=+yp21 & -yp20 & +xp11 & -xp16 & -zp23 & +zp29
cell11.region=region11
cell11.fill=acrylic


cell14=openmc.Cell()
region14=+yp31 & -yp21 & +xp33 & -xp34 & +zp35 & -zp36
cell14.region=region14
cell14.fill=lead

cell15=openmc.Cell()
region15=+yp20 & -yp32 & +xp33 & -xp34 & +zp35 & -zp36
cell15.region=region15
cell15.fill=lead


cell16=openmc.Cell()
cell16.region=~region8 & ~region9 & ~region10 & ~region11 & ~region14 & ~region15 & -xp24 & +xp25 &  -yp26  & +yp27 & -zp28 & +zp35 
cell16.fill=water


root=openmc.Universe(cells=(cell8,cell9,cell10,cell11,cell14,cell15,cell16))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [0, 0, 0, 140, 32, 90]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 160
settings.inactive = 68
settings.particles = 1500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[40,30,50]
plot.width=[200,200]
plot.pixels=[800,800]
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.run()



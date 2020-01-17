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
water.add_nuclide('H1',6.6706e-2)
water.add_nuclide('O16',3.3353e-2)
water.add_nuclide('Gd152',7.9656e-11)
water.add_nuclide('Gd154',8.6825e-10)
water.add_nuclide('Gd155',5.8946e-9)
water.add_nuclide('Gd156',8.1528e-9)
water.add_nuclide('Gd157',6.2331e-9)
water.add_nuclide('Gd158',9.8933e-9)
water.add_nuclide('Gd160',8.7064e-9)
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



mats=openmc.Materials([fuel,water,clad6061,rubber,acrylic])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel cylinder
zc1=openmc.ZCylinder(x0=0.,y0=0.,R=0.6325)
zc2=openmc.ZCylinder(x0=0.,y0=0.,R=0.6415)

zp7=openmc.ZPlane(z0= 0.0)
zp8=openmc.ZPlane(z0=92.075)
zp9=openmc.ZPlane(z0= 94.2975) #top 0f clad


xp10=openmc.XPlane(x0=22.704 )
xp11=openmc.XPlane(x0= 0.0)
zc12=openmc.ZCylinder(x0=0.,y0=0.,R=0.7075)#clad outer surface
xp13=openmc.XPlane(x0= 18.92) #edge of partial row
yp19=openmc.YPlane(y0=0.0 )
yp20=openmc.YPlane(y0=35.948 )
yp21=openmc.YPlane(y0=1.892 )
zp23=openmc.ZPlane(z0= -2.2225)

#side of water reflector
xp24=openmc.XPlane(x0=52.704 ,boundary_type='vacuum')
xp25=openmc.XPlane(x0=-30,boundary_type='vacuum')
yp26=openmc.YPlane(y0=65.948,boundary_type='vacuum' )
yp27=openmc.YPlane(y0=-30,boundary_type='vacuum')
zp28=openmc.ZPlane(z0=107.075,boundary_type='vacuum') #top of water
zp29=openmc.ZPlane(z0=-4.7625)
zp30=openmc.ZPlane(z0=-20.0625,boundary_type='vacuum' ) #bottom of water




##堆芯部分
cell1=openmc.Cell()
cell1.region= -zc1 & +zp7 & -zp8
cell1.fill=fuel


cell2=openmc.Cell()
cell2.region= +zc1 & -zc2 & +zp7 & -zp8


cell3=openmc.Cell( )
cell3.region=-zc12 & +zc2 
cell3.fill=clad6061

cell4=openmc.Cell()
cell4.region= -zc2  & -zp7
cell4.fill=rubber

cell5=openmc.Cell()
cell5.region= -zc2 & +zp8
cell5.fill=rubber


cell6=openmc.Cell()
cell6.region= +zc12 
cell6.fill=water

u1=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6))

all_water=openmc.Cell(fill=water)
u2=openmc.Universe(cells=[all_water])

#Rectangular Lattices 12*18(x*y)
lattice1 = openmc.RectLattice()
lattice1.lower_left = (0, 1.892)
lattice1.pitch = (1.892, 1.892)
lattice1.universes = np.tile(u1, (18, 12))
lattice1.outer=u2


#Rectangular Lattices 10*1(x*y)
lattice2 = openmc.RectLattice()
lattice2.lower_left = (0, 0)
lattice2.pitch = (1.892, 1.892)
lattice2.universes = np.tile(u1, (1, 10))
lattice2.outer=u2



cell7=openmc.Cell()
region7=-xp10 & +xp11 & -yp20 & +yp21 & -zp9 & +zp23
cell7.region= region7
cell7.fill=lattice1


cell8=openmc.Cell()
region8=-xp13 & +xp11 & -yp21 & +yp19 & -zp9 & +zp23
cell8.region= region8
cell8.fill=lattice2


cell9=openmc.Cell()
region9=-xp10 & +xp11 & -yp20 & +yp19 & -zp23 & +zp29
cell9.region=  region9
cell9.fill=acrylic


cell10=openmc.Cell()
cell10.region= -xp24 & +xp25 &  -yp26  & +yp27 & -zp28 & +zp30 & ~region7 & ~region8 & ~region9
cell10.fill=water

root=openmc.Universe(cells=(cell7,cell8,cell9,cell10))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [5, 10, 40, 10, 15,45]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 130
settings.inactive = 72
settings.particles = 1500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[20,20,50]
plot.width=[150,150]
plot.pixels=[800,800]
plot.basis='xy'
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()


openmc.run()



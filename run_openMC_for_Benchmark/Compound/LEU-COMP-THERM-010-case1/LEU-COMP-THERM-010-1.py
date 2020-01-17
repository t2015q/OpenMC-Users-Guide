import openmc
import numpy as np

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('O16',4.6753e-2)
fuel.add_nuclide('U234',5.1835e-6)
fuel.add_nuclide('U235',1.0102e-3)
fuel.add_nuclide('U236',5.1395e-6)
fuel.add_nuclide('U238',2.2157e-2)
fuel.set_density('atom/b-cm',.06993052)


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
rubber.set_density('g/cm3',1.498)



acrylic=openmc.Material(5,'acrylic')
acrylic.add_nuclide('H1',5.6642e-2)
acrylic.add_nuclide('O16',1.4273e-2)
acrylic.add_nuclide('C0',3.5648e-2)
acrylic.add_s_alpha_beta('c_H_in_CH2')
acrylic.set_density('g/cm3',1.185)

plumbum=openmc.Material(6,'plumbum')
plumbum.add_element('Pb',3.2132e-2)
plumbum.set_density('atom/b-cm',3.2132e-2)

mats=openmc.Materials([fuel,water,clad6061,rubber,acrylic,plumbum])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel cylinder
zc1=openmc.ZCylinder(x0=0,y0=0,R=0.6325)
zc2=openmc.ZCylinder(x0=0,y0=0,R=0.6415)

zp7=openmc.ZPlane(z0= 0.0)
zp8=openmc.ZPlane(z0=92.075)
zp9=openmc.ZPlane(z0= 94.2975) #top 0f clad


xp10=openmc.XPlane(x0=33.02 )
xp11=openmc.XPlane(x0= 0.0)
zc12=openmc.ZCylinder(x0=0,y0=0,R=0.7075)#clad outer surface

xp14=openmc.XPlane(x0=85.535)
xp15=openmc.XPlane(x0=52.515)
xp16=openmc.XPlane(x0=138.05)
xp17=openmc.XPlane(x0=105.03)

yp19=openmc.YPlane(y0=0.0 )
yp20=openmc.YPlane(y0=20.32 )

zp23=openmc.ZPlane(z0= -2.2225)

#side of water reflector
xp24=openmc.XPlane(x0=181.525 ,boundary_type='vacuum')
xp25=openmc.XPlane(x0=-43.475,boundary_type='vacuum')
yp26=openmc.YPlane(y0=50.82,boundary_type='vacuum' )
yp27=openmc.YPlane(y0=-30.5,boundary_type='vacuum')
zp28=openmc.ZPlane(z0=109.4975,boundary_type='vacuum') #top of water
zp35=openmc.ZPlane(z0=-20.0625,boundary_type='vacuum' ) #bottom of lead


##lead pb
zp29=openmc.ZPlane(z0=-4.7625) #bottom of acrylic support plate

yp31=openmc.YPlane(y0=-10.2)
yp32=openmc.YPlane(y0=30.52)
xp33=openmc.XPlane(x0=-12.975)
xp34=openmc.XPlane(x0=151.025)

zp36=openmc.ZPlane(z0=103.3375)
yp37=openmc.YPlane(y0=0.0)
yp38=openmc.YPlane(y0=20.32)
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

#Rectangular Lattices 13*8
lattice1 = openmc.RectLattice()
lattice1.lower_left = (0, 0)
lattice1.pitch = (2.54, 2.54)
lattice1.universes = np.tile(u1, (8, 13))  # 13*8
lattice1.outer=u2



lattice2 = openmc.RectLattice()
lattice2.lower_left = (52.515, 0)
lattice2.pitch = (2.54, 2.54)
lattice2.universes = np.tile(u1, (8, 13))
lattice2.outer=u2


lattice3 = openmc.RectLattice()
lattice3.lower_left = (105.03, 0)
lattice3.pitch = (2.54, 2.54)
lattice3.universes = np.tile(u1, (8, 13))
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

cell14=openmc.Cell()
region14=+yp31 & -yp37 & +xp33 & -xp34 & +zp35 & -zp36
cell14.region=region14
cell14.fill=plumbum

cell15=openmc.Cell()
region15=+yp38 & -yp32 & +xp33 & -xp34 & +zp35 & -zp36
cell15.region=region15
cell15.fill=plumbum


cell16=openmc.Cell()
cell16.region= -xp24 & +xp25 &  -yp26  & +yp27 & -zp28 & +zp35 & ~region14 & ~region15 & ~region8 & ~region9 & ~region10 & ~region13
cell16.fill=water


root=openmc.Universe(cells=(cell8,cell9,cell10,cell13,cell14,cell15,cell16))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [0, 0, 0, 138, 20, 92]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 160
settings.inactive = 67
settings.particles = 1500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[60,10.16,50]
plot.width=[200,200]
plot.pixels=[800,800]
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()

openmc.run()



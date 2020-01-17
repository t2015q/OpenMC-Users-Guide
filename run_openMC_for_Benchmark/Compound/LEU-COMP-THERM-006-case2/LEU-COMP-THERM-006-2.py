import openmc
import numpy as np

fuel=openmc.Material(1,'fuel')
fuel.add_nuclide('O16',4.7214e-2)
fuel.add_nuclide('U234',4.8872e-6)
fuel.add_nuclide('U235',6.0830e-4)
fuel.add_nuclide('U238',2.2531e-2)
fuel.set_density('atom/b-cm',7.035819e-2 )




clad=openmc.Material(2,'cladding')
clad.add_nuclide('Al27',5.513700e-2)
clad.set_density('atom/b-cm',5.513700e-2)


water=openmc.Material(3,'water')
water.add_nuclide('H1',6.6735e-2)
water.add_nuclide('O16',3.3368e-2)
water.set_density('atom/b-cm',1.001030e-1)
water.add_s_alpha_beta('c_H_in_H2O')




mats=openmc.Materials([fuel,clad,water])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#fuel
zc1=openmc.ZCylinder(x0=0,y0=0,R=0.625)#fuel
zc2=openmc.ZCylinder(x0=0,y0=0,R=0.7085)#clad

zp8=openmc.ZPlane(z0= 144.15) #top fuel  
zp7=openmc.ZPlane(z0=0.0)   #bottom of fuel

#lattice
xp10=openmc.XPlane(x0=36.98)
xp11=openmc.XPlane(x0=0.)
yp20=openmc.YPlane(y0=36.98)
yp19=openmc.YPlane(y0=0.)



sph9=openmc.Sphere(x0=18.49,y0=18.49,z0=72.075,R=150.0,boundary_type='vacuum')

zp11=openmc.ZPlane(z0= 73.73)  #critical water level=73.73

#water reflector=30.0 cm

xp31=openmc.XPlane(x0=66.98 )
xp32=openmc.XPlane(x0=-30.)
yp33=openmc.YPlane(y0=66.98)
yp34=openmc.YPlane(y0=-30.)
zp29=openmc.ZPlane(z0=-30.)




##堆芯部分，燃料棒u1
cell1=openmc.Cell()
cell1.region= -zc1 
cell1.fill=fuel


cell2=openmc.Cell()
cell2.region=+zc1 & -zc2 
cell2.fill=clad



cell5=openmc.Cell()
cell5.region=   +zc2  & -zp11
cell5.fill=water


cell6=openmc.Cell()
cell6.region= +zc2 & +zp11


u1=openmc.Universe(cells=(cell1,cell2,cell5,cell6))

all_water=openmc.Cell(region= -zp11 ,fill=water)
void=openmc.Cell(region=+zp11)
u2=openmc.Universe(cells=(all_water,void))

#Rectangular Lattices 20*20(x*y)
lattice = openmc.RectLattice()
lattice.lower_left = (0, 0)
lattice.pitch = (1.849, 1.849)
lattice.universes = np.tile(u1, (20, 20))  
lattice.outer=u2

#创建堆芯lattice
cell8=openmc.Cell()
cell8.region= -xp10 & +xp11 & -yp20 & +yp19 & +zp7 & -zp8
cell8.fill=lattice


cell9=openmc.Cell()
cell9.region=-xp31 &  +xp32 & +yp34 & -yp33 & +zp29 & -zp11 & ~cell8.region
cell9.fill=water

#outer
cell11=openmc.Cell()
cell11.region= -sph9 & ~cell9.region & ~cell8.region


#root universe

root=openmc.Universe(cells=(cell8,cell9,cell11))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [15, 15, 40, 20, 20,45]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 250
settings.inactive = 75
settings.particles = 1500
settings.output={'tallies':False}
settings.export_to_xml()

plot=openmc.Plot()
plot.origin=[17.5655,17.5655,50]
plot.width=[250,250]
plot.pixels=[1008,800]
plot.basis='yz'
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()

openmc.run()


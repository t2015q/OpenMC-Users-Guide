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
rubber.add_nuclide('H1',5.0906e-2)
rubber.add_element('Si',8.4315e-5)
rubber.add_nuclide('C0',3.8117e-2)
rubber.add_element('Ca',2.2453e-3)
rubber.add_nuclide('S32',4.1843e-4)
rubber.add_nuclide('O16',1.0903e-2)
rubber.add_s_alpha_beta('c_H_in_CH2')
rubber.set_density('g/cm3',1.321)

poly=openmc.Material(5,'poly')
poly.add_nuclide('C0',3.8811e-2)
poly.add_nuclide('H1',7.7623e-2)
poly.set_density('g/cm3',0.904)
poly.add_s_alpha_beta('c_H_in_CH2')



acrylic=openmc.Material(6,'acrylic')
acrylic.add_nuclide('H1',5.6782e-2 )
acrylic.add_nuclide('O16',1.4196e-2)
acrylic.add_element('C',3.5489e-2)
acrylic.add_s_alpha_beta('c_H_in_CH2')
acrylic.set_density('g/cm3',1.18)

borated=openmc.Material(7,'borated')
borated.add_nuclide('O16',3.3526e-2)
borated.add_nuclide('H1',6.6626e-2)
borated.add_nuclide('B10',2.8267E-05)
borated.add_nuclide('B11',1.1378E-04)
borated.set_density('atom/b-cm',0.10029385533)
borated.add_s_alpha_beta('c_H_in_H2O')


mats=openmc.Materials([fuel,water,clad6061,rubber,acrylic,borated,poly])
mats.cross_sections='/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


zp1=openmc.ZPlane(z0= 0.0) #bottom of fuel
zp2=openmc.ZPlane(z0= -2.54)
zp3=openmc.ZPlane(z0= -20.34,boundary_type='vacuum')


zp6=openmc.ZPlane(z0= 92.075) #top fuel
zp7=openmc.ZPlane(z0= 94.615) # top of top plug
zp8=openmc.ZPlane(z0=109.815,boundary_type='vacuum')


xp10=openmc.XPlane(x0=0.0)
xp11=openmc.XPlane(x0= -58.59)
xp12=openmc.XPlane(x0=-78.59,boundary_type='vacuum')
xp20=openmc.XPlane(x0=0.11)
xp21=openmc.XPlane(x0=2.015)
xp22=openmc.XPlane(x0=22.015,boundary_type='vacuum')

yp30=openmc.YPlane(y0=0.0 )
yp31=openmc.YPlane(y0=75.6 )
yp32=openmc.YPlane(y0=-0.14 )
yp33=openmc.YPlane(y0=75.6 ) #inner surface of experiment tank
yp34=openmc.YPlane(y0=-2.045 ) #outer surface of experiment tank
yp35=openmc.YPlane(y0=77.645 )
yp36=openmc.YPlane(y0=-22.045,boundary_type='vacuum' )
yp37=openmc.YPlane(y0=97.645,boundary_type='vacuum')



zc44=openmc.ZCylinder(x0=0,y0=0,R=0.6325) #fuel
zc45=openmc.ZCylinder(x0=0,y0=0.,R=0.6415) #gap
zc46=openmc.ZCylinder(x0=0,y0=0.,R=0.7075) #clad
zc47=openmc.ZCylinder(x0=0,y0=0.,R=0.7135)#hole ingrid
zp50=openmc.ZPlane(z0= 67.3) #bottom surface of upper grid
zp51=openmc.ZPlane(z0= 68.57) #top surface of upper grid

##堆芯部分
#uo2 fuel
cell1=openmc.Cell()
core_region=-zc44 & +zp1 & -zp6
cell1.region= core_region
cell1.fill=fuel


cell2=openmc.Cell()
core_up= +zp1 & -zp6  & -zc45 & +zc44
cell2.region=core_up


cell3=openmc.Cell( )
cell3.region=-zc46 & +zc45
cell3.fill=clad6061

cell4=openmc.Cell()
cell4.region= -zc45 & +zp6
cell4.fill=rubber


cell5=openmc.Cell()
cell5.region= -zp1 & -zc45
cell5.fill=rubber


cell6=openmc.Cell()
cell6.region= +zc46 & +zp1 & -zp50
cell6.fill=borated

cell7=openmc.Cell()
cell7.region= +zc46  & +zp51
cell7.fill=borated

cell8=openmc.Cell()
cell8.region= +zc46  & -zc47 & +zp50 & -zp51
cell8.fill=borated

cell9=openmc.Cell()
cell9.region= +zc47 & +zp50 & -zp51
cell9.fill=poly

cell10=openmc.Cell()
cell10.region= +zc46 & -zc47 & -zp1
cell10.fill=borated

cell11=openmc.Cell()
cell11.region= +zc47 & -zp1
cell11.fill=poly


u1=openmc.Universe(cells=(cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9,cell10,cell11))

hole=openmc.Cell(fill=borated,region=-zc47 & +zp50 & -zp51 |(-zc47 & -zp1))
poly_region=openmc.Cell(fill=poly,region= +zc47 & +zp50 & -zp51 |(+zc47 & -zp1))
borated_region=openmc.Cell(fill=borated,region=+zp1 & -zp50 | +zp51)
u2=openmc.Universe(cells=(hole,poly_region,borated_region))

all_water=openmc.Cell(fill=borated,region=+zp1 & -zp50 | +zp51 )
all_poly=openmc.Cell(fill=poly,region=-zp1 | (+zp50 & -zp51))
u3=openmc.Universe(cells=(all_water,all_poly))

#lattice 31*40
lattice = openmc.RectLattice()
lattice.lower_left = (-58.59, 0)
lattice.pitch = (1.89, 1.89)
lattice.universes = np.tile(u1, (40, 31))  
lattice.outer=u3

lattice.universes[9,0]=u2  
lattice.universes[19,0]=u2   
lattice.universes[29,0]=u2 


cell12=openmc.Cell()
region12=+xp11 & -xp10 & +yp30 & -yp31 & -zp7 & +zp2
cell12.region=region12
cell12.fill=lattice



cell13=openmc.Cell()
cell13.region= +yp34 & -yp35 & -xp21 & +xp12 & +zp3 & -zp8 & (+yp33 | -yp32  | +xp20  | -zp2)
cell13.fill=acrylic

cell14=openmc.Cell()
cell14.region=+yp36 & -yp37 & -xp22 & +xp12 & +zp3 & -zp8 & (  -yp34 | +yp35 |  +xp21 )
cell14.fill=water

cell15=openmc.Cell()
cell15.region=+yp32 & -yp33  & -xp20   & +xp12 & +zp2 & -zp8 & ~region12
cell15.fill=borated


root=openmc.Universe(cells=(cell12,cell13,cell14,cell15))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
bounds = [-58, 0, 0, 0, 75.6, 91]
src.space = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 100
settings.particles = 2500
settings.output={'tallies':False}
settings.export_to_xml()



plot=openmc.Plot()
plot.origin=[-18.9,40,67.5]
plot.width=[150,150]
plot.pixels=[800,800]
plot.color_by='material'



plot1=openmc.Plot()
plot1.origin=[-17.955,36.855,67.5]
plot1.width=[150,180]
plot1.pixels=[800,800]
plot1.color_by='material'
plot1.basis='yz'


plot_file=openmc.Plots([plot,plot1])
plot_file.export_to_xml()

openmc.run()



import openmc

#Materials
steel=openmc.Material(1,'steel')
steel.add_element('Si',1.3603E-03)
steel.add_element('Ti',5.9844E-04)
steel.add_element('Ni',8.1369E-03)
steel.add_element('Cr',1.6532E-02)
steel.add_element('Fe',5.9088E-02)
steel.add_nuclide('Mn55',1.3039E-03)
steel.set_density('atom/b-cm',8.701954E-02)
steel.temperature=300

water=openmc.Material(2,'water')
water.add_nuclide('H1',6.6742E-02)
water.add_nuclide('O16',3.3371E-02)
water.set_density('atom/b-cm',1.001130E-01)
water.add_s_alpha_beta('c_H_in_H2O')
water.temperature=300

clad=openmc.Material(4,'cladding')
clad.add_nuclide('B10',1.0844E-02)
clad.add_nuclide('B11',4.3649E-02)
clad.add_element('C',1.3623E-02)
clad.set_density('atom/b-cm',6.811600E-02)
clad.temperature=300

fuel=openmc.Material(3,'fuel')
fuel.add_nuclide('H1',5.7694E-02)
fuel.add_nuclide('O16',3.7970E-02)
fuel.add_nuclide('N14',2.3712E-03)
fuel.add_nuclide('U234',9.5863E-07)
fuel.add_nuclide('U235',1.0854E-04)
fuel.add_nuclide('U238',9.5565E-04)
fuel.set_density('atom/b-cm',9.910035E-02)
fuel.add_s_alpha_beta('c_H_in_H2O')
fuel.temperature=300

mats=openmc.Materials([clad,water,fuel,steel])
mats.cross_sections= '/home/tang/nndc_hdf5/cross_sections.xml'
mats.export_to_xml()


#Geometry
zc1=openmc.ZCylinder(x0=0,y0=0,R=55.)
zc2=openmc.ZCylinder(x0=0,y0=0,R=55.6)
zc3=openmc.ZCylinder(x0=0,y0=0,R=99.2)
zc4=openmc.ZCylinder(x0=0,y0=0,R=100.,boundary_type='vacuum')

zp5=openmc.ZPlane(z0=-38.5,boundary_type='vacuum')
zp6=openmc.ZPlane(z0=-37.5)
zp7=openmc.ZPlane(z0=-1.5)
zp8=openmc.ZPlane(z0=0.)
zp9=openmc.ZPlane(z0=108.) #water level
zp10=openmc.ZPlane(z0=248.5,boundary_type='vacuum')

zc11=openmc.ZCylinder(R=54.8)

zp200=openmc.ZPlane(z0=1.7)
zp201=openmc.ZPlane(z0=26.1371) #solution level

zc300=openmc.ZCylinder(x0=0,y0=0,R=2.775)
zc301=openmc.ZCylinder(x0=0,y0=0,R=2.75)
zc302=openmc.ZCylinder(x0=0,y0=0,R=2.25)
zp303=openmc.ZPlane(z0=0.7)



 #This part is preparing for the establishment of lattice

     ##Create a non-hole space
c1000=openmc.Cell(fill=steel,region=-zp200 )
c1001=openmc.Cell(fill=fuel,region=+zp200 & -zp201 )
c1002=openmc.Cell(region=+zp201 )
u1=openmc.Universe(universe_id=1,cells=[c1000,c1001,c1002])


     ##   Create a hole space
c2000=openmc.Cell(fill=fuel,region=-zc300 & -zp200 )
c2001=openmc.Cell(fill=steel,region= +zc300 & -zp200)
c2002=openmc.Cell(fill=fuel,region= +zp200 & -zp201 )
c2003=openmc.Cell(region= +zp201 )
u2=openmc.Universe(universe_id=2,cells=[c2000,c2001,c2002,c2003])

    ##Create a control rod space
#c3000=openmc.Cell(fill=steel,region= -zc302 & -zp303 )
#c3001=openmc.Cell(fill=clad,region= -zc302 & +zp303)
#c3002=openmc.Cell(fill=steel,region= +zc302 & -zc301)
#c3003=openmc.Cell(fill=fuel,region=+zc301 & -zc300 & -zp200)
#c3004=openmc.Cell(fill=steel,region=  +zc300 & -zp200)
#c3005=openmc.Cell(fill=fuel,region= +zc301 & +zp200 & -zp201)
#c3006=openmc.Cell(region= +zc301 & +zp201)

c3000=openmc.Cell(fill=steel,region= -zc302 & -zp303 )
c3001=openmc.Cell(fill=clad,region= -zc302 & +zp303 & -zp201)
c3002=openmc.Cell(fill=steel,region= +zc302 & -zc301 & -zp201 )
c3003=openmc.Cell(fill=fuel,region=+zc301 & -zc300 & -zp200 )
c3004=openmc.Cell(fill=steel,region=  +zc300 & -zp200 )
c3005=openmc.Cell(fill=fuel,region= +zc301 & +zp200 & -zp201)
c3006=openmc.Cell(region= +zp201 )

u3=openmc.Universe(universe_id=3,cells=[c3000,c3001,c3001,c3002,c3003,c3004,c3005,c3006])

    ##Outer space,in order to fill the remaining space of the lattice
c4000=openmc.Cell(fill=steel,region=+zp8 & -zp200  )
c4001=openmc.Cell(fill=fuel,region=+zp200 & -zp201)
c4002=openmc.Cell(region=+zp201 )
u4=openmc.Universe(cells=[c4000,c4001,c4002])

##creat a lattice
lattice=openmc.HexLattice(lattice_id=5)
lattice.center=(0,0)
lattice.pitch=[10.6]
outer_ring=[u1,u2,u2,u2,u2, u1,u2,u2,u2,u2, u1,u2,u2,u2,u2, u1,u2,u2,u2,u2, u1,u2,u2,u2,u2, u1,u2,u2,u2,u2]
m5_ring=[u2,u2,u2,u2, u2,u2,u2,u2, u2,u2,u2,u2, u2,u2,u2,u2, u2,u2,u2,u2, u2,u2,u2,u2]
m4_ring=[u3,u2,u2, u3,u2,u2, u3,u2,u2, u3,u2,u2, u3,u2,u2, u3,u2,u2]
m3_ring=[u2,u2, u2,u2, u2,u2, u2,u2, u2,u2, u2,u2]
m2_ring=[u2,u2,u2,u2,u2,u2]
inner_ring=[u3]
lattice.universes=[outer_ring,m5_ring,m4_ring,m3_ring,m2_ring,inner_ring]
lattice.outer=u4






## Water shield
cell2=openmc.Cell()
cell2.region= -zc4 & +zp5 & -zp10 & (+zc3 | -zp6)
cell2.fill=steel

## Rang of water
cell3=openmc.Cell()
cell3.region= -zc3 & +zp6 & -zp9 & (+zc2 | -zp7 )
cell3.fill=water

## The top of the water  zone is vacuum
cell4=openmc.Cell()
cell4.region= -zc3 & +zc2 & +zp9 & -zp10

## Core shield
cell5=openmc.Cell()
cell5.region= -zc2 & +zp7 & -zp10 & (+zc1 | -zp8)
cell5.fill=steel

#Around the ring inside the core, fill it  with fuel
cell6=openmc.Cell()
cell6.region= -zc1 & +zc11 & +zp8 & -zp201
cell6.fill=fuel

#Around the top of  ring inside the core, fill it  with vacuum
cell7=openmc.Cell()
cell7.region=-zc1 & +zc11 & -zp10 & +zp201




#put lattice in  the ring area
cell1=openmc.Cell()
cell1.region=-zc11 & +zp8 & -zp10
cell1.fill=lattice


##root-geometry
root=openmc.Universe(cells=(cell2,cell3,cell4,cell5,cell6,cell7,cell1))
geom=openmc.Geometry(root)
geom.export_to_xml()


src = openmc.Source()
src.space=openmc.stats.Point((0,0,13.1))
src.energy=openmc.stats.Discrete([14.0e6],[1.0])
src.space = openmc.stats.Box((-5, -5, 0), (5, 5, 11.8))
settings = openmc.Settings()
settings.source = src
settings.batches = 500
settings.inactive = 20
settings.particles = 1000
settings.output={'tallies':False}
settings.export_to_xml()


plot=openmc.Plot()
plot.origin=[0,0,1.6]
plot.width=[150,150]
plot.pixels=[3000,3000]
plot.color_by='material'
plot.basis='yz'
plot.colors={clad:'brown'}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()

openmc.run()





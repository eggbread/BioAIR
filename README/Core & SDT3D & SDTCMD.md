# Core & SDT3D & SDTCMD

This document is manual for Core, sdt3d and sdtcmd.

Environment
> Core - 6.3.0
> Std3d - 2.2

# Connect core with sdt3d

1. Start the core session

![1](assets/1.png)



2.   View -> 3D GUI

# ![2](assets/2.png)



3. Run the python core script 

   

4. File -> Listen to TCP port

![3](assets/3.png)



5. Input 50000 for the port number

![5](assets/4.png)



6. You can see the nodes connected from core

![6](assets/5.png)


**video instruction**
 * [Quick Tutorial Video - simulation on CORE&SDT3D](https://youtu.be/QXDRzjHuMwo)


# Control the sdt3d, using sdtcmd

Using sdtcmd,

We can control/draw nodes, lines, shapes on sdt3d.

## Draw line 

`sdtcmd link [nodeNumber1],[nodeNumber2],[Color]`

![7](assets/7.png)

ex - `/stdcmd link 1,3,green`

## Change label color

`sdtcmd node [nodeNumber] label [Color]`

![9](assets/9.png)

ex - `/stdcmd node 3 label green`

## Change label name

`sdtcmd node [nodeNumber] label on [Name]`

![10](assets/10.png)

ex - `/stdcmd node 3 label on free`

## Draw symbol

`sdtcmd node [nodeNumber] symbol [Symboltype],[Color]`

![11](assets/11.png)

ex - `/stdcmd node 3 symbol sphere,green`

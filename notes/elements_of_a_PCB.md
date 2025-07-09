# Elements of a PCB /Glossary of terms

##  PCB base material

PCB standard substrate is **FR4** fiber glass. 1.6mm is std width. 

fiberglass epoxy composite, FR means flame retardant

most common, multilayer

Other materials:

- CEM-1, FR-1, FR-2: paper based, cheaper less durable and lower TG, 1 layer
- CEM-3: cheaper but less durable, 1-2 layers
- Polyimide: high TG, flexible
- PTFE (Teflon): RF, microwave, radar, 5G good for HF, very low dielectric loss
- Aluminium or Copper: rigid, thermal conductivity: high power

| Material      | Resin Type          | Tg (°C)     | Layer Support    | Use Cases                                   |
| ------------- | ------------------- | ----------- | ---------------- | ------------------------------------------- |
| FR-4          | Epoxy               | 130–180     | 1–Multilayer     | General electronics, industrial, automotive |
| CEM-1 / CEM-3 | Epoxy (paper/glass) | 110–130     | 1–2 layers       | Low-cost consumer products                  |
| FR-1 / FR-2   | Phenolic (PF)       | ~105        | 1 layer only     | Toys, clocks, basic gadgets                 |
| Polyimide     | Polyimide           | >200        | Flexible & rigid | Aerospace, flex PCBs, high-temp apps        |
| PTFE (Teflon) | PTFE                | 160–280     | Multilayer       | RF/microwave, satellite, 5G systems         |
| Flex (PI/PET) | Polyimide or PET    | >200 / <100 | Flexible         | Wearables, foldables, cameras               |
| MCPCB         | Varies (Al/Cu core) | High        | 1–2 layers       | LEDs, power supplies, thermal management    |

## Copper layers

* you may have only 2 **copper layers** or can have more layers of copper inside the pcb

## Traces or tracks

Connect the pads

made of copper 

we can control width, height, and route

Take the color of the solder mask

## copper fill

large areas of copper typically connected to grounds, protect from EMI. Connected to ground via **thermal reliefs** (short tracks that connect pad to copper fill) 

## Keep-out areas

can be marked on one or all layers or faces. E.g. to prevent interferance with an antenna, provide user access, install a screen etc

## Pads and holes 

Used to attach components

2 types: 

* **TH through hole pads** connect electrically front and back. Popular for hobbyists (components are easier to manipulate)

* **SMD surface mounted pads** exist on a single layer. Most common in industry, allow smaller components installed automatically > cheaper. Smallest components are so small they are manufactured with robots

usually round, can be rectangular or oval

normally plated, NPTH holes are not so common

![](.\assets\pads.png)

## Vias

holes that interconnect layers

inside surface typically plated with copper. They are smaller so component pins don't fit and have no pad so you cannot solder components

can be through, blind, or buried. micro vias are made with laser.

![](.\assets\vias.png)

## Annular ring

width is the minimum distance between hole edge and pad edge. If drill is not centered there can be a tangency or even a breakout

## Solder mask

 prevents oxidation of copper, 

masking chemical, thin layer of polymer to prevent oxidation of copper

Also makes it easier to solder components by hand, protects from solder bridges /shorts (to some extent) between pads

gives color (typically green)

## Silkscreen

adds markings, lines and texts. 

useful information for assembly or end user but also Decoration/style

typically white

## Drill bit and drill hit

drill bits typically .3, .6, 1.2mm guided by CNC 

For very small holes (e.g. micro vias) made with laser

drill hit: location where the drill contacts the PCB and makes a hole

## Surface mounted devices

allow manufacturing cheaper smaller PCBs (automatic assy)

## Gold fingers

gold plated connectors at the edge of a PCB 

Allow connecting a PCB to a slot

## Panel

PCBs are manufactured in large panels 

then populated with Pick and Place machine

then cut, leaving break away points

## Solder past and paste stencil

![](.\assets\solder_paste.png)

At large scale the paste is applied with a stainless steel stencil

Can buy reflow ovens to install smd components at home

## Pick and place machine


# PCB Design Process

Goal: creating the plans for a printed circuit design (PCB) which should be functional, manufacturable, beautiful

need to know capabilities of your PCB manufacturer

need to understand design process and tools

procedural and iterative

Kicad is a suite of apps. Workflow:

* [Step 1 Schematic Design](./schematic_design_workflow.md) in **eeschema** capture info about the electrical circuit
* [Step 2 Layout design](./laout_design_workflow.md) in **pbcnew**. physical implementation (there may be many for a given circuit). Output: geometry, features, etc
* [Step 3 Manufacture](manufacturing_PCBs.md) - export layout design and manufacture

## Schematic Design

in **eeschema** (schematic editor) create electrical schematics, describes the circuit selecting symbols from a library. You can also download symbols or create them in the schematic library editor

**Schematic symbols**:  

American Std IEEE (or _US in KiCAD libraries) vs European IEC : Commit to one std!

This seems a good resource: https://www.raypcb.com/electronic-circuit-symbols/

See also: [IEEE standard (PDF)](./assets/ansii_graphic_symbols_for_electrical_and_electronics_diagrams_1993.pdf)

Symbol in schematic represents the function of a component, not physical appearance or final location in the PCB

Running regular **electrical rules checks** helps avoid mistakes early. There's a built in checker 

Need to **associate symbols with layout footprints**. Often the association is already made but often you need to do it

## Layout design

After schematic and footprint associations we start layout design in the editor **pcbnew**: position the footprints on the sheet and connect them using wires, add an outline of the PCB, mounting holes, logos, text, etc

**pcbnew** also has a design rules checker e.g. overlapping footprints, minimum distances etc

footprint is graphical depiction of a real component in the layout: size and location. 

e.g. a resistor has a symbol but can be implemented with a TH or SMD component of different sizes.

export in format compatible with manufacturing. Gerber files: one per layer, contain instructions, exported from Kicad

## Design Workflow

Two 7-step workflows. In reality not linear but iterative.

![](.\assets\PCB_design_workflow.png)

Go to [Schematic Design Workflow](./schematic_design_workflow.md)

Go to [Layout Design Workflow](layout_design_workflow.md)

Go to [Manufacturing](./manufacturing_PCBs.md)
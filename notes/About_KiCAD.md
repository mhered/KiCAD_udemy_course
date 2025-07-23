# Why KiCAD?

- best PCB software 

- free

- unlimited

- active opensource community

- compatible with component libraries: Ultra Librarian, SnapEDA, and KiCad, Octopart

- advanced features e.g. autorouter, python extensions

- continuous improvement, predictable release cycle

- workflow: schematic design separated from layout design

- can manufacture anywhere: exports std gerber files and many take native files

- windows, linux, etc

- configurable: hot keys, python API

- SPICE simulator integrated to simulate

# Sources

Explore the web [Made with KiCAD](https://www.kicad.org/made-with-kicad/)

Explore Demos folder: official Kicad repo: https://gitlab.com/kicad in [Kicad source code > kicad > demos folder](https://gitlab.com/kicad/code/kicad/-/tree/master/demos?ref_type=heads) 

Note: demos folder usually already copied locally during installation: in [Windows]( C:\Users\meheredia\AppData\Local\Programs\KiCad\9.0\share\kicad\demos)  / in [Linux](). 

An example project: [pic_programmer.kicad](https://gitlab.com/kicad/code/kicad/-/tree/master/demos/pic_programmer?ref_type=heads)

# Overview of KiCAD 

KiCAD is a collection of apps

![](.\assets\Kicad_home.png)

## File 

### Open a demo project

**File** > **Open Demo Project...**

3 files (text files, human readable, can be inspected with the text editor)

`*.kicad_pro` -> project

`*.kicad_pcb` -> layout info

`*.kicad_ kicad_sch` -> schematic info

Can open each file individually, better to open the project as a whole opening the `*.kicad_pro` file or drag and drop

with the project open, launch schematic editor with the button or double clicking on the `*.kicad_sch` file

### Create a new project from scratch

**File** > **New Project** select location, give it a name, click on create a new project folder

Automatically creates stubs for: 

`*.kicad_pro` -> project

`*.kicad_pcb` -> layout info

`*.kicad_ kicad_sch` -> schematic info

### Create a new project from a template

**File** > **New Project from Template**

Creates a project already prepopulated with certain things

There are Raspberry Pi HAT templates!

Can also make your own templates >

### Other

Archive/Unarchive to bundle on a ZIP file

Can also import projects from other apps

## View

Text Editor -> everything is a text file. Can also right click 

## Tools

can open apps from project manager or from this menu

## Preferences

Common settings and preferences for different apps are together

**Preferences** > **Configure Paths**

2+1 important paths: symbols, footprints and 3dmodels

Also templates and custom templates folders 

you can alter defaults changing the environment variables, because they take a lot of space specially the 3d models. May want to put them on an external USB HD

Symbols libraries, Footprint libraries etc apparently you can define a project path via environment variables

## About KiCAD

Copy version information to repost issues



# Tour of the Apps

## Schematic Editor

Controls: 

* mouse wheel to zoom
* centre button pressed to pan
* double-click on symbol to bring its properties, association with a footprint, unique ID etc
  can check/uncheck features eg to disable footprint values

### Left toolbar

[(View left toolbar)](./assets/left_toolbar.png)

Grid on/off, Grid overrides, units, cursor crosshairs, toggle invisible pins, select line mode (free, 90degrees, 45 degrees), auto annotation. Most options also accesible through **Menu** > **Preferences** > **Preferences...** > **Schematic Editor** > **Display Options**

Also in **Preferences** > **Schematic Editor** > **Field Name Template** can create custom names for components can be made visible or not

Can have nested schematics sheets > **Hierarchy Navigator** to see sheets. 

**Properties manager** shows properties without double clicking on components

### Top toolbar 

[(View top toolbar)](./assets/top_toolbar.png)

Actions in top toolbar can also be accessed through the menus

**Save**

**Schematic setup** > advanced settings such as field name tamplates, elecrical rules. 

**Page settings** > to configure drawing sheet

**Print**, or **Plot** to export drawings to a file

Paste, Undo / Redo

**Find** and **Replace** text

**Refresh** if corrupt (no longer useful since KiCAD 6) or **Zoom**

**Navigate** between sheet hierarchy or history

**Rotate** and **Flip** 

**Symbol Editor**

**Symbol Browser**

**Footprint Editor** > create footprints 

**Symbol Annotator** > annotate automatically

**Electrical Rules Checker** > errors are more critical than warnings. Can be customized via the Schematic Setup.

**Footprint assignment** > associate footprints to symbols

**Edit Symbol Fields** > allows bulk editing tool in spreadsheet. Can add custom fields, click visible to show in the schematic design

**BOM** > generate BOM

**PCB editor** > can go to PCB editor from main window or from green button in schematics editor window

**Kipython** ?

### Right toolbar 

[(View right toolbar)](./assets/right_toolbar.png)

**Selector**

**Highlight nets**: highlights wires in the same net, green lines or named labels

**Symbol Chooser** (`a`): select and drop symbol

**Power Symbol chooser** (`p`): narrows to power symbols

**Draw Wires** (`w`)

**Draw Buses** (`b`) > and **Entry/Exit Points** (`z`)

**No connect** (`q`) > flag unconnected pins

**Junctions** (`j`) >

Labels: **Net labels** (name a net of all pins connected to avoid too many wires, in same sheet), **Directive Labels**, **Global Labels** (accessible across sheets avoid if possible), **Hierarchical Labels** (preferred between sheets) 

**Hierarchical sheets** > allows creating nested sheets, can expose pins to other sheets

Other graphic tools (e.g. **Insert graphic** from **Menu** > **Place** or  **Interactive delete**  from **Menu** > **Edit** )

### Finding symbols

`a` or click on **Add Symbol** on right panel

Alternatively: Symbol Library Brower button in top panel or is more extensive

There are many libraries in the default installation

Path for symbol libraries: **Preferences** > **Manage Symbol Libraries** > you may have **Global** and **Project Specific** Libraries, may add libraries downloaded from internet in `.lib` format with the folder icon 

If a symbol is missing you may want to:

1. add 3rd party libraries, or
2. create the symbol yourself

### Adding 3rd party libraries

may google kicad symbol for...

dedicated services: kicad publishes in github there are frequent updates

`.lib` contains the symbol itself

`.dcm` contain symbol metadata

 `.kicad_mod` contain the footprint

[Ultra Librarian](https://www.ultralibrarian.com/)

[Octopart](https://octopart.com/en)

[Snapeda](https://www.snapeda.com/)

[DigiKey](https://www.digikey.es/en/resources/design-tools/kicad) and [SparkFun](https://github.com/sparkfun/SparkFun-KiCad-Libraries) also have KiCAD libraries in github that can be imported as a whole not one by one

### Creating custom symbols

elements of a symbol:

* rectangle solid color
* pins placed with a certain logic: VCC top, GND bottom other pins to the sides grouped by functions e.g. not mixing inputs and outputs
* pins have number, name, and maybe a symbol
* designator (U for integrated circuits iaw IEEE 219 75)
* name
* in properties: footprint, datasheet, maybe custom fields 

start with a datasheet

## PCB editor

On right appearance pane

on left properties manager

there are preset views, selection filters to help with targeting

There is a 3D viewer

If I click on a component on one editor the other editor moves to the same component

3d viewer -> specially useful to check access for user interface elements e.g. connectors

## Symbol editor

allows to edit and save symbols or create them from scratch

## Footprint editor

to save or edit footprints 

left pane gives you access to the library

has also a **footprint wizard** that uses a generator

## Gerber viewer

allows inspecting the PCB before uploading for manufacturign

Its a Q control tool

## Image converter

allows taking a bitmap and convert it into a footprint to decorate the PCB

## Calculator tools

e.g. track width  go to recipe part

## Drawing sheet editor

to edit the drawings

also dedicated lecture

## Plugin manager




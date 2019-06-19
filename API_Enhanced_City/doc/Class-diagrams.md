# Visual Paradigm

The class diagrams in API Extended Document were made using [Visual Paradigm](https://visual-paradigm.com/). 
This is a paid software, however you can have a free-trial for 30 days.

You have to know, when exporting diagrams, because it is a free trial, some parasitic text appears:

![](img/class-diagrams/Visual_Paradigm_Parasite.png)

For removing them, we export diagrams in an SVG format, it allows us to modify the diagram very easily.
To remove parasites, open the SVG file with a text editor (Atom, etc.). Go to the bottom of the file, and remove everything similar to what is underlined in this [image](img/class-diagrams/Visual_Paradigm_Parasite_Remove.png).

You have then a clean SVG file, if you want to be able to visualize it on github you need to convert the SVG to a new png file. It can be done using an svg to png converter, many are available on the Internet.

We then get this:

![](img/class-diagrams/ORM_Example.png)
### IR JSON Maker
Create config files for JSON IR remote. The configs for individual remotes are stored in IR_Remotes.xlsx.

You can set up a remote with very little configuring by choosing labels that are either [named css colors](https://www.w3schools.com/cssref/css_colors.asp)
or one that has a default command like `on`, `off`, `play`, `effect+`, `palette+`,`speed+`, `bright+`, `diy1`, etc.
See the full list of labels with default commands in `def_commands` at the top of ir_json_maker.py. 
Labels are lower cased and stripped of spaces before matched so `Dark Magenta` or `Timer 60` are valid labels.

### GIF visualizer
Generate animated GIFs for effects and palettes and markdown files to display them. 

Actual animation is done on a WLED device and captured from /json/live. You must set the IP address of your device before running.

* [Effects](effects.md)
* [Palettes](palettes.md)

### Preset Maker
Pick your favorite palettes and effects then generate presets.json by combining your favorites. Work in progress.

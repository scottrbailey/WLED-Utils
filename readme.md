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
* [Sound Reactive Effects](effects_sr.md)

### GIF visualizer 14
Overhaul of GIF visualizer for WLED 0.14. The addition of 2D matrix, effect meta data, and a much larger
liveview array (over websockets) allows for a much better visualization. 

For rendering 1D effects, the connected node must be in 1D configuration and the number of LEDs configured
should be 100. If you have more LEDs configured, even if they are not active on a segment, it will reduce
the number of pixels lit in liveview.

For rendering 2D effects, it is currently configured for a 24x24 matrix. If you want a larger or smaller matrix
adjust the visualizer.led_size. 

### Preset Maker
Pick your favorite palettes and effects then generate presets.json by combining your favorites. Work in progress.

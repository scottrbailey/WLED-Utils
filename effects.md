### Effects

To aid in showing where colors vs palettes are used, all effects are rendered with the 
_Party_ palette ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/PAL_06.gif) 
and the colors: <br />
![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_1.gif) primary _Fx_<br />
![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_2.gif) secondary _Bg_<br />
![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_3.gif) tertiary _Cs.<br />
For 2D effects the background (secondary) color is set to black.

| ID | Effect | Description | Flags | Colors | Parms
| ---: | --- | --- | --- | --- | --- 
| 0 | Solid | Solid primary color on all LEDs <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_000.gif) |  ⋮ |  | 
| 1 | Blink | Blinks between primary and secondary color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_001.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Duty cycle
| 2 | Breathe | Fades between primary and secondary color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_002.gif) |  ⋮ | 🎨 Fx, Bg | Speed
| 3 | Wipe | Switches between primary and secondary, switching LEDs one by one, start to end <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_003.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 4 | Wipe Random | Same as Wipe, but uses random colors <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_004.gif) |  ⋮ | 🎨  | Speed
| 5 | Random Colors | Applies a new random color to all LEDs <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_005.gif) |  ⋮ | 🎨  | Speed, Fade time
| 6 | Sweep | Switches between primary and secondary, switching LEDs one by one, start to end to start <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_006.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 7 | Dynamic | Sets each LED to a random color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_007.gif) |  ⋮ | 🎨  | Speed, Intensity, Smooth
| 8 | Colorloop | Cycle all LEDs through the rainbow colors <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_008.gif) |  ⋮ | 🎨  | Speed, Saturation
| 9 | Rainbow | Displays rainbow colors along the whole strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_009.gif) |  ⋮ | 🎨  | Speed, Size
| 10 | Scan | A single primary colored light wanders between start and end <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_010.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, # of dots, Overlay
| 11 | Scan Dual | Same as Scan but uses two lights starting at both ends <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_011.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, # of dots, Overlay
| 12 | Fade | Fades smoothly between primary and secondary color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_012.gif) |  ⋮ | 🎨 Fx, Bg | Speed
| 13 | Theater | Pattern of one lit and two unlit LEDs running <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_013.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Gap size
| 14 | Theater Rainbow | Same as Theater but uses colors of the rainbow <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_014.gif) |  ⋮ | 🎨 Bg | Speed, Gap size
| 15 | Running | Sine Waves scrolling <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_015.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Wave width
| 16 | Saw | Sawtooth Waves scrolling <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_016.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Width
| 17 | Twinkle | Random LEDs light up in the primary color with secondary as background <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_017.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 18 | Dissolve | Fills LEDs with primary in random order, then off again <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_018.gif) |  ⋮ | 🎨 Fx, Bg | Repeat speed, Dissolve speed, Random
| 19 | Dissolve Rnd | Fills LEDs with random colors in random order, then off again <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_019.gif) |  ⋮ | 🎨 Bg | Repeat speed, Dissolve speed
| 20 | Sparkle | Single random LEDs light up in the primary color for a short time, secondary is background <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_020.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Overlay
| 21 | Sparkle Dark | All LEDs are lit in the primary color, single random LEDs turn off for a short time <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_021.gif) |  ⋮ | 🎨 Bg, Fx | Speed, Intensity, Overlay
| 22 | Sparkle+ | All LEDs are lit in the primary color, multiple random LEDs turn off for a short time <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_022.gif) |  ⋮ | 🎨 Bg, Fx | Speed, Intensity, Overlay
| 23 | Strobe | All LEDs are lit in the secondary color, all LEDs flash in a single short burst in primary color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_023.gif) |  ⋮ | 🎨 Fx, Bg | Speed
| 24 | Strobe Rainbow | Same as strobe, cycles through the rainbow <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_024.gif) |  ⋮ | 🎨 Bg | Speed
| 25 | Strobe Mega | All LEDs are lit in the secondary color, all LEDs flash in several short bursts in primary color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_025.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 26 | Blink Rainbow | Same as blink, cycles through the rainbow <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_026.gif) |  ⋮ | 🎨 Fx, Bg | Frequency, Blink duration
| 27 | Android | Section of varying length running <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_027.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Width
| 28 | Chase | 2 LEDs in primary color running on secondary <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_028.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, Width
| 29 | Chase Random | Like Chase but leaves trail of random color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_029.gif) |  ⋮ | 🎨 Fx, Cs | Speed, Width
| 30 | Chase Rainbow | Like 28 but leaves trail of rainbow <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_030.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Width
| 31 | Chase Flash | 2 LEDs flash in secondary color while the rest is lit in primary. The flashing LEDs wander from start to end <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_031.gif) |  ⋮ | 🎨 Bg, Fx | Speed
| 32 | Chase Flash Rnd | Like Chase Flash, but the 2 LEDs flash in random colors and leaves a random color behind <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_032.gif) |  ⋮ | 🎨 Fx, Bg | Speed
| 33 | Rainbow Runner | Like Chase, but the 2 LEDs light up in rainbow colors and leave a primary color trail <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_033.gif) |  ⋮ | 🎨 Bg | Speed, Size
| 34 | Colorful | Shifting Red-Amber-Green-Blue pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_034.gif) |  ⋮ | 🎨 1, 2, 3 | Speed, Saturation
| 35 | Traffic Light | Emulates a traffic light <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_035.gif) |  ⋮ | 🎨 Bg | Speed, US style
| 36 | Sweep Random | Like Sweep, but uses random colors <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_036.gif) |  ⋮ | 🎨  | Speed
| 37 | Chase 2 | Pattern of n LEDs primary and n LEDs secondary moves along the strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_037.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Width
| 38 | Aurora | Simulation of the Aurora Borealis <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_038.gif) |  ⋮ | 🎨 1, 2, 3 | Speed, Intensity
| 39 | Stream | Flush bands random hues along the string <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_039.gif) |  ⋮ | 🎨  | Speed, Zone size
| 40 | Scanner | Dot moves between ends, leaving behind a fading trail <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_040.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Fade rate
| 41 | Lighthouse | Dot moves from start to end, leaving behind a fading trail <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_041.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Fade rate
| 42 | Fireworks | Random color blobs light up, then fade again <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_042.gif) |  ⋮ ▦ | 🎨 Fx, Bg | Frequency
| 43 | Rain | Like Fireworks, but the blobs move <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_043.gif) |  ⋮ ▦ | 🎨 Fx, Bg | Speed, Spawning rate
| 44 | Tetrix | Falling blocks stack <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_044.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Width, One color
| 45 | Fire Flicker | LEDs randomly flickering <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_045.gif) |  ⋮ | 🎨 Fx | Speed, Intensity
| 46 | Gradient | Moves a saturation gradient of the primary color along the strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_046.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Spread
| 47 | Loading | Moves a sawtooth pattern along the strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_047.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Fade
| 49 | Fairy | Inspired by twinkle style Christmas lights. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_049.gif) |  ⋮ | 🎨 Fx, Bg | Speed, # of flashers
| 50 | Two Dots | Two areas sweeping <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_050.gif) |  ⋮ | 🎨 1, 2, Bg | Speed, Dot size, Overlay
| 51 | Fairytwinkle | Like Colortwinkle, but starting from all lit <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_051.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 52 | Running Dual | Sine waves in both directions <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_052.gif) |  ⋮ | 🎨 L, Bg, R | Speed, Wave width
| 54 | Chase 3 | Like Chase, but with 3 colors <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_054.gif) |  ⋮ | 🎨 1, 2, 3 | Speed, Size
| 55 | Tri Wipe | Like Wipe but turns LEDs off as "third color" <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_055.gif) |  ⋮ | 🎨 1, 2, 3 | Speed
| 56 | Tri Fade | Fades the whole strip from primary color to secondary color to off <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_056.gif) |  ⋮ | 🎨 1, 2, 3 | Speed
| 57 | Lightning | Short random white strobe similar to a lightning bolt <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_057.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity, Overlay
| 58 | ICU | Two "eyes" running on opposite sides of the strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_058.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity, Overlay
| 59 | Multi Comet | Like Scanner, but creates multiple trails <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_059.gif) |  ⋮ |  | 
| 60 | Scanner Dual | Like Scanner, but with two dots running on opposite sides <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_060.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, Fade rate
| 61 | Stream 2 | Flush random hues along the string <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_061.gif) |  ⋮ |  | Speed
| 62 | Oscillate | Areas of primary and secondary colors move between opposite ends, combining colors where they touch <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_062.gif) |  ⋮ |  | 
| 63 | Pride 2015 | Rainbow cycling with brightness variation <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_063.gif) |  ⋮ |  | Speed
| 64 | Juggle | Eight colored dots running, leaving trails <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_064.gif) |  ⋮ | 🎨  | Speed, Trail
| 65 | Palette | Running color palette <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_065.gif) |  ⋮ | 🎨  | Cycle speed
| 66 | Fire 2012 | Simulates flickering fire in red and yellow <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_066.gif) |  ⋮ | 🎨  | Cooling, Spark rate, Boost
| 67 | Colorwaves | Like Pride 2015, but uses palettes <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_067.gif) |  ⋮ | 🎨 Fx | Speed, Hue
| 68 | Bpm | Pulses moving back and forth on palette <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_068.gif) |  ⋮ | 🎨 Fx | Speed
| 69 | Fill Noise | Noise pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_069.gif) |  ⋮ | 🎨 Fx | Speed
| 70 | Noise 1 | Fast Noise shift pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_070.gif) |  ⋮ | 🎨 Fx | Speed
| 71 | Noise 2 | Fast Noise shift pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_071.gif) |  ⋮ | 🎨 Fx | Speed
| 72 | Noise 3 | Noise shift pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_072.gif) |  ⋮ | 🎨 Fx | Speed
| 73 | Noise 4 | Noise sparkle pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_073.gif) |  ⋮ | 🎨 Fx | Speed
| 74 | Colortwinkles | LEDs light up randomly in random colors and fade off again <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_074.gif) |  ⋮ | 🎨  | Fade speed, Spawn speed
| 75 | Lake | Calm palette waving <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_075.gif) |  ⋮ | 🎨 Fx | Speed
| 76 | Meteor | The primary color creates a trail of randomly decaying color <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_076.gif) |  ⋮ | 🎨 Fx | Speed, Trail length
| 77 | Meteor Smooth | Smoothly animated meteor <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_077.gif) |  ⋮ | 🎨 Fx | Speed, Trail length
| 78 | Railway | Shows primary and secondary color on alternating LEDs. All LEDs fade to their opposite color and back again <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_078.gif) |  ⋮ | 🎨 1, 2 | Speed, Smoothness
| 79 | Ripple | Effect resembling random water ripples <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_079.gif) |  ⋮ ▦ | 🎨 Bg | Speed, Wave #, Overlay
| 80 | Twinklefox | FastLED gentle twinkling with slow fade in/out <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_080.gif) |  ⋮ | 🎨  | Speed, Twinkle rate
| 81 | Twinklecat | Twinkling with fast in / slow out <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_081.gif) |  ⋮ | 🎨  | Speed, Twinkle rate
| 82 | Halloween Eyes | One Pair of blinking eyes at random intervals along strip <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_082.gif) |  ⋮ ▦ | 🎨 Fx, Bg | Duration, Eye fade time, Overlay
| 83 | Solid Pattern | Speed sets number of LEDs on, intensity sets off <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_083.gif) |  ⋮ | 🎨 Fg, Bg | Fg size, Bg size
| 84 | Solid Pattern Tri | Solid Pattern with three colors <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_084.gif) |  ⋮ | 1, 2, 3 | Size
| 85 | Spots | Solid lights with even distance <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_085.gif) |  ⋮ | 🎨 Fx, Bg | Spread, Width, Overlay
| 86 | Spots Fade | Spots, getting bigger and smaller <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_086.gif) |  ⋮ | 🎨 Fx, Bg | Spread, Width, Overlay
| 87 | Glitter | Rainbow with white sparkles <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_087.gif) |  ⋮ | 🎨 1, 2, Glitter color | Speed, Intensity, Overlay
| 88 | Candle | Flicker resembling a candle flame <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_088.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 89 | Fireworks Starburst | Exploding multicolor fireworks <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_089.gif) |  ⋮ | 🎨 Bg | Chance, Fragments, Overlay
| 90 | Fireworks 1D | one dimension fireworks with flare <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_090.gif) |  ⋮ ▦ | 🎨 Fx, Bg | Gravity, Firing side
| 91 | Bouncing Balls | Bouncing ball effect <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_091.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Gravity, # of balls, Overlay
| 92 | Sinelon | Fastled sinusoidal moving eye <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_092.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, Trail
| 93 | Sinelon Dual | Sinelon from both directions <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_093.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, Trail
| 94 | Sinelon Rainbow | Sinelon in rainbow colours <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_094.gif) |  ⋮ | 🎨 Cs | Speed, Trail
| 95 | Popcorn | popping kernels <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_095.gif) |  ⋮ | 🎨 Fx, Bg, Cs | Speed, Intensity, Overlay
| 96 | Drip | Water dripping effect <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_096.gif) |  ⋮ | 🎨 Fx, Bg | Gravity, # of drips, Overlay
| 97 | Plasma | Plasma lamp <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_097.gif) |  ⋮ | 🎨 Fx | Phase, Intensity
| 98 | Percent | Lights up a percentage of segment <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_098.gif) |  ⋮ | 🎨 Fx, Bg | % of fill, One color
| 99 | Ripple Rainbow | Like ripple, but with a dimly lit changing background <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_099.gif) |  ⋮ ▦ | 🎨  | Speed, Wave #
| 100 | Heartbeat | led strip pulsing rhythm similar to a heart beat <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_100.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 101 | Pacifica | Gentle ocean waves <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_101.gif) |  ⋮ | 🎨  | Speed, Angle
| 102 | Candle Multi | Like candle effect, but each LED has it's own flicker pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_102.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 103 | Solid Glitter | Like Glitter, but with solid color background <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_103.gif) |  ⋮ | Bg, Glitter color | Intensity
| 104 | Sunrise | Simulates a gradual sunrise or sunset. Speed sets: 0 - static sun, 1 - 60: sunrise time in minutes,60 - 120: sunset time in minutes - 60, above: "breathing" rise and set <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_104.gif) |  ⋮ | 🎨  | Time [min], Width
| 105 | Phased | Sine waves (in sourcecode) <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_105.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 106 | Twinkleup | Twinkle effect with fade-in <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_106.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 107 | Noise Pal | Peaceful noise that's slow and with gradually changing palettes <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_107.gif) |  ⋮ | 🎨  | Speed, Scale
| 108 | Sine | Controllable sine waves <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_108.gif) |  ⋮ |  | 
| 109 | Phased Noise | Noisy sine waves <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_109.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Intensity
| 110 | Flow | Blend of palette and spot effects <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_110.gif) |  ⋮ | 🎨  | Speed, Zones
| 111 | Chunchun | Birds flying in a circle formation <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_111.gif) |  ⋮ | 🎨 Fx, Bg | Speed, Gap size
| 112 | Dancing Shadows | Moving spotlights <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_112.gif) |  ⋮ | 🎨 Fx | Speed, # of shadows
| 113 | Washing Machine | Spins, slows, reverses directions <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_113.gif) |  ⋮ | 🎨  | Speed, Intensity
| 115 | Blends | Blends random colors across palette <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_115.gif) |  ⋮ | 🎨  | Shift speed, Blend speed
| 116 | TV Simulator | TV light spill simulation <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_116.gif) |  ⋮ |  | Speed, Intensity
| 117 | Dynamic Smooth | Like Dynamic, but with smooth palette blends <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_117.gif) |  ⋮ | 🎨  | Speed, Intensity
| 118 | Spaceships | Circling ships with fading trails. Homage to 80s spaceship shooter games. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_118.gif) |  ▦ | 🎨  | Speed, Blur
| 119 | Crazy Bees | Bees darting from flower to flower. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_119.gif) |  ▦ |  | Speed, Blur
| 120 | Ghost Rider | Color changing ghost riding a kite... in a tornado. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_120.gif) |  ▦ | 🎨  | Fade rate, Blur
| 121 | Blobs | No really, they are blobs. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_121.gif) |  ▦ | 🎨 Fx | Speed, # blobs, Blur
| 122 | Scrolling Text | Edit segment name to set text (#DATE and #TIME to include those) <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_122.gif) |  ▦ | 🎨 Fx, Bg, Gradient | Speed, Y Offset, Trail, Font size, Gradient, Overlay
| 123 | Drift Rose | Spinning arms that adds and removes nodes as it winds and unwinds. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_123.gif) |  ▦ |  | Fade, Blur
| 124 | Distortion Waves | Distorted sine waves with a psychedelic flair. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_124.gif) |  ▦ |  | Speed, Scale
| 125 | Soap | Like soap bubbles, but lasts longer. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_125.gif) |  ▦ | 🎨  | Speed, Smoothness
| 126 | Octopus | A cephalopod stuck in a whirlpool. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_126.gif) |  ▦ | 🎨  | Speed, Offset X, Offset Y, Legs
| 127 | Waving Cell | If a bunch of eucaryotes went to a sports stadium and did the wave, it would look exactly like this. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_127.gif) |  ▦ | 🎨  | Speed, Amplitude 1, Amplitude 2, Amplitude 3
| 128 | Pixels | Random pixels <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_128.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, # of pixels
| 129 | Pixelwave | Pixels emanating from center <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_129.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Speed, Sensitivity
| 130 | Juggles | Juggling balls. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_130.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Speed, # of balls
| 131 | Matripix | Similar to Matrix. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_131.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Speed, Brightness
| 132 | Gravimeter | Volume reactive vu-meter with gravity and perlin noise. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_132.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Rate of fall, Sensitivity
| 133 | Plasmoid | Sine wave based plasma. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_133.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Phase, # of pixels
| 134 | Puddles | Blast coloured puddles based on volume. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_134.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, Puddle size
| 135 | Midnoise | Perlin noise emanating from center. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_135.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, Max. length
| 136 | Noisemeter | Volume reactive vu-meter. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_136.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, Width
| 137 | Freqwave | Maps the major frequencies from the incoming signal to colors in the HSV color space. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_137.gif) |  ⋮ ♫ |  | Time delay, Sound effect, Low bin, High bin, Pre-amp
| 138 | Freqmatrix | The temporal tail for this animation starts at the beginning of the Segment rather than in the center of the segment. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_138.gif) |  ⋮ ♫ |  | Time delay, Sound effect, Low bin, High bin, Sensivity
| 139 | GEQ | A 16x16 graphic equalizer. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_139.gif) |  ▦ ♫ | 🎨 Fx, Peaks | Fade speed, Ripple decay, # of bands, Color bars
| 140 | Waterfall | A volume AND FFT version of a Waterfall that has 'beat' support. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_140.gif) |  ⋮ ♫ | 🎨 Fx, Bg | Speed, Adjust color, Select bin, Volume (min)
| 141 | Freqpixels | Random pixels coloured by frequency. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_141.gif) |  ⋮ ♫ |  | Fade rate, Starting color and # of pixels
| 143 | Noisefire | A perlin noise based volume reactive fire routine. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_143.gif) |  ⋮ ♪ |  | Speed, Intensity
| 144 | Puddlepeak | Blast coloured puddles randomly up and down the strand with the 'beat'. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_144.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, Puddle size, Select bin, Volume (min)
| 145 | Noisemove | Using perlin noise as movement for different frequency bins. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_145.gif) |  ⋮ ♫ | 🎨 Fx, Bg | Speed of perlin movement, Fade rate
| 146 | Noise2D |  <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_146.gif) |  ▦ | 🎨  | Speed, Scale
| 147 | Perlin Move | Using Perlin Noise for movement. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_147.gif) |  ⋮ | 🎨 Fx, Bg | Speed, # of pixels, Fade rate
| 148 | Ripple Peak | Peak detection triggers ripples. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_148.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Fade rate, Max # of ripples, Select bin, Volume (min)
| 149 | Firenoise | Using Perlin Noise for fire. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_149.gif) |  ▦ | 🎨  | X scale, Y scale
| 150 | Squared Swirl | Boxes moving around <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_150.gif) |  ▦ | 🎨  | Blur
| 152 | DNA | A very cool DNA like pattern. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_152.gif) |  ▦ | 🎨  | Scroll speed, Blur
| 153 | Matrix | The Matrix, on a 2D matrix. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_153.gif) |  ▦ | Spawn, Trail | Speed, Spawning rate, Trail, Custom color
| 154 | Metaballs | A cool plasma type effect. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_154.gif) |  ▦ | 🎨  | Speed
| 155 | Freqmap | Map the loudest frequency throughout the length of the LED's. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_155.gif) |  ⋮ ♫ | 🎨 Fx, Bg | Fade rate, Starting color
| 156 | Gravcenter | Volume reactive vu-meter from center with gravity and perlin noise. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_156.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Rate of fall, Sensitivity
| 157 | Gravcentric | Volume reactive vu-meter from center with gravity. Volume provides index to (time rotating) palette colour. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_157.gif) |  ⋮ ♪ | 🎨 Fx, Bg | Rate of fall, Sensitivity
| 158 | Gravfreq | VU Meter from center. Log of frequency is index to center colour. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_158.gif) |  ⋮ ♫ | 🎨 Fx, Bg | Rate of fall, Sensivity
| 159 | DJ Light | An effect emanating from the center to the edges. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_159.gif) |  ⋮ ♫ |  | Speed
| 160 | Funky Plank | A 2D wall of reactivity running from bottom to top <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_160.gif) |  ▦ ♫ |  | Scroll speed, # of bands
| 162 | Pulser | Travelling waves. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_162.gif) |  ▦ | 🎨  | Speed, Blur
| 163 | Blurz | Flash an fftResult bin per frame and then blur/fade. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_163.gif) |  ⋮ ♫ | 🎨 Fx, Color mix | Fade rate, Blur
| 164 | Drift | A rotating kaleidoscope. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_164.gif) |  ▦ | 🎨  | Rotation speed, Blur amount
| 165 | Waverly | Noise waves with some sound. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_165.gif) |  ▦ ♪ | 🎨  | Amplification, Sensitivity
| 166 | Sun Radiation | The sun! Doesn't support segments. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_166.gif) |  ▦ |  | Variance, Brightness
| 167 | Colored Bursts | Rotating rays of color. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_167.gif) |  ▦ | 🎨  | Speed, # of lines, Blur, Gradient, Dots
| 168 | Julia | Animated Julia set fractal named after mathematician Gaston Julia. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_168.gif) |  ▦ | 🎨 Fx | Max iterations per pixel, X center, Y center, Area size
| 172 | Game Of Life | Scrolling game of life. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_172.gif) |  ▦ | 🎨 Fx, Bg | Speed
| 173 | Tartan | Plaid pattern of horizontal and vertical bands. Makes a great kilt. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_173.gif) |  ▦ | 🎨  | X scale, Y scale, Sharpness
| 174 | Polar Lights | The northern lights. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_174.gif) |  ▦ |  | Speed, Scale
| 175 | Swirl | Several blurred circles. Looks good with pink plasma palette. Supports AGC. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_175.gif) |  ▦ ♪ | 🎨 Bg Swirl | Speed, Sensitivity, Blur
| 176 | Lissajous | A frequency based Lissajous pattern. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_176.gif) |  ▦ | 🎨 Fx | X frequency, Fade rate
| 177 | Frizzles | Moving patterns. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_177.gif) |  ▦ | 🎨  | X frequency, Y frequency, Blur
| 178 | Plasma Ball | A ball of plasma. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_178.gif) |  ▦ | 🎨  | Speed, Fade, Blur
| 179 | Flow Stripe | Strip with rotating colours. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_179.gif) |  ⋮ |  | Hue speed, Effect speed
| 180 | Hiphotic | A moving plasma. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_180.gif) |  ▦ | 🎨 Fx | X scale, Y scale, Speed
| 181 | Sindots | Dots revolving in a circle while the 'camera'  <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_181.gif) |  ▦ | 🎨  | Speed, Dot distance, Fade rate, Blur
| 182 | DNA Spiral | Spiraling DNA pattern <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_182.gif) |  ▦ | 🎨  | Scroll speed, Y frequency
| 183 | Black Hole | Colorful dots orbiting a white black hole. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_183.gif) |  ▦ |  | Fade rate, Outer Y freq., Outer X freq., Inner X freq., Inner Y freq.
| 184 | Wavesins | Beat waves and phase shifting. Looks OK in 2D'ish as well. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_184.gif) |  ⋮ | 🎨 Fx | Speed, Brightness variation, Starting color, Range of colors, Color variation
| 185 | Rocktaves | Colours the same for each note between octaves, with sine wave going back and forth. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_185.gif) |  ⋮ ♫ | 🎨 Fx, Bg | 
| 186 | Akemi | The WLED mascot rocking to your tunes. <br /> ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_186.gif) |  ▦ ♫ | Head palette, Arms & Legs, Eyes & Mouth | Color speed, Dance

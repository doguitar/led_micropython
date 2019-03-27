# MicroPython MQTT LED Controller

# Installation

Create a config.json for your controller/mqtt/wifi following the pattern in config.json.example.

Upload boot.py, main.py and config.json to your controller.

If successful, all LEDs will be lit sequentially to test.                     

## Getting Started

Your controller will check the topic specified in the config for a json formatted string which specifies the pattern of the LEDs.

The json can have 3 top level keys, `steps`, `repeat` and `fps`. 

`steps` defines the steps in the pattern. It is an array of individual steps that are executed sequentially. Each step is an array specifying what to do with each LED. 

The format for an individual LED is an array containing two arrays. The first array must contain at least one element, the first element, if greater than zero, will be used as a one based index of the LEDS. The Second array will be the RGB values for that LED from 0-255.

For example, `[[1], [255,255,255]]` will turn the first LED white. `[[1], [0,0,0]]` will turn the first LED black again. LEDs will not be reset between steps and will remain the color specified previously.

There is special handling for LED positions below 1 detailed here.

`repeat` determines whether the pattern repeats after it's complete, defaults to false

`fps`, frames per second, determines the speed of the pattern. depending on how many LEDS,  how complicated the pattern is and the speed of your controller, there will be a cap on how fast the LEDS can be changed.

## Special Handling

An LED position of `0` specifies all LEDS

An LED position of `-1` specifies a modulo and an offset. The modulo and offset must be set in the LED position array as the next two integers. For Example, `[-1, 2, 0]` would specifiy every other LED. You can specify the opposite LEDs by offsetting the pattern by 1, `[-1, 2, 1]`. With this, you can create simple, alternating patterns. 

For example, 
``` 
{
  "steps" : [
    [
      [[-1, 2, 0], [255, 0, 0]],
      [[-1, 2, 1], [0, 255, 0]]    
    ],
    [
      [[-1, 2, 1], [255, 0, 0]],
      [[-1, 2, 0], [0, 255, 0]]    
    ]
  ],
  "repeat" : true,
  "fps": 2
}
```

will alternate red/green leds twice per second.

# Examples

### Alternating Red, Green
``` 
{
  "steps" : [
    [
      [[-1, 2, 0], [255, 0, 0]],
      [[-1, 2, 1], [0, 255, 0]]    
    ],
    [
      [[-1, 2, 1], [255, 0, 0]],
      [[-1, 2, 0], [0, 255, 0]]    
    ]
  ],
  "repeat" : true,
  "fps": 2
}
```

### Alternating Red, Green two Black Leds between
```
{
  "steps" : [
    [
      [[-1, 4, 1], [255, 0, 0]],
      [[-1, 4, 2], [0, 255, 0]],
      [[-1, 4, 3], [0, 0, 0]],
      [[-1, 4, 4], [0, 0, 0]]    
    ],
    [
      [[-1, 4, 1], [0, 0, 0]],
      [[-1, 4, 2], [0, 0, 0]],
      [[-1, 4, 3], [255, 0, 0]],
      [[-1, 4, 4], [0, 255, 0]]    
    ]
  ],
  "repeat" : true,
  "fps": 2
}
```
### Alternating Yellow, Turquoise, Purple
```
{
  "steps" : [
    [
      [[-1, 3, 0], [0, 10, 10]],
      [[-1, 3, 1], [10, 0, 10]],
      [[-1, 3, 2], [10, 10, 0]]
    ],
    [
      [[-1, 3, 1], [0, 10, 10]],
      [[-1, 3, 2], [10, 0, 10]],
      [[-1, 3, 0], [10, 10, 0]]
    ],
    [
      [[-1, 3, 2], [0, 10, 10]],
      [[-1, 3, 0], [10, 0, 10]],
      [[-1, 3, 1], [10, 10, 0]]
    ]
  ],
  "repeat" : true,
  "fps": 2
}
```
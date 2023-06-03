### Flip Dot Maestro Server

##### Quick Start
* Download pyflipdots.exe, pyflipdot_config.yaml, blur.ico and place in a new directory
* Edit pyflipdot_config.yaml with your particular usecase & requirements
* Run pyflipdots.exe - your panel should appear, at the defined size in your yaml config file
* The server listens on the defined IP address & port as defined in your yaml config file (default 0.0.0.0, port 44000)

<p>The server is now ready to be connected to by a Maestro flipdots 'FlipApp' (client).  After UID is implemented, it will be a requirement 
(as stated in the Maestro Protocol Specification) that the FlipApp submits a UID opcode prior to attempting to use the emulated panel.
</p>
<p>Sample Configuration</p>

```yaml
panel:
    resolution:
        height: 52    # panel's total number of 'dots' high
        width: 48     # panel's total number of 'dots' wide
    background_color: "black"  # panel's background colour
    
    pixels:
        height: 10    # single dot width
        width: 10     # single dot height
        on_colour: "#00ff1a" # colour of 'ON' dot
        off_colour: "#0f0f0f" # colour of 'OFF" dot
        outline_colour: "#212423" # colour of dot outline (outer circle)
    
    spacing:
        x: 2  # spacing units between dots horizontally
        y: 2  # spacing units between dots vertically

maestro:
    uid: 99  # emulated Maestro panel UID
    server:
        ip: 0.0.0.0  # IP address to listen on
        port: 44000  # Port to listen on
```

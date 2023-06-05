
##### Text Rendering

<b>note:  these examples will work on actual Maestro flipdots driver AFTER the send UID is implemented.  I will be working on this next.</b> 

##### Files

<ul>
  <li><b>simple_text.py</b> The example FlipApp</li>
  <li><b>dotFont.py</b> The font loading & handling class</li>
  <li><b>dots_all_for_now.yaml</b> An example font file - (A-Z, 0-9, some special characters)</li>
 </ul>

<p>
  Font class now allows for completely dynamic glyph sizes - charwidth and charheight is determined individually by character based
  on the bitmap byte array for that particular glyph.  So we no longer need to define an overall char width/height for a font, as each
  individual glyph can now be of its own individual size (width AND height).
</p>

<p>
 You can create your own font files by making a copy of dots_all_for_now.yaml and editing the contents.  You can also add more characters to the existing font file by adding more bitmap arrays within the bitmaps: section of the font file.  
</p>

![FontDemo2](/Docs/images/font_demo_2.png)

##### Also demonstrated:  Frame Buffering

![FrameBufferDemo](/Docs/images/frame_buffer_demo.png)

```python
# load test font
test_font = dotFont("dots_all_for_now")

# clear the screen
clear_screen()

# create new empty frame
test_frame = new_frame()

# add characters to frame
add_character_to_frame(test_frame, 3, 3, test_font, "A")
add_character_to_frame(test_frame, 10, 10, test_font, "B")

# draw frame
draw_frame(bytes(test_frame))

time.sleep(3)

add_character_to_frame(test_frame, 20, 20, test_font, "C")
add_character_to_frame(test_frame, 30, 30, test_font, "A")

draw_frame(bytes(test_frame))
```


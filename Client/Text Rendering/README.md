
##### Text Rendering

<b>note:  these examples will work on actual Maestro flipdots driver AFTER the send UID is implemented.  I will be working on this next.</b> 

##### Files

<ul>
  <li><b>simple_text.py</b> The example FlipApp</li>
  <li><b>dotFont.py</b> The font loading & handling class</li>
  <li><b>dots_all_for_now.yaml</b> An example font file - only 3 characters included A,B & C</li>
 </ul>


<p>
 You can create your own font files by making a copy of dots_all_for_now.yaml and editing the contents.  You can also add more characters to the existing font file by adding more bitmap arrays within the bitmaps: section of the font file.  
</p>

![SimpleTextDemo](/Docs/images/simple_text_demo.png)

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


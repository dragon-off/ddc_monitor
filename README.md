# ddc_monitor
Управления монитора по i2c DDC

Restore Factory Defaults 0x04 set >0
Restore Factory Luminance/ Contrast Defaults 0x05 set >0
Restore Factory Color Defaults 0x08 set >0
Luminance 0x10 set 0-100
Contrast 0x12 set 0-100
Power Mode 0xD6 set 0x01-on,0x05-off
Input Source 0x60 set 0x01-D-sub; 0x03-DVI; 0x11-HDMI
Audio: Speaker Volume 0x62 set >0
Audio Mute 0x8D set 0x01-on, 0x02-off

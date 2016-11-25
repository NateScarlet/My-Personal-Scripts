import nuke
def nodePresetsStartup():
  nuke.setUserPreset("AddChannels", "depth", {'channels': 'depth', 'color': '1', 'selected': 'true'})
  nuke.setUserPreset("ChannelMerge", "depth.z", {'A': 'depth.Z', 'output': 'depth.Z', 'operation': 'min', 'B': 'depth.Z', 'selected': 'true'})
  nuke.setUserPreset("ColorCorrect", "ShadowWarm", {'shadows.gamma': '0.86', 'shadows.gain': '7.575611115 2.787825584 1.515122175 1', 'selected': 'true', 'lookup': 'shadow {curve 1 s0 x0.01183120441 0 s0}\nmidtone {1-shadow-highlight}\nhighlight {curve x0.06572888792 0 s0 x0.1314577758 1 s0}', 'offset': '0.004999999888 0.002457999857 0.001899999916 0.004999999888'})
  nuke.setUserPreset("Copy", "depth.Z", {'to0': 'depth.Z', 'selected': 'true', 'from0': 'depth.Z'})
  nuke.setUserPreset("Crop", "root.format", {'box': '0 0 {root.format.w} {root.format.h}', 'indicators': '2', 'reformat': 'true', 'selected': 'true', 'crop': 'false'})
  nuke.setUserPreset("Dilate", "Depth", {'channels': 'depth', 'selected': 'true', 'size': '-1'})
  nuke.setUserPreset("Dot", "BG", {'label': '\xe8\x83\x8c\xe6\x99\xaf', 'note_font_color': '0x65ffdaff', 'selected': 'true', 'note_font_size': '70', 'note_font': 'Verdana'})
  nuke.setUserPreset("Dot", "CH", {'note_font_color': '0x7265ffff', 'selected': 'true', 'note_font_size': '50', 'label': '\xe4\xba\xba\xe7\x89\xa9'})
  nuke.setUserPreset("EXPTool", "LightFlicker", {'blue': '{green}', 'random': '{(random(frame/(1/speed))-0.5)/(1/amplitude)}', 'selected': 'true', 'smooth': '5.6', 'lightRandom': '{this.random2.integrate(frame-subSmooth,frame+subSmooth)/(2*subSmooth)}', 'label': 'Light Flicker', 'random2': '{this.random.integrate(frame-this.smooth,frame+this.smooth)/(2*this.smooth)}', 'green': '{red}', 'amplitude': '0.22', 'indicators': '2', 'speed': '2', 'subSmooth': '1.3', 'red': '{this.lightRandom}'})
  nuke.setUserPreset("Expression", "SaturationToRGB", {'expr0': '(max(r,g,b)-min(r,g,b))/max(r,g,b)', 'channel0': 'rgb', 'selected': 'true', 'label': 'SaturationToRGB'})
  nuke.setUserPreset("Expression", "minDepth", {'temp_name0': 'minDepth', 'selected': 'true', 'label': 'minDepth', 'expr0': 'min(minDepth,z)', 'channel0': 'depth', 'temp_expr0': '0.00169'})
  nuke.setUserPreset("Expression", "Depth:NukeToRedshift", {'expr0': '(z==0)?99999:1/z*0.0001', 'channel0': 'depth', 'selected': 'true', 'label': 'Depth:NukeToRedshift'})
  nuke.setUserPreset("Expression", "Depth:RedshiftToNuke", {'expr0': '(z==0)?0:1/(z*10000)', 'channel0': 'depth', 'selected': 'true', 'label': 'Depth:RedshiftToNuke'})
  nuke.setUserPreset("Glow2", "A", {'indicators': '16', 'mix': '0.25', 'saturation': '0.5', 'selected': 'true', 'size': '5'})
  nuke.setUserPreset("Glow2", "EffectOnly", {'effect_only': 'true', 'selected': 'true', 'tolerance': '0.195', 'brightness': '1.66'})
  nuke.setUserPreset("GodRays", "Aberration", {'selected': 'true', 'tile_color': '0xff8200ff', 'maskChannelInput': '-rgba.alpha', 'label': 'Aberration', 'channels': '-rgba.red -rgba.green rgba.blue none', 'translate': '3 -2'})
  nuke.setUserPreset("GodRays", "Aberration_B", {'scale': '1.02', 'selected': 'true', 'label': 'Aberration_B', 'channels': '-rgba.red -rgba.green rgba.blue none', 'mix': '0.5', 'indicators': '16'})
  nuke.setUserPreset("Grade", "Shadow", {'white': '0.001', 'selected': 'true', 'gamma': '1.896666527 2.006666899 2.096666574 2', 'label': 'Shadow'})
  nuke.setUserPreset("Grade", "LiftBlack", {'selected': 'true', 'black': '0.003566666739 0.00690666819 0.01356666628 0', 'label': 'LiftBlack', 'maskChannelInput': '-rgba.alpha', 'unpremult': 'rgba.alpha'})
  nuke.setUserPreset("Grade", "LightGlow", {'add': '0.1538991332 0.0945417881 0.05155908316 0.3199999928', 'selected': 'true', 'maskChannelMask': 'Refractions.red', 'white': '5', 'label': 'LightGlow'})
  nuke.setUserPreset("Grade", "Vigenette", {'white': '0.001', 'selected': 'true', 'gamma': '2', 'label': 'Vignette'})
  nuke.setUserPreset("Grade", "Warm", {'white': '2', 'selected': 'true', 'add': '0.07999999821 0.05123200268 0.03039999865 0.07999999821', 'gamma': '0.6'})
  nuke.setUserPreset("Grade", "Cold", {'selected': 'true', 'label': 'Cold', 'mix': '0.5', 'indicators': '16', 'white': '0.25', 'gamma': '1.188777447 1.3509022 1.53302753 0.5500000119'})
  nuke.setUserPreset("Group13430719196222772261", "Default", {'Child3 whitepoint': '{"(parent.switchMax==1)?\\nmax(\\n        parent.CurveTool1.maxlumapixvalue.r,\\n        parent.CurveTool1.maxlumapixvalue.g,\\n        parent.CurveTool1.maxlumapixvalue.b\\n)\\n:1"}', 'Child0 minlumapixvalue': '{curve}', 'Child0 maxlumapixvalue': '{curve}', 'Child0 ROI': '0 0 1920 1080', 'Child6 framesbehind': '25', 'Child-1 switchMin': 'true', 'Child-1 selected': 'true', 'Child0 minlumapixdata': '{curve} {curve}', 'Child3 blackpoint': '{"(parent.switchMin==1)?\\nmin(\\n       parent.CurveTool1.minlumapixvalue.r,\\n       parent.CurveTool1.minlumapixvalue.g,\\n       parent.CurveTool1.minlumapixvalue.b     \\n)\\n:0"}', 'Child0 operation': 'Max Luma Pixel', 'Child0 autocropdata': '{parent.CurveTool1.ROI.x} {parent.CurveTool1.ROI.y} {parent.CurveTool1.ROI.r} {parent.CurveTool1.ROI.t}', 'Child0 maxlumapixdata': '{curve} {curve}', 'Child6 frmaesfade': '25', 'Child-1 tile_color': '0x79a8ffff', 'Child-1 switchMax': 'true'})
  nuke.setUserPreset("Group14414967680556958356", "A", {'Child16 maskChannelMask': 'Emission.blue', 'Child16 white': '1 1 {parent.Control1.Gain.b} 1', 'Child14 unpremult': 'rgba.alpha', 'Child-1 selected': 'true', 'Child15 gamma': '1 {parent.Control1.Gamma.g} 1 1', 'Child10 size': '-10', 'Child11 white': '{parent.Control.Gain.r} 1 1 1', 'Child13 maskChannelMask': 'Emission.blue', 'Child13 white': '1 1 {parent.Control.Gain.b} 1', 'Child11 maskChannelMask': 'Emission.red', 'Child14 gamma': '{parent.Control1.Gamma.r} 1 1 1', 'Child13 gamma': '1 1 {parent.Control.Gamma.b} 1', 'Child11 gamma': '{parent.Control.Gamma.r} 1 1 1', 'Child14 maskChannelMask': 'Emission.red', 'Child12 gamma': '1 {parent.Control.Gamma.g} 1 1', 'Child10 filter': 'gaussian', 'Child15 white': '1 {parent.Control1.Gain.g} 1 1', 'Child18 Gamma': '1 1 1', 'Child12 white': '1 {parent.Control.Gain.g} 1 1', 'Child19 Gain': '1.5', 'Child16 gamma': '1 1 {parent.Control1.Gamma.b} 1', 'Child-1 tile_color': '0xff8200ff', 'Child15 unpremult': 'rgba.alpha', 'Child16 unpremult': 'rgba.alpha', 'Child18 Gain': '1.5', 'Child19 Gamma': '1.5', 'Child10 channels': 'Emission', 'Child14 white': '{parent.Control1.Gain.r} 1 1 1', 'Child12 maskChannelMask': 'Emission.green', 'Child15 maskChannelMask': 'Emission.green'})
  nuke.setUserPreset("Group1633858218987733247", "Depth3Fog", {'Child19 number': '1', 'Child21 input': 'depth', 'Child3 to0': 'rgba.red', 'Child17 indicators': '8', 'Child-1 label': '[knob_default this.mix 1]', 'Child23 range': '{"2 * parent.Close.range.A - parent.Close.range.B"} {parent.Close.range.A} 1 1', 'Child21 range': '0.003190627632 0.005730653333 0.008270676667 0.01081068429', 'Child31 which': '{parent.preview}', 'Child23 operation': 'luminance key', 'Child1 to0': 'rgba.green', 'Child25 Bchannels': 'alpha', 'Child-1 selected': 'true', 'Child30 channels': 'none', 'Child20 range': '{parent.Middle.range.C} {parent.Middle.range.D} 1 1', 'Child25 operation': 'plus', 'Child20 indicators': '2', 'Child22 input': '{{parent.Middle.input}}', 'Child22 invert': 'true', 'Child20 label': '[value input]', 'Child1 from0': 'rgba.alpha', 'Child2 from0': 'rgba.alpha', 'Child21 operation': 'luminance key', 'Child22 label': '[value input]', 'Child20 operation': 'luminance key', 'Child3 from0': 'rgba.alpha', 'Child15 channels': 'alpha', 'Child31 indicators': '2', 'Child20 input': '{{parent.Middle.input}}', 'Child13 channels': 'alpha', 'Child22 range': '{parent.Middle.range.A} {parent.Middle.range.B} 1 1', 'Child17 black': '0.008999999613 0.02102400549 0.04500000179 0', 'Child14 gamma': '0.8', 'Child23 label': '[value input]', 'Child16 black': '0.008999999613 0.02102400549 0.04500000179 0', 'Child32 which': '{"\\[string is digit \\[input \\[node parent] 1]]"}', 'Child26 maskChannelMask': '{{parent.Premult2.alpha}}', 'Child25 Achannels': 'alpha', 'Child27 channels': 'depth', 'Child21 label': '[value input]\n[knob this.parent.Far.operation [value this.operation]]\n[knob this.parent.Close.operation [value this.operation]]\n[knob this.parent.Multiply1.channels [value this.input]]', 'Child32 indicators': '2', 'Child22 operation': 'luminance key', 'Child33 frame_range': '33-50', 'Child24 output': 'alpha', 'Child16 gamma': '0.8', 'Child-1 tile_color': '0xff8200ff', 'Child29 channels': '{{parent.Grade1.channels}}', 'Child24 Achannels': 'alpha', 'Child33 fps': '25', 'Child24 Bchannels': 'alpha', 'Child23 indicators': '2', 'Child25 output': 'alpha', 'Child2 to0': 'rgba.blue', 'Child23 input': 'depth', 'Child14 indicators': '8', 'Child12 channels': 'alpha', 'Child16 indicators': '8', 'Child19 label': '\n\n', 'Child17 gamma': '0.8', 'Child14 black': '0.008999999613 0.02102400549 0.04500000179 0', 'Child0 operation': 'in', 'Child24 operation': 'plus', 'Child22 indicators': '2', 'Child30 alpha': 'none'})
  nuke.setUserPreset("Group17860204421431859712", "Default", {'Child-1 indicators': '2', 'Child1 autocropdata': '512 389 1536 1167', 'Child2 channels': 'alpha', 'Child11 black': '0.008999999613 0.02880000509 0.04500000179 0', 'Child1 channels': 'depth', 'Child-1 selected': 'true', 'Child9 channel0': 'depth', 'Child1 minlumapixvalue': '0 0 0', 'Child1 ROI': '0 0 1920 1080', 'Child11 white': '0.5', 'Child10 whitepoint': '{parent.CurveTool1.maxlumapixvalue.r}', 'Child13 channels': 'depth', 'Child1 operation': 'Max Luma Pixel', 'Child1 selected': 'true', 'Child11 maskChannelMask': 'depth.Z', 'Child11 gamma': '0.79', 'Child0 A': 'depth.Z', 'Child0 output': 'depth.Z', 'Child13 size': '2.6', 'Child13 ignore_top_line': 'false', 'Child9 expr0': '(z<.9)?z:0', 'Child10 gamma': '0.5', 'Child16 which': '{parent.switch}', 'Child1 maxlumapixvalue': '1 0 0', 'Child10 channels': 'depth', 'Child0 operation': 'in', 'Child15 in': 'depth'})
  nuke.setUserPreset("Group17860204421431859712", "Warmer", {'Child-1 indicators': '3', 'Child1 autocropdata': '512 389 1536 1167', 'Child2 channels': 'alpha', 'Child11 black': '0.01161600742 0.009680000134 0.04840000346 0', 'Child1 channels': 'depth', 'Child-1 selected': 'true', 'Child9 channel0': 'depth', 'Child1 minlumapixvalue': '{curve x50 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 x137 0 x138 0 0 0 0 0 0 0 0} {curve x50 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 x137 0 x138 0 0 0 0 0 0 0 0} 0', 'Child1 ROI': '0 0 1920 1080', 'Child10 whitepoint': '{parent.CurveTool1.maxlumapixvalue.r x51 0.005126}', 'Child13 channels': 'depth', 'Child1 operation': 'Max Luma Pixel', 'Child1 selected': 'true', 'Child11 maskChannelMask': 'depth.Z', 'Child11 gamma': '0.79', 'Child1 minlumapixdata': '{curve x50 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 x137 0 x138 0 0 0 0 0 0 0 0} {curve x50 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 x137 0 x138 0 0 0 0 0 0 0 0}', 'Child0 A': 'depth.Z', 'Child1 maxlumapixdata': '{curve x50 835 835 834 834 833 833 832 832 832 831 831 830 830 829 829 828 828 828 827 827 826 826 825 825 825 824 821 815 809 803 800 794 778 778 776 770 759 757 747 745 739 732 725 719 717 718 714 274 273 273 272 268 270 269 269 265 266 265 263 262 261 260 259 258 256 255 254 253 252 250 249 248 257 257 256 255 255 254 253 253 252 252 251 250 250 249 x137 800 x138 796 796 795 795 794 794 793 793} {curve x50 588 589 590 591 593 593 595 595 597 597 599 600 600 601 603 604 604 606 606 607 608 609 610 611 612 613 614 616 617 619 512 507 515 516 516 512 541 543 518 522 527 555 558 561 431 355 327 686 687 688 689 690 665 666 667 668 628 622 587 587 579 565 552 540 526 512 499 485 473 461 445 432 686 687 687 688 688 688 689 690 689 691 691 691 692 692 x137 869 x138 656 656 656 656 657 657 657 657}', 'Child0 output': 'depth.Z', 'Child13 size': '2.6', 'Child13 ignore_top_line': 'false', 'Child9 expr0': '(z<.9)?z:0', 'Child10 gamma': '0.5', 'Child16 which': '{parent.switch}', 'Child1 maxlumapixvalue': '{curve x51 0.005126} {curve} 0', 'Child10 channels': 'depth', 'Child0 operation': 'in', 'Child15 in': 'depth'})
  nuke.setUserPreset("Group18296031997871164842", "SSS", {'Child-1 label': '[value in]', 'Child10 black': '0 {parent.lift.g} 0 0', 'Child11 black': '0 0 {parent.lift.b} 0', 'Child13 operation': 'copy', 'Child1 channels': 'rgba', 'Child-1 selected': 'true', 'Child9 indicators': '2', 'Child-1 layer_mix': '1', 'Child8 expr0': '1', 'Child11 white': '1 1 {parent.gain.b} 1', 'Child11 maskChannelMask': 'rgba.blue', 'Child11 gamma': '1 1 {parent.gamma.b} 1', 'Child-1 lift': '0 0 0', 'Child-1 gain': '1 1 1', 'Child15 in': 'SSS', 'Child9 maskChannelMask': 'rgba.red', 'Child8 mix': '{1-parent.effect_mix}', 'Child9 black': '{parent.lift.r} 0 0 0', 'Child10 maskChannelMask': 'rgba.green', 'Child9 white': '{parent.gain.r} 1 1 1', 'Child-1 gamma': '1.714808822 1.202397585 0.9827932119', 'Child9 gamma': '{parent.gamma.r} 1 1 1', 'Child8 indicators': '18', 'Child10 gamma': '1 {parent.gamma.g} 1 1', 'Child-1 tile_color': '0x7aa9ffff', 'Child10 white': '1 {parent.gain.g} 1 1', 'Child10 indicators': '2', 'Child10 channels': '{{parent.R1.channels}}', 'Child11 channels': '{{parent.R1.channels}}', 'Child8 channel0': 'rgba', 'Child8 channel1': 'rgb', 'Child11 indicators': '2'})
  nuke.setUserPreset("Group18446744073709551615", "toFirstFrame", {'Child-1 indicators': '2', 'Child-1 label': 'Offset:[value time_offset]', 'Child-1 selected': 'true', 'Child-1 time_offset': '{"\\[value root.first_frame]"}', 'Child-1 time': ''})
  nuke.setUserPreset("Group3467099438493310833", "Default", {'Child-1 indicators': '2', 'Child0 subSmooth': '{smooth/10}', 'Child0 rgbMax': '{"max(\\n       maxlumapixvalue.r,\\n       maxlumapixvalue.g,\\n       maxlumapixvalue.b     \\n)"}', 'Child-1 selected': 'true', 'Child-1 mix': '1', 'Child0 rgbMax_smoothTemp': '{(smooth!=0)?rgbMax.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMax}', 'Child7 operation': 'copy', 'Child0 minlumapixvalue': '{curve} {curve} {curve}', 'Child0 maxlumapixvalue': '{curve} {curve} {curve}', 'Child0 rgbMin': '{"min(\\n       minlumapixvalue.r,\\n       minlumapixvalue.g,\\n       minlumapixvalue.b     \\n)"}', 'Child0 rgbMax_smoothed': '{"(subSmooth!=0)?\\n    (\\n    (smooth!=0)?\\n        rgbMax_smoothTemp.integrate(frame-subSmooth,frame+subSmooth)/(2*subSmooth)\\n        :rgbMax\\n    )\\n:rgbMax_smoothTemp"}', 'Child5 blackpoint': '{(switchMin==1)?parent.CurveTool1.rgbMin_smoothed:0}', 'Child0 autocropdata': '{parent.CurveTool1.ROI.x} {parent.CurveTool1.ROI.y} {parent.CurveTool1.ROI.r} {parent.CurveTool1.ROI.t}', 'Child0 maxlumapixdata': '{curve} {curve}', 'Child7 mix': '{1-parent.mix}', 'Child0 rgbMin_smoothTemp': '{(smooth!=0)?rgbMin.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMin}', 'Child-1 switchMin': 'true', 'Child0 minlumapixdata': '{curve} {curve}', 'Child0 smooth': '{(last_frame-first_frame)/2}', 'Child-1 tile_color': '0x79a8ffff', 'Child0 ROI': '0 0 {width} {height}', 'Child5 whitepoint': '{(switchMax==1)?parent.CurveTool1.rgbMax_smoothed:1}', 'Child0 rgbMin_smoothed': '{"(subSmooth!=0)?\\n    (\\n    (smooth!=0)?\\n        rgbMin_smoothTemp.integrate(frame-subSmooth,frame+subSmooth)/(2*subSmooth)\\n        :rgbMin\\n    )\\n:rgbMin_smoothTemp"}', 'Child0 operation': 'Max Luma Pixel', 'Child-1 switchMax': 'true'})
  nuke.setUserPreset("Group3883314892370062032", "Default", {'Child-1 indicators': '2', 'Child0 selected': 'true', 'Child9 frmaesfade': '25', 'Child0 rgbMax': '{"max(\\n       maxlumapixvalue.r,\\n       maxlumapixvalue.g,\\n       maxlumapixvalue.b     \\n)"}', 'Child-1 selected': 'true', 'Child9 framesbehind': '25', 'Child-1 mix': '1', 'Child0 minlumapixvalue': '{curve} {curve} {curve}', 'Child0 maxlumapixvalue': '{curve} {curve} {curve}', 'Child0 rgbMin': '{"min(\\n       minlumapixvalue.r,\\n       minlumapixvalue.g,\\n       minlumapixvalue.b     \\n)"}', 'Child0 rgbMax_smoothed': '{(smooth!=0)?rgbMax.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMax}', 'Child5 blackpoint': '{parent.CurveTool1.rgbMin_smoothed}', 'Child0 autocropdata': '{parent.CurveTool1.ROI.x} {parent.CurveTool1.ROI.y} {parent.CurveTool1.ROI.r} {parent.CurveTool1.ROI.t}', 'Child0 maxlumapixdata': '{curve} {curve}', 'Child7 mix': '{1-parent.mix}', 'Child-1 switchMin': 'true', 'Child0 minlumapixdata': '{curve} {curve}', 'Child0 smooth': '10', 'Child-1 tile_color': '0x79a8ffff', 'Child0 ROI': '0 0 {width} {height}', 'Child5 whitepoint': '{parent.CurveTool1.rgbMax_smoothed}', 'Child0 rgbMin_smoothed': '{(smooth!=0)?rgbMin.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMin}', 'Child0 operation': 'Max Luma Pixel', 'Child-1 switchMax': 'true'})
  nuke.setUserPreset("Group4116849246171828385", "root.first_frame", {'Child-1 indicators': '2', 'Child-1 label': 'Offset:[value time_offset]', 'Child-1 selected': 'true', 'Child-1 time_offset': '{"\\[value root.first_frame]"}', 'Child-1 time': ''})
  nuke.setUserPreset("Group4538184515349712785", "SSS", {'Child-1 indicators': '2', 'Child9 maskChannelMask': 'SSS.red', 'Child-1 RGB_Gamma': '1.714808822 1.202397585 0.9827932119', 'Child8 maskChannelMask': 'SSS.red', 'Child0 channels': 'SSS', 'Child8 gamma': '1 {parent.RGB_Gamma.g} 1 1', 'Child7 white': '0.8100000024 0.8289999962 1 1', 'Child-1 selected': 'true', 'Child7 gamma': '1 1 {parent.RGB_Gamma.b} 1', 'Child9 gamma': '{parent.RGB_Gamma.r} 1 1 1', 'Child7 maskChannelMask': 'SSS.blue'})
  nuke.setUserPreset("Group4999437065967225279", "Light_Yellow", {'Child20 indicators': '2', 'Child20 blue': 'alpha', 'Child19 green': 'alpha', 'Child-1 selected': 'true', 'Child19 indicators': '2', 'Child18 indicators': '2', 'Child2 from0': 'rgba.alpha', 'Child20 red': 'alpha', 'Child18 blue': 'alpha', 'Child18 disable': '{1-parent.keyer_preview}', 'Child14 channels': '{{parent.Keyer3.input}}', 'Child1 operation': 'in', 'Child16 operation': 'luminance key', 'Child19 blue': 'alpha', 'Child20 green': 'alpha', 'Child20 label': 'blurPreview', 'Child0 channels': 'alpha', 'Child14 lut': 'amount {curve x-1.953731775 0 0 0 1 1 0 0 s0}\nsat_thrsh {curve x-1.953731775 0.1 0.1 0.1 0.1 0.1 0.1 0.1 s0}', 'Child18 label': 'keyerPreview', 'Child20 disable': '{1-parent.blur_preview}', 'Child18 green': 'alpha', 'Child16 range': '0.1867629605 1 1 1', 'Child-1 tile_color': '0xff00ff', 'Child18 red': 'alpha', 'Child2 to0': 'BG_A.Light_Yellow', 'Child19 disable': '{1-parent.hueKeyer_preview}', 'Child19 red': 'alpha', 'Child19 label': 'hueKeyerPreview', 'Child0 size': '3.4', 'Child14 invert': 'false'})
  nuke.setUserPreset("Group5182900274578040651", "default", {'Child-1 indicators': '2', 'Child0 subSmooth': '{smooth/10}', 'Child0 rgbMax': '{"max(\\n       maxlumapixvalue.r,\\n       maxlumapixvalue.g,\\n       maxlumapixvalue.b     \\n)"}', 'Child-1 selected': 'true', 'Child-1 mix': '1', 'Child0 rgbMax_smoothTemp': '{(smooth!=0)?rgbMax.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMax}', 'Child0 minlumapixvalue': '{curve} {curve} {curve}', 'Child0 maxlumapixvalue': '{curve} {curve} {curve}', 'Child7 tile_color': '0x79a8ffff', 'Child0 rgbMin': '{"min(\\n       minlumapixvalue.r,\\n       minlumapixvalue.g,\\n       minlumapixvalue.b     \\n)"}', 'Child7 gain': '1', 'Child9 mix': '{1-parent.mix}', 'Child0 autocropdata': '{parent.CurveTool1.ROI.x} {parent.CurveTool1.ROI.y} {parent.CurveTool1.ROI.r} {parent.CurveTool1.ROI.t}', 'Child0 maxlumapixdata': '{curve} {curve}', 'Child9 operation': 'copy', 'Child7 help': '\xe5\x8f\xaa\xe8\xb0\x83\xe6\x95\xb4\xe4\xba\xae\xe5\xba\xa6\xe4\xb8\x8d\xe5\xbd\xb1\xe5\x93\x8d\xe9\xa5\xb1\xe5\x92\x8c\xe5\xba\xa6\xe5\x92\x8c\xe8\x89\xb2\xe7\x9b\xb8', 'Child0 smooth': '{(last_frame-first_frame)/2}', 'Child0 rgbMin_smoothTemp': '{(smooth!=0)?rgbMin.integrate(frame-smooth,frame+smooth)/(2*smooth):rgbMin}', 'Child-1 switchMin': 'true', 'Child0 minlumapixdata': '{curve} {curve}', 'Child7 gamma': '1', 'Child7 label': '[knob_default gain 1]\n[knob_default gamma 1]', 'Child0 rgbMax_smoothed': '{"(subSmooth!=0)?\\n    (\\n    (smooth!=0)?\\n        rgbMax_smoothTemp.integrate(frame-subSmooth,frame+subSmooth)/(2*subSmooth)\\n        :rgbMax\\n    )\\n:rgbMax_smoothTemp"}', 'Child-1 tile_color': '0x79a8ffff', 'Child5 blackpoint': '{(switchMin==1)?parent.CurveTool1.rgbMin_smoothed:0}', 'Child0 ROI': '0 0 {width} {height}', 'Child6 selected': 'true', 'Child5 whitepoint': '{(switchMax==1)?parent.CurveTool1.rgbMax_smoothed:1}', 'Child0 rgbMin_smoothed': '{"(subSmooth!=0)?\\n    (\\n    (smooth!=0)?\\n        rgbMin_smoothTemp.integrate(frame-subSmooth,frame+subSmooth)/(2*subSmooth)\\n        :rgbMin\\n    )\\n:rgbMin_smoothTemp"}', 'Child0 operation': 'Max Luma Pixel', 'Child-1 switchMax': 'true'})
  nuke.setUserPreset("Group5541083097794424652", "default", {'Child5 unpremult': '-rgba.alpha', 'Child1 channels': 'depth', 'Child-1 selected': 'true', 'Child0 minlumapixvalue': '{curve} {curve} 0', 'Child0 maxlumapixvalue': '{curve} {curve} 0', 'Child5 label': 'minDepth', 'Child5 selected': 'true', 'Child5 temp_name0': 'minDepth', 'Child1 size': '-2', 'Child0 autocropdata': '480 270 1440 810', 'Child0 maxlumapixdata': '{curve} {curve}', 'Child5 temp_expr0': 'mD*multiple', 'Child5 expr0': 'min(minDepth,z)', 'Child0 channels': 'depth', 'Child0 minlumapixdata': '{curve} {curve}', 'Child-1 tile_color': '0x823a7dff', 'Child5 multiple': '1', 'Child4 expr0': '(a==1)?z:0', 'Child0 ROI': '0 0 {width} {height}', 'Child5 mD': '{parent.CurveTool1.maxlumapixvalue.r}', 'Child4 channel0': 'depth', 'Child0 operation': 'Max Luma Pixel', 'Child5 channel0': 'depth'})
  nuke.setUserPreset("Group5808496026448139547", "SNJYW_EP01_04", {'Child42 last': '792', 'Child3 contrast': '1.5', 'Child4 analysisFrame': '765', 'Child16 label': 'SaturationToRGB', 'Child26 indicators': '2', 'Child16 expr0': '(max(r,g,b)-min(r,g,b))/max(r,g,b)', 'Child49 last': '{first}', 'Child40 origset': 'true', 'Child2 gain': '0.68', 'Child42 auto_alpha': 'true', 'Child37 type': 'smooth0', 'Child-1 fps': '25', 'Child43 colorspace': 'linear', 'Child-1 format': '1920 1080 0 0 1920 1080 1 HD_1080', 'Child42 origlast': '792', 'Child17 steps': '50', 'Child-1 hostName': 'localhost', 'Child24 gamma': '2', 'Child44 indicators': '2', 'Child40 format': '1920 1080 0 0 1920 1080 1 HD_1080', 'Child48 colorspace': 'sRGB', 'Child23 white': '2', 'Child42 origset': 'true', 'Child44 origset': 'true', 'Child30 tile_color': '0x79a8ffff', 'Child50 center': '0.002104341285', 'Child40 colorspace': 'linear', 'Child46 softclip_min': '0.5', 'Child49 proxy': 'images/[lindex [split [basename [value root.name]] .] 0]_proxy.%04d.jpg', 'Child43 indicators': '2', 'Child-1 socketPortSend': '6100', 'Child47 frame_range': '750-792', 'Child36 color': '0', 'Child37 p0': '156 796', 'Child37 p1': '130 -146', 'Child48 mov.meta_encoder': 'mov32', 'Child48 mov.mov64_bitrate': '20000', 'Child40 indicators': '8', 'Child1 size': '15', 'Child0 size': '23.5', 'Child45 softclip_min': '0', 'Child48 proxy': 'mov/[lindex [split [basename [value root.name]] .] 0]_proxy.mov', 'Child41 format': '1920 1080 0 0 1920 1080 1 HD_1080', 'Child41 file': 'Z:/SNJYW/Render/EP01/04/EP01_04_sc132/EP01_04_sc132_Fog_A.tif', 'Child20 invert_mask': 'true', 'Child-1 first_frame': '750', 'Child16 channel0': 'rgb', 'Child33 area': '-749.2057789 32 2525.205779 1420', 'Child30 switchMax': 'true', 'Child17 channels': 'alpha', 'Child48 mov.mov32_codec': 'raw ', 'Child48 version': '1', 'Child30 switchMin': 'true', 'Child48 mov.meta_codec': 'raw ', 'Child27 indicators': '1', 'Child43 file': 'Z:/SNJYW/Render/EP01/04/EP01_04_sc132/EP01_04_sc132_BG_A.exr', 'Child-1 advanced': '0', 'Child49 use_limit': 'true', 'Child49 first': '765', 'Child50 dof': '0.200000003', 'Child18 mix': '0.34', 'Child19 whitepoint': '0.145', 'Child42 format': '1920 1080 0 0 1920 1080 1 HD_1080', 'Child35 type': 'smooth1', 'Child34 area': '-808 -296 2776 1710', 'Child-1 last_frame': '792', 'Child19 channels': 'alpha', 'Child49 file': 'images/[lindex [split [basename [value root.name]] .] 0].%04d.jpg', 'Child3 gamma': '1.025478125 1.025478125 1.025478125 0.9100000262', 'Child3 lookup': 'shadow {curve 1 s0 x0.3303062916 0 s0}\nmidtone {1-shadow-highlight}\nhighlight {curve x-0.01870897412 0 s0 x0.4771333933 1 s0}', 'Child43 format': '1920 1080 0 0 1920 1080 1 HD_1080', 'Child48 checkHashOnRead': 'false', 'Child32 operation': 'stencil', 'Child44 version': '2', 'Child36 p1': '2352 912', 'Child36 p0': '1152 658', 'Child50 show_legacy_resize_mode': 'false', 'Child40 file': 'Z:/SNJYW/Render/EP01/04/EP01_04_sc132/EP01_04_sc132_CH_A/EP01_04_sc132_CH_A.%04d.exr', 'Child44 last': '{first}', 'Child36 type': 'smooth1', 'Child25 tile_color': '0x79a8ffff', 'Child18 gamma': '1.14', 'Child-1 mariDataDir': '[getenv NUKE_TEMP_DIR]/mariData', 'Child2 saturation': '0.3', 'Child50 focal_point': '554 474', 'Child47 fps': '25', 'Child20 gamma': '0.9187541604 1.005241871 1.076004148 1', 'Child17 translate': '24 -162', 'Child43 origlast': '0', 'Child23 gamma': '0.6897417903 1.091919184 1.564040422 1', 'Child-1 proxy_format': '1024 778 0 0 1024 778 1 1K_Super_35(full-ap)', 'Child50 shape': '0.44', 'Child3 gain': '1.4', 'Child29 tile_color': '0x79a8ffff', 'Child40 last': '792', 'Child48 file': 'mov/[lindex [split [basename [value root.name]] .] 0].mov', 'Child49 file_type': 'jpeg', 'Child41 last': '0', 'Child49 checkHashOnRead': 'false', 'Child48 file_type': 'mov', 'Child18 white': '1.96', 'Child35 color': '0', 'Child17 scale': '1.16', 'Child21 white': '2.5', 'Child4 serializeKnob': '0.980537 0.564131 0.425112\n0.00705341 0.00135169 0.00137731\n0.00705341 0.00135169 0.00137731\n0.00803844 0.00150398 0.00147154\n0 0 0\n0.00233373 0.000582791 0.000570906\n0.00233373 0.000582791 0.000570906\n0.00152487 0.000342688 0.000349558\n0 0 0\n0.000419887 0.000196556 0.000204418\n0.000419887 0.000196556 0.000204418\n0.000498812 0.000226834 0.000213393\n0 0 0\n1.15577e-005 1.79196e-005 1.25303e-005\n1.15577e-005 1.79196e-005 1.25303e-005\n1.2278e-005 1.89653e-005 1.39519e-005\n0 0 0 0 0 0 0 0 0 \n3939190613814788761', 'Child5 size': '-1', 'Child39 p0': '998 666', 'Child39 p1': '1000 -34', 'Child-1 socketPort': '50107', 'Child-1 proxy': 'true', 'Child42 colorspace': 'linear', 'Child47 colour_sample_bbox': '-0.6020833254 0.2895833254 -0.6000000238 0.2916666567', 'Child0 channels': 'alpha', 'Child25 indicators': '1', 'Child43 auto_alpha': 'true', 'Child4 needsAnalyzing': 'false', 'Child43 last': '{root.last_frame}', 'Child41 colorspace': 'sRGB', 'Child31 input': 'SSS', 'Child49 version': '6', 'Child29 switchMax': 'true', 'Child29 switchMin': 'true', 'Child49 indicators': '2', 'Child23 black': '0.18', 'Child27 tile_color': '0x823a7dff', 'Child31 range': '0 0.001420418676 1 1', 'Child50 math': 'depth', 'Child48 mov.mov64_codec': 'ap4h', 'Child49 jpeg._jpeg_quality': '1', 'Child35 p0': '818 712', 'Child50 size': '25', 'Child35 p1': '-36 682', 'Child44 file': '[value Write_JPG.file]', 'Child40 first': '750', 'Child46 conversion': 'logarithmic compress', 'Child45 conversion': 'logarithmic compress', 'Child40 origfirst': '750', 'Child34 invert': 'true', 'Child31 operation': 'luminance key', 'Child23 maskChannelMask': 'rgba.blue', 'Child25 switchMin': 'true', 'Child-1 project_directory': 'E:/SNJYW/EP01/04/', 'Child42 origfirst': '750', 'Child42 file': 'Z:/SNJYW/Render/EP01/04/EP01_04_sc132/EP01_04_sc132_CH_A/EP01_04_sc132_CH_A.%04d.exr', 'Child39 color': '0', 'Child18 indicators': '16', 'Child22 multiply': '0.28', 'Child42 first': '750', 'Child41 first': '0', 'Child30 indicators': '1', 'Child38 type': 'smooth0', 'Child40 origlast': '792', 'Child43 origfirst': '0', 'Child23 label': 'Fog', 'Child25 switchMax': 'true', 'Child5 channels': 'depth', 'Child50 legacy_resize_mode': 'false', 'Child-1 proxy_type': 'scale', 'Child4 analysisRegion': '877 206 1183 542', 'Child43 origset': 'true', 'Child-1 portRange': '200', 'Child50 max_size': '100', 'Child44 first': '{parent.Write_JPG.last}', 'Child29 indicators': '1', 'Child2 gamma': '0.9406987429 0.9981859326 1.045220852 1', 'Child48 mov.mov64_advanced': '1', 'Child-1 frame': '765', 'Child26 RGB_Gamma': '1.714808822 1.202397585 0.9827932119', 'Child17 to_color': '0', 'Child38 p1': '120 1202', 'Child38 p0': '260 22', 'Child47 clip_warning': 'exposure', 'Child40 auto_alpha': 'true', 'Child42 indicators': '8', 'Child43 first': '{root.first_frame}', 'Child4 lumablend': '0.5', 'Child41 auto_alpha': 'true', 'Child4 profileCurve': 'profile {curve x0.1000000015 0 x0.1333521456 0 x0.1778279394 0 x0.2371373773 0 x0.3162277639 0 x0.4216965139 0 x0.5623413324 0 x0.7498942018 0 x1 0}', 'Child24 white': '0.001', 'Child39 type': 'smooth1'})
  nuke.setUserPreset("Group7870934511641480208", "Ep01_04", {'Child21 in': 'SSS', 'Child18 saturation': '{parent.saturation.r}', 'Child16 Achannels': 'rgb', 'Child19 saturation': '{parent.saturation.g}', 'Child-1 label': '[value in]\n[knob_default saturation 1]\n[knob_default gain 1]\n[knob_default gamma 1]\n[knob_default layer_mix 1]', 'Child12 selected': 'true', 'Child11 whitepoint': '0.01', 'Child16 Bchannels': 'rgb', 'Child1 channels': 'rgba', 'Child-1 selected': 'true', 'Child13 maskChannelMask': 'rgba.green', 'Child13 white': '1 {parent.gain.g} 1 1', 'Child20 maskChannelMask': 'rgba.blue', 'Child13 channels': '{{parent.R1.channels}}', 'Child14 channels': '{{parent.R1.channels}}', 'Child13 black': '0 {parent.lift.g} 0 0', 'Child14 gamma': '1 1 {parent.gamma.b} 1', 'Child13 gamma': '1 {parent.gamma.g} 1 1', 'Child16 operation': 'copy', 'Child-1 saturation': '0.8', 'Child-1 lift': '0 0 0', 'Child16 output': 'rgb', 'Child-1 gain': '1.25999999 1.120895982 0.3905999959', 'Child12 gamma': '{parent.gamma.r} 1 1 1', 'Child11 mix': '{1-parent.layer_mix}', 'Child18 channels': 'rgba.red -rgba.green -rgba.blue -rgba.alpha', 'Child19 channels': '-rgba.red rgba.green -rgba.blue -rgba.alpha', 'Child12 label': '[knob parent.Merge1.Achannels [value channels]]\n[knob parent.Merge1.Bchannels [value channels]]\n[knob parent.Merge1.output [value channels]]', 'Child12 white': '{parent.gain.r} 1 1 1', 'Child-1 gamma': '1.629999995 1.289999843 0.9800000191', 'Child-1 layer_mix': '1', 'Child-1 tile_color': '0x7aa9ffff', 'Child14 maskChannelMask': 'rgba.blue', 'Child14 white': '1 1 {parent.gain.b} 1', 'Child14 black': '0 0 {parent.lift.b} 0', 'Child20 saturation': '{parent.saturation.b}', 'Child12 maskChannelMask': 'rgba.red', 'Child18 maskChannelMask': 'rgba.red', 'Child20 channels': '-rgba.red -rgba.green rgba.blue -rgba.alpha', 'Child19 maskChannelMask': 'rgba.green', 'Child12 black': '{parent.lift.r} 0 0 0'})
  nuke.setUserPreset("Group8867751322934232644", "SaturationBlur", {'Child-1 indicators': '16', 'Child0 indicators': '16', 'Child4 number': '1', 'Child2 colorspace_in': 'HSV', 'Child1 colorspace_out': 'HSV', 'Child0 channels': '-rgba.red rgba.green -rgba.blue none', 'Child-1 selected': 'true', 'Child0 size': '80', 'Child0 mix': '0.3', 'Child-1 tile_color': '0x7aa9ffff'})
  nuke.setUserPreset("HueCorrect", "Lower Blue Lum", {'hue': 'sat {}\nlum {curve 0.5348259211 s0 t-0.01999999955 0.8522388935 1 0.9726368189 0.8467662334 0.6935323716 0.5348259211 s-0.03624998778}\nred {}\ngreen {}\nblue {}\nr_sup {}\ng_sup {}\nb_sup {}\nsat_thrsh {}', 'selected': 'true'})
  nuke.setUserPreset("HueCorrect", "1", {'indicators': '20', 'hue': 'sat {curve 1 0.8412934542 0.2557213306 1 1 1 1}\nlum {curve 1 0.3925373554 0.3925373554 1 1 1 1}\nred {}\ngreen {}\nblue {}\nr_sup {}\ng_sup {}\nb_sup {}\nsat_thrsh {}', 'maskChannelInput': 'Emission.red', 'selected': 'true', 'mix': '0.675'})
  nuke.setUserPreset("HueKeyer", "Yellow_in", {'invert': 'false', 'selected': 'true', 'lut': 'amount {curve x0.811249733 0 x1.066457629 0 x1.321665525 0 x1.576873183 1 x1.832081079 1 x2.087288618 0 x2.342496395 0 s0}\nsat_thrsh {curve x0.811249733 0.1 x1.066457629 0.1 x1.321665525 0.1 x1.576873183 0.1 x1.832081079 0.1 x2.087288618 0.1 x2.342496395 0.1 s0}'})
  nuke.setUserPreset("Keyer", "SSS", {'input': 'SSS', 'operation': 'luminance key', 'selected': 'true', 'range': '0 0.001420418676 1 1', 'label': 'SSS'})
  nuke.setUserPreset("Keyer", "depth", {'input': 'depth', 'operation': 'luminance key', 'selected': 'true', 'label': '[value input]'})
  nuke.setUserPreset("Keyer", "label", {'operation': 'luminance key', 'selected': 'true', 'label': '[value input]'})
  nuke.setUserPreset("Keyer", "ZDefocus_direct", {'invert': 'true', 'selected': 'true', 'label': '[value input]', 'range': '0 0.002045402894 0.002045402894 0.00944842', 'output': 'BG_A.ZDefocus', 'input': 'depth', 'operation': 'luminance key'})
  nuke.setUserPreset("Merge2", "DepthMerge", {'Achannels': 'depth', 'output': 'depth', 'operation': 'min', 'Bchannels': 'depth', 'selected': 'true'})
  nuke.setUserPreset("Merge2", "AO", {'screen_alpha': 'true', 'operation': 'multiply', 'selected': 'true', 'label': 'AO'})
  nuke.setUserPreset("Merge2", "LayerCopy", {'Achannels': 'BumpNormals', 'output': '{{Achannels}}', 'operation': 'copy', 'Bchannels': '{{Achannels}}', 'selected': 'true'})
  nuke.setUserPreset("ModifyMetaData", "frameRange", {'selected': 'true', 'metadata': '{set first_frame "\\[value input.first]"}\n{set last_frame "\\[value input.last]"}'})
  nuke.setUserPreset("Multiply", "alpha*0", {'channels': 'alpha', 'selected': 'true', 'value': '0'})
  nuke.setUserPreset("Premult", "depth", {'channels': 'depth', 'selected': 'true'})
  nuke.setUserPreset("Radial", "Soft:0.5 Invert", {'softness': '0.5', 'invert': 'true', 'selected': 'true', 'area': '-79.98813498 -174 1999.988135 1254'})
  nuke.setUserPreset("Ramp", "Black", {'color': '0', 'p0': '1358 1076', 'p1': '404 22', 'type': 'smooth1', 'selected': 'true'})
  nuke.setUserPreset("Ramp", "Mask", {'p0': '600 600', 'p1': '1400 600', 'premult': 'all', 'selected': 'true', 'label': 'Mask', 'output': 'none'})
  nuke.setUserPreset("Read", "Write1 HoldFrame", {'last': '{first}', 'selected': 'true', 'file': '[value Write1.file]', 'indicators': '2', 'origset': 'true', 'first': '{parent.Write1.last}'})
  nuke.setUserPreset("Shuffle", "DepthToAlpha", {'selected': 'true', 'out': 'alpha', 'in': 'depth'})
  nuke.setUserPreset("Shuffle", "CH_A", {'selected': 'true', 'green': 'black', 'red': 'alpha', 'out': 'CH_A'})
  nuke.setUserPreset("SoftClip", "Log_min:0", {'conversion': 'logarithmic compress', 'softclip_min': '0', 'selected': 'true'})
  nuke.setUserPreset("Transform", "ToCenter", {'indicators': '2', 'label': 'ToCenter', 'translate': '{width/2-center.x} {height/2-center.y}', 'selected': 'true', 'center': '1002 778'})
  nuke.setUserPreset("TransformGeo", "inputToThis", {'translate': '24.25000191 9.119999886 -3.639999151', 'selected': 'true', 'rotate': '26.93956895 -46.47709455 13.99319297', 'label': '[input this 2 Camera1]'})
  nuke.setUserPreset("Write", "ScriptName.mov", {'mov.mov32_fps': '{"\\[value root.fps]"}', 'mov.mov64_bitrate': '20000', 'checkHashOnRead': 'false', 'file_type': 'mov', 'beforeRender': 'file = nuke.tcl(\'eval list {\'+nuke.thisNode()["file"].value()+\'}\');\nabsolutePath = os.path.splitdrive(file)[0];\nproject_directory = nuke.tcl(\'eval list {\'+nuke.root()["project_directory"].value()+\'}\');\npathHead = \'\' if absolutePath else project_directory+\'/\';\ntarget = pathHead+os.path.dirname(file)\nif os.path.exists(target):\n    pass;\nelse:\n    os.makedirs(target);\n', 'mov.meta_encoder': 'mov32', 'selected': 'true', 'mov.mov64_codec': 'ap4h', 'mov.mov64_advanced': '1', 'colorspace': 'sRGB', 'mov.mov32_codec': 'raw ', 'mov.meta_codec': 'raw ', 'version': '3', 'proxy': 'mov/[lindex [split [basename [value root.name]] .] 0]_proxy.mov', 'file': 'mov/[lindex [split [basename [value root.name]] .] 0].mov', 'indicators': '2'})
  nuke.setUserPreset("Write", "InputName.jpg", {'checkHashOnRead': 'false', 'file_type': 'jpeg', 'beforeRender': 'file = nuke.tcl(\'eval list {\'+nuke.thisNode()["file"].value()+\'}\');\nabsolutePath = os.path.splitdrive(file)[0];\nproject_directory = nuke.tcl(\'eval list {\'+nuke.root()["project_directory"].value()+\'}\');\npathHead = \'\' if absolutePath else project_directory+\'/\';\ntarget = pathHead+os.path.dirname(file)\nif os.path.exists(target):\n    pass;\nelse:\n    os.makedirs(target);\n', 'selected': 'true', 'jpeg._jpeg_quality': '1', 'version': '3', 'proxy': 'images/[lindex [split [basename [metadata input/filename]] .] 0]_proxy.jpg', 'file': 'images/[lindex [split [basename [metadata input/filename]] .] 0].jpg'})
  nuke.setUserPreset("Write", "ScriptName.jpg_SingleFrame", {'checkHashOnRead': 'false', 'file_type': 'jpeg', 'beforeRender': 'file = nuke.tcl(\'eval list {\'+nuke.thisNode()["file"].value()+\'}\');\nabsolutePath = os.path.splitdrive(file)[0];\nproject_directory = nuke.tcl(\'eval list {\'+nuke.root()["project_directory"].value()+\'}\');\npathHead = \'\' if absolutePath else project_directory+\'/\';\ntarget = pathHead+os.path.dirname(file)\nif os.path.exists(target):\n    pass;\nelse:\n    os.makedirs(target);\n', 'selected': 'true', 'jpeg._jpeg_quality': '1', 'version': '15', 'use_limit': 'true', 'proxy': 'images/[lindex [split [basename [value root.name]] .] 0]_proxy.%04d.jpg', 'file': 'images/[lindex [split [basename [value root.name]] .] 0].%04d.jpg', 'indicators': '2', 'last': '{first}', 'first': '{"\\[value root.first_frame]"}'})
  nuke.setUserPreset("Write", "InputName.####.png", {'checkHashOnRead': 'false', 'file_type': 'png', 'beforeRender': 'file = nuke.tcl(\'eval list {\'+nuke.thisNode()["file"].value()+\'}\');\nabsolutePath = os.path.splitdrive(file)[0];\nproject_directory = nuke.tcl(\'eval list {\'+nuke.root()["project_directory"].value()+\'}\')+\'/\';\npathHead = \'\' if absolutePath else project_directory;\nos.makedirs(pathHead+os.path.dirname(file));\n', 'selected': 'true', 'label': '<font size="3" color =#548DD4><b> Frame range :</b></font> <font color = red>[value first] - [value last] </font>', 'version': '6', 'use_limit': 'true', 'proxy': 'images/[lindex [split [basename [metadata input/filename]] .] 0]/[lindex [split [basename [metadata input/filename]] .] 0]_proxy.%04d.png', 'file': 'images/[lindex [split [basename [metadata input/filename]] .] 0]/[lindex [split [basename [metadata input/filename]] .] 0].%04d.png', 'indicators': '2', 'last': '{"\\[metadata last_frame]"}', 'first': '{"\\[metadata first_frame]"}', 'png.datatype': '16 bit'})
  nuke.setUserPreset("ZDefocus2", "math:depth", {'center': '0.01153501403', 'selected': 'true', 'dof': '0.5', 'focal_point': '882 569', 'legacy_resize_mode': 'false', 'math': 'depth', 'indicators': '8', 'show_legacy_resize_mode': 'false', 'max_size': '50', 'size': '12.5'})
  nuke.setUserPreset("ZDefocus2", "math:depth CloseRange", {'center': '0.0010277119', 'selected': 'true', 'focal_point': '978 664', 'legacy_resize_mode': 'false', 'math': 'depth', 'show_legacy_resize_mode': 'false', 'max_size': '50', 'size': '25'})
  nuke.setUserPreset("ZDefocus2", "direct", {'z_channel': 'depth3split.Focus', 'selected': 'true', 'legacy_resize_mode': 'false', 'show_legacy_resize_mode': 'false', 'math': 'direct', 'size': '10'})

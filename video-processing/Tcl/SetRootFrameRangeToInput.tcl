[
# setRootFrameRangeToInput v0.2
if {([value this.name] == "setRootFrameRangeToInput") && ([class input] == "Read")} {
    knob root.first_frame [value input.origfirst]
    knob root.last_frame [value input.origlast]
    knob root.lock_range 1
} else {
    python nuke.warning('�ڵ���Ч: [value this.name]')
    return "<font color = red>û��������ȡ�ڵ�\n��˽ڵ��ж��</fonta>"
}
]
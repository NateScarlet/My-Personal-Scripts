#! usr/bin/env python
# -*- coding=UTF-8 -*-
# WuLiFang Studio AutoComper

import os
import sys
import re
import time
import locale
import traceback
from subprocess import call

import nuke

fps = 25
format = 'HD_1080'
VERSION = 0.872

tag_convert_dict = {
    'BG_FOG': 'FOG_BG',
    'BG_ID': 'ID_BG',
    'BG_CO': 'BG',
    'BG_RGB': 'ID_BG',
    'BG_RGB1': 'ID_BG1',
    'BG_KEY_LIGHT': 'LIGHT_KEY_BG',
    'BG_FILL_LIGHT': 'LIGHT_FILL_BG',
    'BG_OCC': 'OCC_BG',
    'CH_CO': 'CH',
    'CH_RGB': 'ID_CH',
    'CH_KEY_LIGHT': 'LIGHT_KEY_CH',
    'CH_ID': 'ID_CH',
    'CH_SD': 'SH_CH',
    'CH_SH': 'SH_CH',
    'CH_A_SH': 'SH_CH_A',
    'CH_B_SH': 'SH_CH_B',
    'CH_C_SH': 'SH_CH_C',
    'CH_D_SH': 'SH_CH_D',
    'CH_AO': 'OCC_CH',
    'CH_OC': 'OCC_CH',
    'CH_OCC': 'OCC_CH',
    'CH_A_OC': 'OCC_CH_A',
    'CH_A_OCC': 'OCC_CH_A',
    'CH_B_OC': 'OCC_CH_B',
    'CH_B_OCC': 'OCC_CH_B',
    'CH_C_OC': 'OCC_CH_C',
    'CH_C_OCC': 'OCC_CH_C',
    'CH_D_OC': 'OCC_CH_D',
    'CH_D_OCC': 'OCC_CH_D',
}
REGULAR_TAGS = [
    'CH_A',
    'CH_B',
    'CH_C',
    'CH_D',
    'BG_A',
    'BG_B',
    'BG_C',
    'BG_D',
    'OCC',
    'SH',
]
toolset = '../../ToolSets/WLF'
DEFAULT_MP = r"\\192.168.1.4\f\QQFC_2015\Render\mp\Brooklyn-Bridge-Panorama.tga"
SYS_CODEC = locale.getdefaultlocale()[1]
script_codec = 'UTF-8'

def comp_wlf(mp=DEFAULT_MP, autograde=True):
    if not nuke.allNodes('Read'):
        raise FootageError('没有读取节点')

    _bg_node = None
    _mp = mp.replace('\\', '/')
    _tag_knob_name = 'wlf_tag'
    _nodes_order = lambda n: ('_' + n[_tag_knob_name].value()).replace('_BG', '1_').replace('_CH', '0_')

    def _get_tag(filename):
        _tag_pattern = re.compile(r'sc.+?_([^.]+)', flags=re.I)
        _default_result = '_OTHER'

        def _get_tag_from_pattern(str):
            _ret = re.search(_tag_pattern, str)
            if _ret:
                _ret = _ret.group(1).upper()
            else:
                _ret = _default_result
            return _ret

        _ret = _get_tag_from_pattern(os.path.basename(filename))

        if _ret not in REGULAR_TAGS:
            _dir_result = _get_tag_from_pattern(os.path.basename(os.path.dirname(filename)))
            if _dir_result != _default_result:
                _ret = _dir_result
        
        return _ret

    def _setup_node(n):
        _tag = _get_tag(nuke.filename(n))
        if not 'rgba.alpha' in n.channels():
            _tag = '_OTHER'
        
        _name = n['name'].value()
        if _name in REGULAR_TAGS:
            _tag = _name

        _temp_tab = nuke.Tab_Knob('User')
        n.addKnob(_temp_tab)

        def _add_knob(k):
            _knob_name = k.name()
            while nuke.exists('{}.{}'.format(_name, k.name())):
                k.setValue(n[_knob_name].value())
                n.removeKnob(n[_knob_name])
            n.addKnob(k)

        k = nuke.Tab_Knob('吾立方')
        _add_knob(k)

        k = nuke.String_Knob(_tag_knob_name, '素材标签')
        _add_knob(k)
        k.setValue(_tag)
        
        n.removeKnob(_temp_tab)
        
        n.setName(_tag, updateExpressions=True)

    for n in nuke.allNodes('Read'):
        _setup_node(n)

    def _get_nodes_by_tag(tags):
        _ret = []    
        if type(tags) is str :
            tags = [tags]
        tags = tuple(map(str.upper, tags))

        for n in nuke.allNodes('Read'):
            if n[_tag_knob_name].value().startswith(tags):
                _ret.append(n)
        _ret.sort(key=_nodes_order, reverse=True)
        return _ret
    
    _bg_ch_nodes = _get_nodes_by_tag(['BG', 'CH'])
    
    if _bg_ch_nodes:
        _last_output = _bg_ch_nodes[0]
    else:
        raise FootageError('BG', 'CH')

    # Create nodes.
    def _autograde_get_max(n):
        rgb_max = get_max(n, 'rgb')
        erode_size = 0
        erode_node = nuke.nodes.Dilate(inputs=[n], size = erode_size)
        # Exclude small highlight
        while rgb_max > 1 and erode_size > n.height() / -100.0:
            erode_node['size'].setValue(erode_size)
            rgb_max = get_max(erode_node, 'rgb')
            if rgb_max < 1:
                break
            erode_size -= 1
        nuke.delete(erode_node)
        
        return rgb_max

    def _merge_depth(nodes):
        if len(nodes) < 2:
            return

        merge_node = nuke.nodes.Merge2(inputs=nodes[:2] + [None] + nodes[2:], tile_color=2184871423L, operation='min', Achannels='depth', Bchannels='depth', output='depth', label='Depth', hide_input=True)
        copy_node = nuke.nodes.Copy(inputs=[None, merge_node], from0='depth.Z', to0='depth.Z')
        return copy_node

    _depth_copy_node = _merge_depth(_bg_ch_nodes)
        
    for i, _read_node in enumerate(_bg_ch_nodes):
        _read_node.selectOnly()
        if 'SSS.alpha' in _read_node.channels():
            n = nuke.createNode('Keyer', '''
                    input SSS
                    output SSS.alpha
                    operation "luminance key"
                    range {0 0.007297795507 1 1}
                '''
            )
        n = nuke.createNode('Reformat', 'resize fit')
        n = nuke.createNode('DepthFix')
        if get_max(_read_node, 'depth.Z') > 1.1 :
            n['farpoint'].setValue(10000)

        n = nuke.createNode('Grade', '''
                unpremult rgba.alpha
                label "白点: \[value this.whitepoint]\n混合:\[value this.mix]\n使亮度范围靠近0-1"
            '''
        )
        if autograde:
            _max = _autograde_get_max(_read_node)
            if _max < 0.5:
                _mix = 0.3
            else:
                _mix = 0.6
            n['whitepoint'].setValue(_max)
            n['mix'].setValue(_mix)

        n = nuke.createNode('Unpremult')
        n = nuke.createNode('ColorCorrect', 'label 亮度调整')
        n = nuke.createNode('ColorCorrect', 'mix_luminance 1 label 颜色调整')
        if 'SSS.alpha' in _read_node.channels():
            n = nuke.createNode('ColorCorrect', 'maskChannelInput SSS.alpha label SSS调整')
        n = nuke.createNode('HueCorrect')
        n = nuke.createNode('Premult')

        def _depthfog():
            n = nuke.createNode('Group', '''
                name DepthFog1
                tile_color 0x2386eaff
                label "深度雾\n由_DepthFogControl控制"
                disable {{_DepthFogControl.disable}}
            '''
            )
            n.begin()
            input = nuke.nodes.Input(name='Input')
            depthkeyer_node = nuke.loadToolset(toolset + '/Keyer/DepthKeyer.nk')
            depthkeyer_node.setInput(0, input)
            depthkeyer_node['range'].setExpression('_DepthFogControl.range')
            grade_node = nuke.nodes.Grade(inputs=[input, depthkeyer_node], black='{_DepthFogControl.fog_color} {_DepthFogControl.fog_color} {_DepthFogControl.fog_color}', unpremult='rgba.alpha', mix='{_DepthFogControl.fog_mix}')
            output = nuke.nodes.Output(inputs=[grade_node])
            n.end()

            return n
        n = _depthfog()
        
        n = nuke.createNode('SoftClip')
        n = nuke.createNode('ZDefocus2', '''
            math depth
            center {{"\[value _ZDefocus.center curve]"}}
            focal_point {1.#INF 1.#INF}
            dof {{"\[value _ZDefocus.dof curve]"}}
            blur_dof {{"\[value _ZDefocus.blur_dof curve]"}}
            size {{"\[value _ZDefocus.size curve]"}}
            max_size {{"\[value _ZDefocus.max_size curve]"}}
            label "\[\nset trg parent._ZDefocus\nknob this.math \[value \$trg.math depth]\nknob this.z_channel \[value \$trg.z_channel depth.Z]\nif \{\[exists _ZDefocus]\} \{return \"由_ZDefocus控制\"\} else \{return \"需要_ZDefocus节点\"\}\n]"
            disable {{"\[if \{\[value _ZDefocus.focal_point \"200 200\"] == \"200 200\" || \[value _ZDefocus.disable]\} \{return True\} else \{return False\}]"}}
        '''
        )
        n = nuke.createNode('Crop', '''
                 box {0 0 {root.width} {root.height}}
            '''
        )

        _bg_ch_nodes[i] = n
        if i > 0:
            _bg_ch_nodes[i] = nuke.nodes.Merge2(
                inputs=[_bg_ch_nodes[i-1], _bg_ch_nodes[i]],
                label=_read_node[_tag_knob_name].value()
            )

        _depth_copy_node.setInput(0, _bg_ch_nodes[-1])
        def _add_zdefocus_control(input):
            # Use for one-node zdefocus control
            n = nuke.nodes.ZDefocus2(inputs=[input], math='depth', output='focal plane setup', center=0.00234567, blur_dof=False, label='** 虚焦总控制 **\n在此拖点定虚焦及设置')
            n.setName('_ZDefocus')
            return n

        _add_zdefocus_control(_depth_copy_node)

        def _add_depthfog_control(input):
            node_color = 596044543
            n = load_toolset('Keyer/DepthKeyer')
            n.setInput(0, input)
            n.setName('_DepthFogControl')
            n['label'].setValue('**深度雾总控制**\n在此设置深度雾范围及颜色')
            n['range'].setValue(1)
            n['gl_color'].setValue(node_color)
            n['tile_color'].setValue(node_color)
            n.addKnob(nuke.Text_Knob('颜色控制'))
            n.addKnob(nuke.Color_Knob('fog_color', '雾颜色'))
            n['fog_color'].setValue((0.009, 0.025133, 0.045))

            k = nuke.Double_Knob('fog_mix', 'mix')
            k.setValue(1)
            n.addKnob(k)
            
        _add_depthfog_control(_depth_copy_node)

        def _merge_mp():
            #TODO:add lut;crop
            n = nuke.createNode('Read', 'name MP')
            n['file'].fromUserText(mp)

            n = nuke.createNode('Reformat', 'resize fit')
            n = nuke.createNode('Transform')
            n = nuke.createNode('ColorCorrect')
            n = nuke.createNode('Grade')
            n = nuke.createNode('ProjectionMP')
            n = nuke.createNode('Defocus', 'disable true')
            n = nuke.createNode('Crop', 'box {0 0 {root.width} {root.height}}')
            
            # lut = None
            # filename = nuke.filename(self.bg_ch_nodes[0])
            # lut_dir = os.path.join(os.path.dirname(filename), 'lut')
            # if os.path.exists(lut_dir):
                # lut_list = list(i for i in os.listdir(os.path.normcase(lut_dir)) if i.endswith('.vf') and 'mp' in i.lower())
                # lut = lut_dir + '/' + lut_list[0]
        
            # if lut:
                # print('MergeMP(): {}'.format(lut))
                # self.insertNode(nuke.nodes.Vectorfield(vfield_file=lut, file_type='vf', label='[basename [value this.knob.vfield_file]]'), read_node)
            
            return n
            
        n = nuke.nodes.Merge(inputs=[input, _depth_copy_node], operation='under', label='MP')
        n = load_toolset('Write', inputs=[n])

        

class Comp(object):

    order = lambda self, n: ('_' + self.node_tag_dict[n]).replace('_BG', '1_').replace('_CH', '0_')
    
    def __init__(self, mp=DEFAULT_MP):

        self._last_output = None
        self.node_tag_dict = {}
        self.tag_node_dict = {}
        self.bg_node = None
        self.bg_ch_nodes = []
        self.mp = mp.replace('\\', '/')
        
        # Get dict
        for i in nuke.allNodes('Read'):
            tag = self.getFootageTag(i)
            self.node_tag_dict[i] = tag
            self.tag_node_dict[tag] = i
        if not self.node_tag_dict:
            nuke.message('请先将素材拖入Nuke')
            raise FootageError

        # Get bg_node
        try:
            self.bg_node = self.getNodesByTag('BG')[0]
        except IndexError:
            self.bg_node = None
        
        # Get bg_ch_nodes
        self.bg_ch_nodes = self.getNodesByTag(['BG', 'CH'])
        
        # Set default _last_output
        if self.bg_ch_nodes:
            self._last_output = self.bg_ch_nodes[0]
        else:
            self._last_output = self.node_tag_dict.keys()[0]
    
    def __call__(self):
        self.rename_read_nodes()
        
        # Merge
        self.merge_over()
        self.add_crop()
        self.add_zdefocus()
        self.add_softclip()
        self.add_depthfog()
        self.merge_occ()
        self.merge_shadow()
        self.merge_screen()
        self.add_premult()
        self.add_huecorrect()
        self.add_colorcorrect()
        self.add_unremult()
        self.add_grade()
        self.merge_depth()
        self.add_reformat()
        self.add_depth()
        self.add_keyer()
        self.add_zdefocus_control()
        self.merge_mp()
        
        # Create write node
        self._last_output.selectOnly()
        _Write = nuke.loadToolset(toolset + r"\Write.nk")

        # Set framerange
        try:
            self.setFrameRangeByNode(self.getNodesByTag(['CH', 'BG'])[-1])
        except IndexError:
            nuke.message('没有找到CH或BG\n请手动设置工程帧范围')
        first, last = nuke.Root()['first_frame'].value(), nuke.Root()['last_frame'].value()
        nuke.frame((first + last) // 2.0)
        
        # Set project
        if not nuke.Root()['project_directory'].value():
            nuke.Root()['project_directory'].setValue('[python {nuke.script_directory()}]')
        nuke.Root()['fps'].setValue(fps)
        nuke.Root()['format'].setValue(format)
        
        self.connectViewer()
        
        self.autoplaceAllNodes()
        self.zoomToFitAll()

        self.showPanels()

    def connectViewer(self):
        viewer_node = nuke.toNode('Viewer1')
        if not viewer_node:
            viewer_node = nuke.nodes.Viewer()
        _Write = nuke.toNode('_Write')
        viewer_node.connectInput(0, self._last_output)
        viewer_node.connectInput(1, self._last_output)
        viewer_node.connectInput(2, self._last_output)
        if _Write:
            viewer_node.connectInput(3, _Write)
        
    def getFootageTag(self, n):
        '''
        Figure out node footage type
        '''
        # Deal with footage that have no alpha
        if not 'rgba.alpha' in n.channels():
            return '_OTHER'
        
        if n['name'].value() in tag_convert_dict.values() + REGULAR_TAGS:
            return n['name'].value()
        
        # Try file name
        _filename = os.path.normcase(nuke.filename(n))
        _s = os.path.basename(_filename)
        _pat = re.compile(r'sc.+?_([^.]+)', flags=re.I)
        result = re.search(_pat, _s)
        if result:
            result = result.group(1).upper()
            # Convert tag use dictionary
            if result in tag_convert_dict.keys():
                result = tag_convert_dict[result]
        else:
            result = '_OTHER'
        # Try folder name
        if result not in REGULAR_TAGS:
            folder_name = os.path.basename(os.path.dirname((os.path.normcase(nuke.filename(n)))))
            dir_tag = re.search(_pat, folder_name)
            if dir_tag and dir_tag.group(1).upper() in REGULAR_TAGS:
                result = dir_tag.group(1).upper()
        return result

    def getNodesByTag(self, tags):
        result = []    
        # Convert input param
        if isinstance(tags, str) :
            tags = [tags]
        tags = tuple(map(str.upper, tags))
        # Output result
        for i in self.node_tag_dict.keys():
            if self.node_tag_dict[i].startswith(tags):
                result.append(i)
        result.sort(key=self.order, reverse=True)
        return result

    def setFrameRangeByNode(self, n):
        nuke.Root()['first_frame'].setValue(n['first'].value())
        nuke.Root()['last_frame'].setValue(n['last'].value())
        nuke.Root()['lock_range'].setValue(True)
                    
    def merge_over(self):
        if len(self.bg_ch_nodes) == 0:
            return False
        elif len(self.bg_ch_nodes) == 1:
            self._last_output = nuke.nodes.Dot(inputs=[self.bg_ch_nodes[0]])
        else:
            for i in self.bg_ch_nodes[1:]:
                if not self._last_output:
                    continue
                merge_node = nuke.nodes.Merge2(inputs=[self._last_output, i], label=self.node_tag_dict[i])
                self._last_output = merge_node

    def merge_occ(self):
        try:
            merge_node = None
            for i in self.getNodesByTag('OC'):
                merge_node = nuke.nodes.Merge2(inputs=[self.bg_node, i], operation='multiply', screen_alpha=True, label='OCC')
                self.insertNode(merge_node, self.bg_node)
            return merge_node
        except IndexError:
            return False
            
    def merge_shadow(self):
        try:
            for i in self.getNodesByTag(['SH', 'SD']):
                grade_node = nuke.nodes.Grade(inputs=[self.bg_node, i], white="0.08420000225 0.1441999972 0.2041999996 0.0700000003", white_panelDropped=True, label='Shadow')
                self.insertNode(grade_node, self.bg_node)
        except IndexError:
            return False

    def merge_screen(self):
        try:
            for i in self.getNodesByTag('FOG'):
                reformat_node = nuke.nodes.Reformat()
                for j in self.bg_ch_nodes:
                    if j == self.bg_node:
                        merge_disable = False
                    else:
                        merge_disable = True
                    merge_node = nuke.nodes.Merge2(inputs=[None, i], operation='screen', maskChannelInput='rgba.alpha', label=self.node_tag_dict[i], disable=merge_disable)
                    self.insertNode(merge_node, j)
                self.insertNode(nuke.nodes.Dot(), i)
                self.insertNode(reformat_node, i)
        except IndexError:
            return False

    def merge_depth(self):
        nodes = self.bg_ch_nodes
        if len(nodes) == 1:
            return
        merge_node = nuke.nodes.Merge2(inputs=nodes[:2] + [None] + nodes[2:], tile_color=2184871423L, operation='min', Achannels='depth', Bchannels='depth', output='depth', label='Depth', hide_input=True)
        for i in nodes:
            print('merge_depth():\t\t{}'.format(os.path.basename(i.metadata('input/filename'))))
            depthfix_node = nuke.loadToolset(toolset + r'\Depthfix.nk')
            if self.getMax(i, 'depth.Z') > 1.1 :
                depthfix_node['farpoint'].setValue(10000)
                print('farpoint -> 10000')
            self.insertNode(depthfix_node, i)
            print('')
        copy_node = nuke.nodes.Copy(inputs=[self._last_output, merge_node], from0='depth.Z', to0='depth.Z')
        self.insertNode(copy_node, self._last_output)
        self._last_output = copy_node
        return copy_node

    def add_reformat(self):
        ret = None
        for i in self.bg_ch_nodes:
            reformat_node = nuke.nodes.Reformat()
            self.insertNode(reformat_node, i)
            ret = reformat_node
        return ret
        
    def add_zdefocus(self):
        ret = None
        for i in self.bg_ch_nodes:
            zdefocus_node = nuke.nodes.ZDefocus2(math=nuke.value('_ZDefocus.math', 'depth'), center='{{[value _ZDefocus.center curve]}}', focal_point='inf inf', dof='{{[value _ZDefocus.dof curve]}}', blur_dof='{{[value _ZDefocus.blur_dof curve]}}', size='{{[value _ZDefocus.size curve]}}', max_size='{{[value _ZDefocus.max_size curve]}}', label='[\nset trg parent._ZDefocus\nknob this.math [value $trg.math depth]\nknob this.z_channel [value $trg.z_channel depth.Z]\nif {[exists _ZDefocus]} {return "由_ZDefocus控制"} else {return "需要_ZDefocus节点"}\n]', disable='{{[if {[value _ZDefocus.focal_point "200 200"] == "200 200" || [value _ZDefocus.disable]} {return True} else {return False}]}}', selected=True )
            self.insertNode(zdefocus_node, i)
            ret = zdefocus_node
        return ret
        
    def add_zdefocus_control(self):
        # Use for one-node zdefocus control
        zdefocus_node = nuke.nodes.ZDefocus2(inputs=[self._last_output], math='depth', output='focal plane setup', center=0.00234567, blur_dof=False, label='** 虚焦总控制 **\n在此拖点定虚焦及设置')
        zdefocus_node.setName('_ZDefocus')
        return zdefocus_node
        
    def add_grade(self):
        ret = None
        for i in self.bg_ch_nodes:
            print('add_grade(): \t\t{}'.format(os.path.basename(i.metadata('input/filename'))))
            rgb_max = self.getMax(i, 'rgb')
            erode_size = 0
            erode_node = nuke.nodes.Dilate(inputs=[i], size = erode_size)
            grade_mix = 0.6
            # Exclude small highlight
            while rgb_max > 1 and erode_size > i.height() / -100.0:
                erode_node['size'].setValue(erode_size)
                print('erode_size = {}'.format(erode_size))
                rgb_max = self.getMax(erode_node, 'rgb')
                if rgb_max < 1:
                    if rgb_max < 0.5:
                        grade_mix = 0.3
                    break
                erode_size -= 1
            nuke.delete(erode_node)
            grade_node = nuke.nodes.Grade(whitepoint=rgb_max, unpremult='rgba.alpha', mix=grade_mix, label='最亮值: {}\n混合:[value this.mix]\n使亮度范围靠近0-1'.format(rgb_max))
            self.insertNode(grade_node, i)
            print('')
            ret = grade_node
        return ret
        
    def add_depth(self):
        for i in self.bg_ch_nodes:
            if 'depth.Z' not in i.channels():
                print('add_depth():\t\t{}'.format(os.path.basename(i.metadata('input/filename'))))
                constant_node = nuke.nodes.Constant(channels='depth', color=1, label='**用渲染出的depth层替换这个**\n或者手动指定数值')
                merge_node = nuke.nodes.Merge2(inputs=[None, constant_node], also_merge='all', label='add_depth')
                self.insertNode(merge_node, i)

    def add_colorcorrect(self):
        ret = None
        for i in self.bg_ch_nodes:
            if 'SSS.alpha' in i.channels():
                colorcorrect_node = nuke.nodes.ColorCorrect(label='SSS调整', maskChannelInput='SSS.alpha')
                self.insertNode(colorcorrect_node, i)
            colorcorrect_node = nuke.nodes.ColorCorrect(label='颜色调整', mix_luminance=1)
            self.insertNode(colorcorrect_node, i)
            colorcorrect_node = nuke.nodes.ColorCorrect(label='亮度调整')
            self.insertNode(colorcorrect_node, i)
            ret = colorcorrect_node
        return ret
        
    def add_huecorrect(self):
        ret = None
        for i in self.bg_ch_nodes:
            huecorrect_node = nuke.nodes.HueCorrect()
            self.insertNode(huecorrect_node, i)
            ret = huecorrect_node
        return ret
    
    def add_premult(self):
        premult_node = False
        for i in self.bg_ch_nodes:
            if 'rgba.alpha' in i.channels():
                premult_node = nuke.nodes.Premult()
                self.insertNode(premult_node, i)
        return premult_node

    def add_unremult(self):
        unpremult_node = False
        for i in self.bg_ch_nodes:
            if 'rgba.alpha' in i.channels():
                unpremult_node = nuke.nodes.Unpremult()
                self.insertNode(unpremult_node, i)
        return unpremult_node    

    def add_depthfog(self):
        node_color = 596044543

        # Add _DepthFogControl node
        _DepthFogControl = nuke.loadToolset(toolset + '/Keyer/DepthKeyer.nk')
        _DepthFogControl.setInput(0, self._last_output)
        _DepthFogControl.setName('_DepthFogControl')
        _DepthFogControl['label'].setValue('**深度雾总控制**\n在此设置深度雾范围及颜色')
        _DepthFogControl['range'].setValue(1)
        _DepthFogControl['gl_color'].setValue(node_color)
        _DepthFogControl['tile_color'].setValue(node_color)
        _DepthFogControl.addKnob(nuke.Text_Knob('颜色控制'))
        _DepthFogControl.addKnob(nuke.Color_Knob('fog_color', '雾颜色'))
        _DepthFogControl['fog_color'].setValue((0.009, 0.025133, 0.045))
        k = nuke.Double_Knob('fog_mix', 'mix')
        k.setValue(1)
        _DepthFogControl.addKnob(k)
        
        # Insert depthfog nodes
        for i in self.bg_ch_nodes:
            group_node = nuke.nodes.Group(tile_color=node_color, label='深度雾\n由_DepthFogControl控制', disable='{_DepthFogControl.disable}')
            group_node.setName('DepthFog1')
            group_node.begin()

            input = nuke.nodes.Input(name='Input')

            depthkeyer_node = nuke.loadToolset(toolset + '/Keyer/DepthKeyer.nk')
            depthkeyer_node.setInput(0, input)
            depthkeyer_node['range'].setExpression('_DepthFogControl.range')

            grade_node = nuke.nodes.Grade(inputs=[input, depthkeyer_node], black='{_DepthFogControl.fog_color} {_DepthFogControl.fog_color} {_DepthFogControl.fog_color}', unpremult='rgba.alpha', mix='{_DepthFogControl.fog_mix}')

            output = nuke.nodes.Output(inputs=[grade_node])

            group_node.end()

            self.insertNode(group_node, i)

    def add_softclip(self):
        for i in self.bg_ch_nodes:
            softclip_node = nuke.nodes.SoftClip(conversion=3)
            self.insertNode(softclip_node, i)

    def add_keyer(self):
        keyer_node = False
        for i in self.bg_ch_nodes:
            if 'SSS.alpha' in i.channels():
                keyer_node = nuke.nodes.Keyer(input='SSS', output='SSS.alpha', operation='luminance key', range='0 0.007297795507 1 1')
                self.insertNode(keyer_node, i)
        return keyer_node

    def add_crop(self): 
        ret = None
        for i in self.bg_ch_nodes:
            crop_node = nuke.nodes.Crop(box='0 0 {root.width} {root.height}')
            self.insertNode(crop_node, i)
            ret = crop_node
        return ret
        
        
    def merge_mp(self):
        #TODO:add lut;crop
        read_node = nuke.nodes.Read(file=self.mp)
        read_node.setName('MP')
        merge_node = nuke.nodes.Merge(inputs=[self._last_output, read_node], operation='under', label='MP')
        self._last_output = merge_node
        
        root_width, root_height = nuke.Root().width(), nuke.Root().height()

        self.insertNode(nuke.nodes.Crop(box='0 0 {root.width} {root.height}'), read_node)
        self.insertNode(nuke.nodes.Defocus(disable=True), read_node)
        self.insertNode(nuke.loadToolset(toolset + r'\MP\ProjectionMP.nk'), read_node)
        ramp_node = nuke.nodes.Ramp(p0='1700 1000', p1='1700 500')
        self.insertNode(nuke.nodes.Grade(inputs=[read_node, ramp_node]), read_node)
        self.insertNode(nuke.nodes.ColorCorrect(), read_node)
        
        lut = None
        filename = nuke.filename(self.bg_ch_nodes[0])
        lut_dir = os.path.join(os.path.dirname(filename), 'lut')
        if os.path.exists(lut_dir):
            lut_list = list(i for i in os.listdir(os.path.normcase(lut_dir)) if i.endswith('.vf') and 'mp' in i.lower())
            lut = lut_dir + '/' + lut_list[0]
        
        if lut:
            print('MergeMP(): {}'.format(lut))
            self.insertNode(nuke.nodes.Vectorfield(vfield_file=lut, file_type='vf', label='[basename [value this.knob.vfield_file]]'), read_node)
        self.insertNode(nuke.nodes.Transform(center='{} {}'.format(root_width / 2.0, root_height / 2.0), label='**在此调整MP位置**'), read_node)
        self.insertNode(nuke.nodes.Reformat(resize='fit'), read_node)
    
    def rename_read_nodes(self):
        for i in nuke.allNodes('Read'):
            if i in self.node_tag_dict:
                i.setName(self.node_tag_dict[i], updateExpressions=True)

    def showPanels(self):
        nuke.nodes.NoOp(label='[\npython {nuke.show(nuke.toNode(\'_ZDefocus\'))}\ndelete this\n]')

    def insertNode(self, node, input_node):
        # Create dot presents input_node 's output
        input_node.selectOnly()
        dot = nuke.createNode('Dot')
        
        # Set node connection
        node.setInput(0, input_node)
        dot.setInput(0, node)
        
        # Delete dot
        nuke.delete(dot)

    def autoplaceAllNodes(self):
        nuke.nodes.NoOp(label='[\npython {map(lambda n: nuke.autoplace(n), nuke.allNodes(group=nuke.Root()))}\ndelete this\n]')

    def clearNodeSelect(self):
        dot = nuke.nodes.Dot()
        dot.selectOnly()
        nuke.delete(dot)

    def zoomToFitAll(self):
        self.clearNodeSelect()
        nuke.nodes.NoOp(label='[\npython {nuke.zoomToFitSelected()}\ndelete this\n]')

    def getMax(self, n, channel='depth.Z' ):
        '''
        Return themax values of a given node's image at middle frame
        @parm n: node
        @parm channel: channel for sample
        '''
        # Get middle_frame
        middle_frame = (n.frameRange().first() + n.frameRange().last()) // 2
        
        # Create nodes
        invert_node = nuke.nodes.Invert( channels=channel, inputs=[n])
        mincolor_node = nuke.nodes.MinColor( channels=channel, target=0, inputs=[invert_node] )
        
        # Execute
        try:
            nuke.execute( mincolor_node, middle_frame, middle_frame )
            max_value = mincolor_node['pixeldelta'].value() + 1
        except RuntimeError, e:
            if 'Read error:' in str(e):
                max_value = -1
            else:
                raise RuntimeError, e
                
        # Avoid dark frame
        if max_value < 0.7:
            nuke.execute( mincolor_node, n.frameRange().last(), n.frameRange().last() )
            max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)
        if max_value < 0.7:
            nuke.execute( mincolor_node, n.frameRange().first(), n.frameRange().first() )
            max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)
            
        # Delete created nodes
        for i in ( mincolor_node, invert_node ):
            nuke.delete( i )

        # Output
        print('getMax({1}, {0}) -> {2}'.format(channel, n.name(), max_value))
        
        return max_value

class MultiComp(object):
    shot_pat = re.compile(r'^.+\\.+_sc[^_]+$', flags=re.I)
    footage_pat = re.compile(r'^.+_sc.+_.+\..+$', flags=re.I)

    footage_filter = lambda self, s: not any(map(lambda excluded_word: excluded_word in s, ['副本', '.lock']))
    
    def __init__(self, dir_=None, target_dir=None, mp=DEFAULT_MP, footage_pat=r'^.+_sc.+_.+\..+$', dir_pat=r'.+',):

        self.dir = ''
        self.target_dir = ''
        self.shot_list = [] # Contain shot dir
        self.footage_dict = {}
        self.mp = mp
        self.dir = dir_
        self.target_dir = target_dir
        self.footage_pat = re.compile(footage_pat, flags=re.I)
        self.dir_pat = re.compile(dir_pat, flags=re.I)

    def __call__(self):

        # Get shot list
        if re.match(self.shot_pat, self.dir):
            self.shot_list = [self.dir]
        else:
            dirs = [self.dir + '\\' + x for x in os.listdir(self.dir)]
            dirs = filter(lambda dir : re.match(self.shot_pat, dir), dirs)
            dirs.sort()
            self.shot_list = dirs


        self.shots_number = len(self.shot_list)
        print_('全部镜头:\n{0}\n总计:\t{1}'.format('\n'.join(self.shot_list), self.shots_number))
        print('')
        for i in range(5)[::-1]:
            sys.stdout.write('\r\r{:2d}'.format(i+1))
            time.sleep(1)
        sys.stdout.write('\r          ')
        
        self.compAll()
        
        cmd = 'EXPLORER /select,"{}\\批量预合成.log"'.format(argv[2].strip('"')).decode(script_codec).encode(SYS_CODEC)
        call(cmd)
        choice = call(u'CHOICE /t 15 /d y /m "此窗口将自动关闭"'.encode(SYS_CODEC))
        if choice == 2:
            call('PAUSE', shell=True)
    
    def compAll(self):  
        error_list = []

        count = 0
        for shot_dir in self.shot_list:
            shot = os.path.basename(shot_dir)
            nk_filename = (self.target_dir + '/' + shot + '.nk').replace('\\', '/')

            count += 1
            print('\n## [{1}/{2}]:\t\t{0}'.format(shot, count, self.shots_number))
            
            if os.path.exists(nk_filename):
                print_('**提示** 已存在{}, 将直接跳过\n'.format(nk_filename))
                continue

            try:
                
                # Comp
                nuke.scriptClear()
                self.importFootage(shot_dir)
                Comp(self.mp)()

                # Save nk
                print_('保存为:\n\t\t\t{}\n'.format(nk_filename))
                nuke.Root()['name'].setValue(nk_filename)
                nuke.scriptSave(nk_filename)

                # Render Single Frame
                write_node = nuke.toNode('_Write')
                if write_node:
                    write_node = write_node.node('Write_JPG_1')
                    write_node['disable'].setValue(False)
                    frame = int(nuke.numvalue('_Write.knob.frame'))
                    try:
                        nuke.execute(write_node, frame, frame)
                    except RuntimeError:
                        try: nuke.execute(write_node, write_node.firstFrame(), write_node.firstFrame())
                        except RuntimeError:
                            try:
                                nuke.execute(write_node, write_node.lastFrame(), write_node.lastFrame())
                            except RuntimeError:
                                error_list.append('{}:\t渲染出错'.format(shot))
            except FootageError:
                error_list.append('{}:\t没有素材'.format(shot))
            except:
                error_list.append('{}:\t未知错误'.format(shot))
                traceback.print_exc()
        info = '错误列表:\n{}\n总计:\t{}'.format('\n'.join(error_list), len(error_list))
        print('')
        print_(info)
        with open(str(self.target_dir+'/批量预合成.log').decode(script_codec).encode(SYS_CODEC), 'w') as log:
            log.write('总计镜头数量:\t{}\n'.format(self.shots_number))
            log.write(info)

    def showDialog(self):
        # Set panel 
        p = nuke.Panel('Precomp')
        p.addFilenameSearch('存放素材的文件夹', 'Z:\SNJYW\Render\EP')
        p.addFilenameSearch('存放至', 'E:\precomp')
        p.addFilenameSearch('指定MP', DEFAULT_MP)
        p.addSingleLineInput('素材名正则', r'^.+_sc.+_.+\..+$')
        p.addSingleLineInput('文件夹名正则', r'^.*[^\\]{8,}$')

        # Show panel
        ok = p.show()
        if ok:
            cmd = 'START "precomp" "{nuke}" -t "{script}" "{footage_path}" "{save_path}" "{mp}" "{footage_pat}" "{dir_pat}"'.format(nuke=nuke.env['ExecutablePath'], script=os.path.normcase(__file__).rstrip('c'), footage_path=p.value('存放素材的文件夹'), save_path=p.value('存放至'), mp=p.value('指定MP'), footage_pat=p.value('素材名正则'), dir_pat=p.value('文件夹名正则'))
            print(cmd)
            if os.path.exists(p.value('存放素材的文件夹')):
                call(cmd, shell=True)
            else:
                nuke.message('素材路径不存在')
        else:
            return False

    def importFootage(self, shot_dir):
        # Get all subdir
        dirs = [x[0] for x in os.walk(shot_dir)]
        print_('导入素材:')
        for d in dirs:
            # Get footage in subdir
            print_('文件夹 {}:'.format(d))
            footages = nuke.getFileNameList(d)
            if not re.match(self.dir_pat, d):
                print_('\t\t\t不匹配文件夹正则, 跳过\n'.format(d))
                continue
            if footages:
                # Filtring
                footages = filter(self.footage_filter, footages)
                footages = filter(lambda path: re.match(self.footage_pat, path), footages)
                # Create read node for every footage
                for f in footages:
                    nuke.createNode( 'Read', "file {" + d + '/' + f + "}") 
                    print('\t' * 3 + f)
            print('')
        print('')

    def importCamera(self):
        pass

Precomp = MultiComp

class FootageError(Exception):
    def __init__(self, *args):
        self.tags = args
        if nuke.env['gui']:
            nuke.message('找不到合成所需的素材: {}'.format(';'.join(self.tags)))
        else:
            print("**错误** - 没有找到素材: {}".format(';'.join(self.tags)).encode(SYS_CODEC))
            
    def __str__(self):
        return ';'.join(self.tags)

def precomp_arnold():
    # set a ordered list of input layer
    layerlist = ['indirect_diffuse', 'direct_diffuse', 'indirect_specular', 'direct_specular', 'reflection',
                 'refraction',
                 'AO', 'depth', 'MV', 'alpha']
    gradelayers = ['indirect_diffuse', 'direct_diffuse', 'indirect_specular', 'direct_specular', 'reflection',
                   'refraction',
                   'AO']
    # Get The Layers Of Selected Read Node

    orderedmerge = []

    Read = nuke.selectedNode()
    layers = nuke.layers(Read)

    for i in layerlist:
        for n in layers:
            if i == n:
                orderedmerge.append(i)

    for o in orderedmerge:
        for l in layers:
            if l == o:
                layers.remove(l)

    layers.remove('rgba')
    layers.remove('rgb')
    orderedshow = layers

    ################Create Shuffle########################################

    x = Read['xpos'].getValue()
    y = Read['ypos'].getValue()

    shufflegroup = []
    gradegroup = []
    dotYgroup = []
    mergegroup = []
    for k in orderedmerge:
        shuffle = nuke.nodes.Shuffle(name=k, postage_stamp=1, note_font_size=25)
        shuffle.setInput(0, Read)
        shuffle.knob('in').setValue(k)
        num = int(orderedmerge.index(k))
        shuffle.setXYpos(int(x + 150 * num), int(y + 250))
        shuffleX = shuffle['xpos'].getValue()
        shuffleY = shuffle['ypos'].getValue()
        shufflegroup.append(shuffle)

        ###Create Grade###
        if num < 7:
            gradenode = nuke.nodes.Grade(name=k, note_font_size=15)
            gradenode.setInput(0, shuffle)
            gradegroup.append(gradenode)
        else:
            pass

        ###Create Dot#####

        if num >= 1 and num < 7:
            dot = nuke.nodes.Dot(name=k, label=k, note_font_size=25)
            dot.setInput(0, gradenode)
            dot.setXYpos(int(shuffleX + 34), int(shuffleY + 180 * num))
            dotX = dot['xpos'].getValue()
            dotY = dot['ypos'].getValue()
            dotYgroup.append(dotY)

        elif num > 6:
            dot = nuke.nodes.Dot(name=k, label=k, note_font_size=25)
            dot.setInput(0, shuffle)
            dot.setXYpos(int(shuffleX + 34), int(shuffleY + 180 * num))
            dotX = dot['xpos'].getValue()
            dotY = dot['ypos'].getValue()
            dotYgroup.append(dotY)

        ###Create Merge####

        if num < 1:
            pass
        elif num > 0 and num < 2:
            merge = nuke.nodes.Merge(name=k, operation='plus', mix=1, inputs=[gradegroup[0], dot], note_font_size=15)
            merge.setXYpos(int(x), int(dotY - 6))
            mergegroup.append(merge)
        elif num > 1 and num < 6:
            merge = nuke.nodes.Merge(name=k, operation='plus', mix=1, inputs=[mergegroup[num - 2], dot],
                                     note_font_size=15)
            mergegroup.append(merge)
            merge.setXYpos(int(x), int(dotY - 6))
        elif num > 5 and num < 7:
            merge = nuke.nodes.Merge(name=k, operation='multiply', mix=0.15, inputs=[mergegroup[num - 2], dot],
                                     note_font_size=15)
            mergegroup.append(merge)
            merge.setXYpos(int(x), int(dotY - 6))
        elif num > 6 and num < 8:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='depth.Z', inputs=[mergegroup[num - 2], dot],
                                   note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 14))
        elif num > 7 and num < 9:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='MV.red', from1='rgba.green', to1='MV.green',
                                   inputs=[mergegroup[num - 2], dot], note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 26))
        elif num > 8 and num < 10:
            copy = nuke.nodes.Copy(name=k, from0='rgba.red', to0='rgba.alpha', inputs=[mergegroup[num - 2], dot],
                                   note_font_size=15)
            mergegroup.append(copy)
            copy.setXYpos(int(x), int(dotY - 14))
            ###Create show Layers####

    for element in orderedshow:
        num += 1
        shuffle = nuke.nodes.Shuffle(name=element, postage_stamp=1, note_font_size=25)
        shuffle.setInput(0, Read)
        shuffle.knob('in').setValue(element)
        shuffle.setXYpos(int(x + 150 * num), int(y + 250))

    nuke.connectViewer(0, mergegroup[-1])

def print_(obj):
    print(str(obj).encode(SYS_CODEC))

def insert_node(node, input_node):
    input_node.selectOnly()
    dot = nuke.createNode('Dot')

    node.setInput(0, input_node)
    dot.setInput(0, node)

    nuke.delete(dot)

def load_toolset(name, dir='../../ToolSets/WLF', inputs=None):
    _toolset_node = nuke.loadToolset(os.path.join(dir, '{}.nk'.format(name)))
    if _toolset_node and inputs:
        for i, n in enumerate(inputs):
            _toolset_node.setInput(i, n)
    
    return _toolset_node

def load_gizmo(name, inputs=None):
    _gizmo = nuke.load(name)
    if _gizmo and inputs:
        for i, n in enumerate(inputs):
            _gizmo.setInput(i, n)

    return _gizmo

def get_max(n, channel='depth.Z' ):
    '''
    Return themax values of a given node's image at middle frame
    @parm n: node
    @parm channel: channel for sample
    '''
    # Get middle_frame
    middle_frame = (n.frameRange().first() + n.frameRange().last()) // 2
    
    # Create nodes
    invert_node = nuke.nodes.Invert( channels=channel, inputs=[n])
    mincolor_node = nuke.nodes.MinColor( channels=channel, target=0, inputs=[invert_node] )
    
    # Execute
    try:
        nuke.execute( mincolor_node, middle_frame, middle_frame )
        max_value = mincolor_node['pixeldelta'].value() + 1
    except RuntimeError, e:
        if 'Read error:' in str(e):
            max_value = -1
        else:
            raise RuntimeError, e
            
    # Avoid dark frame
    if max_value < 0.7:
        nuke.execute( mincolor_node, n.frameRange().last(), n.frameRange().last() )
        max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)
    if max_value < 0.7:
        nuke.execute( mincolor_node, n.frameRange().first(), n.frameRange().first() )
        max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)
        
    # Delete created nodes
    for i in ( mincolor_node, invert_node ):
        nuke.delete( i )

    # Output
    print('getMax({1}, {0}) -> {2}'.format(channel, n.name(), max_value))
    
    return max_value

def main():
    argv = list(map(lambda s: os.path.normcase(s).rstrip('\\/'), sys.argv))

    call(u'CHCP 936 & TITLE 批量预合成_吾立方 & CLS'.encode(SYS_CODEC), shell=True)
    print_('{:-^50s}'.format('确认设置'))
    print_('素材路径:\t\t{0[1]}\n保存路径:\t\t{0[2]}\nMP:\t\t\t{0[3]}\n素材名正则匹配:\t\t{0[4]}\n文件夹名正则匹配:\t{0[5]}'.format(argv))

    if not os.path.exists(argv[2]):
        os.makedirs(argv[2])
        print('Created:\t{}'.format(argv[2]))
    print('')
    for i in range(5)[::-1]:
        sys.stdout.write('\r{:2d}'.format(i+1))
        time.sleep(1)
    sys.stdout.write('\r          ')
    print('')

    Precomp(argv[1], argv[2], argv[3], argv[4], argv[5])()

if __name__ == '__main__' and  len(sys.argv) == 6:
    try:
        main()
    except SystemExit as e:
        exit(e)
    except:
        import traceback
        traceback.print_exc()
if __name__ == '__main__':
    try:
        comp_wlf(autograde=False)
    except SystemExit as e:
        exit(e)
    except:
        import traceback
        traceback.print_exc()
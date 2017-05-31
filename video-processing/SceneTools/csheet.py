# usr/bin/env python
# -*- coding=UTF-8 -*-

import os
import sys
import re
import time
import subprocess
from subprocess import call
import nuke

VERSION = 2.12

argvs = sys.argv
prompt_codec = 'gbk'
script_codec = 'UTF-8'
file_name = None

def print_(obj):
    print(str(obj).decode(script_codec).encode(prompt_codec))

def pause():
    call('PAUSE', shell=True)

class Contactsheet(object):

    last_output = None
    backdrop_read_node = None
    read_nodes = None
    shot_width, shot_height = 1920, 1080
    contactsheet_shot_width, contactsheet_shot_height = 1920, 1160

    def __init__(self, image_dir='images'):

        self.image_list = self.getImageList(image_dir)
        self.image_dir = image_dir.replace('\\', '/')
        self.read_nodes = []
        self.jpg_output = None

        self.main()
        
        global image
        image = self.jpg_output
        
    def main(self):

        nuke.Root()['project_directory'].setValue(os.getcwd().replace('\\', '/'))

        self.createReadNodes()
        self.Contactsheet()
        self.createBackdrop('灯光合成模板_底板.jpg')
        self.mergeBackdrop()
        self.modifyShot()
        self.modifyBackdrop()
        #nuke.scriptSave('E:\\temp.nk')
        self.writeJPG()
        return 

    def Contactsheet(self):
        contactsheet_node = nuke.nodes.Csheet(inputs=self.read_nodes, width='{rows*shot_format.w+gap*(rows+1)}', height='{columns*shot_format.h+gap*(columns+1)}', rows='{{ceil(pow([inputs this], 0.5))}}', columns='{rows}', gap=50, roworder='TopBottom')
        contactsheet_node.addKnob(nuke.WH_Knob('shot_format'))
        contactsheet_node['shot_format'].setValue([self.contactsheet_shot_width, self.contactsheet_shot_height])
        contactsheet_node.setName('_Csheet')
        self.contactsheet_node = contactsheet_node
        return contactsheet_node
    
    def createReadNodes(self):
        for i in self.image_list:
            read_node = nuke.nodes.Read(file=self.image_dir + '/' + i)
            if read_node.hasError():
                nuke.delete(read_node)
                print_('排除:\t\t\t{} (不能读取)'.format(i))
            else:
                self.read_nodes.append(read_node)

    def createBackdrop(self, image='灯光合成模板_底板.jpg'):
        if os.path.exists(os.path.abspath(image.decode(script_codec).encode(prompt_codec))):
            read_node = nuke.nodes.Read(file=image)
            self.backdrop_read_node = read_node
            print_('使用背板:\t\t{}'.format(image))
            return read_node
        else:
            self.backdrop_read_node = nuke.nodes.Constant()
            print_('**提示**\t\t找不到背板文件,将用纯黑代替')
            return False

    def getImageList(self, dir='images'):
        image_list = list(i.decode(prompt_codec).encode(script_codec) for i in os.listdir(dir))

        if not image_list:
            raise FootageError
        
        # Exclude excess image
        mtime = lambda file: os.stat(dir + '\\' + file.decode(script_codec). encode(prompt_codec)).st_mtime
        image_list.sort(key=mtime, reverse=True)
        getShotName = lambda file_name : file_name.split('.')[0].rstrip('_proxy').lower()
        shot_list = []
        result = []
        for image in image_list:
            shot = getShotName(image)
            if shot in shot_list:
                print_('排除:\t\t\t{} (较旧)'.format(image))
            else:
                shot_list.append(shot)
                print_('包含:\t\t\t{}'.format(image))
                result.append(image)
        result.sort()
        print_('总计图像数量:\t\t{}'.format(len(image_list)))
        print_('总计有效图像:\t\t{}'.format(len(result)))
        print_('总计镜头数量:\t\t{}'.format(len(shot_list)))
        return result
    
    def mergeBackdrop(self):
        merge_node = nuke.nodes.Merge2(inputs=[self.backdrop_read_node, self.contactsheet_node])
        _reformat_backdrop_node = nuke.nodes.Reformat(type='scale', scale='{_Csheet.width/input.width*backdrop_scale}')
        k = nuke.Double_Knob('backdrop_scale', '背板缩放')
        k.setValue(1.13365)
        _reformat_backdrop_node.addKnob(k)
        _reformat_backdrop_node.setName('_Reformat_Backdrop')
        insertNode(_reformat_backdrop_node, self.backdrop_read_node)
        insertNode(nuke.nodes.Transform(translate='{1250*_Reformat_Backdrop.scale} {100*_Reformat_Backdrop.scale}', center='{input.width/2} {input.height/2}'), self.contactsheet_node)
        self.last_output = merge_node
        return merge_node
        
    def modifyShot(self):
        nuke.addFormat('{} {} contactsheet_shot'.format(self.contactsheet_shot_width, self.contactsheet_shot_height))
        for i in self.read_nodes:
            reformat_node = nuke.nodes.Reformat(format='contactsheet_shot',center=False, black_outside=True)
            transform_node = nuke.nodes.Transform(translate='0 {}'.format(self.contactsheet_shot_height-self.shot_height))
            text_node = nuke.nodes.Text2(message='[lrange [split [basename [metadata input/filename]] ._] 3 3]', box='0 0 0 80', color='0.145 0.15 0.14 1')
            insertNode(text_node, i)
            insertNode(transform_node, i)
            insertNode(reformat_node, i)
        
    def modifyBackdrop(self):
        nuke.addFormat('11520 6480 backdrop')
        reformat_node = nuke.nodes.Reformat(format='backdrop')
        if EP:
            if EP.startswith('EP'):
                ep = EP[2:]
            else:
                ep = EP
            insertNode(nuke.nodes.Text2(message=ep, box='288 6084 1650 6400', xjustify='center', yjustify='center', global_font_scale=3, color='0.155'), self.backdrop_read_node)
        if SCENE:
            insertNode(nuke.nodes.Text2(message=SCENE, box='288 4660 1650 5000', xjustify='center', yjustify='center', global_font_scale=3, color='0.155'), self.backdrop_read_node)
        insertNode(reformat_node, self.backdrop_read_node)
        
    def writeJPG(self):
        write_node = nuke.nodes.Write(inputs=[self.last_output], file=file_name, file_type='jpg', _jpeg_quality='1', _jpeg_sub_sampling='4:4:4')
        print_('输出色板:\t\t{}'.format(file_name))
        nuke.render(write_node, 1, 1)
        self.jpg_output = os.path.abspath(file_name)
        return file_name

def insertNode(node, input_node):
    # Create dot presents input_node 's output
    input_node.selectOnly()
    dot = nuke.createNode('Dot')
    
    # Set node connection
    node.setInput(0, input_node)
    dot.setInput(0, node)
    
    # Delete dot
    nuke.delete(dot)

class FootageError(Exception):
    def __init__(self):
        print_('\n**错误** - 在images文件夹中没有可用图像\n')

def downlowdImages():
    if self.isDownload:
        print_('下载文件自:\t\t{}'.format(self.image_download_path))
        subprocess.call(['XCOPY', '/Y', '/D', '/I', '/V', self.image_download_path, 'images'])

def uploadCsheet():
    if self.isUpload:
        if not os.path.exists(self.image_upload_path):
            os.mkdir(self.image_upload_path)
        print_('上传文件至:\t\t{}'.format(self.image_upload_path))
        subprocess.call(['XCOPY', '/Y', '/D', '/I', '/V', self.file_name, self.image_upload_path])

def main(config=None):
    try: 
        try:
            dir = sys.argv[1]
        except IndexError:
            dir = 'images'
        Contactsheet('images')
    except ImportError:
        call('CHCP 936 & TITLE 生成色板_v{} & CLS'.format(VERSION), shell=True)

        downlowdImages()
        Contactsheet('images')
        uploadCsheet()

        if config['isCsheetOpen']:
            call(u'EXPLORER "{}"'.format(image).encode(prompt_codec))

        if not config:
            from config import Config
            config = Config().config
        call('"{}" -t "{}"'.format(config['NUKE'], __file__), shell=True)


if __name__ == '__main__':
    try:
        main()
    except FootageError:
        pause()
    except:
        import traceback
        traceback.print_exc()
        pause()
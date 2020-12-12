import bpy
import numpy as np
from numpy.lib.stride_tricks import as_strided 

import time

class blImage():
    pixels = None
    image = None
    height = 0
    width = 0
    def __init__(self, name):
        try:
            self.image = bpy.data.images[name]
            self.width, self.height = self.image.size
            self.pixels = np.zeros(self.height*self.width*4, dtype=np.float32)
            self.image.pixels.foreach_get(self.pixels)
            self.pixels = np.reshape(self.pixels, (self.height, self.width, 4) )
            
        except:
            print('no image.')

    def update(self):
        self.image.pixels.foreach_set(self.pixels.flatten().ravel().astype(np.float32))
        self.image.preview.reload()
        

#畳み込み積分フィルタ
def convolve2d(img, kernel):
    sub_shape = tuple(np.subtract(img.shape, kernel.shape) + 1) #フィルタ行列の大きさ
    submatrices = as_strided(img,kernel.shape + sub_shape,img.strides * 2) #サブ行列（注目ピクセル近傍イメージ）
    convolved_matrix = np.einsum('ij,ijkl->kl', kernel, submatrices)
    return convolved_matrix


#新規画像を作成する
def CreateNewImage(context, name='NewImage', width=1024, height=1024, use_alpha = True):
    context.area.spaces.active.image = bpy.data.images.new(name = name, width=width, height=height, alpha = use_alpha)
    return context.area.spaces.active.image.name


def FillColor(context, color=(1.0, 1.0, 1.0, 1.0) ):
    img = blImage(context.area.spaces.active.image.name)
    img.pixels[:,:]= color
    img.update()
    


def RGB2Gray(img):
    gray_fac = (0.2126, 0.7152, 0.0722, 0.0)
    return np.einsum('ijk,k->ij',img, gray_fac, optimize='greedy') 

def createGrayImage(context):
    orgImg = blImage(context.area.spaces.active.image.name)
    DestName = context.area.spaces.active.image.name + '_Gray'
    CreateNewImage(context, DestName, orgImg.width, orgImg.height)
    destImg = blImage(DestName)
    grayImg = RGB2Gray(orgImg.pixels)

    result = np.einsum( 'ij,k->ijk', grayImg, (1., 1., 1., .0) ,optimize='greedy') 
    result[:,:,3] = 1.0

    destImg.pixels = result
    destImg.update()




#とりあえずグレイスケール化しての移動平均ぼかしになってる
def MoveMeanImage(context):
    orgImg = blImage(context.area.spaces.active.image.name)
    DestName = context.area.spaces.active.image.name + '_Nomal'
    DestName = CreateNewImage(context, DestName, orgImg.width, orgImg.height)
    destImg = blImage(DestName)


    grayImg = RGB2Gray(orgImg.pixels)
    kernel_size = 5
    kernel = np.ones( (kernel_size,kernel_size)) /(kernel_size*kernel_size) 
    result = convolve2d(grayImg, kernel)
    col0 = result[0]
    colE = result[-1]


    for i in range(int(kernel_size /2)):
        result = np.vstack([col0,result])
        result = np.vstack([result,colE])

    row0 = result[:,0].reshape(-1,1)
    rowE = result[:,-1].reshape(-1,1)

    for i in range(int(kernel_size /2)):
        result = np.hstack([row0,result])
        result = np.hstack([result,rowE])


    destImg.pixels[..., 0] = result
    destImg.pixels[..., 1] = result
    destImg.pixels[..., 2] = result
    destImg.pixels[..., 3] = 1.0
    destImg.update()


def createNomalImage(context):
    orgImg = blImage(context.area.spaces.active.image.name)
    DestName = context.area.spaces.active.image.name + '_Nomal'
    DestName = CreateNewImage(context, DestName, orgImg.width, orgImg.height)
    destImg = blImage(DestName)


    grayImg = RGB2Gray(orgImg.pixels)
    kernel_size = 5
    kernel = np.ones( (kernel_size,kernel_size)) /(kernel_size*kernel_size) 
    result = convolve2d(grayImg, kernel)
    col0 = result[0]
    colE = result[-1]


    for i in range(int(kernel_size /2)):
        result = np.vstack([col0,result])
        result = np.vstack([result,colE])

    row0 = result[:,0].reshape(-1,1)
    rowE = result[:,-1].reshape(-1,1)

    for i in range(int(kernel_size /2)):
        result = np.hstack([row0,result])
        result = np.hstack([result,rowE])


    destImg.pixels[..., 0] = result
    destImg.pixels[..., 1] = result
    destImg.pixels[..., 2] = result
    destImg.pixels[..., 3] = 1.0
    destImg.update()
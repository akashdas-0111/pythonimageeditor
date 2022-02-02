from winreg import LoadKey
from image import Image
import numpy as np

def adjust_brightness(image,factor):
    x_pixels,y_pixels,num_channels=image.array.shape
    new_im=Image(x_pixels=x_pixels,y_pixels=y_pixels,num_channels=num_channels)
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x,y,c]=image.array[x,y,c]*factor
    new_im.array=image.array*factor

    return new_im

def adjust_constrast(image,factor,mid=0.5):
    x_pixels,y_pixels,num_channels=image.array.shape
    new_im=Image(x_pixels=x_pixels,y_pixels=y_pixels,num_channels=num_channels)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x,y,c]=(image.array[x,y,c]-mid)*factor+mid

    # new_im.array=(mid.array-mid)*factor+mid  
    return new_im      


def blur(image,kernal_size):
    x_pixels,y_pixels,num_channels=image.array.shape
    new_im=Image(x_pixels=x_pixels,y_pixels=y_pixels,num_channels=num_channels)
    
    neighbour_range=kernal_size//2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total=0
                for x_i in range(max(0,x-neighbour_range),min(x_pixels-1,x+neighbour_range)+1):
                    for y_i in range(max(0,y-neighbour_range),min(y_pixels-1,y+neighbour_range)+1):
                        total+=image.array[x_i,y_i,c]
                new_im.array[x,y,c]=total/(kernal_size**2)

    return new_im


def apply_kernal(image,kernal):
    x_pixels,y_pixels,num_channels=image.array.shape
    new_im=Image(x_pixels=x_pixels,y_pixels=y_pixels,num_channels=num_channels)
    kernal_size=kernal.shape[0]
    neighbour_range=kernal_size//2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total=0
                for x_i in range(max(0,x-neighbour_range),min(x_pixels-1,x+neighbour_range)+1):
                    for y_i in range(max(0,y-neighbour_range),min(y_pixels-1,y+neighbour_range)+1):
                        x_k=x_i+neighbour_range-x
                        y_k=y_i+neighbour_range-y
                        kernal_val=kernal[x_k,y_k]
                        total+=image.array[x_i,y_i,c]*kernal_val
                new_im.array[x,y,c]=total

    return new_im

def combine_image(image1,image2):
    x_pixels,y_pixels,num_channels=image1.array.shape
    new_im=Image(x_pixels=x_pixels,y_pixels=y_pixels,num_channels=num_channels)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x,y,c]=(image1.array[x,y,c]**2+image2.array[x,y,c]**2)**0.5

    return new_im
if __name__ =='__main__':
    lake=Image(filename='lake.png')
    city=Image(filename='city.png')

    # brightened_im=adjust_brightness(lake,5.5)
    # brightened_im.write_image('brightened.png')

    # darkened_im=adjust_brightness(lake,0.1)
    # darkened_im.write_image('dull1.jpg')

    # incr_contrast=adjust_constrast(lake,2,0.5)
    # incr_contrast.write_image('incrcontrast2.png')

    # dec_contrast=adjust_constrast(city,0.5,0.5)
    # dec_contrast.write_image('deccontrast.png')

    # blur_3=blur(city,20)
    # blur_3.write_image('blurimg.png')

    sobel_x_kernal = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    sobel_y_kernal= np.array([[1,0,-1],[2,0,-2],[1,0,-1]])

    sobel_x=apply_kernal(city,sobel_x_kernal)
    # sobel_x.write_image('edge_x.png')
    sobel_y=apply_kernal(city,sobel_y_kernal)
    # sobel_x.write_image('edge_y.png')


    sobel_xy=combine_image(sobel_x,sobel_y)
    sobel_xy.write_image('edge_xy.png')
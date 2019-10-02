import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import csv, math, png
from copy import copy, deepcopy
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def visualization():
    path = input("Enter file path: ")

    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]
        print(row_data)




# TODO falta agregarlo al pipeline
def normalized_visibilities():
    path = '/home/hperez/Desktop/uv_values_0.csv'
    total = 0


    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]
        if(len(row_data) == 10):
            if row_data[0] == '9':
                # TODO segun Miguel falta agregar la raiz y dividir por el numero de visibilidades
                total += (float(row_data[7]) ** 2) + (float(row_data[8]) ** 2)

    print(total) #6609480360.685198


def extract_values_from_fits():
    fits_path = '/home/hperez/workspace/Github/lambda_pred/data/output.fits'

    hdu_list = fits.open(fits_path)
    hdu_list.info()

    image_data = hdu_list[0].data
    print(image_data)
    print(type(image_data))
    print(image_data.shape)

    print("Min:   ", np.min(image_data))
    print("Max:   ", np.max(image_data))
    print("Mean:  ", np.mean(image_data))
    print("Stdev: ", np.std(image_data))

    sum = np.sum(image_data)
    print("Sum:      ", sum)
    print("Sum ** 2: ", sum**2)

def hermitian_matrix():
    csv_path = '/home/hperez/Desktop/gridded_uv_values.csv'
    csv_full = '/home/hperez/Desktop/gridded_uv_full.csv'

    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]
    f.close()
    
    new_data = deepcopy(data)

    with open(csv_full, 'w') as f:
        for i in range(len(data)):
            writer = csv.writer(f)
            writer.writerow(data[i])

            u = float(new_data[i][0]) * -1
            v = float(new_data[i][1]) * -1
            Vo_y = float(new_data[i][3]) * -1

            new_data[i][0] = str(u)
            new_data[i][1] = str(v)
            new_data[i][3] = str(Vo_y)

            writer_new = csv.writer(f)
            writer_new.writerow(new_data[i])
    f.close()

def apply_ifft2d():
    csv_full = '/home/hperez/Desktop/co65_grideado/gridded_uv_full.csv'
    with open(csv_full) as f:
        reader = csv.reader(f)
        next(reader) #Only if first line has the data description
        data = [r for r in reader]
    f.close()

    N = 256
    M = 256

    deltau = 8.733250 
    deltav = 8.733250 #en co65 

    uvgrid = np.zeros((N, M)) + 1j*np.zeros((N, M))

    for i in range(len(data)):
        u_pixel = int(np.floor(0.5 + float(data[i][0])/deltau) + N/2)
        v_pixel = int(np.floor(0.5 + float(data[i][1])/deltav) + M/2)
        uvgrid[v_pixel, u_pixel] += float(data[i][2]) + 1j*float(data[i][3])

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.imshow(uvgrid.real, interpolation='bilinear', cmap=cm.Greys_r)

    ax2 = fig.add_subplot(122)
    ax2.imshow(uvgrid.imag, interpolation='bilinear', cmap=cm.Greys_r)
    
    plt.show()

    dirty_image = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(uvgrid)))
    
    img = Image.fromarray(dirty_image, 'L')
    img.save('/home/hperez/Desktop/img.png')
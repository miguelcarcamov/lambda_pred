import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def visualization():
    path = input("Enter file path: ")

    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]
        print(row)




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

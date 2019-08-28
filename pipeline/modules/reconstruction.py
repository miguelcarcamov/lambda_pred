import os, sys, subprocess, time
import numpy as np


def create_directory(directory = ""):
    if os.path.exists(directory) == False:
        os.mkdir(directory)
        #sys.exit(directory, " path directory already exists.")


def start(n=0, directory="", lambda_min=0, lambda_max=0, step=0):
    start = time.time()

    reconstruction_path = directory + "/reconstruction"

    create_directory(reconstruction_path)

    command = {
        'recon_path': '/home/hperez/gpuvmem/bin/gpuvmem',
        'x': '16',
        'y': '16',
        'v': '256',
        'I': './data/input.dat',
        'o': reconstruction_path + '/residuals.ms',
        'p': reconstruction_path + '/mem/',
        't': '5000000',
        'z': str(lambda_min),
        'm': './data/model_images/mod_in_0.fits',
        'i': directory + '/simulation/simulation_out_',
        'O': reconstruction_path + '/final_output_'
    }

    lambda_values = np.linspace(float(lambda_min), float(lambda_max), num=int(step), endpoint=True, dtype=float)

    with Bar('Reconstruction', max=n) as bar:
        for count in range(n):
            for i in range(step):
                fvalues = reconstruction_path + "/lambda_" + str(lambda_values[i]).replace('.', '_') + '.txt'
                i_real = command['i'] + str(count) + '.ms'
                O_real = command['O'] + str(count) + '_' + str(i) + '.fits'

                process = subprocess.Popen([
                    command['recon_path'],
                    '-X', command['x'],
                    '-Y', command['y'],
                    '-V', command['v'],
                    '-i', i_real,
                    '-I', command['I'],
                    '-o', command['o'],
                    '-O', O_real,
                    '-m', command['m'],
                    '-t', command['t'],
                    '-p', command['p'],
                    '-f', fvalues,
                    '-z', command['z'],
                    '-Z', str(lambda_values[i]),
                    '--verbose'
                ], stdout=subprocess.PIPE)
                output, error = process.communicate()
            bar.next()

    #os.remove('./alpha.fits')
    stop = time.time()
    total_time = (stop - start) / 60
    print("\nReconstruction time: ", total_time, " (min)")


def simple_recon():
    start = time.time()
    print("Start simple recon")

    command = {
        'gpuvmem': '~/workspace/Github/gpuvmem/bin/gpuvmem',
        'x': '16',
        'y': '16',
        'v': '256',
        'I': '../data/input.dat',
        'o': '../test/residuals.ms',
        'p': '../test/mem/',
        't': '5000000',
        'z': '0.001',
        'Z': '0.05',
        'm': '../data/mod_in_0.fits',
        'i': '../data/co65.ms',
        'O': '../test/final_out.fits',
        'values': '../test/values.txt'
    }

    process = subprocess.Popen([
        command['gpuvmem'],
        '-X', command['x'],
        '-Y', command['y'],
        '-V', command['v'],
        '-i', command['i'],
        '-I', command['I'],
        '-o', command['o'],
        '-O', command['O'],
        '-m', command['m'],
        '-t', command['t'],
        '-p', command['p'],
        '-f', command['values'],
        '-z', command['z'],
        '-Z', command['Z'],
        '--verbose'
    ], stdout=subprocess.PIPE)
    output, error = process.communicate()

    stop = time.time()
    total_time = (stop - start) / 60
    print("\nReconstruction time: ", total_time, " (min)")

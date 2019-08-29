import os, sys, time
import numpy as np
from subprocess import Popen, PIPE, CalledProcessError

def reconstruction():
    print("Options for Reconstruction: ")
    print("    1. Test co65")
    print("    2. Test HLTau")
    print("    3. Other")
    r = input("option: ")

    if r == '1':
        test_co65()
    elif r == '2':
        test_hltau()
    else:
        sys.exit("Option not implemented yet.")


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

                process = Popen([
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
                ], stdout=PIPE)
                output, error = process.communicate()
            bar.next()

    #os.remove('./alpha.fits')
    stop = time.time()
    total_time = (stop - start) / 60
    print("\nReconstruction time: ", total_time, " (min)")


def test_co65():
    start = time.time()

    command = {
        'gpuvmem': '/home/hperez/Desktop/gpuvmem/bin/gpuvmem',
        'x': '16',
        'y': '16',
        'v': '256',
        'I': '../data/input.dat',
        'o': '../test/residuals.ms',
        'p': '../test/mem/',
        't': '5000000',
        'z': '0.001',
        'Z': '0.05,0.0',
        'm': '../data/model_images/mod_in_0.fits',
        'i': '../data/co65.ms',
        'O': '../test/final_out.fits',
        'values': '../test/values.txt'
    }

    with Popen([
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
    ], stdout=PIPE, universal_newlines=True) as p:
        for line in p.stdout:
            print(line,  end='')

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

    stop = time.time()
    total_time = (stop - start) / 60
    print("\nReconstruction time: ", total_time, " (min)")

def test_hltau():
    start = time.time()

    command = {
        'gpuvmem': '/home/hperez/Desktop/gpuvmem/bin/gpuvmem',
        'x': '16',
        'y': '16',
        'v': '256',
        'I': '../data/input.dat',
        'o': '../test/residuals.ms',
        'p': '../test/mem/',
        't': '5000000',
        'z': '0.001',
        'Z': '0.05,0.0',
        'm': '../data/model_images/hltau5_whead.fits',
        'i': '../data/hltau_reducido.ms',
        'O': '../test/final_out.fits',
        'values': '../test/values.txt'
    }

    with Popen([
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
    ], stdout=PIPE, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

    stop = time.time()
    total_time = (stop - start) / 60
    print("\nReconstruction time: ", total_time, " (min)")

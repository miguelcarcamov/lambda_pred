import os, sys, time
import numpy as np
from subprocess import Popen, PIPE, CalledProcessError

def start():
    print("Options for Reconstruction: ")
    print("    (1) Test co65")
    print("    (2) Test HLTau")
    print("    (3) iFFT")
    print("    (4) Other")
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


def apply_ifft():
    path = "/home/hperez/Desktop/gridded_uv_values.csv"

    x_u = []
    y_v = []
    z_vo_real = []
    z_vo_imag = []

    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]
    
    complex_data = []
    

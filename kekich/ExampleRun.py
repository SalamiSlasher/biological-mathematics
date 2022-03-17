#!/bin/python3

import subprocess
from multiprocessing.pool import ThreadPool
from itertools import product
import numpy as np
import json
import os
from pathlib import Path

BASE_PARAMS = {
    'species': 3,
    'a': 3.,
    'alpha': 0.3,
    'b': [0.4] * 3,
    'points': 2 ** 14,
    'd': [0.2] * 3,
    'dd': [0.001] * 9,
    'sigma_m': [0.04] * 3,
    'sigma_w': [0.04] * 9,
}


def iter_datas(title, xs, ys, zs):
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            for k, z in enumerate(zs):
                yield {
                    'name': '{}_{}_{}_{}'.format(title, i, j, k),
                    'x': x,
                    'y': y,
                    'z': z,
                    'i': i,
                    'j': j,
                    'k': k,
                }


def preparation(params):
    with open(params['title'] + '.json', 'w') as f:
        json.dump(params, f)
    
    if not os.path.exists(params['title']):
        os.makedirs(params['title'])

    for p in Path('.').glob('{0}/{0}*'.format(params['title'])):
        p.unlink()

        
def iter_ccto(dim):
    params = BASE_PARAMS
    params['title'] = 'HM_{}D'.format(dim)
    params['dim'] = dim
    params['x_label'] = 'd12'
    params['y_label'] = 'sm2'
    # params['z_label'] = 'zm2'  # DANGEON MASTER
    
    params['x_len'] = 30
    params['y_len'] = 30
    params['z_len'] = 30
    params['datas'] = list(iter_datas(
        params['title'],
        list(np.linspace(0.00000001, 0.001, params['x_len'])), #d12
        list(np.linspace(0.00000001, 0.2, params['y_len'])), #sm2
        list(np.linspace(0.00000001, 0.420, params['z_len'])), #sm2  
    ))
    preparation(params)
    for data in params['datas']:
        params['dd'][1] = data['x']
        params['sigma_m'][1] = data['y']
        yield data['name'], params
    

def iter_hm(dim):
    params = BASE_PARAMS
    params['alpha'] = 0.2
    params['sigma_m'] = [0.04, 0.06, 0.04]
    params['title'] = 'HM_{}D'.format(dim)
    params['dim'] = dim
    params['x_label'] = 'swii'
    params['y_label'] = 'swij'
    params['x_len'] = 30
    params['y_len'] = 30
    params['z_len'] = 30
    
    params['datas'] = list(iter_datas(
        params['title'],
        list(np.linspace(0.00000001, 0.15, params['x_len'])), #swii
        list(np.linspace(0.00000001, 0.15, params['y_len'])), #swij
        list(np.linspace(0.00000001, 0.15, params['z_len'])), #swij  
    ))
    preparation(params)
    for data in params['datas']:
        params['sigma_w'] = [
                            data['x'], data['y'], data['z'],
                            data['x'], data['y'], data['z'],
                            data['x'], data['y'], data['z']]
        yield data['name'], params


def wrap_scalat(s):
    return str(s)

def wrap_list(l):
    return list(map(str, l))

def work(cmd):
    subprocess.call(cmd)

tp = ThreadPool()
    
for name, params in iter_hm(dim=3):
    cmd = list(map(str, [
        './a.exe', 'point',
        '-t', params['title'] + '/' + name,
        '--cbor',
        '-dim', wrap_scalat(params['dim']),
        '-al', wrap_scalat(params['alpha']),
        '-points', wrap_scalat(params['points']),
        '-a', wrap_scalat(params['a']),
        '-b'] + wrap_list(params['b']) + [
        '-dvec'] + wrap_list(params['d']) + [
        '-dmat'] + wrap_list(params['dd']) + [
        '-sm'] + wrap_list(params['sigma_m']) + [
        '-sw'] + wrap_list(params['sigma_w']) + [
    ]))
    tp.apply_async(work, (cmd,))

tp.close()
tp.join()

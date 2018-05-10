from ear.classify import classify as classify_ear
from face.find import normalize as classify_face
from iris.iris_5 import classify as classify_iris

import matplotlib.pyplot as plt
import numpy as np


def tp_fp_helper(stats, thresh, same, z):
    predict = z > thresh
    if same:
        if predict:
            stats['tp'] += 1
        else:
            stats['fn'] += 1
    else:
        if predict:
            stats['fp'] += 1
        else:
            stats['tn'] += 1
    return stats


def tp_fp(thresh):
    stats = {
        'ear': {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0},
        'face': {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0},
        'iris': {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0},
        'all': {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0},
    }
    z_same = {
        'ear': [],
        'face': [],
        'iris': [],
        'all': []
    }
    z_diff = {
        'ear': [],
        'face': [],
        'iris': [],
        'all': []
    }
    for i in range(10 * 4):
        for j in range(10 * 4):
            if i == j:
                continue
            z_ear, same = classify_ear(i, j)
            z_face, _ = classify_face(i, j)
            # z_iris, _ = classify_iris(i, j)
            z_iris = 0
            z = np.mean([z_ear, z_face])

            stats['ear'] = tp_fp_helper(stats['ear'], thresh, same, z_ear)
            stats['face'] = tp_fp_helper(stats['face'], thresh, same, z_face)
            stats['iris'] = tp_fp_helper(stats['iris'], thresh, same, z_iris)
            stats['all'] = tp_fp_helper(stats['all'], thresh, same, z)

            if same:
                z_same['ear'].append(z_ear)
                z_same['face'].append(z_face)
                z_same['iris'].append(z_iris)
                z_same['all'].append(z)
            else:
                z_diff['ear'].append(z_ear)
                z_diff['face'].append(z_face)
                z_diff['iris'].append(z_iris)
                z_diff['all'].append(z)

    return {
        'ear': {'tpr': stats['ear']['tp'] / (stats['ear']['tp'] + stats['ear']['fn']),
                'fpr': 1 - (stats['ear']['tn'] / (stats['ear']['fp'] + stats['ear']['tn']))},
        'face': {'tpr': stats['face']['tp'] / (stats['face']['tp'] + stats['face']['fn']),
                 'fpr': 1 - (stats['face']['tn'] / (stats['face']['fp'] + stats['face']['tn']))},
        'iris': {'tpr': stats['iris']['tp'] / (stats['iris']['tp'] + stats['iris']['fn']),
                 'fpr': 1 - (stats['iris']['tn'] / (stats['iris']['fp'] + stats['iris']['tn']))},
        'all': {'tpr': stats['all']['tp'] / (stats['all']['tp'] + stats['all']['fn']),
                'fpr': 1 - (stats['all']['tn'] / (stats['all']['fp'] + stats['all']['tn']))},
    }


stats_all = []
for thresh in range(-15, 25, 3):
    print('thresh', thresh)
    stats = tp_fp(thresh)
    stats_all.append(stats)

all_fpr = {'ear': [],
           'face': [],
           'iris': [],
           'all': []}
all_tpr = {'ear': [],
           'face': [],
           'iris': [],
           'all': []}

for item in stats_all:
    all_fpr['ear'].append(item['ear']['fpr'])
    all_fpr['face'].append(item['face']['fpr'])
    all_fpr['iris'].append(item['iris']['fpr'])
    all_fpr['all'].append(item['all']['fpr'])

    all_tpr['ear'].append(item['ear']['tpr'])
    all_tpr['face'].append(item['face']['tpr'])
    all_tpr['iris'].append(item['iris']['tpr'])
    all_tpr['all'].append(item['all']['tpr'])

plt.plot(all_fpr['iris'], all_tpr['iris'], '-b')
plt.plot(all_fpr['ear'], all_tpr['ear'], '-r')
plt.plot(all_fpr['face'], all_tpr['face'], '-g')
plt.plot(all_fpr['all'], all_tpr['all'], '-y')
plt.plot([0, 1], [0, 1], '-')

plt.xlabel('True positive rate (Sensitivity)')
plt.ylabel('False positive rate (Specificity)')
plt.title('ROC')
plt.grid(True)
plt.show()

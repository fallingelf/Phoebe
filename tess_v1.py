#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 06:42:42 2020

@author: wqs
"""
import os
from time import time as _time
import numpy as np
import pandas as pd
import phoebe, ellc
from phoebe import u # units
import matplotlib.pyplot as plt


os.environ['PHOEBE_ENABLE_ONLINE_PASSBANDS']='False'

os.chdir(r'/home/wqs/Desktop/Projects/PHOEBE/data')
v1=pd.read_csv('tess_v1.dat',sep=',',header=None)
times,fluxes,sigmas=v1[0].values,v1[1].values,v1[2].values

logger = phoebe.logger('error')

b = phoebe.default_binary()
b.add_constraint('semidetached', 'secondary')
b.add_constraint('whitedwarf', 'primary')

b.set_value('period', component='binary', value=0.139613*u.d)
b.set_value('t0_supconj', component='binary', value=0.2841677980365126)
b.flip_constraint('mass@secondary', solve_for='sma@binary')

b.set_value('incl', component='binary', value=30.10952829129269*u.deg)
b.set_value('teff', component='primary', value=229788.95464824955*u.K)
b.set_value('teff', component='secondary', value=2638.8454077624147*u.K)
b.set_value('mass', component='secondary', value=0.25*u.solMass)
b.set_value('q', component='binary', value=0.21776628261552058)
b['q@binary'].set_limits([0.1736,0.25])

b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,101),
              times=times, fluxes=fluxes, sigmas=sigmas, dataset='t', 
              passband='TESS:T', overwrite=True)
# b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,101), dataset='b', 
#               passband='Johnson:B', overwrite=True)
# b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,101), dataset='v', 
#               passband='Johnson:V', overwrite=True)
# b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,101), dataset='r', 
#               passband='Johnson:R', overwrite=True)
# b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,101), dataset='i', 
#               passband='Johnson:I', overwrite=True)
# b.add_dataset('mesh', compute_phases=[0],overwrite=True, columns=['teffs', 'loggs'])

b['gravb_bol@primary'] = 0
b['irrad_frac_refl_bol@primary']=0
b['irrad_frac_refl_bol@secondary']=0.8
b.set_value_all('atm', value='blackbody')
b.set_value_all('ld_mode', value='manual')
b.set_value_all('ld_func', value='linear')
b.set_value_all('ld_coeffs', value=[0.])
b.set_value_all('ld_mode_bol','manual')
b.set_value_all('ld_func_bol','linear')
b.set_value_all('ld_coeffs_bol', value=[0.])
b.set_value_all('atm', component='secondary', value='phoenix')
b.set_value_all('ld_mode', component='secondary', value='lookup')
b.set_value_all('distortion_method@primary', value='sphere')
b.set_value_all('pblum_mode', dataset='t', value='dataset-scaled')

# b.run_compute(compute='phoebe01', model='ph01_res_bb', overwrite=True)

b.add_solver('optimizer.nelder_mead', 
              fit_parameters=['incl@binary', 'q@binary', 'teff@primary', 'teff@secondary'], 
              compute='phoebe01', solver='nelder_mead01', overwrite=True)
print(b.get_solver(kind='nelder_mead'))

start_t=_time()
b.run_solver(kind='nelder_mead', maxiter=1000, solution='nm_sol', overwrite=True)
end_t=_time()
print('\n\n the total run time is {:.0.1f} min \n'.format((end_t-start_t)/60))
print(b.get_solution('nm_sol').filter(qualifier=['message', 'nfev', 'niter', 'success']))
print(b.adopt_solution('nm_sol', trial_run=True))
b.adopt_solution('nm_sol')
b.run_compute(compute='phoebe01', model='ph01_res_phoenix', overwrite=True)


_ = b.plot(kind='lc', dataset='t', model='ph01_res_phoenix', x='phases', y='fluxes', 
            s={'dataset': 0.005}, marker={'dataset': '.'}, show=True)
_ = b.plot(kind='lc', dataset='t', model='ph01_res_phoenix', x='phases', y='residuals', 
            z={'dataset': 0, 'ph01_res_phoenix': 1},  save='tess_v1_res.png', show=True)

# _ = b.plot(kind='lc', dataset='t', x='phases', y='fluxes', c={'ph01_res_bb':'blue','ph01_res_phoenix':'red'}, show=True)
# _ = b.plot(kind='lc', dataset='b', x='phases', y='fluxes', c={'ph01_res_bb':'blue','ph01_res_phoenix':'red'}, show=False)
# _ = b.plot(kind='lc', dataset='v', x='phases', y='fluxes', c={'ph01_res_bb':'blue','ph01_res_phoenix':'red'}, show=False)
# _ = b.plot(kind='lc', dataset='r', x='phases', y='fluxes', c={'ph01_res_bb':'blue','ph01_res_phoenix':'red'}, show=False)
# _ = b.plot(kind='lc', dataset='i', x='phases', y='fluxes', c={'ph01_res_bb':'blue','ph01_res_phoenix':'red'}, show=True)

# plt.plot(b['value@compute_phases@t'],b['value@fluxes@t@ph01_res_phoenix']-b['value@fluxes@t@ph01_res_bb'])
# plt.plot(b['value@compute_phases@b'],b['value@fluxes@b@ph01_res_phoenix']-b['value@fluxes@b@ph01_res_bb'])
# plt.plot(b['value@compute_phases@v'],b['value@fluxes@v@ph01_res_phoenix']-b['value@fluxes@v@ph01_res_bb'])
# plt.plot(b['value@compute_phases@r'],b['value@fluxes@r@ph01_res_phoenix']-b['value@fluxes@r@ph01_res_bb'])
# plt.plot(b['value@compute_phases@i'],b['value@fluxes@i@ph01_res_phoenix']-b['value@fluxes@i@ph01_res_bb'])














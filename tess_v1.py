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

b.set_value('incl', component='binary', value=35.84199483113191*u.deg)
b.set_value('teff', component='primary', value=182191.2006931246*u.K)
b.set_value('teff', component='secondary', value=3514.383865182288*u.K)
b.set_value('mass', component='secondary', value=0.3*u.solMass)
b.set_value('q', component='binary', value=0.23136093619138703)
b['q@binary'].set_limits([0.14,0.5])

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
# b.add_dataset('mesh', compute_phases=[0,0.25,0.5,0.75], columns=['teffs'])

# b.add_feature('spot', component='primary', feature='hotregion1')
# b.set_value(qualifier='relteff', feature='hotregion1', value=1)
# b.set_value(qualifier='colat', feature='hotregion1', value=90)
# b.set_value(qualifier='long', feature='hotregion1', value=90)
# b.set_value(qualifier='radius', feature='hotregion1', value=30)

# b.add_feature('spot', component='primary', feature='hotregion2')
# b.set_value(qualifier='relteff', feature='hotregion2', value=1)
# b.set_value(qualifier='colat', feature='hotregion2', value=90)
# b.set_value(qualifier='long', feature='hotregion2', value=270)
# b.set_value(qualifier='radius', feature='hotregion2', value=30)

b['gravb_bol@primary'] = 1
b['gravb_bol@secondary'] = 0.32
b['irrad_frac_refl_bol@primary']=1
b['irrad_frac_refl_bol@secondary']=0.5
b.set_value_all('atm', value='blackbody')
b.set_value_all('ld_mode', value='manual')
b.set_value_all('ld_func', value='linear')
b.set_value_all('ld_coeffs', value=[0.])
b.set_value_all('ld_mode_bol','manual')
b.set_value_all('ld_func_bol','linear')
b.set_value_all('ld_coeffs_bol', value=[0.])
b.set_value_all('atm', component='secondary', value='phoenix')
b.set_value_all('ld_mode', component='secondary', value='interp')
b.set_value_all('distortion_method@primary', value='sphere')
b.set_value_all('pblum_mode', dataset='t', value='dataset-scaled')

# b.set_value('Rv', value=3.1)
# b.set_value('Av',1.4)

b.add_solver('optimizer.nelder_mead', 
              fit_parameters=['incl@binary', 'q@binary', 'teff@primary', 'teff@secondary'], 
              compute='phoebe01', solver='nelder_mead01', overwrite=True)
print(b.get_solver(kind='nelder_mead'))

start_t=_time()
b.run_solver(kind='nelder_mead', maxiter=1000, solution='nm_sol', overwrite=True)
end_t=_time()
print('\n\n the total run time is {:.1f} min \n'.format((end_t-start_t)/60))
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














#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 19:25:48 2020

@author: wqs
"""
import os,sys
import phoebe,ellc
from time import time as _time
from phoebe import u # units
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
    
logger = phoebe.logger('error')

data_lc=pd.read_csv(r'/home/wqs/Desktop/Projects/phoebe/Phoebe-main/data/clear_mn.dat',header=0,sep=' ')
times=data_lc['JDHEL'].values-2457458
fluxes=10**(-0.4*data_lc['V-C'].values)*25
sigmas=fluxes*np.log(10)*(-0.4)*data_lc['s1'].values
plt.errorbar(times,fluxes,sigmas)

b = phoebe.default_binary()
b.add_constraint('semidetached', 'secondary')
b.add_constraint('whitedwarf', 'primary')

b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,201),
              times=times, fluxes=fluxes, sigmas=sigmas, dataset='lc01', 
              passband='Johnson:V', overwrite=True)

b.set_value('t0_supconj', component='binary', value=0.62831)
b.set_value('period', component='binary', value=0.1412437990*u.d)
b.set_value('incl', component='binary', value=75*u.deg)

b.flip_constraint('mass@secondary', solve_for='sma@binary')
b.set_value('mass', component='secondary', value=0.31*u.solMass)
b.set_value('q', component='binary', value=0.39)
b['q@binary'].set_limits([0.1736,0.5])

b.set_value('teff', component='primary', value=20000*u.K)
b.set_value('teff', component='secondary', value=3000*u.K)

b['gravb_bol@primary'] = 0
b['irrad_frac_refl_bol@primary']=0
b.set_value_all('atm', component='primary', value='blackbody')
b.set_value_all('ld_mode', component='primary', value='manual')
b.set_value_all('ld_func', component='primary', value='linear')
b.set_value_all('ld_coeffs', component='primary', dataset='lc01', value=[0.])
b.set_value_all('ld_mode_bol@primary','manual')
b.set_value_all('ld_func_bol@primary','linear')
b.set_value_all('ld_coeffs_bol', component='primary', value=[0.])
b.set_value_all('atm', component='secondary', value='phoenix')
b.set_value_all('ld_mode', component='secondary', value='lookup')
b.set_value_all('distortion_method@primary', value='sphere')
b.set_value_all('pblum_mode', 'dataset-scaled')

b.run_compute(compute='phoebe01', model='model_no_spot', overwrite=True)

b.add_feature('spot', component='primary', feature='hotregion1')
b.set_value(qualifier='relteff', feature='hotregion1', value=10)
b.set_value(qualifier='colat', feature='hotregion1', value=20)
b.set_value(qualifier='long', feature='hotregion1', value=252)
b.set_value(qualifier='radius', feature='hotregion1', value=30)

b.add_feature('spot', component='primary', feature='hotregion2')
b.set_value(qualifier='relteff', feature='hotregion2', value=10)
b.set_value(qualifier='colat', feature='hotregion2', value=160)
b.set_value(qualifier='long', feature='hotregion2', value=72)
b.set_value(qualifier='radius', feature='hotregion2', value=30)

#b.add_solver('optimizer.nelder_mead',solver='nelder_mead01',overwrite=True,
#             fit_parameters=['incl@binary', 'q@binary', 'teff@secondary', 'teff@primary'])
#print(b.get_solver(kind='nelder_mead'))
#t_start=_time()
#b.run_solver(kind='nelder_mead', maxiter=1000, solution='nm_sol')
#t_end=_time()
#print('the total run time is {:.0f} s'.format(t_end-t_start))
#print(b.get_solution('nm_sol').filter(qualifier=['message', 'nfev', 'niter', 'success']))
#print(b.adopt_solution('nm_sol', trial_run=True))
#b.adopt_solution('nm_sol')
b.run_compute(compute='phoebe01', model='model_with_spot', overwrite=True)

_ = b.plot(kind='lc', x='phases', y='fluxes', 
           s={'dataset': 0.005}, c={'model_no_spot': 'red', 'model_with_spot': 'green', 'dataset': 'black'},
           marker={'dataset': '.'})
_ = b.plot(kind='lc', x='phases', y='residuals', 
           z={'dataset': 0, 'model': 1}, c={'model_no_spot': 'red', 'model_with_spot': 'green', 'dataset': 'black'},
           save='mnhya_res.pdf', show=True)
























#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:52:45 2020

mesh does not support b['pblum_mode']='dataset-scaled'

@author: wqs
"""

import os,sys
import phoebe,ellc
from time import time as _time
from phoebe import u # units
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
    
data_lc=pd.read_csv(r'/home/wqs/Desktop/Projects/phoebe/Phoebe-main/data/clear_mn.dat',header=0,sep=' ')
times=data_lc['JDHEL'].values-2457458
fluxes=10**(-0.4*data_lc['V-C'].values)*25
sigmas=fluxes*np.log(10)*(-0.4)*data_lc['s1'].values

b = phoebe.default_binary()
b.add_constraint('semidetached', 'secondary')
b.add_constraint('whitedwarf', 'primary')

b.add_dataset('lc', compute_phases=phoebe.linspace(0,1,201), overwrite=True)
b.add_dataset('mesh', compute_phases=[0,0.25,0.5,0.75], columns=['teffs'])

b.set_value('t0_supconj', component='binary', value=0.62831)
b.set_value('period', component='binary', value=0.1412437990*u.d)
b.set_value('incl', component='binary', value=75*u.deg)

b.flip_constraint('mass@secondary', solve_for='sma@binary')
b.set_value('mass', component='secondary', value=0.31*u.solMass)
b.set_value('q', component='binary', value=0.39)
b['q@binary'].set_limits([0.1736,0.5])

b.set_value('teff', component='primary', value=20000*u.K)
b.set_value('teff', component='secondary', value=3000*u.K)

b.add_feature('spot', component='primary', feature='hotregion1')
b.set_value(qualifier='relteff', feature='hotregion1', value=10)
b.set_value(qualifier='colat', feature='hotregion1', value=20)
b.set_value(qualifier='long', feature='hotregion1', value=252)
b.set_value(qualifier='radius', feature='hotregion1', value=40)

#b.add_feature('spot', component='primary', feature='hotregion2')
#b.set_value(qualifier='relteff', feature='hotregion2', value=40)
#b.set_value(qualifier='colat', feature='hotregion2', value=160)
#b.set_value(qualifier='long', feature='hotregion2', value=72)
#b.set_value(qualifier='radius', feature='hotregion2', value=40)

b.set_value_all('gravb_bol', value=0)
b.set_value_all('irrad_frac_refl_bol', value=0)
b.set_value_all('atm', value='blackbody')
b.set_value_all('ld_mode', value='manual')
b.set_value_all('ld_func', value='linear')
b.set_value_all('ld_coeffs', value=[0.])
b.set_value_all('ld_mode_bol','manual')
b.set_value_all('ld_func_bol','linear')
b.set_value_all('ld_coeffs_bol', value=[0.])
#b.set_value_all('atm', component='primary', value='blackbody')
#b.set_value_all('ld_mode', component='primary', value='manual')
#b.set_value_all('ld_func', component='primary', value='linear')
#b.set_value_all('ld_coeffs', component='primary', value=[0.])
#b.set_value_all('ld_mode_bol@primary','manual')
#b.set_value_all('ld_func_bol@primary','linear')
#b.set_value_all('ld_coeffs_bol', component='primary', value=[0.])
#b.set_value_all('atm', component='secondary', value='phoenix')
#b.set_value_all('ld_mode', component='secondary', value='lookup')
b.set_value_all('distortion_method@primary', value='sphere')

b.run_compute(compute='phoebe01', model='after_nm', overwrite=True)
afig, mplfig = b.plot('lc', x='phases', show=True)
afig, mplfig = b.plot('mesh', x='us', y='vs', component='primary', phase=0., fc='teffs', show=True)
afig, mplfig = b.plot('mesh', x='us', y='vs', component='primary', phase=0.25, fc='teffs', show=True)
afig, mplfig = b.plot('mesh', x='us', y='vs', component='primary', phase=0.5, fc='teffs', show=True)
afig, mplfig = b.plot('mesh', x='us', y='vs', component='primary', phase=0.75, fc='teffs', show=True)


#afig, mplfig = b.plot('mesh', x='us', y='vs', phase=0., fc='teffs', show=True)
#afig, mplfig = b.plot('mesh', x='us', y='vs', phase=0.25, fc='teffs', show=True)
#afig, mplfig = b.plot('mesh', x='us', y='vs', phase=0.5, fc='teffs', show=True)
#afig, mplfig = b.plot('mesh', x='us', y='vs', phase=0.75, fc='teffs', show=True)
#

















#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:43:48 2020

@author: wqs
"""

import phoebe
from phoebe import u # units
import numpy as np
import matplotlib.pyplot as plt

logger = phoebe.logger('error')

b = phoebe.default_binary()
b.add_constraint('semidetached', 'secondary')

b.set_value('period', component='binary', value=0.1769*u.d)
b.set_value('incl', component='binary', value=70*u.deg)
b.set_value('teff', component='primary', value=10000*u.K)
b.set_value('teff', component='secondary', value=3650*u.K)
b.flip_constraint('mass@primary', solve_for='sma@binary')
b.set_value('mass', component='primary', value=1.2*u.solMass)
b.flip_constraint('mass@secondary', solve_for='q')
b.set_value('mass', component='secondary', value=0.42*u.solMass)
b.set_value('requiv', component='primary', value=0.6*u.solRad)



phases = phoebe.linspace(0,1,101)
b.add_dataset('lc', times=b.to_time(phases),dataset='lc01',overwrite=True, passband="Johnson:V")
b.add_dataset('mesh', times=b.to_time(phases),dataset='mesh01',overwrite=True, columns=['teffs', 'loggs'])

b.set_value('atm', component='primary', value='blackbody')
b.set_value('ld_mode', component='primary', value='manual')
b.set_value('ld_func', component='primary', value='quadratic')
b.set_value('ld_coeffs', component='primary', dataset='lc01', value=[0.1225,0.3086])
b.set_value_all('ld_mode_bol@primary','manual')
b.set_value_all('ld_func_bol@primary','quadratic')
b.set_value('ld_coeffs_bol', component='primary', value=[0.1421,0.3693])

b.set_value_all('atm', component='secondary', value='phoenix')
b.set_value('abun', component='secondary', value=0)

#b['distortion_method@primary']='sphere'
#b.set_value('ntriangles@secondary', value=10000)

b['gravb_bol@primary'] = 1
b['irrad_frac_refl_bol@primary']=1

print(b.run_checks())
b.run_compute(model='WD_RD',overwrite=True)
#b.plot(show=True)
#b.plot(dataset='lc01', show=True)
fig, mplfig = b['mesh@model'].plot(phase=0.0, show=True,
                                   x='us', y='vs', c='r',
                                   xlim=(-2,2),ylim=(-2,2))












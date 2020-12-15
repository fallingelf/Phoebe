#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:43:48 2020

the atmosphere model 'phoenix' operated by the backend 'ellc' gives 
different light curves from that given by the same atmosphere model 
operated by the backend 'phoebe'    

@author: wqs
"""

import matplotlib.pyplot as plt

plt.rc('font', family='serif', size=14, serif='STIXGeneral')
plt.rc('mathtext', fontset='stix')

import phoebe,ellc
import numpy as np
from phoebe import u # units

logger = phoebe.logger('error')

#print(phoebe.conf.interactive_constraints)
phoebe.interactive_constraints_on()

b = phoebe.default_binary()
b.add_constraint('semidetached', 'secondary')
b.add_constraint('whitedwarf', 'primary')

b.flip_constraint('mass@primary', solve_for='sma@binary')
b.set_value('mass', component='primary', value=1*u.solMass)
b.flip_constraint('mass@secondary', solve_for='q')
b.set_value('mass', component='secondary', value=0.3*u.solMass)
b.set_value('teff@primary', 150000)
b.set_value('teff@secondary', 4500)
b.set_value('incl', component='binary', value=50*u.deg)

lctimes = phoebe.linspace(0, 1, 101)
b.add_dataset('lc', compute_times=lctimes)

b.add_compute('ellc', compute='ellc_phoenix')
b.add_compute('ellc', compute='ellc_ck2004')
b.add_compute('phoebe', compute='phoebe_phoenix')

b.set_value_all('atm', component='primary', value='blackbody')
b.set_value_all('ld_mode', component='primary', value='manual')
b.set_value_all('ld_func', component='primary', value='linear')
b.set_value_all('ld_coeffs', component='primary', dataset='lc01', value=[0])
b.set_value_all('ld_mode_bol@primary','manual')
b.set_value_all('ld_func_bol@primary','linear')
b.set_value_all('ld_coeffs_bol', component='primary', value=[0])
b.set_value_all('distortion_method@primary', value='sphere')
b.set_value_all('atm', component='secondary', value='phoenix')
b.set_value_all('ld_mode', component='secondary', value='lookup')

b.run_compute(compute='ellc_phoenix', pblum_method='phoebe', model='ellc_phoenix_res')
b.run_compute(compute='phoebe_phoenix', pblum_method='phoebe', model='phoebe_phoenix_res')

b.set_value_all('atm', component='secondary', value='ck2004')
b.run_compute(compute='ellc_ck2004', pblum_method='phoebe', model='ellc_ck2004_res')

afig, mplfig = b.plot('lc01', x='phases', show=True)

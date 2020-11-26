# Phoebe
learning phoebe for modeling the eclipsing binary

---------------
# plot
help（b.plot）
### plot orbital
    fig, mplfig = b['orb01@run_with_incl_80'].plot(time=0.5, uncover=True, xlim=(-0.014,0.016), ylim=(-0.004,0.004), 
                                                    xunit='AU', yunit='AU', xlabel='X POS', ylabel='Z POS', 
                                                    linestyle='-.', s=0.02, projection='3d', show=True,
                                                    legend=True, legend_kwargs={'loc': 'upper right', 'facecolor': None})
### specified labels                          
    fig, mplfig = b['orb01@primary@run_with_incl_80'].plot(label='primary', time=0.5, uncover=True, xlim=(-0.014,0.016), ylim=(-0.004,0.004), 
                                                    xunit='AU', yunit='AU', xlabel='X POS', ylabel='Z POS',
                                                          linestyle='-.', s=0.02, projection='3d')
    fig, mplfig = b['orb01@secondary@run_with_incl_80'].plot(label='secondary', time=0.5, uncover=True, xlim=(-0.014,0.016), ylim=(-0.004,0.004), 
                                                    xunit='AU', yunit='AU', xlabel='X POS', ylabel='Z POS', 
                                                             linestyle='-.', s=0.02, projection='3d', show=True, 
                                                    legend=True, legend_kwargs={'loc': 'upper right', 'facecolor': None})
### plot lc
    afig, mplfig = b['lc01@dataset'].plot(yerror='sigmas', c='r', show=True)

# compute


# solver
PHOEBE includes wrappers around several different inverse-problem "algorithms" with a common interface. These available "algorithms" are divided into three categories:
    
    estimators: provides proposed values for a number of parameters from the datasets as input alone, not requiring full forward-models via run_compute.
    optimizers: runs off-the-shelf optimizers to attempt to find the local (or global) solution.
    samplers: samples the local parameter space to estimate uncertainties and correlations.

#### see the currently implemented set of solvers 

    print(phoebe.list_available_solvers())
    ['estimator.ebai', 'estimator.lc_geometry', 'estimator.lc_periodogram', 'estimator.rv_geometry', 'estimator.rv_periodogram', 
    'optimizer.cg', 'optimizer.differential_evolution', 'optimizer.nelder_mead', 'optimizer.powell', 
    'sampler.dynesty', 'sampler.emcee']

## run_solver
to use a solver you must first call b.add_solver, set the desired options, and then call b.run_solver. The proposed values can be viewed via b.adopt_solution by passing trial_run=True; otherwise, the changes will be made and all changed parameters (including those changed via constraints) will be returned.

    b.add_solver('estimator.lc_geometry', lc='lc01', solver='my_lcgeom_solver')
    b.run_solver(solver='my_lcgeom_solver', solution='my_lcgeom_solution')
    print(b.adopt_solution(trial_run=True))
    print(b.adopt_solution())
    
## The Merit Function
Both optimizers and samplers require running a forward model and use a merit function to compare the synthetic model to the observational data.

#### accessing the values used in the merit function

    b.calculate_residuals
    b.calculate_chi2
    b.calculate_lnlikelihood
    b.calculate_lnp

# passband

### print(phoebe.list_installed_passbands())     
    ['Bolometric:900-40000', 'Johnson:V']

### phoebe.list_passbands()
    ['Johnson:U',  'Gaia:RVS', 'Hipparcos:Hp', 'Tycho:V', 'Cousins:I', 'Tycho:B', 'LSST:g', 'Johnson:B', 'LSST:u', 'Bolometric:900-40000', 'Johnson:V', 'Gaia:G', 'LSST:r',     'LSST:z', 'Gaia:BP', 'Kepler:mean', 'Stromgren:u', 'Johnson:R', 'LSST:y3', 'BRITE:red', 'Stromgren:b', 'Cousins:R', 'TESS:T', 'KELT:R', 'Stromgren:y', 'LSST:i', 'Gaia:RP', 'Johnson:I', 'Stromgren:v', 'BRITE:blue']

### the local and global directories
    phoebe.list_passband_directories()
    ['/home/wqs/.local/lib/python3.6/site-packages/phoebe/atmospheres/tables/passbands/', '/home/wqs/.phoebe/atmospheres/tables/passbands/']

### install from files
    phoebe.install_passband(fname,local=True)

### download
    phoebe.download_passband('Johnson:V',local=False)

### updates
    print(phoebe.list_all_update_passbands_available())
    phoebe.update_all_passbands() #for all passbands
    phoebe.update_passband('Johnson:V') #for single passband such as 'Johnson:V'


































































































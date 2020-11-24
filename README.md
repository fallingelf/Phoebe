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

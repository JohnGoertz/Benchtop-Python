import numpy as np
import pandas as pd
import scipy.stats as stats

############################################################################################################
# From 01: Plotting data, uncertainty, curve fits
def classical_fit_intervals(func,p_opt,x,y,xplot):
    tile_x = np.tile(x,[y.size//x.size,1]).T
    n = y.size
    m = p_opt.size
    dof = n-m                                                # Degrees of freedom
    res = y - func(tile_x,*p_opt)                            # Residuals
    t = stats.t.ppf(0.975, n - m)                            # Student's t distribution
    chi2 = np.sum((res / func(tile_x,*p_opt))**2)            # chi-squared; estimates error in data
    chi2_red = chi2 / dof                                    # reduced chi-squared; measures goodness of fit
    s_err = np.sqrt(np.sum(res**2) / dof)                    # standard error of the fit at each point

    ci = t * s_err * np.sqrt(1/n + (xplot - np.mean(x))**2 / np.sum((x - np.mean(x))**2))

    pi = t * s_err * np.sqrt(1 + 1/n + (xplot - np.mean(x))**2 / np.sum((x - np.mean(x))**2))

    return ci, pi

def classical_fit_param_summary(p_opt,p_cov, names = None):
    p_std = np.sqrt(np.diag(p_cov))
    nstd = stats.norm.ppf((1. + 0.95)/2.)
    p_ci_lower = p_opt - nstd * p_std
    p_ci_upper = p_opt + nstd * p_std
    summary = pd.DataFrame(data = [p_opt,p_std,p_ci_lower,p_ci_upper],
                           index = ('Optimal Value','Standard Error','95% CI Lower Limit','95% CI Upper Limit'),
                           columns = names)
    return summary  
# encoding: utf-8
"""Tools for calculating vertical velocity in s-coordinate models."""
__docformat__ = "restructuredtext en"

import numpy as np

def omegaHz(u, v, pm, pn, Hz, Hz_t=0):
    '''
    Calculate omega, the grid-relative vertical velocity, on the s-coordinate.
    By definition, omega(sigma=-1) = omega(sigma=0) = 0.
    
    Solutions are based on continuity in a sigma coordinate:
    
    Hz_t + (Hz*u)_x + (Hz*v)_y + (Hz*omega)_sigma = 0
    
    Parameters
    ----------
    u, v : 3D or 4D array
        The horizontal velocity values, on their respective CGrid points
    pm, pn : 2D array
        The grid metrics, inverse grid widths
    Hz : 3D or 4D array
        The vertical layer thickness at rho-points
    Hz_t : 2D or 4D array
        The rate of change of the the vertical coordinate.  [Default = 0]
    
    Returns
    -------
    omegaHz : 3D array
        The grid-relative vertical velocity on w-points multiplied by Hz,
        i.e., Hz*omega in the equation above.
    
    '''
    
    uflux = u[..., 1:-1, :] * 0.5 * (Hz[..., 1:-1, :-1] + Hz[..., 1:-1, 1:])
    vflux = v[..., :, 1:-1]  * 0.5 * (Hz[..., :-1, 1:-1] + Hz[..., 1:, 1:-1])
    omegaHz_sigma = -Hz_t - np.diff(uflux, axis=-1)*pm[1:-1, 1:-1] - np.diff(vflux, axis=-2)*pn[1:-1, 1:-1] 
    
    return np.cumsum(omegaHz_sigma, axis=-3)
    



if __name__ == '__main__':

    import octant

    Hz = octant.depths.get_Hz(2, 4, 30, 5.0, 1.0, 100.0*ones((40, 50)), 10.0)

    x = 500.0 * arange(50)
    y = 500.0 * arange(40)

    x, y = np.meshgrid(x, y)

    xu = 0.5 * (x[:, 1:] + x[:, :-1])
    u = 0.5 * ones((30, 40, 49)) * sin(xu / 10000.0)
    v = zeros((30, 39, 50))

    pm = 0.002 * ones((40, 50))
    pn = 0.002 * ones((40, 50))
    
    
    o = omega(u, v, pm, pn, Hz)
    
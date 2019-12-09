# dsw7@sfu.ca
# accelerating and decelerating joints
from numpy import trapz


def d_theta_parabolic(C, k, clk):
    """
    A downwards concave parabola of form:
        f(x) = -c(x)(x - a)
    Here:
        C   -> x
        k   -> c
        clk -> a
    """
    return -1 * k * C * (C - clk)


def parabolic_path(THETA_START, THETA_END, NET_CLOCKS):
    """
    THETA_START -> start angle
    THETA_END   -> end angle
    NET_CLOCKS  -> how many cycles SCAM iterates
    """
    # get the area we wish to match
    # note that area of dTHETA/dC yields total degrees passed
    area_LINEAR = THETA_END - THETA_START 
    
    # get the area of a parabola scaled to 1.00
    clocks = list(range(0, NET_CLOCKS + 1))
    d_theta_prescaled = [d_theta_parabolic(c, k=1.0, clk=NET_CLOCKS) for c in clocks]
    area_prescaled = trapz(d_theta_prescaled)
    
    # get the new scaling constant
    new_constant = area_LINEAR / area_prescaled
    
    # and now scale down parabola to match the area of the linear fit
    d_theta_postscaled = [d_theta_parabolic(c, k=new_constant, clk=NET_CLOCKS) for c in clocks]
    # area_postscaled = trapz(d_theta_postscaled)
    
    return d_theta_postscaled
    
    

# visualize results
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy import integrate
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
    
    size = 0.8 # select plot size
    save_plots = False
    
    # in SCAM_GOTO.py, we have a starting position and an ending position:
    THETA_START = 0.00
    THETA_END = 60.0
    
    # we also clock over CLOCK number of cycles:
    CLOCK = 100
    
    # the domain
    C_values = list(range(0, CLOCK + 1))    
    
    # in the simple linear case, we have the following degrees per clock:
    d_THETA = (THETA_END - THETA_START) / CLOCK
    
    # angle as a function of clock
    linear_fit = [c * d_THETA for c in C_values]
    plt.figure(figsize=(size * 5, size * 5))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('C (clock number)', size=12)
    plt.ylabel(r'$\theta\:(^\circ)$', size=14)
    plt.plot(C_values, linear_fit, c='k', lw=0.75)
    if save_plots: 
        plt.savefig('angle_as_a_function_of_C.png', bbox_inches='tight', dpi=600)
    plt.show()
    
    # now plot the first derivative
    plt.figure(figsize=(size * 5, size * 5))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('C (clock number)', size=12)
    plt.ylabel(r'$\Delta\theta\:(^\circ)$', size=14)
    plt.plot([d_THETA] * (CLOCK + 1), c='k', lw=0.75)
    if save_plots: 
        plt.savefig('first_derivative.png', bbox_inches='tight', dpi=600)
    plt.show()
    
    # get total area
    AREA = d_THETA * CLOCK
    
    # then switch to parabolic trace
    # note that here, the area under the parabola is huge
    # plot unscaled parabolic trace
    d_THETA_values = [d_theta_parabolic(c, k=1.0, clk=CLOCK) for c in C_values]
    plt.figure(figsize=(size * 5, size * 5))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('C (clock number)', size=12)
    plt.ylabel(r'$\Delta\theta\:(^\circ)$', size=14)
    plt.plot(C_values, d_THETA_values, c='k', lw=0.75)
    if save_plots: 
        plt.savefig('first_derivative_unscaled.png', bbox_inches='tight', dpi=600)
    plt.show()

    # we need to scale down this area to match AREA
    scaled_down = parabolic_path(THETA_START, THETA_END, CLOCK)

    # now plot the scaled data
    plt.figure(figsize=(size * 5, size * 5))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('C (clock number)', size=12)
    plt.ylabel(r'$\Delta\theta\:(^\circ)$', size=14)
    plt.plot(C_values, scaled_down, c='k', lw=0.75)
    if save_plots: 
        plt.savefig('first_derivative_scaleddown.png', bbox_inches='tight', dpi=600)
    plt.show()

    # get cumulative sum
    cum_trapezoidal_sum = integrate.cumtrapz(scaled_down)
    
    # plot cumulative trapezoidal sum
    plt.figure(figsize=(size * 5, size * 5))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('C (clock number)', size=12)
    plt.ylabel(r'$\theta\:(^\circ)$', size=14)
    plt.plot(cum_trapezoidal_sum, c='k', lw=0.75)
    if save_plots: 
        plt.savefig('cum_trapezoidal.png', bbox_inches='tight', dpi=600)
    plt.show()
    
    
    

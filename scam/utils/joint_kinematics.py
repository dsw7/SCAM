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


def parabolic_path(start, end, cycles):
    """
    start -> start angle
    end -> end angle
    cycles -> how many cycles SCAM iterates over
    """
    # get the area we wish to match
    # note that area of dTHETA/dC yields total degrees passed
    area_linear = end - start 
    
    # get the area of a parabola scaled to 1.00
    clocks = list(range(0, cycles + 1))
    d_theta_prescaled = [d_theta_parabolic(c, k=1.0, clk=cycles) for c in clocks]
    area_prescaled = trapz(d_theta_prescaled)
    
    # get the new scaling constant
    new_constant = area_linear / area_prescaled
    
    # and now scale down parabola to match the area of the linear fit
    d_theta_postscaled = [d_theta_parabolic(c, k=new_constant, clk=cycles) for c in clocks]
    return d_theta_postscaled
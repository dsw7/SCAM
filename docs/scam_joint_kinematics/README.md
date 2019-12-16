### Joint kinematics
---  

<p align="justify">
From SCAM GOTO, we know that each joint angle changes linearly  
per cycle. This is simple to understand, but not realistic  
as this yields jerk at start and stop positions. Here is a plot  
depicting angle as a function of cycle for this case:  
</p>

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_joint_kinematics/angle_as_a_function_of_C.png" width="380">  

<p align="justify">
  Let's call the linear function yielding this result <i>f</i> and let's  
  also get the first derivative. <i>C</i> is the current tick.  
</p>

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20f%28C%29%5C%5C%20f%27%28C%29%20%5Cend%7Balign%7D">  

A plot of the first derivative (angular velocity):  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_joint_kinematics/first_derivative.png" width="380">  

<p align="justify">
We want to now "convert" this linear relationship to a non-linear  
relationship. That is, we want the angular velocity to start and  
end around 0. The maximum velocity can safely occur around the  
midpoint of this non-linear relationship. So we can fit the velocity  
to a concave down parabola (here we pass over 100 cycles):  
</p>

<img src="https://latex.codecogs.com/gif.latex?g%28C%29%20%3D%20-k%28C%29%28C%20-%20100%29">  

A plot of this function follows (where _k_ = 1.00):  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_joint_kinematics/first_derivative_unscaled.png" width="380">  

<p align="justify">
  Note that the angular velocity is 0 at <i>C</i> = 0 and <i>C</i> = 100.  
We have to match this parabola to the linear relationship in SCAM GOTO.  
To do so, we scale down the parabola via <i>k</i>. <i>k</i> can be found  
as follows: 
</p>

<img src="https://latex.codecogs.com/gif.latex?k%20%3D%20%5Cfrac%7B%5Ctheta_f%20-%20%5Ctheta_i%7D%7B-%5Cint_0%5E%7B100%7D%28C%29%28C-100%29dC%7D">  

<p align="justify">
Here, we are simply getting <i>k</i> by finding the ratio of the area of  
the linear relationship to that of the non-linear relationship. That is,  
</p>

<img src="https://latex.codecogs.com/gif.latex?k%3D%5Cfrac%7B60%5E%5Ccirc%20-%200%5E%5Ccirc%7D%7B166560%5E%5Ccirc%7D">  

The new parabola follows,  

<img src="https://latex.codecogs.com/gif.latex?-%5Cfrac%7B60%5E%5Ccirc%20-%200%5E%5Ccirc%7D%7B166560%5E%5Ccirc%7D%28C%29%28C-100%29">  

And here is the plot:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_joint_kinematics/first_derivative_scaleddown.png" width="380">  

<p align="justify">
  A plot of the cumulative area as a function of <i>C</i> is shown below.  
Note that here the joint velocity starts at around 0 and ends around  
0 with a smooth acceleration/deceleration between the start and end  
angles.  
</p>

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_joint_kinematics/cum_trapezoidal.png" width="380">




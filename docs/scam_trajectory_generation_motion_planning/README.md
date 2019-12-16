### Trajectory Generation and Motion Planning  

Here I describe the mathematics underlying trajectory generation and motion planning for SCAM's end effector. Here I only describe linear trajectories. The general idea is as follows: the end effector starts at _P_(x<sub>i</sub>, y<sub>i</sub>, z<sub>i</sub>) and moves to _Q_(x<sub>f</sub>, y<sub>f</sub>, z<sub>f</sub>). The velocity is maximized at the midpoint between _P_ and _Q_ and minimized near _P_ and _Q_. I show this in the following figure:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_trajectory_generation_motion_planning/layout.png" width="500">

Notice that both dx and dy are maximized at the midpoint between _P_ and _Q_. Assume that IK(x, y) is the inverse kinematics algorithm for the 2R portion of SCAM. We can solve for the first two joint angles for all **non-linearly** spaced _x_, _y_ coordinates. That is:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_trajectory_generation_motion_planning/layout_with_IK.png" width="500">

This array of angle pairs can then be sent to SCAM's microcontroller. These angle arguments will force the first two links in SCAM to gently accelerate before reaching the midpoint between _P_ and _Q_, followed by a gradual deceleration after the midpoint.

### How does SCAM plan non-constant velocity motion?

In the above example, the direction of travel can be broken down into both _x_ and _y_ components (_z_ remains constant). We also know that SCAM iterates over a predefined number of cycles, _C_. Therefore we find:

<!---
\begin{align*}
\Delta &x=\frac{x_f - x_i}{C}\\
\Delta &y=\frac{y_f - y_i}{C}
\end{align}
--->
<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20%5CDelta%20%26x%3D%5Cfrac%7Bx_f%20-%20x_i%7D%7BC%7D%5C%5C%20%5CDelta%20%26y%3D%5Cfrac%7By_f%20-%20y_i%7D%7BC%7D%20%5Cend%7Balign%7D">

We get two arrays of linearly spaced _x_ and _y_ values:

<!---
\begin{bmatrix}
x_i\\
x_i + \Delta x\\
x_i + 2\Delta x\\
x_i + 3\Delta x\\
x_i + 4\Delta x\\
\vdots \\
x_f
\end{bmatrix},
\begin{bmatrix}
y_i\\
y_i + \Delta y\\
y_i + 2\Delta y\\
y_i + 3\Delta y\\
y_i + 4\Delta y\\
\vdots \\
y_f
\end{bmatrix}
--->
<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7D%20x_i%5C%5C%20x_i%20&plus;%20%5CDelta%20x%5C%5C%20x_i%20&plus;%202%5CDelta%20x%5C%5C%20x_i%20&plus;%203%5CDelta%20x%5C%5C%20x_i%20&plus;%204%5CDelta%20x%5C%5C%20%5Cvdots%20%5C%5C%20x_f%20%5Cend%7Bbmatrix%7D%2C%20%5Cbegin%7Bbmatrix%7D%20y_i%5C%5C%20y_i%20&plus;%20%5CDelta%20y%5C%5C%20y_i%20&plus;%202%5CDelta%20y%5C%5C%20y_i%20&plus;%203%5CDelta%20y%5C%5C%20y_i%20&plus;%204%5CDelta%20y%5C%5C%20%5Cvdots%20%5C%5C%20y_f%20%5Cend%7Bbmatrix%7D">

Both of which can be imaged to a domain _t_:

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7D%20t_1%5C%5C%20t_2%5C%5C%20t_3%5C%5C%20t_4%5C%5C%20t_5%5C%5C%20%5Cvdots%20%5C%5C%20t_n%20%5Cend%7Bbmatrix%7D%20%5Cmapsto%20%5Cbegin%7Bbmatrix%7D%20x_i%5C%5C%20x_i%20&plus;%20%5CDelta%20x%5C%5C%20x_i%20&plus;%202%5CDelta%20x%5C%5C%20x_i%20&plus;%203%5CDelta%20x%5C%5C%20x_i%20&plus;%204%5CDelta%20x%5C%5C%20%5Cvdots%20%5C%5C%20x_f%20%5Cend%7Bbmatrix%7D%2C%20%5Cbegin%7Bbmatrix%7D%20t_1%5C%5C%20t_2%5C%5C%20t_3%5C%5C%20t_4%5C%5C%20t_5%5C%5C%20%5Cvdots%20%5C%5C%20t_n%20%5Cend%7Bbmatrix%7D%20%5Cmapsto%20%5Cbegin%7Bbmatrix%7D%20y_i%5C%5C%20y_i%20&plus;%20%5CDelta%20y%5C%5C%20y_i%20&plus;%202%5CDelta%20y%5C%5C%20y_i%20&plus;%203%5CDelta%20y%5C%5C%20y_i%20&plus;%204%5CDelta%20y%5C%5C%20%5Cvdots%20%5C%5C%20y_f%20%5Cend%7Bbmatrix%7D">

Here, the velocity of the end effector in the x direction and the y direction is constant. This raises a serious concern: the acceleration of _x_ and _y_ at the start (_P_) and end (_Q_) of the path is infinite and negatively infinite, respectively. How can this be overcome? An easy solution is to delinearize the velocity. We start by finding the area of a plot of velocity as a function of _t_ via a Riemann sum:

<!---
\begin{align*} 
a_x &= \sum_{i=1}^C t_i\Delta x\\
a_y &= \sum_{i=1}^C t_i\Delta y
\end{align}
--->
<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20a_x%20%26%3D%20%5Csum_%7Bi%3D1%7D%5EC%20t_i%5CDelta%20x%5C%5C%20a_y%20%26%3D%20%5Csum_%7Bi%3D1%7D%5EC%20t_i%5CDelta%20y%20%5Cend%7Balign%7D">

We can then fit a concave down parabola and find its area:  

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20f%28t%29%20%26%3D%20-%28t%20-%201%29%28t%20-%20C%29%5C%5C%20a_p%20%26%3D%20-%5Cint_1%5EC%28t%20-%201%29%28t%20-%20C%29dt%20%5Cend%7Balign%7D">

We want to equalize the area of the parabola to that of the Riemann sums, that is: 
<!---
\begin{align*}
a_x &= -k_x\int_1^C(t - 1)(t - C)dt\\
a_y &= -k_y\int_1^C(t - 1)(t - C)dt
\end{align}
--->

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20a_x%20%26%3D%20-k_x%5Cint_1%5EC%28t%20-%201%29%28t%20-%20C%29dt%5C%5C%20a_y%20%26%3D%20-k_y%5Cint_1%5EC%28t%20-%201%29%28t%20-%20C%29dt%20%5Cend%7Balign%7D">

To do so, we find two scalars _k_, which we have included as normalization constants in the above integrals,
<!---
\begin{align*}
k_x &= \frac{a_x}{a_p}\\
k_y &= \frac{a_y}{a_p}
\end{align}
--->

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20k_x%20%26%3D%20%5Cfrac%7Ba_x%7D%7Ba_p%7D%5C%5C%20k_y%20%26%3D%20%5Cfrac%7Ba_y%7D%7Ba_p%7D%20%5Cend%7Balign%7D">

<p align="justified">
So do delinearize our end effector velocity in the x and y directions, we fit to:
</p>

<!---
\begin{align*}
x'(t) &= -k_x(t - 1)(t - C)\\
y'(t) &= -k_y(t - 1)(t - C)
\end{align}
--->

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20x%27%28t%29%20%26%3D%20-k_x%28t%20-%201%29%28t%20-%20C%29%5C%5C%20y%27%28t%29%20%26%3D%20-k_y%28t%20-%201%29%28t%20-%20C%29%20%5Cend%7Balign%7D">

Here I show an example of x direction delinearization for the following parameters:

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20P%28x%2C%20y%29%20%26%3D%20%280.3%2C%200.3%2C%200.0%29%5C%5C%20Q%28x%2C%20y%29%20%26%3D%20%280.5%2C%200.5%2C%200.0%29%5C%5C%20C%20%26%3D%20100%20%5Cend%7Balign%7D">

Note that:

<img src="https://latex.codecogs.com/gif.latex?%5CDelta%20x%20%3D%20%5Cfrac%7B0.5%20-%200.3%7D%7B100%7D%20%3D%200.002">

We want to maximize <img src="https://latex.codecogs.com/gif.latex?%5CDelta%20x"> at the midpoint between _P_ and _Q_ and minimize <img src="https://latex.codecogs.com/gif.latex?%5CDelta%20x"> at _P_ and _Q_. The parabola that fits these requirements follows:

<img src="https://latex.codecogs.com/gif.latex?x%27%28t%29%3D-1.237%5Ctimes%2010%5E%7B-6%7D%28t%20-%201%29%28t%20-%20100%29">

A plot of this function is shown below. I have also shown the linear (constant) velocity plot. The areas of both plots are equivalent.

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_trajectory_generation_motion_planning/de_linearize_plot.png" width="500">

And here is a plot of the actual position of _x_ as a function of _t_, or:

<img src="https://latex.codecogs.com/gif.latex?%5Cint%20x%27%28t%29dt%3Dx%28t%29%20&plus;%20c">

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_trajectory_generation_motion_planning/integrated_delinearized.png" width="500">

I have shown the position at constant velocity in light gray. Note that both traces for linear and non-linear velocity diverge from _P_ and converge to _Q_. The non-linear case is more appropriate however, as the velocity increases and decreases smoothly thus minimizing jerk.
                                                                                                                               

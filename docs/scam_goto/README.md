### GOTO Example  
Here I show how to make SCAM's end effector travel to some coordinates of choosing. To run the script, simply open a prompt/terminal and input:  
```
$ python3 /scam/main.py  
``` 
The prompt will return the following:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_goto/example_UI.png" width="500" align=middle>  

A few options will come up. Here I have selected _C_ which allows me to fill two additional fields: x and y. These fields are the 2-dimensional coordinates representing where I want SCAM's end effector to park. In the example, I have selected x = -0.4 and y = -0.4. Below I depict the result:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_goto/-0.4_-0.4.png">  

### The mathematics    
The program starts with two angles:  

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20%5Ctheta_i_1%20%3D%200%5E%5Ccirc%5C%5C%20%5Ctheta_i_2%20%3D%200%5E%5Ccirc%20%5Cend%7Balign%7D">  
<!---
\begin{align*} 
\theta_i_1 = 0^\circ\\
\theta_i_2 = 0^\circ
\end{align}
--->  

Two coordinates are collected from the user, from which two angles are obtained:  

<img src="https://latex.codecogs.com/gif.latex?%5Ctheta_1%2C%20%5Ctheta_2%20%3D%20f%28x%2C%20y%29">  

Here, _f_ refers to the function that solves for the two angles using the inverse kinematics for a 2R mechanism given knowledge of _x_, _y_. Note that in general, uppercase _x_ and _y_ are used to denote the solution coordinates. SCAM must now move the first two links from an initial position to some final position. To do so, the joint angles are updated incrementally _C_ number of times thus yielding the final end effector position. The differential for each angle is computed as follows:  

<!---
\begin{align*} 
\Delta\theta_1 = \frac{\theta_1 - \theta_i_1}{C}\\
\Delta\theta_2 = \frac{\theta_2 - \theta_i_2}{C}\\
\end{align}
--->  

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20%5CDelta%5Ctheta_1%20%3D%20%5Cfrac%7B%5Ctheta_1%20-%20%5Ctheta_i_1%7D%7BC%7D%5C%5C%20%5CDelta%5Ctheta_2%20%3D%20%5Cfrac%7B%5Ctheta_2%20-%20%5Ctheta_i_2%7D%7BC%7D%5C%5C%20%5Cend%7Balign%7D">

This is a far from perfect solution. One problem is that linearly spaced increments result in joints accelerating/decelerating over an infinitesimally short period of time. The joint kinematics section provides a solution to this problem.

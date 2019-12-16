# SCAM  
## Selective Compliance Autosampling Manipulator  
I cannot continue with this project right now due to other priorities!

---  
<p align="justify">
A 3 DOF SCARA style manipulator designed, built and programmed by David S. Weber 
for automating the loading of the Corning 353072 96-well microplate.
This repository contains code for modelling SCAM forward and inverse kinematics.  
See individual folders for more information.
</p> 

---  
### SCAM Solid OpenGL Rendering:
<img src="https://github.com/dsw7/SCAM/blob/master/SCAM_NON_WIREFRAME/img_nonwireframe.png">

---  
### SCAM Wireframe OpenGL Rendering:
<img src="https://github.com/dsw7/SCAM/blob/master/SCAM.png">

---  
### Corning 353072 96-well Microplate:
<img src="https://www.corning.com/catalog/cls/products/f/falcon96WellPolystyreneMicroplates/images/falcon96WellPolystyreneMicroplates_A.jpg/_jcr_content/renditions/product.zoom.1200.jpg" width="500">

---  
### Description of directories:  
    ~/SCAM/2R_IK                    
        // the inverse kinematics for the 2R portion of SCARA RRP
    ~/SCAM/SCAM_GOTO                
        // a basic script depicting how the SCAM end effector 
        // actuates to user defined position at constant joint velocity
    ~/SCAM/SCAM_JOINT_KINEMATICS    
        // a script depicting how the SCAM end effector can actuate
        // to user defined position at quadratically defined joint velocities 
    ~/SCAM/SCAM_JOINT               
        // depiction of a single joint
    ~/SCAM/SCAM_NON_WIREFRAME       
        // depiction of SCAM using GL_POLYGONS,
        // depth buffering, lighting & normal vectors
    ~/SCAM/SCAM_TRAJECTORY_GENERATION_MOTION_PLANNING
        // a description of the mathematics underlying linear trajectory generation
        // and non-linear motion planning
    ~/SCAM/STEPPER_DRIVER_NOT_TESTED
        // reusable .ino code for operating stepper motors
    ~/SCAM/UTILS
        // a directory for storing utility scripts                               
---  

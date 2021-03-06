### SCAM Solid Depiction

This depiction is nearly identical to ~~SCAM_TRAJECTORY_GENERATION_MOTION_PLANNING~~ with the exception of the actual manipulator animation rendering. I changed the following:

* I used filled GL_POLYGONS instead of wireframes to render primitive shapes.  
* I added depth buffering to my animation: objects closer to viewer obscure aligned objects further from the viewer.  
* I added lighting.  
* I added normal vectors to my shapes such that the light ray / polygon surface angle of incidence can be computed. This is important for rendering realistic shading effects.  

Here is the new result:  

<img src="https://github.com/dsw7/SCAM/blob/master/docs/scam_non_wireframe/img_nonwireframe.png" width="400">  

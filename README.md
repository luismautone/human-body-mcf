# Mean Curvature Flow for Fairness

The Python script creates a human 3D model with a limb partiality.
The code simulates an amputation through the deformation of the human shape: firstly vertices and faces belonging to the limb are identified; next a <i>Mean Curvature Flow</i> is applied to them, it has the effect of "smoothing out" the geometry.

<p align="center">![Registrazione schermo 2022-07-14 alle 13 08 10](https://user-images.githubusercontent.com/34343511/196124124-eb3d1ebd-5b69-4e2e-bb88-b16ca891ce1c.gif)</p>

The explored method is part of my MSc thesis in Computer Science at Sapienza University titled "Fairness in Geometry Processing".

## Thesis project

The thesis context is <b>Fair Machine Learning</b>, the study of correcting bias respect to sensitive variables in automated decision processes based on ML models.
Generally current human body model generation methods create human bodies compliant with the standard person capabilities and we have very little material on bodies considered a deviation from the norm. The objective is to work on geometric methods that favor a representation of all human bodies in their diversity.

Specifically we focused on the body modeling aspect of Virtual Humans and its creation given by <i>statistical body models</i>. Statistical body models are geometric models that describe human pose and body shape in a unified framework by leveraging an encoding for mesh surfaces; this technique procudes fastly a human 3D model with a quite satisfactory level of detail. 
We chose <b>SMPL</b> (<i>Skinned Multi-Person Linear</i> Model)[https://smpl.is.tue.mpg.de] as our statistical model.

We generated a 3D dataset with two types of classes: \alpha shapes have the most common appearance for a human body, for each human model we pass to SMPL 72 parameters all set to 0 in order to have a T-pose and 10 parameters with random values ranging from -5 to 5; the goal for shapes of class β was specifically to reproduce the appearance of a person that no longer possesses a limb so we wanted to have a realistic representation of this type of disability. It was important that we did not have a clean cut near the point of amputation, but instead a "smooth" deformation as given by the Mean Curvature Flow algorithm.
Specifically we applied a Conformalized Mean Curvature Flow and we took (mkazhdan code)[[https://arxiv.org/pdf/1203.6819.pdf](https://github.com/mkazhdan/ConformalizedMCF)] as a reference, so convergence problems like extreme expansion of the shape were avoided. 

Next we used an Autoencoder Neural Network for the creation of a latent space that contains the representation for both classes of bodies.

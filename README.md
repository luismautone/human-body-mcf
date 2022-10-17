# Mean Curvature Flow for Fairness

The Python script creates a random human 3D model with a leg partiality.
The code simulates an amputation through the deformation of the human shape: firstly vertices and faces belonging to the limb are identified; next a [<i>Mean Curvature Flow</i>](https://en.wikipedia.org/wiki/Mean_curvature_flow) is applied to them: it has the effect of "smoothing out" the geometry.

![](https://github.com/luismautone/MCF-FairnessGeometryProcessing/blob/main/images/mcf.gif)

The explored method is part of my CS Master's thesis at Sapienza University titled <i>Fairness in Geometry Processing</i>.

## Thesis project

The thesis context is <b>Fair Machine Learning</b>, the study of correcting bias respect to sensitive variables in automated decision processes based on ML models.
Generally current human body model generation methods create human bodies compliant with the standard person capabilities and we have very little material on bodies considered a deviation from the norm. The objective is to work on geometric methods that favor a representation of all human bodies in their diversity.

In particular we focused on the body modeling aspect of Virtual Humans and its creation given by <i>statistical body models</i>. Statistical body models are geometric models that describe human pose and body shape in a unified framework by leveraging an encoding for mesh surfaces; this technique fastly produces a human 3D model with a quite satisfactory level of detail. 
We chose [<b>SMPL</b>](https://smpl.is.tue.mpg.de) as our statistical model.

We generated a 3D dataset with two types of classes: α shapes have the most common appearance for a human body; β shapes reproduce the appearance of a person that no longer possesses a limb. It was important for having a realistic appearance that we did not have a clean cut near the point of amputation, but instead a "smooth" deformation.
Specifically we applied a <b><i>Conformalized Mean Curvature Flow</i></b> and we took [<b>mkazhdan code</b>](https://github.com/mkazhdan/ConformalizedMCF) as a reference, so convergence problems like extreme expansion of the shape were avoided.

<p align="center"><img width="1141" alt="Schermata 2022-10-17 alle 12 06 27" src="https://user-images.githubusercontent.com/34343511/196150981-12eeeb9d-7508-406e-a1d1-67a85d75d3ab.png"></p>
<p align="center"><img width="1283" alt="Schermata 2022-10-17 alle 12 06 33" src="https://user-images.githubusercontent.com/34343511/196151017-009fda55-5920-480d-8680-ce8027895ecc.png"></p>

Next we trained an <b>Autoencoder Neural Network</b> on the dataset for the creation of a latent space that contains the representation for both classes of bodies. For further details go here ().

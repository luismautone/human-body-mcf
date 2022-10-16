from smplpytorch.pytorch.smpl_layer import SMPL_Layer

def smpl_create(): # Create the SMPL layer

    smpl_layer = SMPL_Layer(
        center_idx=0,
        gender='male',
        model_root='smplpytorch/native/models')

    return smpl_layer
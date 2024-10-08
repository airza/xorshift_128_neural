import torch
device = torch.device("mps")
torch.set_default_device(device)
class DifferentiableShiftNetwork(torch.nn.Module):
    def __init__(self,bits,certainty,n=None):
        super().__init__()
        self.bits = bits
        self.certainty = torch.nn.Parameter(torch.Tensor([certainty]).to(device),requires_grad=True)
        self.eyes = bit_shift_matricies(bits).requires_grad_(False)
        if n is not None:
            self.n = torch.nn.Parameter(torch.Tensor([n]).to(device),requires_grad=True)
        else:
            self.n = torch.nn.Parameter(torch.zeros(1), requires_grad=True)

    def forward(self, x):
        c = self.certainty[0]
        return differentiable_shift(x,self.n,self.eyes,c,self.bits)
def gaussian(x, n, sigma=1):
    return torch.exp(-((x-n)**2)/(2*sigma**2))
def weighed_smooth_vector(x, n, sigma=1):
    v = gaussian(x, n, sigma)
    return v/torch.sum(v,0)
def bit_to_minus(n,bits):
    return n-(bits-1)
def brange(bits):
    return range(1-bits,bits)
def bit_shift_matricies(bits):
    eyes = torch.stack([torch.roll(torch.eye(bits), i, 0) for i in brange(bits)])
    for i in range(2 * bits - 1):
        b = bit_to_minus(i,bits)
        if b<0:
            eyes[i][:][b:] = 0.0
        elif b>=0:
            eyes[i][:][:b] = 0.0
    return eyes
def differentiable_shift(x,n,eyes,certainty,bits):
    shift = weighed_smooth_vector(torch.arange(1 - bits, bits, 1), n, 1.0 / certainty)
    mults = torch.sum(shift[:,None,None]*eyes,0)
    return torch.matmul(x,mults)
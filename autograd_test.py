import torch

# requires_grad=False by default
x = torch.ones(2, 2, requires_grad=True)
print(x)
"""tensor([[1., 1.],
        [1., 1.]], requires_grad=True)"""
y = x + 2
# y.retain_grad()
print(y)
"""tensor([[3., 3.],
        [3., 3.]], grad_fn=<AddBackward0>)"""
z = y * y * 3
print(z)
# z.retain_grad()
"""tensor([[27., 27.],
        [27., 27.]], grad_fn=<MulBackward0>)"""
out = z.mean()
print(out)
"""tensor(27., grad_fn=<MeanBackward0>)"""
# because out contains single scalar, out.backward() == out.backward(torch.tensor(1.))
out.backward()
print(x.grad)
"""tensor([[4.5000, 4.5000],
        [4.5000, 4.5000]])"""
# backward pathway out->z->y->x, if not retain_grad(), the grad of y and z are thrown away (intermediate variable)
print(y.grad)
print(z.grad)
"""tensor([[4.5000, 4.5000],
        [4.5000, 4.5000]])
tensor([[0.2500, 0.2500],
        [0.2500, 0.2500]])"""


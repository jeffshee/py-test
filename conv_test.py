# Input (N, C_in, H_in, W_in)
# Output (N, C_out, H_out, W_out)
#
# H_in, W_in = (28, 28)
# padding = (0, 0)
# dilation = (1, 1)
# kernel_size = (5, 5)
# stride = (1, 1)
#
# H_out = int((H_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1)
# W_out = int((W_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1)
# print(H_out, W_out)


def conv(C_in, H_in, W_in, C_out, kernel_size, stride=(1, 1),
         padding=(0, 0), dilation=(1, 1)):
    H_out = int((H_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1)
    W_out = int((W_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1)
    print(C_out, H_out, W_out)
    return C_out, H_out, W_out

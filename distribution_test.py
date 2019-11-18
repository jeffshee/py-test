import warnings
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, entropy
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

# Generate random numbers from normal distributions
x1 = np.random.normal(0, 1, (10000,))
x2 = np.random.normal(0, 1, (10000,))
# Estimate pdf
d1 = gaussian_kde(x1)
d2 = gaussian_kde(x2)

fig = plt.figure()
# Plot histogram
n1, bin1, _ = plt.hist(x1, bins=100, histtype='step', density=True)
n2, bin2, _ = plt.hist(x2, bins=100, histtype='step', density=True)
# Plot estimated pdf
plt.plot(bin1, d1(bin1))
plt.plot(bin2, d2(bin2))
# Calculate KL divergence
min_x = min(bin1.min(), bin2.min())
max_x = max(bin1.max(), bin2.max())
x = np.linspace(min_x, max_x, 100)
print('D_kl', entropy(d1(x), d2(x)))
dm = 1 / 2 * (d1(x) + d2(x))
# Calculate JS divergence
print('D_js', 1 / 2 * entropy(d1(x), dm) + 1 / 2 * entropy(d2(x), dm))
plt.show()

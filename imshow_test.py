import time

import matplotlib.pyplot as plt
import torchvision.utils as utils
from torchvision import transforms

import dataloader_test


def tensor2PIL(tensor, normalize=False):
    img_grid = utils.make_grid(tensor, normalize=normalize)
    return transforms.ToPILImage()(img_grid)


# plt.pause() that don't suck when using interactive mode
# https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7
def pause(interval):
    manager = plt._pylab_helpers.Gcf.get_active()
    if manager is not None:
        canvas = manager.canvas
        if canvas.figure.stale:
            canvas.draw_idle()
        canvas.start_event_loop(interval)
    else:
        time.sleep(interval)


# non-interactive mode
def showPIL(pil):
    plt.ioff()
    plt.imshow(pil)
    plt.show()


# interactive mode
def showPIL_i(pil):
    plt.ion()
    plt.imshow(pil)
    plt.draw()
    # add a little pause if your live data changes too rapidly
    pause(1)


sample, _ = dataloader_test.get_sample()
showPIL(tensor2PIL(sample))

for i in range(10000):
    sample, _ = dataloader_test.get_sample()
    showPIL_i(tensor2PIL(sample))

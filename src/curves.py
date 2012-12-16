import numpy as np
import scipy.io as sio

from lie_algebra_se2 import rotation

class DiscreteCurve:

    def __init__(self, smin=0., smax=1., N=100):
        
        self.smin = smin
        self.smax = smax
        self.N = N

        self.h = (self.smax - self.smin)/self.N
        self.points = np.zeros((self.N, 2))

    def length(self):
        return self.N

    def __getitem__(self, index):
        return self.points[index]

    def __setitem__(self, index, value):
        self.points[index] = value

    def translate(self, disp):
        """
        Uniformly translate points on the curve.

        """
        self.points += np.array(disp)

    def scale(self, factor):
        """
        Scale points of the curve.

        """
        self.points *= factor

    def rotate(self, angle):
        """
        Rotate curve over a given angle.

        """
        R = rotation(-angle)
        self.points = np.dot(self.points, R)

    def save(self, filename):

        d = {'points': self.points, 'N': self.N, 
             'smin': self.smin, 'smax': self.smax}
        sio.savemat(filename, d, oned_as='row')
        
    def load(self, filename):

        d = sio.loadmat(filename)
        self.points = d['points']
        self.N = d['N'][0][0]
        self.smin = d['smin'][0][0]
        self.smax = d['smax'][0][0]


def sample_curve(x, y, smin=0., smax=1., N=100):
    """
    Sample points at regular parameter values to obtain a discrete curve.

    """
    c = DiscreteCurve(smin, smax, N)

    for n in xrange(0, N):
        s = smin + (smax-smin)*n/(N-1)
        c.points[n, :] = x(s), y(s)

    return c


def Circle(radius=1., x0=0., y0=0., N=100):
    """
    Constructor for discrete circle.

    """
    x = lambda s: x0 + radius*np.cos(2*np.pi*s)
    y = lambda s: y0 + radius*np.sin(2*np.pi*s)
    return sample_curve(x, y, 0., 1., N)


def FigureEight(radius=1., x0=0., y0=0., N=100):
    """
    Figure-eight shape.

    """
    x = lambda s: x0 + radius*np.sin(4*np.pi*s)
    y = lambda s: y0 + radius*np.sin(2*np.pi*s)
    return sample_curve(x, y, 0., 1., N)


def LogSpiral(radius=1., x0=0., y0=0., N=100):
    """
    Logarithmic spiral.

    """
    x = lambda s: x0 + radius*np.exp(-s)*np.cos(2*np.pi*s)
    y = lambda s: y0 + radius*np.exp(-s)*np.sin(2*np.pi*s)
    return sample_curve(x, y, 0., 1., N)


def ConstantCurve(x0=0., y0=0., N=100):
    """
    Curve which consists of N copies of the same point.

    """
    d = DiscreteCurve(N=N)
    d.translate((x0, y0))
    return d

from __future__ import print_function

import objc, tensorlib
from .rtclass import RTClass
from collections import defaultdict

class ColorInvertFilter(RTClass):
    """ Wrapper for tensorlib/ColorInvertFilter """
    pass

class HalftoneFilter(RTClass):
    """ Wrapper for tensorlib/HalftoneFilter """
    pass

class SoftEleganceFilter(RTClass):
    """ Wrapper for tensorlib/SoftElegaceFilter """
    pass

class MissEtikateFilter(RTClass):
    """ Wrapper for tensorlib/MissEtikateFilter """
    pass

class SepiaFilter(RTClass):
    """ Wrapper for tensorlib/SepiaFilter """
    pass

class AtkinsonFilter(RTClass):
    """ Wrapper for tensorlib/pixel/AtkinsonFilter """
    pass

class VignetteFilter(RTClass):
    """ Wrapper for tensorlib/VignetteFilter """
    pass

class GrayscaleFilter(RTClass):
    """ Wrapper for tensorlib/GrayscaleFilter """
    pass

class PolkaDotFilter(RTClass):
    """ Wrapper for tensorlib/PolkaDotFilter """
    pass

def split_abbreviations(s):
    abbreviations = []
    current_token = ''
    for char in s:
        if current_token is '':
            current_token += char
        elif char.islower():
            current_token += char
        else:
            abbreviations.append(str(current_token))
            current_token = ''
            current_token += char
    if current_token is not '':
        abbreviations.append(str(current_token))
    return abbreviations

COLORSPACE_MODES = defaultdict(lambda: 'Unknown', {
    'L': "Gray",
    'Gray': "Gray",
    
    'RGB': "RGB",
    'CMYK': "CMYK",
    'LAB': "LAB",
    
    'NCL': "DeviceN",
    'NCL2': "DeviceN",
    'DeviceN': "DeviceN",
    
    'P': "Indexed",
    'Indexed': "Indexed",
    
    'PAT': "Pattern",
    'PPAT': "Pattern",
    'Pattern': "Pattern",
})

COLORSPACE_MODEL = lambda midx: "NS%sColorSpaceModel" % COLORSPACE_MODES[midx]

class Pipe(list):
    """ A linear pipeline of processors to be applied en masse. """
    def process(self, img):
        for p in self:
            img = p.process(img)
        return img

class NOOp(object):
    """ A no-op processor. """
    def process(self, img):
        return img

'''
class ChannelFork(defaultdict):
    """ A processor wrapper that, for each image channel:
        - applies a channel-specific processor, or
        - applies a default processor. """
    
    default_mode = 'RGB' # 'NSRGBColorSpaceModel'
    
    def __init__(self, default_factory, *args, **kwargs):
        if default_factory is None:
            default_factory = NOOp
        if not callable(default_factory):
            raise AttributeError(
                "ChannelFork() requires a callable default_factory.")
        
        self.channels = COLORSPACE_MODEL[kwargs.pop('mode', self.default_mode)]
        
        super(ChannelFork, self).__init__(default_factory, *args, **kwargs)
    
    def __setitem__(self, idx, value):
        if value in (None, NOOp):
            value = NOOp()
        super(ChannelFork, self).__setitem__(idx, value)
    
    @property
    def mode(self):
        return self.channels.mode
    
    @mode.setter
    def mode(self, mode_string):
        self._set_mode(mode_string)
    
    def _set_mode(self, mode_string):
        self.channels = ImageMode.getmode(mode_string)
    
    def compose(self, *channels):
        return Image.merge(
            self.channels.mode,
            channels)
    
    def process(self, img):
        if img.mode != self.channels.mode:
            img = img.convert(self.channels.mode)
        
        processed_channels = []
        for idx, channel in enumerate(img.split()):
            processed_channels.append(
                self[self.channels.bands[idx]].process(channel))
        
        return self.compose(*processed_channels)

class CMYKInk(object):
    """ Renders an input L-mode image,
        by simulating a CMYK primary ink color.
    """
    
    WHITE =     (255,   255,    255)
    CYAN =      (0,     250,    250)
    MAGENTA =   (250,   0,      250)
    YELLOW =    (250,   250,    0)
    KEY =       (0,     0,      0)
    CMYK =      (CYAN, MAGENTA, YELLOW, KEY)
    
    def __init__(self, ink_value=None):
        if ink_value is None:
            ink_value = self.KEY
        self.ink_value = ink_value
    
    def process(self, img):
        from PIL import ImageOps
        return ImageOps.colorize(
            img.convert('L'),
            self.WHITE,
            self.ink_value)


class ChannelOverprinter(ChannelFork):
    """ A ChannelFork subclass that rebuilds its output image using
        multiply-mode to simulate CMYK overprinting effects.
    """
    default_mode = 'CMYK'
    
    def _set_mode(self, mode_string):
        if mode_string != self.default_mode:
            raise AttributeError(
                "ChannelOverprinter can operate in %s mode only" %
                    self.default_mode)
    
    def compose(self, *channels):
        from PIL import ImageChops
        return reduce(ImageChops.multiply, channels)
    
    def process(self, img):
        inks = zip(self.default_mode,
            [CMYKInk(ink_label) \
                for ink_label in CMYKInk.CMYK])
        
        clone = ChannelOverprinter(
            self.default_factory,
            mode=self.channels.mode)
        
        for channel_name, ink in inks:
            clone[channel_name] = Pipe([
                self[channel_name], ink])
        
        return super(ChannelOverprinter, clone).process(img)
'''

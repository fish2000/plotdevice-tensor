//
//  AtkinsonFilter.h
//  PlotDevice
//
//  Created by fish2k on 12/7/13.
//
//

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <GPUImage/GPUImage.h>

#import "../FilterBase.h"

/// inline macro that adds the error so that it doesn't overflow an unsigned char
#ifndef adderror
#define adderror( b, e ) ( ((b) < -(e)) ? 0x00 : ( ((0xFF - (b)) < (e)) ? 0xFF : (b + e) ) )
#endif

/// threshold matrix (in leu of "if something > somethingelse" and suchlike)
static unsigned char threshold[256];

/// forward declaration of the bytearray-level atkinson function
unsigned char *atkinson(unsigned char *pixels, int w, int h, int bpp, int len);

/// FilterBase subclass boilerplate interface
@interface AtkinsonFilter : FilterBase {}

@end
//
//  AtkinsonFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#include <stdio.h>
#include <string.h>

#import "AtkinsonFilter.h"

/// bytearray-level atkinson pixel processing function
unsigned char *atkinson(unsigned char *inputPixels, int w, int h, int bpp, int len) {
    int x, y, off, err;
    unsigned char *outputPixels = malloc(sizeof(unsigned char) * len);
    unsigned char old, new;
    
    if (w * h != len) {
        /// if the dimensions don't fully check out,
        /// I fucking walk
        return NULL;
    }
    
    //memcpy(outputPixels, inputPixels, sizeof(unsigned char) * len * bpp);
    memset(outputPixels, 0, sizeof(unsigned char) * len);
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            off = (y * w) + x;
            outputPixels[off] = inputPixels[off * bpp];
        }
    }
    
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            /// pixel (x, y) offset within the 1D char buffer
            off = (y * w) + x;
            
            /// threshold and error value
            old = outputPixels[off];
            new = threshold[ outputPixels[off] ];
            err = (old - new) >> 3;
            
            /// update the image
            outputPixels[off] = new;
            
            /// add error values
            if (x+1 < w) {
                outputPixels[off + 1] = adderror(outputPixels[off + 1], err);
            }
            if (x+2 < w) {
                outputPixels[off + 2] = adderror(outputPixels[off + 2], err);
            }
            if (x > 0 && y+1 < h) {
                outputPixels[off + w - 1] = adderror(outputPixels[off + w - 1], err);
            }
            if (y+1 < h) {
                outputPixels[off + w] = adderror(outputPixels[off + w], err);
            }
            if (x+1 < w && y+1 < h) {
                outputPixels[off + w + 1] = adderror(outputPixels[off + w + 1], err);
            }
            if (y+2 < h) {
                outputPixels[off + 2 * w] = adderror(outputPixels[off + 2 * w], err);
            }
        }
    }
    
    return outputPixels;
}

/// AtkinsonFilter -- FilterBase subclass implementation
@implementation AtkinsonFilter

- (id)init {
    int i;
    self = [super init];
    
    if (self) {
        for (i = 0; i < 128; i++) {
            threshold[i] = 0x00;
        }
        for (i = 128; i < 256; i++) {
            threshold[i] = 0xFF;
        }
        filter = (GPUImageFilter *)[[GPUImageGrayscaleFilter alloc] init];
    }
    return self;
}

- (NSImage *)process:(NSImage *)input {
    [self STDOUT:@"Preprocessing atkinson filter image"];
    NSImage *inputGrayscale = [filter imageByFilteringImage:input];
    NSBitmapImageRep *inputRep = [NSBitmapImageRep
                                    imageRepWithData:[
                                        inputGrayscale TIFFRepresentation]];
    
    int w = (int)[inputRep pixelsWide];
    int h = (int)[inputRep pixelsHigh];
    int bpp = (int)[inputRep bitsPerPixel] / 8;
    int length = w * h;
    
    [self STDOUT:@"About to call atkinson():"];
    [self STDOUT:@"      WIDTH = %i, HEIGHT = %i, LENGTH = %li, BPP = %i",
        w, h, length, bpp];
    unsigned char *inputData = [inputRep bitmapData];
    unsigned char *outputData = atkinson(inputData, w, h, bpp, length);
    
    if (outputData == NULL) {
        [self STDERR:@"Bad dimensions passed to atkinson():"];
        [self STDERR:@"    WIDTH = %i, HEIGHT = %i, LENGTH = %li",
            w, h, length];
        return inputGrayscale;
    }
    
    NSBitmapImageRep *outputRep = [[[NSBitmapImageRep alloc]
                                    initWithBitmapDataPlanes:&outputData
                                    pixelsWide:w
                                    pixelsHigh:h
                                    bitsPerSample:8
                                    samplesPerPixel:1
                                    hasAlpha:NO
                                    isPlanar:NO
                                    colorSpaceName:NSCalibratedWhiteColorSpace
                                    bytesPerRow:w
                                    bitsPerPixel:8] autorelease];
    
    [self STDOUT:@"About to return atkinson-ized image"];
    NSImage *output = [[NSImage alloc] initWithSize:NSMakeSize(w, h)];
    [output addRepresentation:outputRep];
    return output;
}

@end


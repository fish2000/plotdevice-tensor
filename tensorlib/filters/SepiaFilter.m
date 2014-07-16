//
//  SepiaFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "SepiaFilter.h"

@implementation SepiaFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageSepiaFilter alloc] init];
    }
    return self;
}

@end
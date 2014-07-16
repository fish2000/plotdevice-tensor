//
//  VignetteFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "VignetteFilter.h"

@implementation VignetteFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageVignetteFilter alloc] init];
    }
    return self;
}

@end
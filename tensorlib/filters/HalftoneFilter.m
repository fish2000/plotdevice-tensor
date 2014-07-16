//
//  HalftoneFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "HalftoneFilter.h"

@implementation HalftoneFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageHalftoneFilter alloc] init];
    }
    return self;
}

@end
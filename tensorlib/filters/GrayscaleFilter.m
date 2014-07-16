//
//  GrayscaleFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "GrayscaleFilter.h"

@implementation GrayscaleFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageGrayscaleFilter alloc] init];
    }
    return self;
}

@end
//
//  ColorInvertFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "ColorInvertFilter.h"

@implementation ColorInvertFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageColorInvertFilter alloc] init];
    }
    return self;
}

@end
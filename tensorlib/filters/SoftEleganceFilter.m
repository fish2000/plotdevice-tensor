//
//  SoftEleganceFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "SoftEleganceFilter.h"

@implementation SoftEleganceFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageSoftEleganceFilter alloc] init];
    }
    return self;
}

@end
//
//  PolkaDotFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "PolkaDotFilter.h"

@implementation PolkaDotFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImagePolkaDotFilter alloc] init];
    }
    return self;
}

@end
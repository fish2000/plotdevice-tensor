//
//  MissEtikateFilter.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "MissEtikateFilter.h"

@implementation MissEtikateFilter

- (id)init {
    self = [super init];
    if (self) {
        filter = (GPUImageFilter *)[[GPUImageMissEtikateFilter alloc] init];
    }
    return self;
}

@end
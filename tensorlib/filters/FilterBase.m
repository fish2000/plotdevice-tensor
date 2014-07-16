//
//  FilterBase.m
//  PlotDevice
//
//  Created by fish2k on 12/13/13.
//
//

#import "FilterBase.h"

@implementation FilterBase
@synthesize filter;

- (id)init {
    self = [super init];
    if (!self) {
        return nil;
    }
    return self;
}

- (NSImage *)process:(NSImage *)input {
    return [filter imageByFilteringImage:input];
}

- (void)STDOUT:(NSString *)string, ... {
#ifdef TENSORLIB_STDOUT
    NSString *out = [NSString stringWithFormat:@"[%@] %@",
        [self className], string];
    va_list args;
    
    va_start(args, string);
    NSLogv(out, args);
    NSString *stdOutString = [[NSString alloc] initWithFormat:out arguments:args];
    va_end(args);
    
    fprintf(stdout, "%s\n", [stdOutString UTF8String]);
    [stdOutString release];
#endif
}

- (void)STDERR:(NSString *)string, ... {
#ifdef TENSORLIB_STDERR
    NSString *err = [NSString stringWithFormat:@"[%@] ERROR: %@",
        [self className], string];
    va_list args;
    
    va_start(args, string);
    NSLogv(err, args);
    NSString *stdErrString = [[NSString alloc] initWithFormat:err arguments:args];
    va_end(args);
    
    fprintf(stderr, "%s\n", [stdErrString UTF8String]);
    [stdErrString release];
#endif
}

@end
const std = @import("std");
const print = std.debug.print;
const this = @This();

test "What is this" {
    print("{}\n", .{this});
}

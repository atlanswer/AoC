const std = @import("std");
const print = std.debug.print;

test "packed struct" {
    const Position = packed struct {
        x: usize,
        y: usize,
        z: usize,
    };

    const s1: Position = .{ .x = 1, .y = 2, .z = 3 };
    const s1_2: Position = .{ .x = 1, .y = 2, .z = 3 };
    const s2: Position = .{ .x = 4, .y = 5, .z = 6 };

    print("s1 == s2: {any}\n", .{s1 == s1_2});
    print("s1 == s2: {any}\n", .{s1 == s2});
}

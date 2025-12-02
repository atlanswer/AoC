const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;

test "test test" {
    // print("This is a test.\n", .{});
}

pub fn main() void {
    const input =
        \\L68
        \\L30
        \\R48
        \\L5
        \\R60
        \\L55
        \\L1
        \\L99
        \\R14
        \\L82
    ;
    // print("{s}\n", .{input});

    var lineIterator = std.mem.splitScalar(u8, input, '\n');

    var index: u8 = 1;
    while (lineIterator.next()) |line| : (index += 1) {
        print("line {d}: {s}\n", .{ index, line });
    }

    // print("Type: {}\n", .{@TypeOf(input.*)});
    // print("Type info:\n{}\n", .{@typeInfo(@TypeOf(input.*))});
}

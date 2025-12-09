const std = @import("std");
const print = std.debug.print;

test "Vector" {
    const Position = @Vector(3, usize);
    const v1 = Position{ 1, 2, 3 };
    const v1_2 = Position{ 1, 2, 3 };
    const v2 = Position{ 4, 5, 6 };

    print("{any}: {any}\n", .{ @TypeOf(v1), v1 });
    print("v1 == v1_2: {any}\n", .{v1 == v1_2});
    // print("mem.eql: {any}\n", .{std.mem.eql(usize, v1, v1_2)});
    print("v1 == v2: {any}\n", .{v1 == v2});
    // print("mem.eql: {any}\n", .{std.mem.eql(usize, v1, v2)});
}

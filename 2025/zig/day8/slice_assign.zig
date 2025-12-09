const std = @import("std");
const print = std.debug.print;
const expect = std.testing.expect;

test "slice" {
    var dba = std.heap.DebugAllocator(.{}).init;
    defer expect(dba.deinit() == std.heap.Check.ok) catch unreachable;

    const allocator = dba.allocator();

    var arr = try std.ArrayList(usize).initCapacity(allocator, 10);
    defer arr.deinit(allocator);

    for (0..10) |i| {
        arr.appendAssumeCapacity(i);
    }

    // arr.items[2..4] = arr.items[6..8];
    @memcpy(arr.items[0..4], arr.items[6..10]);

    print("arr: {any}\n", .{arr});
}

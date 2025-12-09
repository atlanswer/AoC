const std = @import("std");
const print = std.debug.print;
const expect = std.testing.expect;

test "auto_hash_map" {
    var dba: std.heap.DebugAllocator(.{}) = .init;
    defer expect(dba.deinit() == std.heap.Check.ok) catch unreachable;
    const allocator = dba.allocator();

    const Position = packed struct { x: usize, y: usize, z: usize };
    const PositionSet = std.AutoArrayHashMap(Position, void);

    var p_set: PositionSet = .init(allocator);
    defer p_set.deinit();

    try p_set.put(.{ .x = 1, .y = 2, .z = 3 }, {});

    for (p_set.keys()) |k| {
        const p: Position = .{ .x = 1, .y = 2, .z = 3 };
        print("key: {any}\n", .{k});
        print("same: {any}\n", .{p == k});
    }
}

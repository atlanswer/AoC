const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;

test "Execution time" {
    var timer = try std.time.Timer.start();
    try main();
    print("Execution time: {d} ms.\n", .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms});
}

test "ArrayList" {
    var grid = std.ArrayList([]const u8).empty;

    try grid.append(allocator, "123");
    try grid.append(allocator, "456");
    try grid.append(allocator, "789");

    print("{any}: {any}\n", .{ @TypeOf(grid), grid });
    print("grid[1][1]: {c}\n", .{grid.items[1][1]});
}

test "tuple" {
    const tu = .{ 1, 2 };

    print("{any}: {any}\n", .{ @TypeOf(tu), tu });
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

pub fn main() !void {
    defer arena.deinit();

    const input =
        \\..@@.@@@@.
        \\@@@.@.@.@@
        \\@@@@@.@.@@
        \\@.@@@@..@.
        \\@@.@@@@.@@
        \\.@@@@@@@.@
        \\.@.@.@.@@@
        \\@.@@@.@@@@
        \\.@@@@@@@@.
        \\@.@.@@@.@.
    ;
    // const input = try getInput();

    var input_it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    // var grid = std.ArrayList(std.array_list.Aligned(u8, null)).empty;

    while (input_it.next()) |line| {
        print("line: {s}\n", .{line});
    }
}

// fn getAdjacentRolls()

fn getInput() ![]u8 {
    const cwd = try std.process.getCwdAlloc(allocator);
    const AOC_DAY = std.fs.path.basename(cwd);
    const input_file_path = try std.fs.path.resolve(allocator, &.{ cwd, "..", "..", "input", AOC_DAY, "input.txt" });

    const input_file = try std.fs.openFileAbsolute(input_file_path, .{});
    defer input_file.close();

    var threaded = std.Io.Threaded.init(allocator);
    defer threaded.deinit();

    var reader = input_file.reader(threaded.io(), try allocator.alloc(u8, 1024));

    return try reader.interface.allocRemaining(allocator, .unlimited);
}

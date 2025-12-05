const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;

test "Execution time" {
    var timer = try std.time.Timer.start();
    try main();
    print("Execution time: {d} ms.\n", .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms});
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

const Grid = std.ArrayList([]u8);
const Coordinate = struct { r: usize, c: usize };

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\..@@.@@@@.
    //     \\@@@.@.@.@@
    //     \\@@@@@.@.@@
    //     \\@.@@@@..@.
    //     \\@@.@@@@.@@
    //     \\.@@@@@@@.@
    //     \\.@.@.@.@@@
    //     \\@.@@@.@@@@
    //     \\.@@@@@@@@.
    //     \\@.@.@@@.@.
    // ;
    const input = try getInput();

    var input_it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    var grid = Grid.empty;

    while (input_it.next()) |row| {
        const row_slice = try allocator.alloc(u8, row.len);
        @memcpy(row_slice, row);
        try grid.append(allocator, row_slice);
    }

    var res: usize = 0;

    var removed: usize = 1;
    while (removed > 0) {
        removed = 0;
        for (0..grid.items.len) |r| {
            for (0..grid.items[0].len) |c| {
                if (grid.items[r][c] != '@') continue;

                const count = try getAdjacentRolls(grid, Coordinate{ .r = r, .c = c });

                if (count < 4) {
                    grid.items[r][c] = '.';
                    removed += 1;
                }
            }
        }
        // print("removed: {d}\n", .{removed});
        res += removed;
    }

    print("removed rolls total: {d}\n", .{res});
}

fn getAdjacentRolls(grid: Grid, coordinate: Coordinate) std.mem.Allocator.Error!usize {
    const n_rows = grid.items.len;
    const n_cols = grid.items[0].len;
    // print("rows: {d}, cols: {d}\n", .{ n_rows, n_cols });

    var res: usize = 0;

    var dr: isize = -1;
    while (dr <= 1) : (dr += 1) {
        var dc: isize = -1;
        while (dc <= 1) : (dc += 1) {
            if (dr == 0 and dc == 0) continue;

            if (dr == -1 and coordinate.r == 0) continue;
            const row = std.math.add(isize, std.math.cast(isize, coordinate.r) orelse continue, dr) catch continue;
            if (row >= n_rows) continue;

            if (dc == -1 and coordinate.c == 0) continue;
            const col = std.math.add(isize, std.math.cast(isize, coordinate.c) orelse continue, dc) catch continue;
            if (col >= n_cols) continue;

            if (grid.items[@bitCast(row)][@bitCast(col)] == '@') {
                res += 1;
            }
        }
    }

    return res;
}

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

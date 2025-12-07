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

const Manifold = std.ArrayList([]const u8);

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\.......S.......
    //     \\...............
    //     \\.......^.......
    //     \\...............
    //     \\......^.^......
    //     \\...............
    //     \\.....^.^.^.....
    //     \\...............
    //     \\....^.^...^....
    //     \\...............
    //     \\...^.^...^.^...
    //     \\...............
    //     \\..^...^.....^..
    //     \\...............
    //     \\.^.^.^.^.^...^.
    //     \\...............
    // ;
    const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    const Timelines = std.ArrayList(usize);
    var timelines = Timelines.empty;

    const first_line = input_it.next().?;
    for (first_line) |char| {
        assert(char == '.' or char == 'S');
        try timelines.append(allocator, if (char == 'S') 1 else 0);
    }

    while (input_it.next()) |line| {
        // print("line: {s}\n", .{line});

        var new_timelines = try Timelines.initCapacity(allocator, line.len);
        new_timelines.appendNTimesAssumeCapacity(0, line.len);

        for (line, 0..) |char, c| {
            assert(char == '.' or char == '^');
            if (char == '^' and timelines.items[c] > 0) {
                if (c > 0) new_timelines.items[c - 1] += timelines.items[c];
                if (c < line.len - 1) new_timelines.items[c + 1] += timelines.items[c];
            }
            if (char == '.') {
                new_timelines.items[c] += timelines.items[c];
            }
        }

        timelines = new_timelines;
    }

    var res: usize = 0;
    for (timelines.items) |t| {
        res += t;
    }

    print("split count: {d}\n", .{res});
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

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

    var res: usize = 0;

    var beam_front = std.ArrayList(bool).empty;

    while (input_it.next()) |line| : ({
        // print("beam: ", .{});
        // for (beam_front.items) |beam| {
        //     const char: u8 = if (beam) '|' else '.';
        //     print("{c}", .{char});
        // }
        // print("\n", .{});
    }) {
        // print("line: {s}\n", .{line});

        if (beam_front.items.len == 0) {
            for (line) |char| {
                assert(char != '^' and (char == '.' or char == 'S'));
                try beam_front.append(allocator, if (char == '.') false else true);
            }
            continue;
        }

        for (line, 0..) |char, idx| {
            assert(char == '.' or char == '^');
            if (char == '^' and beam_front.items[idx]) {
                beam_front.items[idx] = false;
                if (idx > 1) beam_front.items[idx - 1] = true;
                if (idx < line.len - 1) beam_front.items[idx + 1] = true;
                res += 1;
            }
        }
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

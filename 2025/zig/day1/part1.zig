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
    //     \\L68
    //     \\L30
    //     \\R48
    //     \\L5
    //     \\R60
    //     \\L55
    //     \\L1
    //     \\L99
    //     \\R14
    //     \\L82
    // ;
    // print("{s}\n", .{input});
    var input: [1024 * 20]u8 = undefined;
    // const input = try getInput();

    try getInput(&input);

    print("{s}\n", .{input});

    {
        return;
    }

    var dial: i32 = 50;
    var passwd: u32 = 0;

    var line_it = std.mem.splitScalar(u8, input, '\n');
    while (line_it.next()) |line| {
        const direction: u8 = line[0];
        const distance = try std.fmt.parseInt(i32, line[1..], 10);

        dial = if (direction == 'L') dial - distance else dial + distance;
        dial = try std.math.rem(i32, dial, 100);

        if (dial == 0) passwd += 1;

        print("{c}: {d} | {d}, {d}\n", .{ direction, distance, dial, passwd });
    }

    print("passwd: {d}\n", .{passwd});
}

fn getInput(buffer: []u8) !void {
    const cwd = try std.process.getCwdAlloc(allocator);
    const AOC_DAY = std.fs.path.basename(cwd);
    const input_file_path = try std.fs.path.resolve(allocator, &.{ cwd, "..", "..", "input", AOC_DAY, "input.txt" });

    const input_file = try std.fs.openFileAbsolute(input_file_path, .{});
    defer input_file.close();

    const num = try input_file.read(buffer);
    print("{d} bytes read.\n", .{num});
}

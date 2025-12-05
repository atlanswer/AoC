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

const Range = struct { left: usize, right: usize };
const Ranges = std.ArrayList(Range);

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\3-5
    //     \\10-14
    //     \\16-20
    //     \\12-18
    //     \\
    //     \\1
    //     \\5
    //     \\8
    //     \\11
    //     \\17
    //     \\32
    // ;
    const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    var res: usize = 0;
    var ranges = Ranges.empty;

    while (input_it.next()) |line| {
        if (line.len == 0) {
            break;
        }

        var range_it = std.mem.tokenizeScalar(u8, line, '-');
        const left = try std.fmt.parseInt(usize, range_it.next().?, 10);
        const right = try std.fmt.parseInt(usize, range_it.next().?, 10);

        try ranges.append(allocator, Range{ .left = left, .right = right });
    }
    // print("ranges: {any}\n", .{ranges});

    while (true) {
        var new_ranges = Ranges.empty;

        for (ranges.items) |range| {
            try dedupeRanges(&new_ranges, range);
        }

        if (new_ranges.items.len == ranges.items.len) {
            ranges = new_ranges;
            break;
        }
        ranges = new_ranges;
    }
    // print("ranges after dedupe: {any}\n", .{ranges});

    for (ranges.items) |range| {
        res += range.right - range.left + 1;
    }

    print("fresh total: {d}\n", .{res});
}

fn dedupeRanges(ranges: *Ranges, range: Range) !void {
    try ranges.ensureUnusedCapacity(allocator, 1);

    for (ranges.items) |*existing_range| {
        if (range.left > existing_range.right) continue;
        if (range.right < existing_range.left) continue;

        if (range.left >= existing_range.left and range.right <= existing_range.right) break;
        if (range.left <= existing_range.left and range.right >= existing_range.right) {
            existing_range.left = range.left;
            existing_range.right = range.right;
            break;
        }

        if (range.left < existing_range.left and range.right >= existing_range.left and range.right <= existing_range.right) {
            existing_range.left = range.left;
            break;
        }

        if (range.right > existing_range.right and range.left >= existing_range.left and range.left <= existing_range.right) {
            existing_range.right = range.right;
            break;
        }
    } else {
        try ranges.append(allocator, range);
    }
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

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
    //     \\987654321111111
    //     \\811111111111119
    //     \\234234234234278
    //     \\818181911112111
    // ;
    const input = try getInput();
    // print("{s}\n", .{input});

    var total_output_joltage: usize = 0;

    var input_it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    while (input_it.next()) |bank| {
        // print("bank: {s}\n", .{bank});
        total_output_joltage += getJoltage(bank);
    }

    print("total output joltage: {d}\n", .{total_output_joltage});
}

fn getJoltage(bank: []const u8) usize {
    const n_batt = 12;
    var joltage_arr: [n_batt]u8 = undefined;
    var n_remain: usize = n_batt;
    var search_left: usize = 0;
    var search_right: usize = undefined;

    while (n_remain > 0) : (n_remain -= 1) {
        var candidate: u8 = 0;
        var candidate_idx: usize = 0;
        search_right = bank.len - (n_remain - 1);

        for (bank[search_left..search_right], search_left..) |c, i| {
            if (c > candidate) {
                candidate = c;
                candidate_idx = i;
            }
        }

        joltage_arr[n_batt - n_remain] = candidate - '0';
        search_left = candidate_idx + 1;
    }

    // print("joltage: {any}\n", .{joltage});

    var joltage: usize = 0;

    return for (joltage_arr, 0..) |v, i| {
        joltage += v * std.math.pow(usize, 10, joltage_arr.len - 1 - i);
    } else joltage;
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

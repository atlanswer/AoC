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

const Problems = std.ArrayList([]const u8);

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\123 328  51 64 
    //     \\ 45 64  387 23 
    //     \\  6 98  215 314
    //     \\*   +   *   +  
    // ;
    const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    var res: usize = 0;

    var problems = Problems.empty;

    while (input_it.next()) |line| {
        // print("line: {s}\n", .{line});
        try problems.append(allocator, line);
    }
    // print("problems: {any}\n", .{problems});

    var numbers = std.ArrayList(usize).empty;
    var number_arr = std.ArrayList(u8).empty;
    var operator: u8 = ' ';

    var col: isize = std.math.cast(isize, problems.items[0].len - 1).?;
    while (true) : (col -= 1) {
        if (number_arr.items.len != 0) {
            try numbers.append(allocator, 0);
            const cur_number = &numbers.items[numbers.items.len - 1];

            var idx: usize = 0;
            while (number_arr.pop()) |char| : (idx += 1) {
                const digit = char - '0';
                const power = std.math.pow(usize, 10, idx);
                const number_to_add = try std.math.mul(usize, power, @intCast(digit));
                cur_number.* = try std.math.add(usize, cur_number.*, number_to_add);
            }
            // print("new number: {d}\n", .{cur_number.*});
            // print("numbers updated: {any}\n", .{numbers});
        }

        if (operator != ' ') {
            defer operator = ' ';

            var prob_res: usize = if (operator == '+') 0 else 1;
            defer res += prob_res;

            // print("numbers: {any}\n", .{numbers});

            while (numbers.pop()) |number| {
                prob_res = if (operator == '+')
                    try std.math.add(usize, prob_res, number)
                else
                    try std.math.mul(usize, prob_res, number);
            }
            // print("new problem: {c}, res: {d}\n", .{ operator, prob_res });
        }

        if (col < 0) break;
        const col_idx = std.math.cast(usize, col).?;

        for (0..problems.items.len) |row_idx| {
            const char = problems.items[row_idx][col_idx];
            if (char != ' ') {
                if (char == '+' or char == '*') {
                    operator = char;
                } else {
                    try number_arr.append(allocator, char);
                }
            }
        }
    }

    print("grand total: {d}\n", .{res});
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

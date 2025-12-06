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

const ProbRow = std.ArrayList(usize);
const ProbRows = std.ArrayList(ProbRow);
const OperatorRow = std.ArrayList(u8);

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

    var prob_rows = ProbRows.empty;
    var operator_row = OperatorRow.empty;

    while (input_it.next()) |line| {
        // print("line: {s}\n", .{line});
        var prob_row = ProbRow.empty;

        if (input_it.peek() == null) {
            var operator_it = std.mem.tokenizeScalar(u8, line, ' ');
            while (operator_it.next()) |operator| {
                assert(operator.len == 1);
                try operator_row.append(allocator, operator[0]);
            }
            break;
        }

        var number_it = std.mem.tokenizeScalar(u8, line, ' ');
        while (number_it.next()) |number_s| {
            const number = try std.fmt.parseInt(usize, number_s, 10);
            try prob_row.append(allocator, number);
        }
        try prob_rows.append(allocator, prob_row);
    }

    for (0..prob_rows.items[0].items.len) |idx| {
        var prob_res: usize = if (operator_row.items[idx] == '+') 0 else 1;
        for (prob_rows.items) |prob_row| {
            prob_res = if (operator_row.items[idx] == '+')
                try std.math.add(usize, prob_res, prob_row.items[idx])
            else
                try std.math.mul(usize, prob_res, prob_row.items[idx]);
        }
        res += prob_res;
    }

    // print("prob: {any}\n", .{prob_rows});
    // print("operator: {any}\n", .{operator_row});
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

const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;

test "Execution time" {
    try expect(try isValidId(55) == false);
    try expect(try isValidId(6464) == false);
    try expect(try isValidId(123123) == false);
    try expect(try isValidId(11) == false);
    try expect(try isValidId(22) == false);
    try expect(try isValidId(99) == false);
    try expect(try isValidId(1010) == false);
    try expect(try isValidId(1188511885) == false);
    try expect(try isValidId(222222) == false);
    try expect(try isValidId(446446) == false);
    try expect(try isValidId(38593859) == false);

    var timer = try std.time.Timer.start();
    try main();
    print("Execution time: {d} ms.\n", .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms});
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

pub fn main() !void {
    defer arena.deinit();

    // const input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
    const input = try getInput();
    // print("{s}\n", .{input});

    var invalid_id_sum: usize = 0;

    var input_it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, input, "\n"), ',');

    while (input_it.next()) |range| {
        var range_it = std.mem.tokenizeScalar(u8, range, '-');

        const first_id = range_it.next().?;
        const last_id = range_it.next().?;
        if (first_id[0] == '0' or last_id[0] == '0') return error.IdStartsAt0;

        const lv = try std.fmt.parseInt(usize, first_id, 10);
        const rv = try std.fmt.parseInt(usize, last_id, 10);

        // print("{s} - {s}\n", .{ first_id, last_id });
        // print("{d} - {d}\n", .{ lv, rv });
        for (lv..rv + 1) |id| {
            invalid_id_sum += if (try isValidId(id)) 0 else id;
        }
    }

    print("sum of invalid ids: {d}\n", .{invalid_id_sum});
}

fn isValidId(id: usize) !bool {
    const id_arr = try std.fmt.allocPrint(allocator, "{d}", .{id});
    const id_len = id_arr.len;
    // print("id: {s}, len: {d}\n", .{ id_arr, id_len });

    if (id_len % 2 != 0) return true;

    const first_half = id_arr[0 .. id_len / 2];
    const second_half = id_arr[id_len / 2 ..];
    // print("first half: {s}, second half: {s}\n", .{ first_half, second_half });

    if (std.mem.eql(u8, first_half, second_half)) return false;

    return true;
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

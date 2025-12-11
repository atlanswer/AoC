const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;

test "Execution time" {
    var timer = try std.time.Timer.start();
    try main();
    print(
        "Execution time: {d} ms.\n",
        .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms},
    );
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

const Position = packed struct { x: usize, y: usize };
const Positions = std.ArrayList(Position);
const Grid = std.ArrayList(std.ArrayList(u8));

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\7,1
    //     \\11,1
    //     \\11,7
    //     \\9,7
    //     \\9,5
    //     \\2,5
    //     \\2,3
    //     \\7,3
    // ;
    const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    var positions: Positions = .empty;
    var width: usize = 0;
    var height: usize = 0;

    var cnt: usize = 0;

    while (input_it.next()) |line| : ({}) {
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const x = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const y = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        const position: Position = .{ .x = x, .y = y };
        try positions.append(allocator, position);

        if (x > height) height = x + 1;
        if (y > width) width = y + 1;

        cnt += 1;
    }

    print("Grid width: {}, height: {}\n", .{ width, height });
    print("Line count: {}\n", .{cnt});

    // var max_area: usize = 0;
    // var count: usize = 0;

}

fn getArea(pa: Position, pb: Position) usize {
    const dx = if (pa.x > pb.x) pa.x - pb.x + 1 else pb.x - pa.x + 1;
    const dy = if (pa.y > pb.y) pa.y - pb.y + 1 else pb.y - pa.y + 1;
    return dx * dy;
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

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

const Position = @Vector(2, usize);
const Positions = std.ArrayList(Position);

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

    while (input_it.next()) |line| : ({}) {
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const x = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const y = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        const position: Position = .{ x, y };
        try positions.append(allocator, position);
    }

    var max_area: usize = 0;
    var count: usize = 0;

    for (0..positions.items.len) |i| {
        for (i + 1..positions.items.len) |j| {
            const area = getArea(positions.items[i], positions.items[j]);

            if (area > max_area) {
                max_area = area;
            }

            count += 1;
            if (count % 1000 == 0) {
                print("counting: {}\n", .{count});
            }
        }
    }

    print("res: {}\n", .{max_area});
}

fn getArea(pa: Position, pb: Position) usize {
    const dx = if (pa[0] > pb[0]) pa[0] - pb[0] + 1 else pb[0] - pa[0] + 1;
    const dy = if (pa[1] > pb[1]) pa[1] - pb[1] + 1 else pb[1] - pa[1] + 1;
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

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

const Position = struct { x: usize, y: usize, z: usize };

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\162,817,812
    //     \\57,618,57
    //     \\906,360,560
    //     \\592,479,940
    //     \\352,342,300
    //     \\466,668,158
    //     \\542,29,236
    //     \\431,825,988
    //     \\739,650,466
    //     \\52,470,668
    //     \\216,146,977
    //     \\819,987,18
    //     \\117,168,530
    //     \\805,96,715
    //     \\346,949,466
    //     \\970,615,88
    //     \\941,993,340
    //     \\862,61,35
    //     \\984,92,344
    //     \\425,690,689
    // ;
    const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    var positions = std.ArrayList(Position).empty;

    while (input_it.next()) |line| : ({}) {
        // print("line: {s}\n", .{line});
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const x = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const y = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const z = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        try positions.append(allocator, Position{ .x = x, .y = y, .z = z });
    }
    // print("positions: {any}\n", .{positions});

    var distances = std.ArrayList(struct { pa: *const Position, pb: *const Position, distance: f64 }).empty;

    for (0..positions.items.len) |i| {
        for (i + 1..positions.items.len) |j| {
            const pa = positions.items[i];
            const pb = positions.items[j];
            const distance = try getDistance(pa, pb);

            try distances.append(allocator, .{ .pa = &pa, .pb = &pb, .distance = distance });
        }
    }
    // print("distances: {any}\n", .{distances});
    // print("len: {d}\n", .{distances.items.len});

    // print("split count: {d}\n", .{res});
}

fn getDistance(pa: Position, pb: Position) !f64 {
    const x2 = std.math.pow(usize, if (pa.x > pb.x) pa.x - pb.x else pb.x - pa.x, 2);
    const y2 = std.math.pow(usize, if (pa.y > pb.y) pa.y - pb.y else pb.y - pa.y, 2);
    const z2 = std.math.pow(usize, if (pa.z > pb.z) pa.z - pb.z else pb.z - pa.z, 2);
    const sum = x2 + y2 + z2;
    return std.math.sqrt(@as(f64, @floatFromInt(sum)));
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

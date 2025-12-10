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

const Position = packed struct { x: usize, y: usize, z: usize };
const Positions = std.ArrayList(Position);
const Distance = struct { distance: usize, pa: *const Position, pb: *const Position };
const Distances = std.ArrayList(Distance);
const Circuit = std.AutoArrayHashMap(*const Position, void);
const Circuits = std.ArrayList(Circuit);

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

    var positions: Positions = .empty;

    while (input_it.next()) |line| : ({}) {
        // print("line: {s}\n", .{line});
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const x = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const y = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const z = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        const position: Position = .{ .x = x, .y = y, .z = z };
        try positions.append(allocator, position);
    }

    var distances = try Distances.initCapacity(
        allocator,
        positions.items.len * (positions.items.len - 1) / 2,
    );

    for (0..positions.items.len) |i| {
        for (i + 1..positions.items.len) |j| {
            const pa: *const Position = &positions.items[i];
            const pb: *const Position = &positions.items[j];
            const distance = getDistance(pa.*, pb.*);

            distances.appendAssumeCapacity(.{
                .pa = pa,
                .pb = pb,
                .distance = distance,
            });
        }
    }

    const asc = struct {
        fn inner(_: void, a: Distance, b: Distance) bool {
            return a.distance < b.distance;
        }
    }.inner;

    std.mem.sortUnstable(Distance, distances.items, {}, asc);

    var circuits: Circuits = .empty;

    for (distances.items) |distance| {
        var pending_idxes = std.ArrayList(usize).empty;

        for (0..circuits.items.len) |idx| {
            if (circuits.items[idx].contains(distance.pa) or circuits.items[idx].contains(distance.pb)) {
                try pending_idxes.append(allocator, idx);
            }
        }

        if (pending_idxes.items.len == 0) {
            var new_circuit: Circuit = .init(allocator);
            try new_circuit.put(distance.pa, {});
            try new_circuit.put(distance.pb, {});
            try circuits.append(allocator, new_circuit);

            continue;
        }

        var first_circuit: *Circuit = &circuits.items[pending_idxes.items[0]];
        try first_circuit.put(distance.pa, {});
        try first_circuit.put(distance.pb, {});

        for (pending_idxes.items[1..]) |idx| {
            const circuit = circuits.items[idx];
            for (circuit.keys()) |k| {
                try first_circuit.put(k, {});
            }
        }

        var idx: usize = pending_idxes.items.len - 1;
        while (idx >= 1) : (idx -= 1) _ = circuits.swapRemove(pending_idxes.items[idx]);

        var n_connected: usize = 0;
        for (circuits.items) |circuit| {
            n_connected += circuit.count();
        }
        if (n_connected == positions.items.len) {
            print("distance: {}\n", .{distance});

            print("res: {}\n", .{distance.pa.x * distance.pb.x});

            break;
        }
    }
}

fn getDistance(pa: Position, pb: Position) usize {
    const x2 = std.math.pow(usize, if (pa.x > pb.x) pa.x - pb.x else pb.x - pa.x, 2);
    const y2 = std.math.pow(usize, if (pa.y > pb.y) pa.y - pb.y else pb.y - pa.y, 2);
    const z2 = std.math.pow(usize, if (pa.z > pb.z) pa.z - pb.z else pb.z - pa.z, 2);
    return x2 + y2 + z2;
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

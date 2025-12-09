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

const connection: usize = 10;

pub fn main() !void {
    defer arena.deinit();

    const input =
        \\162,817,812
        \\57,618,57
        \\906,360,560
        \\592,479,940
        \\352,342,300
        \\466,668,158
        \\542,29,236
        \\431,825,988
        \\739,650,466
        \\52,470,668
        \\216,146,977
        \\819,987,18
        \\117,168,530
        \\805,96,715
        \\346,949,466
        \\970,615,88
        \\941,993,340
        \\862,61,35
        \\984,92,344
        \\425,690,689
    ;
    // const input = try getInput();

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');

    while (input_it.next()) |line| : ({}) {
        // print("line: {s}\n", .{line});
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const x = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const y = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const z = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        // try positions.append(allocator, Position{ .x = x, .y = y, .z = z });
    }

    // var distance_list = try DistanceList.initCapacity(
    //     allocator,
    //     positions.items.len * (positions.items.len - 1) / 2,
    // );

    // for (0..positions.items.len) |i| {
    //     for (i + 1..positions.items.len) |j| {
    //         const pa = positions.items[i];
    //         const pb = positions.items[j];
    //         const distance = getDistance(pa, pb);

    //         distance_list.appendAssumeCapacity(.{
    //             .pa = pa,
    //             .pb = pb,
    //             .distance = distance,
    //         });
    //     }
    // }
    // print("connections: {d}\n", .{distance_list.items.len});

    // const asc = struct {
    //     fn inner(_: void, a: DistanceRecord, b: DistanceRecord) bool {
    //         return a.distance < b.distance;
    //     }
    // }.inner;

    // std.mem.sortUnstable(DistanceRecord, distance_list.items, {}, asc);

    // print("distance_list:\n", .{});
    // for (0..connection) |idx| {
    //     print("{any}\n", .{distance_list.items[idx]});
    // }

    // for (0..connection) |idx| {
    //     const record = distance_list.items[idx];
    //     const pa = record.pa;
    //     const pb = record.pb;

    //     var c: usize = 0;
    //     const end = circuits.items.len;

    //     while (c < end) : (c += 1) {
    //         const cur_circuit = circuits.items[c];

    //         var have_pa = false;
    //         var have_pb = false;
    //         for (cur_circuit.items) |p| {
    //             if (p.x == pa.x and p.y == pa.y and p.z == pa.z) {
    //                 have_pa = true;
    //             }
    //             if (p.x == pb.x and p.y == pb.y and p.z == pb.z) {
    //                 have_pb = true;
    //             }
    //         } else {
    //             if (have_pa and have_pb) break;
    //             if (have_pa) {
    //                 try circuits.items[c].append(allocator, pb);
    //                 break;
    //             }
    //             if (have_pb) {
    //                 try circuits.items[c].append(allocator, pa);
    //                 break;
    //             }
    //         }
    //     } else {
    //         var new_circuit = std.ArrayList(Position).empty;
    //         try new_circuit.append(allocator, pa);
    //         try new_circuit.append(allocator, pb);
    //         try circuits.append(allocator, new_circuit);
    //     }
    // }

    // print("circuits:\n", .{});
    // for (circuits.items) |circuit| {
    //     print("{any}\n", .{circuit});
    // }

    // var sizes = try std.ArrayList(usize).initCapacity(allocator, connection);
    // for (circuits.items) |circuit| {
    //     sizes.appendAssumeCapacity(circuit.items.len);
    // }

    // std.sort.insertion(usize, sizes.items, {}, comptime std.sort.desc(usize));
    // print("sizes: {any}\n", .{sizes.items});

    // var res: usize = 1;
    // for (0..3) |idx| {
    //     res *= sizes.items[idx];
    // }
    // print("res: {d}\n", .{res});
}

// fn getDistance(pa: Position, pb: Position) usize {
//     const x2 = std.math.pow(usize, if (pa.x > pb.x) pa.x - pb.x else pb.x - pa.x, 2);
//     const y2 = std.math.pow(usize, if (pa.y > pb.y) pa.y - pb.y else pb.y - pa.y, 2);
//     const z2 = std.math.pow(usize, if (pa.z > pb.z) pa.z - pb.z else pb.z - pa.z, 2);
//     return x2 + y2 + z2;
// }

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

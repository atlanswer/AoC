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

const Position = packed struct { r: usize, c: usize };
const Positions = std.ArrayList(Position);
const Grid = std.ArrayList(std.ArrayList(u8));
const HLine = struct { r: usize, cs: usize, ce: usize };
const HLines = std.ArrayList(HLine);
const VLine = struct { c: usize, rs: usize, re: usize };
const VLines = std.ArrayList(VLine);

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

    var line_count: usize = 0;
    var horizontal_lines = HLines.empty;
    var vertical_lines = VLines.empty;

    while (input_it.next()) |line| : ({}) {
        var coordinate_it = std.mem.tokenizeScalar(u8, line, ',');

        const r = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);
        const c = try std.fmt.parseInt(usize, coordinate_it.next().?, 10);

        const position: Position = .{ .r = r, .c = c };

        if (r > height) height = r + 1;
        if (c > width) width = c + 1;

        if (positions.items.len > 0) {
            const last_position = positions.getLast();

            if (position.r == last_position.r) {
                const cs, const ce = if (position.c < last_position.c)
                    .{ position.c, last_position.c }
                else
                    .{ last_position.c, last_position.c };
                try horizontal_lines.append(allocator, .{ .r = position.r, .cs = cs, .ce = ce });
            }

            if (position.c == last_position.c) {
                const rs, const re = if (position.r < last_position.r)
                    .{ position.r, last_position.r }
                else
                    .{ last_position.r, position.r };
                try vertical_lines.append(allocator, .{ .c = position.c, .rs = rs, .re = re });
            }
        }

        try positions.append(allocator, position);

        line_count += 1;
    }

    print("Grid width: {}, height: {}\n", .{ width, height });
    print("Line count: {}\n", .{line_count});

    std.mem.sortUnstable(HLine, horizontal_lines.items, {}, struct {
        fn hLineLessThan(_: void, a: HLine, b: HLine) bool {
            return a.r < b.r;
        }
    }.hLineLessThan);

    std.mem.sortUnstable(VLine, vertical_lines.items, {}, struct {
        fn vLineLessThan(_: void, a: VLine, b: VLine) bool {
            return a.c < b.c;
        }
    }.vLineLessThan);

    print("horizontal_lines:\n", .{});
    for (horizontal_lines.items) |h| {
        print("{}\n", .{h});
    }
    print("vertical_lines:\n", .{});
    for (vertical_lines.items) |v| {
        print("{}\n", .{v});
    }

    var max_area: usize = 0;

    for (positions.items, 0..) |p1, i| {
        for (positions.items[i + 1 ..]) |p2| {
            const rs, const re = if (p1.r < p2.r) .{ p1.r, p2.r } else .{ p2.r, p1.r };
            const cs, const ce = if (p1.c < p2.c) .{ p1.c, p2.c } else .{ p2.c, p1.c };
        }
    }
}

fn searchBetween(
    list: *const union(enum) {
        vlist: VLines,
        hlist: HLines,
        fn len(list: @This()) usize {
            return switch (list) {
                .vlist => |l| l.items.len,
                .hlist => |l| l.items.len,
            };
        }
        fn get(list: @This(), idx: usize) usize {
            assert(idx >= 0);
            assert(idx < list.len());
            return switch (list) {
                .hlist => |l| l.items[idx],
                .vlist => |l| l.items[idx],
            };
        }
    },
    low: usize,
    high: usize,
) error{NotFound}!.{ usize, usize } {
    var i_start: usize = 0;
    var i_end: usize = list.len() - 1;

    if (list.get(i_start) > high or list.get(i_end) < low)
        return error{NotFound};

    while (i_start < i_end) {
        const mid = (i_end - i_start) / 2;
    }
}

fn getArea(pa: Position, pb: Position) usize {
    const dx = if (pa.r > pb.r) pa.r - pb.r + 1 else pb.r - pa.r + 1;
    const dy = if (pa.c > pb.c) pa.c - pb.c + 1 else pb.c - pa.c + 1;
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

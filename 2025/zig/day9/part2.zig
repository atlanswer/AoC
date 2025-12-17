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

    const input =
        \\7,1
        \\11,1
        \\11,7
        \\9,7
        \\9,5
        \\2,5
        \\2,3
        \\7,3
    ;
    // const input = try getInput();

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
        outer: for (positions.items[i + 1 ..]) |p2| {
            const rs, const re = if (p1.r < p2.r) .{ p1.r, p2.r } else .{ p2.r, p1.r };
            const cs, const ce = if (p1.c < p2.c) .{ p1.c, p2.c } else .{ p2.c, p1.c };
            const cond = rs == 2 and cs == 3 and re == 9 and ce == 5;
            if (!cond) continue;
            print("tl: {},{}, br: {},{}\n", .{ rs, cs, re, ce });

            // Horizontal lines
            {
                const i_low = searchBetween(.{ .hlines = &horizontal_lines }, rs, .gt);
                print("i_low: {any}\n", .{i_low});
                const i_high = searchBetween(.{ .hlines = &horizontal_lines }, re, .lt);
                print("i_high: {any}\n", .{i_high});

                print("hline: low: {any}, high: {any}\n", .{ i_low, i_high });

                if (i_low != null and i_high != null) {
                    if (i_low.? > i_high.?) continue;
                    var idx: usize = i_low.?;
                    while (idx <= i_high.?) : (idx += 1) {
                        const hline = horizontal_lines.items[idx];
                        if (hline.cs <= cs and hline.ce > cs) continue :outer;
                        if (hline.cs < ce and hline.ce >= ce) continue :outer;
                    }
                }
            }
            // Vertical lines
            {
                const i_low = searchBetween(.{ .vlines = &vertical_lines }, cs, .gt);
                const i_high = searchBetween(.{ .vlines = &vertical_lines }, ce, .lt);

                print("vline: low: {any}, high: {any}\n", .{ i_low, i_high });

                if (i_low != null and i_high != null) {
                    if (i_low.? > i_high.?) continue;
                    var idx: usize = i_low.?;
                    while (idx <= i_high.?) : (idx += 1) {
                        const vline = vertical_lines.items[idx];
                        if (vline.rs <= rs and vline.re > rs) continue :outer;
                        if (vline.rs < re and vline.re >= re) continue :outer;
                    }
                }
            }

            const area = getArea(p1, p2);
            if (area > max_area) max_area = area;
        }
    }

    print("max area: {}\n", .{max_area});
}

fn searchBetween(
    list: union(enum) {
        vlines: *const VLines,
        hlines: *const HLines,
        fn len(list: @This()) usize {
            return switch (list) {
                .vlines => |l| l.items.len,
                .hlines => |l| l.items.len,
            };
        }
        fn get(list: @This(), idx: usize) usize {
            assert(idx >= 0);
            assert(idx < list.len());
            return switch (list) {
                .hlines => |l| l.items[idx].r,
                .vlines => |l| l.items[idx].c,
            };
        }
    },
    context: usize,
    relation: enum { lt, gt },
) ?usize {
    var i_start: usize = 0;
    var i_end: usize = list.len();
    print("i_start: {}, i_end: {}\n", .{i_start, i_end});

    while (i_start < i_end) {
        const i_mid = i_start + (i_end - i_start) / 2;
        print("i_mid: {}\n", .{i_mid});

        switch (relation) {
            .gt => {
                if (list.get(i_mid) <= context) {
                    i_start = i_mid + 1;
                    continue;
                }
                if (i_mid == 0 or list.get(i_mid - 1) <= context) {
                    return i_mid;
                } else {
                    i_end = i_mid;
                    continue;
                }
            },
            .lt => {
                if (list.get(i_mid) >= context) {
                    i_end = i_mid;
                    continue;
                }
                if (i_mid == list.len() - 1 or list.get(i_mid + 1) >= context) {
                    return i_mid;
                } else {
                    i_start = i_mid + 1;
                }
            },
        }
    }
    return null;
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

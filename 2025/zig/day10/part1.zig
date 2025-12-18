const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;
const getInput = @import("aoc-utils.zig").getInput;
const timeIt = @import("aoc-utils.zig").timeIt;

test "Execution time" {
    try timeIt(main);
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    //     \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    //     \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    // ;
    const input = try getInput(allocator);

    // var min_light: usize = std.math.maxInt(usize);
    // var max_light: usize = 0;
    // var min_button: usize = std.math.maxInt(usize);
    // var max_button: usize = 0;

    var res: usize = 0;

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');
    while (input_it.next()) |line| : ({}) {
        // print("{s}\n", .{line});

        var lights: u16 = 0;
        var buttons = std.ArrayList(u16).empty;

        var section_it = std.mem.splitScalar(u8, line, ' ');
        while (section_it.next()) |section| {
            // Light diagram
            if (section[0] == '[' and section[section.len - 1] == ']') {
                const l = section.len - 2;

                for (0..l) |i| {
                    if (section[1 .. section.len - 1][i] == '#') {
                        lights |= @as(u16, 1) <<| (15 - i);
                    }
                }

                // if (l > max_light) max_light = l;
                // if (l < min_light) min_light = l;
            }
            // Button wiring schematic
            if (section[0] == '(' and section[section.len - 1] == ')') {
                var button: u16 = 0;
                var wire_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                while (wire_it.next()) |wire_s| {
                    const wire: usize = try std.fmt.parseInt(usize, wire_s, 10);
                    button |= @as(u16, 1) <<| (15 - wire);
                }
                try buttons.append(allocator, button);
            }
            // Joltage requirement
            // if (section[0] == '{' and section[section.len - 1] == '}') {}
        }
        // print("lights: {b:0>16}\n", .{lights});
        // print("button:\n", .{});
        // for (buttons.items) |button| {
        //     print("{b:0>16}\n", .{button});
        // }

        var step: usize = 1;
        outer: while (true) : (step += 1) {
            assert(step <= buttons.items.len);

            const combs = try combination(buttons.items.len, step);

            for (combs.items) |comb| {
                var result: u16 = 0;

                for (comb.items) |i| {
                    result = switchLight(result, buttons.items[i]);
                }

                if (result == lights) break :outer;
            }
        }

        // print("step: {}\n", .{step});

        res += step;

        // if (buttons.items.len > max_button) max_button = buttons.items.len;
        // if (buttons.items.len < min_button) min_button = buttons.items.len;
    }

    // print("min light: {}\n", .{min_light});
    // print("max light: {}\n", .{max_light});
    // print("min button: {}\n", .{min_button});
    // print("max button: {}\n", .{max_button});

    print("res: {}\n", .{res});
}

fn switchLight(light: u16, button: u16) u16 {
    return (~light & button) | (light & ~button);
}

// test "combination" {
//     print("C(3, 2): ", .{});
//     for ((try combination(3, 2)).items) |c| {
//         print("{}\n", .{c});
//     }
// }

fn combination(n: usize, k: usize) !std.ArrayList(std.ArrayList(usize)) {
    var result: std.ArrayList(std.ArrayList(usize)) = .empty;
    var idxs: std.ArrayList(usize) = try .initCapacity(allocator, k);
    for (0..k) |idx| idxs.appendAssumeCapacity(idx);
    // print("idxs: {}\n", .{idxs});

    outer: while (true) {
        try result.append(allocator, try idxs.clone(allocator));

        var i: usize = k - 1;
        while (i >= 0 and idxs.items[i] == n - k + i) : ({
            if (i == 0) break :outer;
            i -= 1;
        }) {}

        idxs.items[i] += 1;
        for (i + 1..k) |nidx| idxs.items[nidx] = idxs.items[nidx - 1] + 1;
        // print("idxs: {}\n", .{idxs});
    }

    return result;
}

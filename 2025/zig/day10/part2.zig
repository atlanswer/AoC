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

const Counter = @Vector(8, usize);

pub fn main() !void {
    defer arena.deinit();

    const input =
        \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    ;
    // const input = try getInput(allocator);

    var res: usize = 0;

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');
    while (input_it.next()) |line| : ({}) {
        // print("{s}\n", .{line});

        var buttons: std.ArrayList(Counter) = .empty;
        var joltages: Counter = undefined;

        var section_it = std.mem.splitScalar(u8, line, ' ');
        while (section_it.next()) |section| {
            // Light diagram
            // if (section[0] == '[' and section[section.len - 1] == ']') {}

            // Button wiring schematic
            if (section[0] == '(' and section[section.len - 1] == ')') {
                var button_arr: [8]usize = .{ 0, 0, 0, 0, 0, 0, 0, 0 };
                var wire_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                while (wire_it.next()) |wire_s| {
                    const wire: usize = try std.fmt.parseInt(usize, wire_s, 10);
                    button_arr[wire] = 1;
                }
                const button: Counter = button_arr;
                try buttons.append(allocator, button);
            }

            // Joltage counter
            if (section[0] == '{' and section[section.len - 1] == '}') {
                var idx: usize = 0;
                var joltage_arr: [8]usize = .{ 0, 0, 0, 0, 0, 0, 0, 0 };
                var joltage_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                while (joltage_it.next()) |joltage_s| : (idx += 1) {
                    const joltage = try std.fmt.parseInt(usize, joltage_s, 10);
                    joltage_arr[idx] = joltage;
                }
                joltages = joltage_arr;
            }
        }

        // print("button:\n", .{});
        // for (buttons.items) |button| {
        //     print("{any}\n", .{button});
        // }
        // print("joltages: {}\n", .{joltages});

        const step: usize = try findPresses(joltages, buttons);
        print("step: {d}\n", .{step});

        res += 1;
    }

    print("res: {}\n", .{res});
}

fn findPresses(joltages: Counter, buttons: std.ArrayList(Counter)) !usize {
    print("current joltage counter: {any}\n", .{joltages});
    const max_joltage: usize = @reduce(.Max, joltages);
    assert(max_joltage != 0);
    print("max joltage: {d}\n", .{max_joltage});

    for (1..max_joltage + 1) |cur_max_joltage| {
        if (cur_max_joltage > buttons.items.len) break;
        const comb = try combination(buttons.items.len, cur_max_joltage);
        print("cur_max: {}\n", .{cur_max_joltage});
        print("comb:\n", .{});
        for (comb.items) |c| {
            print("{any}\n", .{c});
        }
    }

    return 1;
}

fn switchLight(light: u16, button: u16) u16 {
    return (~light & button) | (light & ~button);
}

fn combination(n: usize, k: usize) !std.ArrayList(std.ArrayList(usize)) {
    var result: std.ArrayList(std.ArrayList(usize)) = .empty;
    var idxs: std.ArrayList(usize) = try .initCapacity(allocator, k);
    for (0..k) |idx| idxs.appendAssumeCapacity(idx);

    outer: while (true) {
        try result.append(allocator, try idxs.clone(allocator));

        var i: usize = k - 1;
        while (i >= 0 and idxs.items[i] == n - k + i) : ({
            if (i == 0) break :outer;
            i -= 1;
        }) {}

        idxs.items[i] += 1;
        for (i + 1..k) |nidx| idxs.items[nidx] = idxs.items[nidx - 1] + 1;
    }

    return result;
}
